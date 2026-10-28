"""gen236_start.py (editor job): V2.36 straight JOG START with the LEFT foot swinging first - a content gap, not a tuning item.
Diagnosis (j34_chain1 / j36_stopr / j36_rsl / jstart): the start route searches SHM_JogStartDB_<side> by the UNLOADED foot (V1.3.9);
PSD_SHM_JogStartS_L (left foot steps first) holds no straight jog start (its forward entries are TurnL045 / TurnR045 and the relaxed RUN
start), so every straight request from a left-unloaded stance plays TurnL045 = the 'wrong start family' (65-92 cm drag); the right
database has the vendor straight starts.
Plan (V2.8 contact-planned start, jog version):
  * frame 0 = the stance the stops end in (final_src last frame); root = the MEASURED in-game jog start (onset ONSET s, then ACC cm/s2
    to the loop speed) - the clip root is the capsule path;
  * X = left = first swing foot: weight shifts onto the stance foot (pelvis APA_CM toward it) while the trunk starts to lean in, X lifts at
    T_LIFT and lands where the jog loop places it at its heel strike when the root has covered the stance geometry; from there the legs follow
    the loop on a root-consistent clock and the stance foot's small stance->loop offset fades during its own next swing (no slide);
  * whole body: trunk / head / pelvis blend stance -> loop from T_LEAN (the lean comes BEFORE the first step); the arms leave the hang toward
    the jog carriage from T_ARM over ARM_T with the swing amplitude growing (no instant full jog swing);
  * curves: footspeed_l/_r (planned balls, loop units), Enable_OrientationWarping / Disable_FootLock / pbi_authoredforwardlean copied from the loop
    after the first step.
Output /Game/GraceRanger/SHME/Animations/V236/SHM236_JogStart_F_Lfoot (+ _Rfoot with 'feet': ['l','r']). builtins.G236ST = {'dry_run': True,
'feet': ['l'], ...knobs}. Stick JSON to Saved/Codex/SHME_V236_20261028/stick/. Prints G236ST {...}."""
import unreal as u, json, math, builtins, pathlib, importlib, sys
P = pathlib.Path(u.Paths.project_dir()).resolve(); sys.path.insert(0, str(P / 'Tools/SHME_V1_20260925'))
import v137_animedit as ae; importlib.reload(ae)
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'G236ST', {})); DRY = bool(cfg.get('dry_run', True)); FEET = cfg.get('feet', ['l'])
K = lambda k, d: float(cfg.get(k, d))
LOOP = '/Game/GraceRanger/Animations/Continuity/A_CT_Jog_Fwd'
FINAL = cfg.get('final_src', '/Game/GraceRanger/SHME/Animations/Stops/SHM_A_CP2_Jog_Fwd_Stop')
OUTDIR = '/Game/GraceRanger/SHME/Animations/V236'; SD = P / 'Saved/Codex/SHME_V236_20261028'
FPS = 30.0; DT = 1.0 / FPS
VMAX = K('vmax', 300.0); ACC = K('acc', 470.0); ONSET = K('onset', 0.10); T_LIFT = K('t_lift', 0.16); APA_CM = K('apa_cm', 2.0)
T_LEAN = K('t_lean', 0.0); LEAN_T = K('lean_t', 0.45); T_ARM = K('t_arm', 0.05); ARM_T = K('arm_t', 0.45); AMP_T = K('amp_t', 0.55)
SWING_H = K('swing_h', 9.0); FADE_LEN = K('fade', 0.45); TAIL = K('tail', 0.55)
def v_of(t):
    if t <= 0: return 0.0
    if t < ONSET: return 0.5 * ACC / ONSET * t * t                     # smooth onset (acceleration ramps 0 -> ACC)
    return min(VMAX, 0.5 * ACC * ONSET + ACC * (t - ONSET))
_ts = [0.0]; _ds = [0.0]
for i in range(1, 2001): t_ = i * 0.002; _ts.append(t_); _ds.append(_ds[-1] + 0.5 * (v_of(t_) + v_of(t_ - 0.002)) * 0.002)
def d_of(t):
    if t <= 0: return 0.0
    if t >= _ts[-1]: return _ds[-1] + VMAX * (t - _ts[-1])
    i = int(t / 0.002); w = (t - _ts[i]) / 0.002; return _ds[i] + (_ds[i + 1] - _ds[i]) * w
loop = u.load_asset(LOOP); fsrc = u.load_asset(FINAL)
NAMES = [str(n) for n in AL.get_animation_track_names(loop)]
NK1 = ae.num_frames(loop) - 1; T1 = float(loop.get_play_length())
Lk = ae.read_local(loop, NAMES, list(range(NK1 + 1)))
Fk = ae.read_local(fsrc, NAMES, [ae.num_frames(fsrc) - 1]); ST = {b: Fk[b][0] for b in NAMES}
clip = ae.Clip(loop, ['root', 'pelvis', 'foot_l', 'foot_r', 'ball_l', 'ball_r', 'calf_l', 'calf_r', 'head', 'neck_01', 'spine_03', 'spine_05', 'hand_l', 'hand_r',
                      'lowerarm_l', 'lowerarm_r', 'upperarm_l', 'upperarm_r', 'clavicle_l', 'clavicle_r', 'thigh_l', 'thigh_r'] + [b for b in ('ik_foot_l', 'ik_foot_r', 'ik_foot_root') if b in NAMES])
D = ae.vsub(Lk['root'][NK1][0], Lk['root'][0][0]); VLOOP = ae.vlen(D) / T1; FWD = ae.vnorm(D); LEFT = ae.vnorm(ae.vcross(FWD, (0.0, 0.0, 1.0)))
def slerp(a, b, t):
    d = sum(a[i] * b[i] for i in range(4))
    if d < 0: b = tuple(-x for x in b); d = -d
    if d > 0.9995: return ae.qnorm(tuple(a[i] + (b[i] - a[i]) * t for i in range(4)))
    th = math.acos(min(d, 1.0)); s = math.sin(th)
    return tuple((math.sin((1 - t) * th) * a[i] + math.sin(t * th) * b[i]) / s for i in range(4))
def lerp(a, b, t): return tuple(a[i] + (b[i] - a[i]) * t for i in range(len(a)))
def mj(x): x = min(1.0, max(0.0, x)); return x * x * x * (10 - 15 * x + 6 * x * x)
def loop_local(tau):
    c, r = divmod(tau, T1); f = r / T1 * NK1; i = int(math.floor(f)); w = f - i; i = min(i, NK1 - 1)
    o = {}
    for b in NAMES:
        (t0, q0, s0), (t1, q1, s1) = Lk[b][i], Lk[b][i + 1]
        t = lerp(t0, t1, w); q = slerp(q0, q1, w)
        if b == 'root': t = ae.vadd(t, ae.vsc(D, c))
        o[b] = (t, q, lerp(s0, s1, w))
    return o
def rel(loc, bone):
    tmp = {b: [loc[b]] for b in loc}; r0 = loc['root']; tmp['root'] = [((0.0, 0.0, 0.0), r0[1], r0[2])]
    return clip.comp(bone, 0, tmp)
_BW = {s: [rel(loop_local(k * T1 / NK1), 'ball_' + s)[0] for k in range(NK1 + 1)] for s in 'lr'}
BZ0 = {s: min(p[2] for p in _BW[s]) for s in 'lr'}
def _wspeed(s, k):
    a = _BW[s][(k - 1) % NK1]; b = _BW[s][(k + 1) % NK1]; dt = 2 * T1 / NK1
    return math.hypot(b[0] - a[0], b[1] - a[1] + VLOOP * dt) / dt
PL = {s: [(_BW[s][k][2] < BZ0[s] + 4.0 and _wspeed(s, k) < 90.0) for k in range(NK1)] for s in 'lr'}
def planted(s, tau): return PL[s][int(round((tau % T1) / T1 * NK1)) % NK1]
def next_land(s, tau):
    for k in range(1, NK1 * 2):
        t = tau + k * T1 / NK1
        if planted(s, t) and not planted(s, t - T1 / NK1): return t
    return tau + T1
def next_lift(s, tau):
    for k in range(1, NK1 * 2):
        t = tau + k * T1 / NK1
        if not planted(s, t) and planted(s, t - T1 / NK1): return t
    return tau + T1
BALL_LOCAL = {s: Lk['ball_' + s][0][0] for s in 'lr'}
def foot_at_ball(s, ball, q): return ae.vsub(ball, ae.qrot(q, BALL_LOCAL[s]))
ST_FOOT = {s: rel(ST, 'foot_' + s) for s in 'lr'}; ST_BALL = {s: rel(ST, 'ball_' + s)[0] for s in 'lr'}
LEGS = ('root', 'thigh_l', 'calf_l', 'foot_l', 'ball_l', 'thigh_r', 'calf_r', 'foot_r', 'ball_r', 'ik_foot_l', 'ik_foot_r', 'ik_foot_root')
ARMS = [b for b in NAMES if b.startswith(('clavicle_', 'upperarm_', 'lowerarm_', 'hand_', 'thumb_', 'index_', 'middle_', 'ring_', 'pinky_'))]
UB = [b for b in NAMES if b not in LEGS and b not in ARMS and not b.startswith(('calf_twist', 'thigh_twist'))]
def qavg(qs):
    ref = qs[0]; acc = [0.0] * 4
    for q in qs:
        if sum(q[i] * ref[i] for i in range(4)) < 0: q = tuple(-x for x in q)
        for i in range(4): acc[i] += q[i]
    return ae.qnorm(tuple(acc))
MEAN = {b: qavg([Lk[b][k][1] for k in range(NK1)]) for b in ARMS}
def swing(p0, p1, t0, t1, t, h):
    if t <= t0: return p0
    if t >= t1: return p1
    x = (t - t0) / (t1 - t0); w = mj(x)
    return (p0[0] + (p1[0] - p0[0]) * w, p0[1] + (p1[1] - p0[1]) * w, p0[2] + (p1[2] - p0[2]) * w + h * math.sin(math.pi * x) * (1 - 0.3 * x))
def build(X):
    S = 'r' if X == 'l' else 'l'
    tauHS = next_land(X, 0.02)
    LH = loop_local(tauHS); sBallLoop = rel(LH, 'ball_' + S)[0]; xLoop = rel(LH, 'foot_' + X); qSHS = rel(LH, 'foot_' + S)[1]
    need = ae.vdot(ST_BALL[S], FWD) - ae.vdot(sBallLoop, FWD)            # root travel at X's heel strike so the stance ball keeps its place
    t_hs = next(k * 0.005 for k in range(1, 600) if d_of(k * 0.005) >= need)
    t_hs = max(t_hs, T_LIFT + 0.20)
    rtHS = ae.vsc(FWD, d_of(t_hs))
    sBall = ST_BALL[S]; sLoopW = ae.vadd(rtHS, sBallLoop)
    off0 = (sBall[0] - sLoopW[0], sBall[1] - sLoopW[1], 0.0)
    tauLiftS = next_lift(S, tauHS)
    L = t_hs + TAIL; N = int(math.ceil(L / DT)) + 1
    frames = []; tau = tauHS
    for f in range(N):
        t = f * DT; d = d_of(t); rt = ae.vsc(FWD, d)
        if t <= t_hs: Lp = loop_local(tauHS)
        else: tau = tauHS + (d - d_of(t_hs)) / VLOOP; Lp = loop_local(tau)
        wl = mj((t - T_LEAN) / LEAN_T)
        pose = {}
        for b in UB: pose[b] = (lerp(ST[b][0], Lp[b][0], wl), slerp(ST[b][1], Lp[b][1], wl), lerp(ST[b][2], Lp[b][2], wl))
        wa = mj((t - T_ARM) / ARM_T); amp = mj((t - t_hs + 0.15) / AMP_T)
        for b in ARMS:
            base = slerp(ST[b][1], MEAN[b], wa)
            dq = ae.qmul(ae.qinv(MEAN[b]), Lp[b][1])
            if dq[3] < 0: dq = tuple(-x for x in dq)
            pose[b] = (lerp(ST[b][0], Lp[b][0], wa), ae.qnorm(ae.qmul(base, slerp((0.0, 0.0, 0.0, 1.0), dq, amp))), lerp(ST[b][2], Lp[b][2], wa))
        for b in NAMES:
            if b not in pose: pose[b] = Lp[b] if t > t_hs else ST[b]
        apa = APA_CM * math.sin(math.pi * min(1.0, t / (T_LIFT + 0.15))) * (1 if S == 'r' else -1) if t < T_LIFT + 0.15 else 0.0
        pt, pq, ps = pose['pelvis']; pose['pelvis'] = ((pt[0] - apa, pt[1], pt[2]), pq, ps)
        pose['root'] = (rt, Lk['root'][0][1], Lk['root'][0][2])
        ft = {}
        if t <= t_hs:
            qs = slerp(ST_FOOT[S][1], qSHS, mj((t - T_LIFT) / (t_hs - T_LIFT)))
            ft[S] = (foot_at_ball(S, sBall, qs), qs)
            landpos = ae.vadd(rtHS, xLoop[0])
            ft[X] = (swing(ST_FOOT[X][0], landpos, T_LIFT, t_hs, t, SWING_H), slerp(ST_FOOT[X][1], xLoop[1], mj((t - T_LIFT) / (t_hs - T_LIFT))))
        else:
            lx = rel(Lp, 'foot_' + X); ft[X] = (ae.vadd(rt, lx[0]), lx[1])
            ls = rel(Lp, 'foot_' + S)
            fade = 1.0 if tau <= tauLiftS else 1.0 - mj((tau - tauLiftS) / FADE_LEN)
            ft[S] = (ae.vadd(ae.vadd(rt, ls[0]), ae.vsc(off0, fade)), ls[1])
        frames.append((pose, ft))
    local = {b: [fr[0][b] for fr in frames] for b in NAMES}
    for f, (pose, ft) in enumerate(frames):
        for s in 'lr':
            kh = clip.comp('calf_' + s, f, local)[0]
            ae.solve_leg(clip, local, s, f, ft[s][0], ft[s][1], kh)
    for s in 'lr':
        b = 'ik_foot_' + s
        if b in NAMES and 'ik_foot_root' in NAMES:
            for f in range(N):
                fp, fq = clip.comp('foot_' + s, f, local); pp, pq = clip.comp('ik_foot_root', f, local)
                lt = ae.qrot(ae.qinv(pq), ae.vsub(fp, pp)); lq = ae.qnorm(ae.qmul(ae.qinv(pq), fq)); local[b][f] = (lt, lq, local[b][f][2])
    def cw(b, f): return clip.comp(b, f, local)[0]
    ferr = max(ae.vlen(ae.vsub(cw('foot_' + s, f), frames[f][1][s][0])) for f in range(N) for s in 'lr')
    drift = 0.0
    for s in 'lr':
        fz = max(BZ0[s], ST_BALL[s][2]) + 1.0
        for f in range(1, N):
            a, b_ = cw('ball_' + s, f - 1), cw('ball_' + s, f)
            if a[2] < fz and b_[2] < fz:
                dd = math.hypot(b_[0] - a[0], b_[1] - a[1]); drift += dd if dd > 0.05 else 0.0
    e0 = max(ae.vlen(ae.vsub(ae.vsub(cw(bn, 0), local['root'][0][0]), rel(ST, bn)[0])) for bn in ('foot_l', 'foot_r', 'head', 'pelvis', 'hand_l', 'hand_r'))
    LF = loop_local(tau); eF = max(ae.vlen(ae.vsub(ae.vsub(cw(bn, N - 1), local['root'][N - 1][0]), rel(LF, bn)[0])) for bn in ('foot_l', 'foot_r', 'head', 'pelvis'))
    info = {'X': X, 'S': S, 'tauHS': round(tauHS, 3), 't_hs': round(t_hs, 3), 'need_cm': round(need, 1), 'off0': [round(x, 1) for x in off0], 'len': round(L, 3),
            'foot_err': round(ferr, 2), 'planted_drift': round(drift, 2), 'entry_err': round(e0, 2), 'exit_err': round(eF, 2),
            'lean': [round(ae.vdot(ae.vsub(cw('head', f), cw('pelvis', f)), FWD), 1) for f in range(0, N, 3)], 'hand_z': [round(cw('hand_l', f)[2], 1) for f in range(0, N, 3)]}
    SB = ['pelvis', 'spine_03', 'spine_05', 'neck_01', 'head', 'clavicle_l', 'upperarm_l', 'lowerarm_l', 'hand_l', 'clavicle_r', 'upperarm_r', 'lowerarm_r', 'hand_r',
          'thigh_l', 'calf_l', 'foot_l', 'ball_l', 'thigh_r', 'calf_r', 'foot_r', 'ball_r']
    name = 'SHM236_JogStart_F_%sfoot' % X.upper()
    (SD / 'stick' / (name + '.json')).write_text(json.dumps({'name': name, 'dt': DT, 'bones': SB, 'frames': [[[round(x, 1) for x in cw(b, f)] for b in SB] for f in range(N)]}))
    cur = {'footspeed_l': [], 'footspeed_r': []}
    for f in range(N):
        for s in 'lr':
            a = cw('ball_' + s, max(0, f - 1)); b_ = cw('ball_' + s, min(N - 1, f + 1))
            cur['footspeed_' + s].append(math.hypot(b_[0] - a[0], b_[1] - a[1]) / (DT * (min(N - 1, f + 1) - max(0, f - 1))))
    for cn in ('Enable_OrientationWarping', 'Disable_FootLock', 'pbi_authoredforwardlean'):
        try:
            vals = [AL.get_float_value(loop, cn, (tauHS + (d_of(f * DT) - d_of(t_hs)) / VLOOP) % T1) if f * DT > t_hs else AL.get_float_value(loop, cn, tauHS % T1) * (0.0 if cn == 'pbi_authoredforwardlean' else 1.0) for f in range(N)]
            cur[cn] = vals
        except Exception: pass
    return name, local, info, cur
def write(name, local, cur):
    path = OUTDIR + '/' + name
    ae.leg_guard(loop, local, label=name)
    seq = u.load_asset(path) if EAL.does_asset_exist(path) else EAL.duplicate_asset(LOOP, path)
    for tr in [str(t) for t in AL.get_animation_notify_track_names(seq)]:
        AL.remove_animation_notify_events_by_track(seq, tr)
        try: AL.remove_animation_notify_track(seq, tr)
        except Exception: pass
    n = len(local['root']); c = ae.controller(seq)
    try: c.open_bracket(u.Text('SHME V2.36 jog start ' + name), True)
    except Exception: c.open_bracket('SHME V2.36 ' + name, True)
    try:
        c.set_number_of_frames(u.FrameNumber(n - 1), True)
        for b in NAMES:
            ks = local[b]
            if not c.set_bone_track_keys(b, [u.Vector(*k[0]) for k in ks], [u.Quat(*k[1]) for k in ks], [u.Vector(*k[2]) for k in ks], True): raise RuntimeError('keys ' + b)
    finally: c.close_bracket(True)
    for cn in [str(x) for x in AL.get_animation_curve_names(seq, u.RawCurveTrackTypes.RCT_FLOAT)]: AL.remove_curve(seq, cn, False)
    ts = [f * DT for f in range(n)]
    for cn, vals in cur.items():
        AL.add_curve(seq, cn, u.RawCurveTrackTypes.RCT_FLOAT, False); AL.add_float_curve_keys(seq, cn, ts, vals)
    try: seq.set_editor_property('loop', False)
    except Exception: pass
    return EAL.save_loaded_asset(seq, False), path
out = {'loop': LOOP, 'final_src': FINAL, 'clips': {}}
for X in FEET:
    name, local, info, cur = build(X)
    if not DRY: info['saved'], info['path'] = write(name, local, cur)
    out['clips'][name] = info
(SD / ('gen236_start_%s.json' % ('dry' if DRY else 'write'))).write_text(json.dumps(out, indent=1, default=str))
print('G236ST ' + json.dumps(out, default=str))
