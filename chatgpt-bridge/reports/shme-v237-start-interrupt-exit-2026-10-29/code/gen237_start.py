"""gen237_start.py (editor job): V2.37 footstep-planned JOG START (from rest) and RE-PUSH (from inside a jog stop) - new candidate assets.

Why (V2.36 SHM236_JogStart_F_Lfoot, first broken frame, same space):
  * source: the loaded stance foot S was rotated toward the loop's AIRBORNE toe-off orientation of S at X's heel strike (qSHS) while its
    ball stayed pinned: foot pitch 39 deg (flat) at 0.20 s -> 69 at 0.33 -> 122 at 0.57 s (ankle 9 cm IN FRONT of the ball = folded over
    the toes, weight on it). In game the stance ball then slid back 16-17 cm from clip time 0.19 s (j36_wjs / j34_chain1, visible AND MM
    mesh) with a 144-158 deg ankle->ball yaw flip;
  * at X's heel strike S jumped into the loop's flight pose (ball +18 cm in one frame) and the lateral stance->loop offset faded over
    0.45 s of loop time = into S's next stance (2.7 cm lateral drift of a planted ball);
  * the root accelerated at 470 cm/s2 while the in-game capsule starts at 165 -> 245 cm/s2 (EffortAccScale 0.86): MM played the clip at
    rate 0.70-0.84 (slow-motion start) and the start family (StartTransferMaxTime 0.65 s) ended before the first landing (clip 0.45 s)
    -> the search jumped into the vendor CP2 start at 0.87.
Plan (one action = the start of the jog, not one clip pose):
  * root = the measured capsule (a = A0 -> A1 over A_T s; v0 for a re-push); the clip root IS the capsule path;
  * contacts on the BALL; every landing is planned: first swing foot X lifts at T_LIFT after a small weight shift to S (APA) and lands
    REACH(v) ahead of the root; then the feet alternate with the step time / double support of the current speed (cadence rises, step
    length grows: 30 -> 65 -> 105 cm ...), lateral track goes from the stance to the loop track step by step; the last planned landing IS a
    loop landing (same foot, same reach) -> from there the loop on a root-consistent clock (no offset to fade);
  * a planted foot keeps its landing rotation; it rolls onto its ball only for reach (cap HEEL_CAP) and for the push-off before its own
    lift (HEEL_PUSH x speed); the swing follows the loop's own swing shape (heel kick, toe-off pitch) scaled by the step length;
  * whole body: trunk / head lean in from 0 s (before the first step), pelvis height / bob and arm carriage / swing amplitude follow the
    SPEED (not the clock), arms swing on the step clock (counter to the legs).
Generic: cfg 'src' / 'src_t' (frame-0 pose: stance or a stop clip at the re-press time), 'v0', 'acc0'/'acc1'; feet state at frame 0 is read
from the source clip (planted = ball low and still in the source's own root-moving space).
Output OUTDIR/<name>. builtins.G237ST = {'dry_run': True, 'clips': [{'name':..., 'first': 'l'|'r', 'src':..., 'src_t':..., 'v0':...}], ...knobs}.
Stick JSON -> Saved/Codex/SHME_V237_20261029/stick/. Prints G237ST {...}."""
import unreal as u, json, math, builtins, pathlib, importlib, sys
P = pathlib.Path(u.Paths.project_dir()).resolve(); sys.path.insert(0, str(P / 'Tools/SHME_V1_20260925'))
import v137_animedit as ae; importlib.reload(ae)
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'G237ST', {})); DRY = bool(cfg.get('dry_run', True))
K = lambda k, d: float(cfg.get(k, d))
LOOP = '/Game/GraceRanger/Animations/Continuity/A_CT_Jog_Fwd'
STANCE = '/Game/GraceRanger/SHME/Animations/Stops/SHM_A_CP2_Jog_Fwd_Stop'
OUTDIR = cfg.get('outdir', '/Game/GraceRanger/SHME/Animations/V237'); SD = P / 'Saved/Codex/SHME_V237_20261029'; (SD / 'stick').mkdir(parents=True, exist_ok=True)
FPS = 30.0; DT = 1.0 / FPS
VMAX = K('vmax', 300.0); A0 = K('acc0', 165.0); A1 = K('acc1', 245.0); A_T = K('acc_t', 0.5)
T_LIFT = K('t_lift', 0.17); SW1 = K('sw1', 0.33); APA_CM = K('apa_cm', 1.8)
REACH0 = K('reach0', 14.0); REACH_V = K('reach_v', 0.07); STEP_K = K('step_k', 0.15); DS0 = K('ds0', 0.12); DSV = K('dsv', 0.17)
HEEL_CAP = K('heel_cap', 50.0); HEEL_PUSH0 = K('heel_push0', 18.0); HEEL_PUSHV = K('heel_pushv', 14.0); PUSH_T = K('push_t', 0.16); TOE_MAX = K('toe_max', 85.0)
KNEE_MARGIN = K('knee_margin', 0.4); HEEL_MARGIN = K('heel_margin', 1.5); LOOPDEV = K('loopdev', 0.55); APEX_MIN = K('apex_min', 4.5)
LEAN_T = K('lean_t', 0.50); ARM_T0 = K('arm_t0', 0.05); ARM_T = K('arm_t', 0.55); AMP_V = K('amp_v', 230.0); BODY_V = K('body_v', 260.0)
LB0 = K('lb0', 24.0); LBV = K('lbv', 16.0); LANDC = K('landc', 2.5); NLAT = K('nlat', 2.0); RP_T = K('rp_t', 0.40); TAIL = K('tail', 0.50); NSTEP_MAX = int(K('nstep_max', 7))
loop = u.load_asset(LOOP)
NAMES = [str(n) for n in AL.get_animation_track_names(loop)]
NK1 = ae.num_frames(loop) - 1; T1 = float(loop.get_play_length())
Lk = ae.read_local(loop, NAMES, list(range(NK1 + 1)))
BONES = ['root', 'pelvis', 'foot_l', 'foot_r', 'ball_l', 'ball_r', 'calf_l', 'calf_r', 'head', 'neck_01', 'spine_03', 'spine_05', 'hand_l', 'hand_r',
         'lowerarm_l', 'lowerarm_r', 'upperarm_l', 'upperarm_r', 'clavicle_l', 'clavicle_r', 'thigh_l', 'thigh_r'] + [b for b in ('ik_foot_l', 'ik_foot_r', 'ik_foot_root') if b in NAMES]
clip = ae.Clip(loop, BONES)
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
# ---- loop contact table (same rule as gen236_stop: ball low and nearly still in the world; short runs / gaps cleaned)
_BW = {s: [rel(loop_local(k * T1 / NK1), 'ball_' + s)[0] for k in range(NK1 + 1)] for s in 'lr'}
BZ0 = {s: min(p[2] for p in _BW[s]) for s in 'lr'}
def _wspeed(s, k):
    a = _BW[s][(k - 1) % NK1]; b = _BW[s][(k + 1) % NK1]; dt = 2 * T1 / NK1
    return math.hypot(b[0] - a[0], b[1] - a[1] + VLOOP * dt) / dt
PL = {}
for s in 'lr':
    raw = [(_BW[s][k][2] < BZ0[s] + 4.0 and _wspeed(s, k) < 90.0) for k in range(NK1)]
    for k in range(NK1):
        if not raw[k] and raw[(k - 1) % NK1] and (raw[(k + 1) % NK1] or raw[(k + 2) % NK1]): raw[k] = True
    keep = list(raw)
    for k in range(NK1):
        if raw[k]:
            n = 0; j = k
            while raw[j % NK1] and n < NK1: n += 1; j += 1
            m = 0; j = k
            while raw[j % NK1] and m < NK1: m += 1; j -= 1
            if n + m - 1 < 3: keep[k] = False
    PL[s] = keep
def planted(s, tau): return PL[s][int(round((tau % T1) / T1 * NK1)) % NK1]
def events(s, land=True):
    o = []
    for k in range(NK1):
        a, b = PL[s][(k - 1) % NK1], PL[s][k]
        if land and b and not a: o.append(k * T1 / NK1)
        if not land and a and not b: o.append(k * T1 / NK1)
    return o
LANDS = {s: events(s, True) for s in 'lr'}; LIFTS = {s: events(s, False) for s in 'lr'}
SEQ = sorted([(t, s) for s in 'lr' for t in LANDS[s]])                       # loop landings in order (t, foot)
STEP_T = T1 / len(SEQ)
def lift_before(s, tl):                                                       # the loop lift of foot s that precedes its landing tl
    c = [x for x in LIFTS[s] if x < tl - 1e-6] or [x - T1 for x in LIFTS[s]]
    return max(c)
LOOP_BALL = lambda s, tau: rel(loop_local(tau), 'ball_' + s)[0]
LOOP_FOOT = lambda s, tau: rel(loop_local(tau), 'foot_' + s)
def fpitch(foot, ball): return math.degrees(math.atan2(foot[2] - ball[2], ae.vdot(ae.vsub(ball, foot), FWD)))
# the loop's own toe-off: foot pitch over its landing (flat) pitch at the frame the ball leaves (the push-off may reach it, never earlier)
FLATL = {s: min(fpitch(LOOP_FOOT(s, x)[0], LOOP_BALL(s, x)) for x in LANDS[s]) for s in 'lr'}
TOE_EXTRA = {s: max(0.0, max(fpitch(LOOP_FOOT(s, x)[0], LOOP_BALL(s, x)) for x in LIFTS[s]) - min(fpitch(LOOP_FOOT(s, x)[0], LOOP_BALL(s, x)) for x in LANDS[s])) for s in 'lr'}
BALL_LOCAL = {s: Lk['ball_' + s][0][0] for s in 'lr'}
def foot_at_ball(s, ball, q): return ae.vsub(ball, ae.qrot(q, BALL_LOCAL[s]))
def ball_of(s, foot, q): return ae.vadd(foot, ae.qrot(q, BALL_LOCAL[s]))
LEGS = ('root', 'thigh_l', 'calf_l', 'foot_l', 'ball_l', 'thigh_r', 'calf_r', 'foot_r', 'ball_r', 'ik_foot_l', 'ik_foot_r', 'ik_foot_root')
ARMS = [b for b in NAMES if b.startswith(('clavicle_', 'upperarm_', 'lowerarm_', 'hand_', 'thumb_', 'index_', 'middle_', 'ring_', 'pinky_'))]
UB = [b for b in NAMES if b not in LEGS and b not in ARMS]
def qavg(qs):
    ref = qs[0]; acc = [0.0] * 4
    for q in qs:
        if sum(q[i] * ref[i] for i in range(4)) < 0: q = tuple(-x for x in q)
        for i in range(4): acc[i] += q[i]
    return ae.qnorm(tuple(acc))
MEAN = {b: qavg([Lk[b][k][1] for k in range(NK1)]) for b in ARMS}
MEANT = {b: tuple(sum(Lk[b][k][0][i] for k in range(NK1)) / NK1 for i in range(3)) for b in ARMS}
PMEAN = tuple(sum(Lk['pelvis'][k][0][i] for k in range(NK1)) / NK1 for i in range(3))
def _loop_curve(name):
    try: return [AL.get_float_value(loop, name, k * T1 / NK1) for k in range(NK1)]
    except Exception: return None
FS_LOOP = _loop_curve('footspeed_l')
_bs = [math.hypot(_BW['l'][(k + 1) % NK1][0] - _BW['l'][k][0], _BW['l'][(k + 1) % NK1][1] - _BW['l'][k][1] + VLOOP * T1 / NK1) / (T1 / NK1) for k in range(NK1)]
FS_SCALE = (max(FS_LOOP) / max(_bs)) if FS_LOOP and max(_bs) > 0 else 1.0
# loop swing shape per foot: (lift tau, land tau, deviation of the ball path from the straight lift->land line in WORLD terms, normalised x)
def loop_swing(s, tl):
    t0 = lift_before(s, tl); n = 24; pts = []
    for i in range(n + 1):
        tau = t0 + (tl - t0) * i / n; pts.append(ae.vadd(LOOP_BALL(s, tau), ae.vsc(FWD, VLOOP * (tau - t0))))
    a, b = pts[0], pts[-1]; dev = [ae.vsub(pts[i], lerp(a, b, i / n)) for i in range(n + 1)]
    return t0, dev, ae.vlen(ae.vsub(b, a))
def dev_at(dev, x):
    n = len(dev) - 1; f = min(max(x, 0.0), 1.0) * n; i = min(int(f), n - 1); w = f - i
    return lerp(dev[i], dev[i + 1], w)
# ---- root profile
def make_root(v0):
    ts = [0.0]; vs = [v0]; ds = [0.0]; h = 0.002
    for i in range(1, 2501):
        t = i * h; a = A0 + (A1 - A0) * mj(t / A_T) if v0 < 1.0 else A1
        v = min(VMAX, vs[-1] + a * h); ts.append(t); vs.append(v); ds.append(ds[-1] + 0.5 * (v + vs[-2]) * h)
    def v_of(t): i = min(int(max(t, 0.0) / h), len(vs) - 1); return vs[i]
    def d_of(t):
        if t <= 0: return 0.0
        if t >= ts[-1]: return ds[-1] + VMAX * (t - ts[-1])
        i = int(t / h); w = (t - ts[i]) / h; return ds[i] + (ds[i + 1] - ds[i]) * w
    return v_of, d_of
def reach(v): return REACH0 + REACH_V * v
def step_t(v): return STEP_T * (1.0 + STEP_K * (1.0 - v / VMAX))
def ds_t(v): return DS0 - DSV * (v / VMAX)                                     # double support (> 0) at low speed, flight (< 0) at jog
def lift_behind(v): return LB0 + LBV * (v / VMAX)                              # a stance foot leaves once the root is this far past it (loop: 44)
def t_reach(p, t_from, d_of, v_of):
    t = t_from
    while t < 4.0 and d_of(t) - ae.vdot(p, FWD) < lift_behind(v_of(t)): t += 0.005
    return t
# ---- source frame-0 state
def src_state(src, src_t):
    seq = u.load_asset(src); nf = ae.num_frames(seq); f0 = (nf - 1) if src_t in (None, 'last') else min(nf - 1, int(round(float(src_t) * FPS)))
    fr = sorted(set([max(0, f0 - 1)] + list(range(f0, nf))))
    Sk = ae.read_local(seq, NAMES, fr); cs = ae.Clip(seq, BONES)
    loc = {b: [Sk[b][fr.index(f0)]] for b in NAMES}; ST = {b: Sk[b][fr.index(f0)] for b in NAMES}
    def compw(b, f): return cs.comp(b, fr.index(f), Sk)[0]                       # source component space incl. its root motion
    stt = {}
    for s in 'lr':
        fa, fb = fr[0], fr[min(2, len(fr) - 1)]; pa, pb = compw('ball_' + s, fa), compw('ball_' + s, fb); dtt = max((fb - fa) * DT, DT)
        w = ((pb[0] - pa[0]) / dtt, (pb[1] - pa[1]) / dtt, (pb[2] - pa[2]) / dtt)
        rb = rel(ST, 'ball_' + s)[0]; low = rb[2] < BZ0[s] + 3.0; still = math.hypot(w[0], w[1]) < 40.0
        stt[s] = {'planted': bool(low and still), 'ball': rb, 'vel': w, 'land_t': None}
        if not stt[s]['planted']:                     # in the air: when does the source land it (ball low and still in its own world)?
            for f in range(f0 + 1, nf - 1):
                a_, b_ = compw('ball_' + s, f), compw('ball_' + s, f + 1)
                rz = b_[2] - compw('root', f + 1)[2]
                if rz < BZ0[s] + 3.0 and math.hypot(b_[0] - a_[0], b_[1] - a_[1]) / DT < 40.0: stt[s]['land_t'] = (f + 1 - f0) * DT; break
    r0 = compw('root', fr[0]); r1 = compw('root', fr[min(2, len(fr) - 1)]); vroot = ae.vdot(ae.vsub(r1, r0), FWD) / max((fr[min(2, len(fr) - 1)] - fr[0]) * DT, DT)
    return ST, stt, vroot, nf, f0
def plan(ST, stt, v0, first, v_of, d_of):
    """landings: list of {foot, t_lift, t_land, p, v} ending on a loop landing (handover)."""
    lat0 = {s: ae.vdot(rel(ST, 'ball_' + s)[0], LEFT) for s in 'lr'}
    steps = []; pos = {s: stt[s]['ball'] for s in 'lr'}
    last_land = {s: (-1.0 if v0 >= 1.0 and stt[s]['planted'] else None) for s in 'lr'}   # re-push: a planted foot landed before frame 0 (no fresh stance minimum)
    infl = [s for s in 'lr' if not stt[s]['planted']]
    if infl:                                       # re-push: the foot in the air lands first, at its own (stop) landing time
        F = infl[0]; tl = max(0.12, stt[F]['land_t'] or 0.25); tlift = 0.0
    else:
        F = first; tlift = T_LIFT; tl = T_LIFT + SW1
        if v0 >= 1.0:                                  # re-push with both feet down: the trailing foot leaves by reach, not after a weight shift
            tlift = max(DT, min(T_LIFT, t_reach(pos[F], 0.0, d_of, v_of))); tl = tlift + SW1 * (1.0 - 0.3 * min(1.0, v0 / VMAX))
    k = 0
    while True:
        v = v_of(tl); dr = d_of(tl)
        jloop = None
        if v >= VMAX * 0.97 and k >= 2:                # handover: land exactly like the loop does (same foot, its loop reach)
            cands = [x for x in SEQ if x[1] == F]; jloop = min(cands, key=lambda x: abs(ae.vdot(LOOP_BALL(F, x[0]), FWD) - reach(VMAX)))[0]
            p = ae.vadd(ae.vsc(FWD, dr), LOOP_BALL(F, jloop))
        else:
            ll = [x for x in SEQ if x[1] == F][0][0]; latL = ae.vdot(LOOP_BALL(F, ll), LEFT); w = mj((k + 1) / (NLAT + 1))
            lat = lat0[F] + (latL - lat0[F]) * w
            p = ae.vadd(ae.vsc(FWD, dr + reach(v)), ae.vsc(LEFT, lat)); p = (p[0], p[1], (BZ0[F] + (stt[F]['ball'][2] - BZ0[F]) * (1 - w)) if stt[F]['planted'] or k > 0 else BZ0[F] + 1.5)
        steps.append({'foot': F, 't_lift': round(tlift, 3), 't_land': round(tl, 3), 'p': p, 'v': round(v, 1), 'ahead': round(ae.vdot(p, FWD) - dr, 1),
                      'len': round(ae.vdot(ae.vsub(p, pos[F]), FWD), 1), 'loop_tau': jloop})
        pos[F] = p; last_land[F] = tl
        if jloop is not None or k >= NSTEP_MAX: break
        O = 'r' if F == 'l' else 'l'
        lo = last_land[O] if last_land[O] is not None else 0.0
        tlift = max(min(tl + ds_t(v), t_reach(pos[O], max(lo, 0.0), d_of, v_of)), lo + 0.15, DT); tl_next = max(tl + step_t(v), tlift + 0.24)
        F, tl, k = O, tl_next, k + 1
    # final lifts: the other foot by the same rule; the handover foot when the loop lifts it (or by reach)
    F = steps[-1]['foot']; O = 'r' if F == 'l' else 'l'; tN = steps[-1]['t_land']
    fin = {O: max(min(tN + ds_t(VMAX), t_reach(pos[O], last_land[O] or 0.0, d_of, v_of)), (last_land[O] or 0.0) + 0.15)}
    tt = tN + DT
    while tt < tN + 1.0 and planted(F, steps[-1]['loop_tau'] + (d_of(tt) - d_of(tN)) / VLOOP): tt += 0.005
    fin[F] = min(tt, t_reach(pos[F], tN, d_of, v_of))
    return steps, fin
def build(spec):
    name = spec['name']; src = spec.get('src', STANCE); src_t = spec.get('src_t', 'last')
    ST, stt, vsrc, nf, f0 = src_state(src, src_t)
    v0 = float(spec['v0']) if 'v0' in spec else (0.0 if spec.get('from_rest', True) else max(0.0, vsrc))
    v_of, d_of = make_root(v0)
    first = spec.get('first') or min('lr', key=lambda s: ae.vdot(stt[s]['ball'], FWD))   # both planted: the trailing foot steps first
    if spec.get('land_t') is not None: cfg['land_t'] = spec['land_t']
    steps, fin_lift = plan(ST, stt, v0, first, v_of, d_of)
    last = steps[-1]; tN = last['t_land']; tauN = last['loop_tau']
    # phase clock: landing k <-> loop landing (counted back from the handover), linear between; root-consistent after the handover
    idx = [i for i, x in enumerate(SEQ) if abs(x[0] - tauN) < 1e-6 and x[1] == last['foot']][0]
    taus = []
    for j in range(len(steps)):
        back = len(steps) - 1 - j; ii = idx - back; c, rr = divmod(ii, len(SEQ)); taus.append(SEQ[rr][0] + c * T1)
    tland = [s_['t_land'] for s_ in steps]
    def clock(t):
        if t >= tN: return tauN + (d_of(t) - d_of(tN)) / VLOOP
        if t <= tland[0]: return taus[0] - (tland[0] - t)
        for j in range(1, len(tland)):
            if t <= tland[j]: return taus[j - 1] + (taus[j] - taus[j - 1]) * (t - tland[j - 1]) / (tland[j] - tland[j - 1])
        return taus[-1]
    # lifts also follow the step clock: a stance foot leaves no later than the loop lifts it at that phase (pelvis bob / arms agree)
    def t_of_tau(target, t0):
        t = t0
        while t < t0 + 2.0 and clock(t) < target: t += 0.005
        return t
    prev = {}
    for j, st in enumerate(steps):
        F = st['foot']
        if j >= 1 and F in prev:
            lt = lift_before(F, taus[j] % T1) + (taus[j] - taus[j] % T1)
            st['t_lift'] = round(max(prev[F] + 0.15, min(st['t_lift'], t_of_tau(lt, prev[F]))), 3)
        prev[F] = st['t_land']
    for F in 'lr':
        if F in prev:
            nl = [x for x in LIFTS[F] + [x + T1 for x in LIFTS[F]] + [x + 2 * T1 for x in LIFTS[F]] + [x + 3 * T1 for x in LIFTS[F]] if x > clock(prev[F]) % T1 + 0.02]
            lt = min(nl) + (clock(prev[F]) - clock(prev[F]) % T1)
            fin_lift[F] = max(prev[F] + 0.15, min(fin_lift[F], t_of_tau(lt, prev[F])))
    L = tN + TAIL; N = int(math.ceil(L / DT)) + 1
    # per-foot timeline
    ST_FOOT = {s: rel(ST, 'foot_' + s) for s in 'lr'}
    tl = {s: [] for s in 'lr'}
    for s in 'lr':
        cur = stt[s]['ball']; cur_q = ST_FOOT[s][1]; t_cur = 0.0; mine = [x for x in steps if x['foot'] == s]; first_sw = not stt[s]['planted']
        for st in mine:
            if not first_sw: tl[s].append(('plant', t_cur, st['t_lift'], cur, cur_q))
            jl = taus[steps.index(st)] % T1; t0l, dev, lnL = loop_swing(s, jl if any(abs(jl - x) < 1e-6 for x in LANDS[s]) else min(LANDS[s], key=lambda x: abs(x - jl)))
            q_land = LOOP_FOOT(s, jl)[1]
            tl[s].append(('swing', 0.0 if first_sw else st['t_lift'], st['t_land'], cur, cur_q, st['p'], q_land, dev, lnL, stt[s]['vel'] if first_sw else None))
            first_sw = False; cur = st['p']; cur_q = q_land; t_cur = st['t_land']
        tl[s].append(('plant', t_cur, fin_lift[s], cur, cur_q))
        tl[s].append(('join', fin_lift[s], 99.0, cur, cur_q))
    def seg_at(s, t):
        for sg in tl[s]:
            if sg[1] <= t + 1e-9 and t <= sg[2] + 1e-9: return sg
        raise RuntimeError('timeline gap %s %.3f %s' % (s, t, [(x[0], round(x[1], 3), round(x[2], 3)) for x in tl[s]]))
    frames = []; HO = {s: {'mode': 'pin'} for s in 'lr'}; LASTQ = {s: ST_FOOT[s][1] for s in 'lr'}; EXA = {s: [] for s in 'lr'}
    LEGL = {s: ae.vlen(Lk['calf_' + s][0][0]) + ae.vlen(Lk['foot_' + s][0][0]) - HEEL_MARGIN for s in 'lr'}
    SRC0 = {s: ae.vlen(ae.vsub(rel(ST, 'thigh_' + s)[0], rel(ST, 'foot_' + s)[0])) for s in 'lr'}
    def legl(s, t):                                    # frame 0 keeps the source's own leg (no fix-up of the entry pose); the margin returns over 0.3 s
        w0 = 1.0 - mj(t / 0.3); return max(LEGL[s], SRC0[s] + 0.3) * w0 + LEGL[s] * (1.0 - w0)
    for f in range(N):
        t = f * DT; tau = clock(t); Lp = loop_local(tau); v = v_of(t); rt = ae.vsc(FWD, d_of(t))
        wl = mj(t / (LEAN_T if v0 < 1.0 else RP_T))
        wb = mj(v / BODY_V) * (1.0 if v0 < 1.0 else mj(t / RP_T)); pose = {}
        for b in UB: pose[b] = (lerp(ST[b][0], Lp[b][0], wl), slerp(ST[b][1], Lp[b][1], wl), lerp(ST[b][2], Lp[b][2], wl))
        # pelvis: height and bob follow the speed (stance height -> jog height), not the clock
        pose['pelvis'] = (lerp(ST['pelvis'][0], Lp['pelvis'][0], wb), slerp(ST['pelvis'][1], Lp['pelvis'][1], wl), ST['pelvis'][2])
        wa = mj((t - ARM_T0) / ARM_T) if v0 < 1.0 else mj(t / RP_T); amp = mj(v / AMP_V) * wa
        for b in ARMS:
            base = slerp(ST[b][1], MEAN[b], wa)
            dq = ae.qmul(ae.qinv(MEAN[b]), Lp[b][1])
            if dq[3] < 0: dq = tuple(-x for x in dq)
            pose[b] = (lerp(ST[b][0], lerp(MEANT[b], Lp[b][0], amp), wa), ae.qnorm(ae.qmul(base, slerp((0.0, 0.0, 0.0, 1.0), dq, amp))), lerp(ST[b][2], Lp[b][2], wa))
        for b in NAMES:
            if b not in pose: pose[b] = Lp[b]                  # leg chain bones are re-solved below; ik_foot_root stays the loop's
        if v0 < 1.0 and t < T_LIFT + 0.15:             # anticipatory weight shift onto the stance foot before the first lift
            S_ = 'r' if steps[0]['foot'] == 'l' else 'l'; apa = APA_CM * math.sin(math.pi * min(1.0, t / (T_LIFT + 0.15))) * (1 if S_ == 'r' else -1)
            pt, pq, ps = pose['pelvis']; pose['pelvis'] = ((pt[0] - apa, pt[1], pt[2]), pq, ps)
        pose['root'] = (rt, Lk['root'][0][1], Lk['root'][0][2])
        ft = {}; pn = {}
        tmpL = {b: [pose[b]] for b in NAMES}
        def reach_roll(s, ball, q, a_min, cap):
            """rotate the foot about its ball (heel up) by a_min, more only while the hip cannot reach the ankle; total capped"""
            hip = clip.comp('thigh_' + s, 0, tmpL)[0]
            ex0 = max(0.0, fpitch(foot_at_ball(s, ball, q), ball) - FLATL[s])     # the total pitch over flat is capped, not the added roll
            a_min = max(0.0, min(a_min, cap - ex0)); cap = max(a_min, cap - ex0)
            for kk in range(int(a_min), int(cap) + 1):
                q2 = ae.qnorm(ae.qmul(ae.qaxis(LEFT, -kk), q)) if kk else q
                if ae.vlen(ae.vsub(hip, foot_at_ball(s, ball, q2))) <= legl(s, t): return q2, float(kk)
            return ae.qnorm(ae.qmul(ae.qaxis(LEFT, -cap), q)), float(cap)
        for s in 'lr':
            sg = seg_at(s, t); ex = 0.0
            if sg[0] == 'join':
                # the last lift of this foot: it joins the loop path with its 3D offset (pinned spot - loop ball at the lift) faded over the rest
                # of THAT swing (until the loop lands it) - never during a stance; its rotation leaves the last planted rotation over 0.3 of the swing
                lf = LOOP_FOOT(s, tau); lb = ae.vadd(rt, LOOP_BALL(s, tau)); stt_ = HO[s]
                if stt_['mode'] == 'pin':
                    nxt = min([x for x in LANDS[s] + [x + T1 for x in LANDS[s]] + [x + 2 * T1 for x in LANDS[s]] if x > tau % T1 + 1e-6]) + (tau - tau % T1)
                    stt_.update({'mode': 'fade', 'off': ae.vsub(sg[3], lb), 'tau0': tau, 'tau1': nxt, 'q0': LASTQ[s]})
                x_ = (tau - stt_['tau0']) / max(stt_['tau1'] - stt_['tau0'], 1e-3) if stt_['mode'] == 'fade' else 1.0
                w = 1.0 - mj(x_)
                if w <= 0.0: stt_['mode'] = 'loop'
                q = slerp(stt_['q0'], lf[1], mj(x_ / 0.3)) if stt_['mode'] == 'fade' else lf[1]
                off = ae.vsc(stt_.get('off', (0.0, 0.0, 0.0)), max(w, 0.0))
                bp = ae.vadd(ae.vadd(lb, off), (0.0, 0.0, APEX_MIN * math.sin(math.pi * min(1.0, x_)) * w))
                if x_ < 0.4: q, ex = reach_roll(s, bp, q, 0, 25)
                ft[s] = (foot_at_ball(s, bp, q), q); pn[s] = planted(s, tau) and w <= 0.0; EXA[s].append(0.0); continue
            if sg[0] == 'plant':
                _, ta, tb, p0, q0 = sg; pn[s] = True; hp = 0.0
                if tb < 99.0:                          # push-off: the heel rises before its own lift (ball pinned)
                    hp = (HEEL_PUSH0 + HEEL_PUSHV * v_of(tb) / VMAX) * mj((t - (tb - PUSH_T)) / PUSH_T) * (1.0 if v0 < 1.0 else mj(t / 0.12))
                cap = HEEL_CAP
                if tb < 99.0: cap = HEEL_CAP + max(0.0, min(TOE_EXTRA[s], TOE_MAX) - HEEL_CAP) * mj((t - (tb - PUSH_T)) / PUSH_T)
                q, ex = reach_roll(s, p0, q0, hp, cap)          # push and reach share one cap: 50 deg in the stance, the loop's toe-off only at the push
                LASTQ[s] = q; ft[s] = (foot_at_ball(s, p0, q), q); EXA[s].append(ex)
            else:
                _, ta, tb, p0, q0, p1, q1, dev, lnL, vel0 = sg; pn[s] = False
                x = (t - ta) / max(tb - ta, 1e-3); ln = math.hypot(p1[0] - p0[0], p1[1] - p0[1]); sc = min(1.0, ln / max(lnL, 1.0))
                qa = LASTQ[s] if vel0 is None else q0
                base = lerp(p0, p1, mj(x)) if vel0 is None else None
                if vel0 is not None:                   # a foot already in the air at frame 0: Hermite from its own velocity
                    T_ = tb - ta; h00 = 2 * x ** 3 - 3 * x * x + 1; h10 = x ** 3 - 2 * x * x + x; h01 = -2 * x ** 3 + 3 * x * x
                    base = tuple(h00 * p0[i] + h10 * T_ * vel0[i] * (1.0 if i < 2 else 0.0) + h01 * p1[i] for i in range(3))
                dv = dev_at(dev, x); zd = dv[2] * (sc ** LOOPDEV); zmin = APEX_MIN * math.sin(math.pi * x) * (1.0 if vel0 is None else (1 - x))
                wa_ = mj((x - 0.78) / 0.22)            # the landing: horizontal motion ends in the air, the ball comes down last
                xy = (base[0] + dv[0] * sc * (1 - wa_), base[1] + dv[1] * sc * (1 - wa_))
                zc = p1[2] + LANDC * (1.0 - mj((x - 0.8) / 0.2)) if x > 0.55 else -1e9
                bp = (xy[0], xy[1], max(base[2] + max(zd, zmin), zc))
                # rotation: lift rotation -> the loop's own swing orientation (scaled by the step) -> the loop landing orientation
                lq = LOOP_FOOT(s, tau)[1]; mid = slerp(qa, lq, sc ** 0.7)
                q = slerp(slerp(qa, mid, mj(x / 0.3)), q1, mj((x - 0.6) / 0.4))
                if x < 0.4 and vel0 is None: q, ex = reach_roll(s, bp, q, 0, 25)
                fp_ = foot_at_ball(s, bp, q); hip = clip.comp('thigh_' + s, 0, tmpL)[0]; dh = ae.vsub(fp_, hip); lh = ae.vlen(dh)
                if lh > legl(s, t) - 0.5: fp_ = ae.vadd(hip, ae.vsc(dh, (legl(s, t) - 0.5) / lh))   # a swing never reaches beyond the leg
                ft[s] = (fp_, q); EXA[s].append(0.0)
        frames.append((pose, ft, pn))
    local = {b: [fr[0][b] for fr in frames] for b in NAMES}
    PLN = {s: [fr[2][s] for fr in frames] for s in 'lr'}
    EXT = {s: ae.vlen(ae.vsub(rel(ST, 'thigh_' + s)[0], rel(ST, 'foot_' + s)[0])) for s in 'lr'}
    heel_max = {s: round(max(EXA[s]), 1) for s in 'lr'}
    need = []
    for f, (pose, ft, _pn) in enumerate(frames):
        dm = 0.0
        for s in 'lr':
            if not PLN[s][f]: continue
            hip = clip.comp('thigh_' + s, f, local)[0]; fp = ft[s][0]
            Lm = max(ae.vlen(local['calf_' + s][f][0]) + ae.vlen(local['foot_' + s][f][0]) - KNEE_MARGIN, EXT[s] + 0.3) if f * DT >= 0.3 else max(legl(s, f * DT) + HEEL_MARGIN - KNEE_MARGIN, EXT[s] + 0.3)
            hz = hip[2] - fp[2]; hor = math.hypot(hip[0] - fp[0], hip[1] - fp[1])
            if hz * hz + hor * hor > Lm * Lm: dm = max(dm, hz - math.sqrt(max(Lm * Lm - hor * hor, 0.0)))
        need.append(dm)
    mx = [max(need[max(0, f - 4):f + 5]) for f in range(N)]; drop = [max(sum(mx[max(0, f - 4):f + 5]) / len(mx[max(0, f - 4):f + 5]), need[f]) for f in range(N)]
    for f in range(N):
        pt, pq, ps = local['pelvis'][f]; local['pelvis'][f] = ((pt[0], pt[1], pt[2] - drop[f]), pq, ps)
    for f, (pose, ft, _pn) in enumerate(frames):
        for s in 'lr':
            kh = clip.comp('calf_' + s, f, local)[0]; ae.solve_leg(clip, local, s, f, ft[s][0], ft[s][1], kh)
    for s in 'lr':
        b = 'ik_foot_' + s
        if b in NAMES and 'ik_foot_root' in NAMES:
            for f in range(N):
                fp, fq = clip.comp('foot_' + s, f, local); pp, pq = clip.comp('ik_foot_root', f, local)
                local[b][f] = (ae.qrot(ae.qinv(pq), ae.vsub(fp, pp)), ae.qnorm(ae.qmul(ae.qinv(pq), fq)), local[b][f][2])
    # ---- checks (same space: component incl. root = the clip's world)
    def cw(b, f): return clip.comp(b, f, local)[0]
    ferr = max(ae.vlen(ae.vsub(cw('foot_' + s, f), frames[f][1][s][0])) for f in range(N) for s in 'lr')
    drift = {s: 0.0 for s in 'lr'}; pitch = {s: 0.0 for s in 'lr'}; zjump = 0.0
    flat = {s: math.degrees(math.atan2(rel(ST, 'foot_' + s)[0][2] - rel(ST, 'ball_' + s)[0][2], ae.vdot(ae.vsub(rel(ST, 'ball_' + s)[0], rel(ST, 'foot_' + s)[0]), FWD))) for s in 'lr'}
    for s in 'lr':
        for f in range(1, N):
            a, b_ = cw('ball_' + s, f - 1), cw('ball_' + s, f)
            zjump = max(zjump, abs(b_[2] - a[2]))
            if PLN[s][f] and PLN[s][f - 1] and f * DT <= tN + TAIL: drift[s] += math.hypot(b_[0] - a[0], b_[1] - a[1])
            if PLN[s][f]:
                fo = cw('foot_' + s, f); pitch[s] = max(pitch[s], math.degrees(math.atan2(fo[2] - b_[2], ae.vdot(ae.vsub(b_, fo), FWD))) - flat[s])
    LF = loop_local(clock((N - 1) * DT)); eF = max(ae.vlen(ae.vsub(ae.vsub(cw(bn, N - 1), local['root'][N - 1][0]), rel(LF, bn)[0])) for bn in ('foot_l', 'foot_r', 'head', 'pelvis', 'hand_l', 'hand_r'))
    e0 = max(ae.vlen(ae.vsub(ae.vsub(cw(bn, 0), local['root'][0][0]), rel(ST, bn)[0])) for bn in ('foot_l', 'foot_r', 'head', 'pelvis', 'hand_l', 'hand_r'))
    legmax = {s: round(max(ae.vlen(ae.vsub(cw('thigh_' + s, f), cw('foot_' + s, f))) for f in range(N)), 1) for s in 'lr'}
    FE = [round(max(ae.vlen(ae.vsub(cw('foot_' + s, f), frames[f][1][s][0])) for s in 'lr'), 1) for f in range(N)]
    info = {'toe_extra': TOE_EXTRA, 'foot_err_frames': [(f, FE[f]) for f in range(N) if FE[f] > 1.5], 'v0': v0, 'planted0': {s: stt[s]['planted'] for s in 'lr'}, 'steps': [{k: (([round(x, 1) for x in vv]) if k == 'p' else vv) for k, vv in st.items()} for st in steps],
            'len': round(L, 3), 'frames': N, 'foot_err': round(ferr, 2), 'planted_drift': {s: round(drift[s], 2) for s in 'lr'}, 'loaded_pitch_over_flat_max': {s: round(pitch[s], 1) for s in 'lr'},
            'ball_z_jump_max': round(zjump, 2), 'heel_roll_max': heel_max, 'pelvis_drop_max': round(max(drop), 1), 'entry_err': round(e0, 2), 'exit_err_vs_loop': round(eF, 2), 'leg_len_max': legmax,
            'pelvis_z': [round(cw('pelvis', f)[2], 1) for f in range(0, N, 3)], 'lean': [round(ae.vdot(ae.vsub(cw('head', f), cw('pelvis', f)), FWD), 1) for f in range(0, N, 3)],
            'root_v': [round(v_of(f * DT)) for f in range(0, N, 3)]}
    SB = ['pelvis', 'spine_03', 'spine_05', 'neck_01', 'head', 'clavicle_l', 'upperarm_l', 'lowerarm_l', 'hand_l', 'clavicle_r', 'upperarm_r', 'lowerarm_r', 'hand_r',
          'thigh_l', 'calf_l', 'foot_l', 'ball_l', 'thigh_r', 'calf_r', 'foot_r', 'ball_r']
    (SD / 'stick' / (name + '.json')).write_text(json.dumps({'name': name, 'dt': DT, 'bones': SB, 'root': [[round(x, 1) for x in local['root'][f][0]] for f in range(N)],
        'planted': {s: PLN[s] for s in 'lr'}, 'steps': info['steps'], 'frames': [[[round(x, 1) for x in cw(b, f)] for b in SB] for f in range(N)]}))
    cur = {'footspeed_l': [], 'footspeed_r': []}
    for f in range(N):
        for s in 'lr':
            a = cw('ball_' + s, max(0, f - 1)); b_ = cw('ball_' + s, min(N - 1, f + 1))
            cur['footspeed_' + s].append(FS_SCALE * math.hypot(b_[0] - a[0], b_[1] - a[1]) / (DT * (min(N - 1, f + 1) - max(0, f - 1))))
    # FootPlacement leaves the pelvis to the clip (ABP DisablePelvisCurveName): from rest it ramps in over 0.15 s (idle had the FootPlacement
    # pelvis), inside a stop it starts at 1 (the V237 stop carries it), and it hands back to FootPlacement over the last 0.3 s (loop)
    cur['SHM237_FPPelvisOff'] = [(mj(f * DT / 0.15) if v0 < 1.0 else 1.0) * (1.0 - mj((f * DT - (L - 0.3)) / 0.3)) for f in range(N)]
    for cn in ('Enable_OrientationWarping', 'Disable_FootLock', 'pbi_authoredforwardlean'):
        try: cur[cn] = [AL.get_float_value(loop, cn, clock(f * DT) % T1) * (mj(v_of(f * DT) / VMAX) if cn == 'pbi_authoredforwardlean' else 1.0) for f in range(N)]
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
    try: c.open_bracket(u.Text('SHME V2.37 ' + name), True)
    except Exception: c.open_bracket('SHME V2.37 ' + name, True)
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
specs = cfg.get('clips') or [{'name': 'SHM237_JogStart_F_Lfoot', 'first': 'l'}, {'name': 'SHM237_JogStart_F_Rfoot', 'first': 'r'}]
out = {'loop': LOOP, 'T1': T1, 'vloop': round(VLOOP, 1), 'step_t': round(STEP_T, 3), 'lands': LANDS, 'lifts': LIFTS, 'seq': SEQ, 'fs_scale': round(FS_SCALE, 3), 'clips': {}}
for spec in specs:
    try: name, local, info, cur = build(spec)
    except Exception as e: out['clips'][spec['name']] = {'error': str(e)[:400]}; continue
    if not DRY: info['saved'], info['path'] = write(name, local, cur)
    out['clips'][name] = info
(SD / ('gen237_start_%s.json' % ('dry' if DRY else 'write'))).write_text(json.dumps(out, indent=1, default=str))
print('G237ST ' + json.dumps(out, default=str))
