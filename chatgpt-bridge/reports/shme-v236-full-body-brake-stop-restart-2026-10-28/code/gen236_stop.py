"""gen236_stop.py (editor job): V2.36 jog STOP family - NEW candidate assets (the production stop clip and the jog loop are never edited).
Built from the production jog loop A_CT_Jog_Fwd (the loop every jog stop leaves) and the stand idle af_Stand_Idle_NaturalBaseline_Phase275
@57.8 (the V2.8 settled stance, so the idle that follows continues the clip), on the MEASURED in-game capsule stop (fixed 30 / 60:
300 cm/s, constant 410 cm/s2 -> 0 in 0.73 s, 110 cm).

Why: the vendor CP2 jog stop is ONE clip entered at whatever time the pose search finds; its brake step lands 55-63 cm ahead of the final
root with a 27 cm apex ('march'), a 41 cm staggered stance and a late 43 cm correction step that is the closing step of out-of-phase
entries (V2.35 r1-r6). A stop is a different action for each support phase at release -> one clip per release phase (bin), each
planned from its own support.

Naming: SHM236_JogStop_B<l|r>_P<k>: B = the BRAKE foot = the first foot that LANDS after the release (the foot that takes the
deceleration); the other foot is the closing foot. P<k> = release phase bin (loop time tau0 = phases[k]).
Plan per bin (time t from the release, game units, +Y forward):
  * root = capsule stop profile (the clip root IS the capsule path; nothing else moves the capsule).
  * contacts on the BALL (FootPlacement plants the ball): a foot on the floor at the release stays pinned until its loop toe-off on a
    slowing loop clock (rate floor RFLOOR); the brake foot lands at its loop landing time; each later step lands STEP_T x (1 + slow) after
    the previous one. A landing whose final idle spot is within REACH cm ahead of the root lands there (final); otherwise it lands REACH
    ahead (a shortened brake step, never a lunge to the final spot). When the last foot is final, the other closes to its idle spot only if it
    is more than CLOSE cm away (low step, apex <= CLOSE_APEX). Swing apex scales with the step (no knee-high last step).
  * whole body (the same action time as the feet): trunk / neck / head go from the jog carriage to the idle stance over TRUNK_T s from
    the release (no 0.15 s pop upright), plus a small forward 'arrival' nod NOD deg at the capsule stop that the neck counters (head level);
    arms: the jog swing keeps its cadence but its AMPLITUDE decays (tau ARM_TAU) about a mean carriage that opens / drops into the idle
    hang over ARM_T s (elbows extend, hands fall to the hip), plus a small forward swing of the upper arms at each brake landing (inertia,
    ARM_FWD deg); pelvis: absorbs each brake landing (PEL_DIP cm x speed) and settles to the idle height (no deep lunge).
  * curves: SHM_StopSettle (1 until the final plant + 0.1 s, the idle takeover waits for it), footspeed_l / _r (from the planned balls,
    loop curve units), pbi_authoredforwardlean (loop value fading with the trunk).
builtins.G236S = {'dry_run': True, 'phases': [[tau0, 'name'], ...] | None, 'nph': 0, 'only': None, ...knobs}. Prints G236S {...}; writes
stick JSON (component positions of the key bones per frame) to Saved/Codex/SHME_V236_20261028/stick/<name>.json for the source review."""
import unreal as u, json, math, builtins, pathlib, importlib, sys
P = pathlib.Path(u.Paths.project_dir()).resolve(); sys.path.insert(0, str(P / 'Tools/SHME_V1_20260925'))
import v137_animedit as ae; importlib.reload(ae)
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'G236S', {})); DRY = bool(cfg.get('dry_run', True)); ONLY = cfg.get('only')
LOOP = '/Game/GraceRanger/Animations/Continuity/A_CT_Jog_Fwd'
IDLE = cfg.get('final_src', '/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/Phase275Support/Idle/af_Stand_Idle_NaturalBaseline_Phase275')
# V2.36b: the final stance decides the NEXT start's family: the production CP2 jog stop ends in the stance its paired straight jog start
# (SHM_JogQ_A_CP2_Jog_Fwd_Start, right-support start DB) begins from; the idle frame (V2.8 walk stops) read as left support -> the left start DB
# has no straight start -> TurnL045 for a straight request (85 cm drag). final_src / final_last select the target stance.
OUTDIR = cfg.get('outdir', '/Game/GraceRanger/SHME/Animations/V236')
SD = P / 'Saved/Codex/SHME_V236_20261028'; (SD / 'stick').mkdir(parents=True, exist_ok=True)
FPS = 30.0; DT = 1.0 / FPS
K = lambda k, d: float(cfg.get(k, d))
V0 = K('v0', 300.0); ACC = K('acc', 410.0); IDLE_T = K('idle_t', 57.8)
REACH = K('reach', 14.0); REACH_V = K('reach_v', 0.07); CLOSE = K('close', 5.0); CLOSE_APEX = K('close_apex', 3.5); CLOSE_T = K('close_t', 0.30)
RFLOOR = K('rfloor', 0.8); SLOW = K('slow', 0.30); DS0 = K('ds', 0.05)
APEX_K = K('apex_k', 0.11); APEX_MIN = K('apex_min', 4.0); APEX_MAX = K('apex_max', 9.0)
TRUNK_T = K('trunk_t', 0.60); NOD = K('nod', 2.5); NECK_K = K('neck_k', 0.75)
ARM_TAU = K('arm_tau', 0.34); ARM_T0 = K('arm_t0', 0.08); ARM_T = K('arm_t', 0.95); ARM_SET = K('arm_set', 5.0); ARM_SET_P = K('arm_set_p', 0.9); ARM_SET_D = K('arm_set_d', 0.35); ARM_FWD = K('arm_fwd', 6.0)
PEL_DIP = K('pel_dip', 1.0); HOLD = K('hold', 0.40); VCAP = K('vcap', 30.0); LIFT_K1 = K('lift_k1', 1.3); LIFT_K2 = K('lift_k2', 0.5); LOOPFOLLOW = K('loopfollow', 0.85); KNEE_MARGIN = K('knee_margin', 0.3); HEEL_MARGIN = K('heel_margin', 2.0); HEEL_SIGN = K('heel_sign', -1.0); REACH_DROP = [0.0]; HEEL = [0.0]; PEL_RISE = K('pel_rise', 1.0); PEL_T0 = K('pel_t0', 0.15); PEL_T = K('pel_t', 0.6); HEEL_CAP = K('heel_cap', 55.0); STEP_MAX = K('step_max', 38.0); STEP_MAX_V = K('step_max_v', 0.08)
TS = V0 / ACC; DFIN = V0 * V0 / (2.0 * ACC)
def stop_d(t): t = min(max(t, 0.0), TS); return V0 * t - 0.5 * ACC * t * t
def stop_v(t): return max(0.0, V0 - ACC * max(t, 0.0)) if t < TS else 0.0
loop = u.load_asset(LOOP); idle = u.load_asset(IDLE)
NAMES = [str(n) for n in AL.get_animation_track_names(loop)]
NK1 = ae.num_frames(loop) - 1; T1 = float(loop.get_play_length())
Lk = ae.read_local(loop, NAMES, list(range(NK1 + 1)))
IFR = (ae.num_frames(idle) - 1) if cfg.get('final_last') else int(round(IDLE_T * FPS))
Ik = ae.read_local(idle, NAMES, [IFR]); IDL = {b: Ik[b][0] for b in NAMES}
clip = ae.Clip(loop, ['root', 'pelvis', 'foot_l', 'foot_r', 'ball_l', 'ball_r', 'calf_l', 'calf_r', 'head', 'spine_05', 'hand_l', 'hand_r', 'lowerarm_l', 'lowerarm_r'] +
               [b for b in ('ik_foot_l', 'ik_foot_r') if b in NAMES])
D = ae.vsub(Lk['root'][NK1][0], Lk['root'][0][0]); VLOOP = ae.vlen(D) / T1; FWD = ae.vnorm(D); LEFT = ae.vnorm(ae.vcross(FWD, (0.0, 0.0, 1.0)))
def slerp(a, b, t):
    d = sum(a[i] * b[i] for i in range(4))
    if d < 0: b = tuple(-x for x in b); d = -d
    if d > 0.9995: return ae.qnorm(tuple(a[i] + (b[i] - a[i]) * t for i in range(4)))
    th = math.acos(min(d, 1.0)); s = math.sin(th)
    return tuple((math.sin((1 - t) * th) * a[i] + math.sin(t * th) * b[i]) / s for i in range(4))
def lerp(a, b, t): return tuple(a[i] + (b[i] - a[i]) * t for i in range(len(a)))
def mj(x): x = min(1.0, max(0.0, x)); return x * x * x * (10 - 15 * x + 6 * x * x)
def bump(t, tc, rise, decay):
    if t < tc - rise: return 0.0
    if t < tc: return mj((t - (tc - rise)) / rise)
    return math.exp(-(t - tc) / decay) * (1.0 - mj((t - tc - 3 * decay) / decay))
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
# ---- loop contact table
BZ = {s: [rel(loop_local(k * T1 / NK1), 'ball_' + s)[0][2] for k in range(NK1 + 1)] for s in 'lr'}
BZ0 = {s: min(BZ[s]) for s in 'lr'}
# planted = the ball is low AND nearly still in the world (root moves at VLOOP); runs shorter than 3 keys removed, gaps <= 2 keys filled
_BW = {s: [rel(loop_local(k * T1 / NK1), 'ball_' + s)[0] for k in range(NK1 + 1)] for s in 'lr'}
def _wspeed(s, k):
    a = _BW[s][(k - 1) % NK1]; b = _BW[s][(k + 1) % NK1]; dt = 2 * T1 / NK1
    return math.hypot(b[0] - a[0] + 0.0, b[1] - a[1] + VLOOP * dt) / dt
PL = {}
for s in 'lr':
    raw = [(_BW[s][k][2] < BZ0[s] + 4.0 and _wspeed(s, k) < 90.0) for k in range(NK1)]
    for k in range(NK1):                                  # fill short gaps
        if not raw[k] and raw[(k - 1) % NK1] and (raw[(k + 1) % NK1] or raw[(k + 2) % NK1]): raw[k] = True
    keep = list(raw)
    for k in range(NK1):                                  # drop short runs
        if raw[k]:
            n = 0; j = k
            while raw[j % NK1] and n < NK1: n += 1; j += 1
            m = 0; j = k
            while raw[j % NK1] and m < NK1: m += 1; j -= 1
            if n + m - 1 < 3: keep[k] = False
    PL[s] = keep
def planted(s, tau): k = int(round((tau % T1) / T1 * NK1)) % NK1; return PL[s][k]
def next_event(s, tau, land=True):
    for k in range(1, NK1 * 2):
        t = tau + k * T1 / (NK1 * 2)
        if land and planted(s, t) and not planted(s, t - T1 / (NK1 * 2)): return t
        if not land and not planted(s, t) and planted(s, t - T1 / (NK1 * 2)): return t
    return tau + T1
LANDS = {s: sorted(set(round(next_event(s, k * T1 / NK1) % T1, 3) for k in range(NK1))) for s in 'lr'}
STEP_T = T1 / (len(LANDS['l']) + len(LANDS['r']))
LAND_AHEAD = {s: [round(ae.vdot(rel(loop_local(t), 'ball_' + s)[0], FWD), 1) for t in LANDS[s]] for s in 'lr'}   # loop ball ahead of the root at landing
IDLE_REL = {s: rel(IDL, 'foot_' + s) for s in 'lr'}; IDLE_BALL = {s: rel(IDL, 'ball_' + s)[0] for s in 'lr'}
BALL_LOCAL = {s: Lk['ball_' + s][0][0] for s in 'lr'}
EXT_IDLE = {s: ae.vlen(ae.vsub(rel(IDL, 'thigh_' + s)[0], rel(IDL, 'foot_' + s)[0])) for s in 'lr'}
def foot_at_ball(s, ball, q): return ae.vsub(ball, ae.qrot(q, BALL_LOCAL[s]))
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
PMEAN = tuple(sum(Lk['pelvis'][k][0][i] for k in range(NK1)) / NK1 for i in range(3))
MEANT = {b: tuple(sum(Lk[b][k][0][i] for k in range(NK1)) / NK1 for i in range(3)) for b in ARMS}
def swing(p0, v0, p1, t0, t1, t, h, z0=None):
    if t <= t0: return p0
    if t >= t1: return p1
    T = t1 - t0; x = (t - t0) / T
    h00 = 2 * x ** 3 - 3 * x * x + 1; h10 = x ** 3 - 2 * x * x + x; h01 = -2 * x ** 3 + 3 * x * x
    xy = [h00 * p0[i] + h10 * T * v0[i] + h01 * p1[i] for i in range(2)]
    zb = (z0 if z0 is not None else p0[2]) * (1 - mj(x)) + p1[2] * mj(x)
    return (xy[0], xy[1], zb + h * math.sin(math.pi * x) * (1 - 0.35 * x))
def plan(tau0):
    """contact plan from the release at loop time tau0: list of steps {foot, t_lift, t_land, p_land, final, kind}"""
    L0 = loop_local(tau0); pl = {s: planted(s, tau0) for s in 'lr'}
    # loop clock with a floor: tau(t)
    def clock(t):
        n = max(1, int(t / 0.005)); tt = 0.0; tau = tau0
        for i in range(n): r = max(RFLOOR, stop_v(tt) / V0); tau += r * (t / n); tt += t / n
        return tau
    def t_of_tau(target):
        t = 0.0
        while t < 3.0 and clock(t) < target: t += 0.005
        return t
    land0 = {s: t_of_tau(next_event(s, tau0, True)) for s in 'lr'}
    lift0 = {s: (t_of_tau(next_event(s, tau0, False)) if pl[s] else 0.0) for s in 'lr'}
    B = min('lr', key=lambda s: land0[s] if not pl[s] else 9.0)
    if pl['l'] and pl['r']: B = min('lr', key=lambda s: lift0[s])   # double support at release: the foot leaving first steps first
    C = 'r' if B == 'l' else 'l'
    steps = []; state = {s: {'final': False, 'pos': None} for s in 'lr'}
    tB = land0[B] if not pl[B] else lift0[B] + STEP_T * 0.8
    foot, t_land, t_lift = B, tB, (0.0 if not pl[B] else lift0[B])
    prev_land = None
    for k in range(6):
        rootY = stop_d(t_land); fin = ae.vadd(ae.vsc(FWD, DFIN), IDLE_BALL[foot])
        ahead = ae.vdot(ae.vsub(fin, ae.vsc(FWD, rootY)), FWD) - ae.vdot(IDLE_BALL[foot], FWD)
        reach = REACH + REACH_V * stop_v(t_land)
        if ahead <= reach + 0.5 or t_land >= TS: p = fin; final = True
        else: p = ae.vadd(ae.vsc(FWD, rootY + reach + ae.vdot(IDLE_BALL[foot], FWD)), ae.vsc(LEFT, ae.vdot(IDLE_BALL[foot], LEFT))); p = (p[0], p[1], IDLE_BALL[foot][2]); final = False
        po_ = state['r' if foot == 'l' else 'l']['pos']
        smax = STEP_MAX + STEP_MAX_V * stop_v(t_land)
        if po_ is not None and k > 0 and ae.vdot(p, FWD) - ae.vdot(po_, FWD) > smax:     # V2.36: no over-wide stance; one more short step instead
            ya = ae.vdot(po_, FWD) + smax; p = ae.vadd(ae.vsc(FWD, ya), ae.vsc(LEFT, ae.vdot(IDLE_BALL[foot], LEFT))); p = (p[0], p[1], IDLE_BALL[foot][2]); final = False
        steps.append({'foot': foot, 't_lift': round(t_lift, 3), 't_land': round(t_land, 3), 'p': p, 'final': final, 'kind': 'brake' if k == 0 else 'step',
                      'ahead_cm': round(ae.vdot(ae.vsub(p, ae.vsc(FWD, rootY)), FWD), 1), 'v_land': round(stop_v(t_land), 1)})
        state[foot] = {'final': final, 'pos': p}
        other = 'r' if foot == 'l' else 'l'
        if final and state[other]['final']: break
        if final and state[other]['pos'] is not None:
            po = state[other]['pos']; fo = ae.vadd(ae.vsc(FWD, DFIN), IDLE_BALL[other])
            if math.hypot(po[0] - fo[0], po[1] - fo[1]) > CLOSE:
                tl = max(t_land + DS0 * 2, TS - 0.05); steps.append({'foot': other, 't_lift': round(tl, 3), 't_land': round(tl + CLOSE_T, 3), 'p': fo, 'final': True,
                    'kind': 'close', 'ahead_cm': None, 'v_land': 0.0})
            break
        # next step by the other foot
        v = stop_v(t_land); ds = DS0 * (1.0 + (1.0 - v / V0))
        if state[other]['pos'] is None: nl = lift0[other] if pl[other] else 0.0   # planted at the release: its own toe-off; in flight: already swinging
        else: nl = t_land + ds                                                   # trailing foot lifts after the double support
        nt = t_land + STEP_T * (1.0 + SLOW * (1.0 - v / V0))
        if state[other]['pos'] is None and not pl[other]: nt = max(nt, land0[other])
        foot, t_lift, t_land = other, nl, nt
    return B, C, steps, pl, L0
def build(tau0, name):
    B, C, steps, pl, L0 = plan(tau0)
    feet0 = {s: rel(L0, 'foot_' + s) for s in 'lr'}; ball0 = {s: rel(L0, 'ball_' + s)[0] for s in 'lr'}
    e = 1e-3; vloop = {}
    for s in 'lr':
        pa = rel(loop_local(tau0), 'foot_' + s)[0]; pb = rel(loop_local(tau0 + e), 'foot_' + s)[0]
        vloop[s] = tuple((pb[i] - pa[i]) / e + FWD[i] * V0 for i in range(3))
    t_end = max(st['t_land'] for st in steps); t_fin = max(t_end, TS)
    L = t_fin + 0.15 + HOLD; N = int(math.ceil(L / DT)) + 1
    # per-foot timeline: segments of (planted at p from t_a to t_b) / (swing from p0 to p1 over [t_lift, t_land])
    tl = {s: [] for s in 'lr'}
    QFIN = {s: IDLE_REL[s][1] for s in 'lr'}
    for s in 'lr':
        cur = ae.vadd((0.0, 0.0, 0.0), ball0[s]); cur_q = feet0[s][1]; t_cur = 0.0; inflight = not pl[s]
        mine = [st for st in steps if st['foot'] == s]
        for st in mine:
            if inflight and st is mine[0]:
                vv = vloop[s]; sp = math.hypot(vv[0], vv[1]) * st['t_land']; cap = min(1.0, VCAP / sp) if sp > 1e-6 else 1.0
                tl[s].append(('swing0', 0.0, st['t_land'], cur, (vv[0] * cap, vv[1] * cap, 0.0), st['p'], cur_q)); inflight = False
            else:
                tl[s].append(('plant', t_cur, st['t_lift'], cur, None, None, cur_q))
                T_ = max(st['t_land'] - st['t_lift'], 1e-3); k_ = LIFT_K1 if (pl[s] and st is mine[0]) else LIFT_K2
                vf = min(k_ * stop_v(st['t_lift']), VCAP / T_) if st['kind'] != 'close' else 0.0
                tl[s].append(('swing1' if (pl[s] and st is mine[0]) else 'swing', st['t_lift'], st['t_land'], cur, ae.vsc(FWD, vf), st['p'], cur_q))
            cur = st['p']; t_cur = st['t_land']; cur_q = QFIN[s]
        if inflight:                                  # a foot in flight that never got a step (should not happen): land it at its idle spot
            fo = ae.vadd(ae.vsc(FWD, DFIN), IDLE_BALL[s]); tl[s].append(('swing0', 0.0, max(0.3, t_end), cur, vloop[s], fo, cur_q)); cur = fo; t_cur = max(0.3, t_end)
        tl[s].append(('plant', t_cur, 99.0, cur, None, None, None))
    land_times = sorted(st['t_land'] for st in steps if st['kind'] != 'close')
    PLANTED_AT = {s: [any(sg[0] == 'plant' and sg[1] + (0.0 if sg[1] <= 0.0 else 0.04) <= f * DT <= sg[2] for sg in tl[s]) for f in range(N)] for s in 'lr'}
    frames = []; tau = tau0
    for f in range(N):
        t = f * DT
        if f: tau += max(RFLOOR, stop_v(t) / V0) * DT
        Lp = loop_local(tau)
        pose = {}
        wt = mj(t / TRUNK_T); wa = mj((t - ARM_T0) / ARM_T); amp = math.exp(-max(0.0, t) / ARM_TAU) * (1.0 - mj((t - t_fin) / 0.25))
        for b in UB: pose[b] = (lerp(Lp[b][0], IDL[b][0], wt), slerp(Lp[b][1], IDL[b][1], wt), lerp(Lp[b][2], IDL[b][2], wt))
        wp = max(mj((t - (t_end - 0.15)) / 0.45), PEL_RISE * mj((t - PEL_T0) / PEL_T))   # V2.36c: the body rises as it slows (no held jog crouch)
        pose['pelvis'] = (lerp(lerp(Lp['pelvis'][0], PMEAN, wt), IDL['pelvis'][0], wp), pose['pelvis'][1], pose['pelvis'][2])
        for b in ARMS:
            base = slerp(MEAN[b], IDL[b][1], wa)
            dq = ae.qmul(ae.qinv(MEAN[b]), Lp[b][1])
            if dq[3] < 0: dq = tuple(-x for x in dq)
            pose[b] = (lerp(lerp(MEANT[b], Lp[b][0], amp), IDL[b][0], wa), ae.qnorm(ae.qmul(base, slerp((0.0, 0.0, 0.0, 1.0), dq, amp))), lerp(Lp[b][2], IDL[b][2], wa))
        for b in LEGS:
            if b in NAMES: pose[b] = Lp[b] if b != 'root' else Lp[b]
        for b in NAMES:
            if b not in pose: pose[b] = Lp[b]
        rt = ae.vsc(FWD, stop_d(t)); pose['root'] = (rt, Lk['root'][0][1], Lk['root'][0][2])
        # pelvis absorption at the brake landings (scaled by the landing speed)
        dip = sum(PEL_DIP * (stop_v(tl_) / V0) * bump(t, tl_ + 0.06, 0.06, 0.12) for tl_ in land_times)
        pt, pq, ps = pose['pelvis']; pose['pelvis'] = ((pt[0], pt[1], pt[2] - dip), pq, ps)
        ft = {}
        for s in 'lr':
            seg = next(sg for sg in tl[s] if sg[1] <= t + 1e-9 and t <= sg[2] + 1e-9)
            kind, ta, tb, p0, v0, p1, q0 = seg
            if kind == 'plant':
                q = q0 if q0 is not None else QFIN[s]
                if kind == 'plant' and tb >= 99.0: q = QFIN[s]
                ft[s] = (foot_at_ball(s, p0, q), q)
            else:
                ln = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
                if kind == 'swing0': h = max(0.0, 2.0 + 0.04 * ln)
                elif ln < CLOSE * 3 + 10: h = CLOSE_APEX
                else: h = min(APEX_MAX, max(APEX_MIN, APEX_K * ln))
                x = (t - ta) / max(tb - ta, 1e-3)
                q = slerp(q0, QFIN[s], mj(x)); bp = swing(p0, v0 if v0 else (0.0, 0.0, 0.0), p1, ta, tb, t, h, z0=p0[2])
                if kind in ('swing0', 'swing1'):     # leave on the loop's own path (natural toe-off / swing), blend into the planned landing
                    lb, lq = rel(Lp, 'ball_' + s)[0], rel(Lp, 'foot_' + s)[1]; lb = ae.vadd(rt, lb); w_ = mj(x / LOOPFOLLOW)
                    bp = lerp(lb, bp, w_); q = slerp(lq, q, w_)
                ft[s] = (foot_at_ball(s, bp, q), q)
        frames.append((pose, ft))
    # planted foot rotations: hold the landing rotation (flat final) - set plant q from the previous swing's end
    local = {b: [fr[0][b] for fr in frames] for b in NAMES}
    # ---- whole-body additive layer (component-space rotations about the body's lateral axis)
    for f in range(len(frames)):
        t = f * DT
        nod = NOD * bump(t, TS + 0.04, 0.14, 0.18)            # forward arrival nod at the capsule stop
        if nod > 1e-3 and 'spine_03' in NAMES:
            ae.apply_bone_delta(clip_full, local, 'spine_03', f, ae.qaxis(LEFT, -nod * 0.6))
            ae.apply_bone_delta(clip_full, local, 'spine_05', f, ae.qaxis(LEFT, -nod * 0.4))
            ae.apply_bone_delta(clip_full, local, 'neck_01', f, ae.qaxis(LEFT, nod * NECK_K))
        fw = ARM_FWD * sum((stop_v(tl_) / V0) * bump(t, tl_ + 0.05, 0.07, 0.16) for tl_ in land_times)
        # arms settle after the body stops: the hands keep a little forward momentum and swing back once (damped pendulum)
        if t > TS - 0.05: fw += ARM_SET * math.sin(2 * math.pi * (t - TS + 0.05) / ARM_SET_P) * math.exp(-(t - TS + 0.05) / ARM_SET_D) * (1.0 - mj((t - L + 0.12) / 0.1))
        if abs(fw) > 1e-3:
            for s in 'lr': ae.apply_bone_delta(clip_full, local, 'upperarm_' + s, f, ae.qaxis(LEFT, fw))
    # pelvis reach limit: a wide stance cannot carry the idle pelvis height -> lower the pelvis just enough (knees keep KNEE_MARGIN cm of
    # bend), smoothed over +-4 frames (no pops); recorded as reach_drop
    # 1) a planted foot that the hip leaves behind rolls onto its ball (heel up, ball pinned) like a trailing foot does
    HEEL[0] = 0.0
    for s in 'lr':
        ang = []
        for f, (pose, ft) in enumerate(frames):
            a_ = 0.0
            if PLANTED_AT[s][f]:
                hip = clip_full.comp('thigh_' + s, f, local)[0]; ball = ae.vadd(ft[s][0], ae.qrot(ft[s][1], BALL_LOCAL[s]))
                Lh = max(ae.vlen(local['calf_' + s][f][0]) + ae.vlen(local['foot_' + s][f][0]) - (HEEL_MARGIN if f * DT > 0.12 else 0.4), EXT_IDLE[s] + 0.3)
                for k in range(0, int(HEEL_CAP) + 1):
                    q = ae.qnorm(ae.qmul(ae.qaxis(LEFT, HEEL_SIGN * k), ft[s][1])); fp = foot_at_ball(s, ball, q)
                    if ae.vlen(ae.vsub(hip, fp)) <= Lh: a_ = float(k); break
                else: a_ = HEEL_CAP
            ang.append(a_)
        mx = [max(ang[max(0, f - 2):f + 3]) for f in range(len(ang))]
        sm_ = [sum(mx[max(0, f - 2):f + 3]) / len(mx[max(0, f - 2):f + 3]) for f in range(len(mx))]
        sm_ = [sm_[f] * mj(f * DT / 0.1) for f in range(len(sm_))]      # the entry frame stays the loop pose
        for f, (pose, ft) in enumerate(frames):
            if sm_[f] > 0.05:
                ball = ae.vadd(ft[s][0], ae.qrot(ft[s][1], BALL_LOCAL[s])); q = ae.qnorm(ae.qmul(ae.qaxis(LEFT, HEEL_SIGN * sm_[f]), ft[s][1]))
                ft[s] = (foot_at_ball(s, ball, q), q)
        HEEL[0] = max(HEEL[0], max(sm_))
    # 2) what the heel cannot give: lower the pelvis (only beyond a straight leg)
    need = []
    for f, (pose, ft) in enumerate(frames):
        dm = 0.0
        for s in 'lr':
            if not PLANTED_AT[s][f]: continue
            hip = clip_full.comp('thigh_' + s, f, local)[0]; fp = ft[s][0]
            Lm = max(ae.vlen(local['calf_' + s][f][0]) + ae.vlen(local['foot_' + s][f][0]) - KNEE_MARGIN, EXT_IDLE[s] + 0.3)
            hz = hip[2] - fp[2]; hor = math.hypot(hip[0] - fp[0], hip[1] - fp[1])
            if hz * hz + hor * hor > Lm * Lm: dm = max(dm, hz - math.sqrt(max(Lm * Lm - hor * hor, 0.0)))
        need.append(dm)
    mx = [max(need[max(0, f - 4):f + 5]) for f in range(len(need))]
    drop = [sum(mx[max(0, f - 4):f + 5]) / len(mx[max(0, f - 4):f + 5]) for f in range(len(mx))]
    drop = [max(drop[f], need[f]) * mj(f * DT / 0.12) for f in range(len(drop))]
    for f in range(len(frames)):
        pt, pq, ps = local['pelvis'][f]; local['pelvis'][f] = ((pt[0], pt[1], pt[2] - drop[f]), pq, ps)
    REACH_DROP[0] = round(max(drop), 1)
    for f, (pose, ft) in enumerate(frames):
        for s in 'lr':
            kh = clip_full.comp('calf_' + s, f, local)[0]
            ae.solve_leg(clip_full, local, s, f, ft[s][0], ft[s][1], kh)
    for s in 'lr':
        b = 'ik_foot_' + s
        if b in NAMES and 'ik_foot_root' in NAMES:
            for f in range(len(frames)):
                fp, fq = clip_full.comp('foot_' + s, f, local); pp, pq = clip_full.comp('ik_foot_root', f, local)
                lt = ae.qrot(ae.qinv(pq), ae.vsub(fp, pp)); lq = ae.qnorm(ae.qmul(ae.qinv(pq), fq)); local[b][f] = (lt, lq, local[b][f][2])
    # ---- checks
    def cw(b, f): return clip_full.comp(b, f, local)[0]
    fe_all = [(ae.vlen(ae.vsub(cw('foot_' + s, f), frames[f][1][s][0])), f, s) for f in range(len(frames)) for s in 'lr']
    ferr = max(x[0] for x in fe_all); ferr_at = [(round(x[0], 1), round(x[1] * DT, 2), x[2]) for x in sorted(fe_all, reverse=True)[:4]]
    drift = 0.0; pen = 0.0; apex = {}
    for s in 'lr':
        for f in range(1, len(frames)):
            a, b_ = cw('ball_' + s, f - 1), cw('ball_' + s, f)
            pen = min(pen, b_[2] - BZ0[s])
            fz = max(BZ0[s], IDLE_BALL[s][2]) + 1.0
            if a[2] < fz and b_[2] < fz:
                d_ = math.hypot(b_[0] - a[0], b_[1] - a[1]); drift += d_ if d_ > 0.05 else 0.0
    for i, st in enumerate(steps):
        f0 = int(st['t_lift'] / DT); f1 = min(len(frames) - 1, int(math.ceil(st['t_land'] / DT)))
        st['apex_cm'] = round(max(cw('ball_' + st['foot'], f)[2] for f in range(f0, f1 + 1)) - BZ0[st['foot']], 1)
        st['p'] = [round(x, 1) for x in st['p']]
    fin = len(frames) - 1
    fe = max(ae.vlen(ae.vsub(ae.vsub(cw('foot_' + s, fin), local['root'][fin][0]), IDLE_REL[s][0])) for s in 'lr')
    he = ae.vlen(ae.vsub(ae.vsub(cw('head', fin), local['root'][fin][0]), rel(IDL, 'head')[0]))
    e0 = max(ae.vlen(ae.vsub(ae.vsub(cw(bn, 0), local['root'][0][0]), rel(loop_local(tau0), bn)[0])) for bn in ('foot_l', 'foot_r', 'head', 'pelvis', 'hand_l', 'hand_r'))
    lean = [round(ae.vdot(ae.vsub(cw('head', f), cw('pelvis', f)), FWD), 1) for f in range(0, len(frames), 3)]
    pz = [round(cw('pelvis', f)[2], 1) for f in range(0, len(frames), 3)]
    hz = [round(0.5 * (cw('hand_l', f)[2] + cw('hand_r', f)[2]), 1) for f in range(0, len(frames), 3)]
    hy = [round(cw('hand_l', f)[1] - cw('pelvis', f)[1], 1) for f in range(0, len(frames), 3)]
    info = {'heel_max_deg': round(HEEL[0], 1), 'reach_drop_max': REACH_DROP[0], 'tau0': round(tau0, 3), 'B': B, 'C': C, 'planted_at_release': pl, 'steps': steps, 'len': round(L, 3), 'frames': N, 't_stop': round(TS, 3),
            'foot_err': round(ferr, 2), 'foot_err_at': ferr_at, 'planted_drift': round(drift, 2), 'penetration': round(pen, 2), 'entry_err': round(e0, 2),
            'final_foot_err': round(fe, 2), 'final_head_err': round(he, 2), 'lean_head_minus_pelvis_cm_0.1s': lean, 'pelvis_z': pz, 'hand_z': hz, 'hand_l_y_rel': hy}
    # stick data for the source review (component space incl. root motion)
    SB = ['pelvis', 'spine_03', 'spine_05', 'neck_01', 'head', 'clavicle_l', 'upperarm_l', 'lowerarm_l', 'hand_l', 'clavicle_r', 'upperarm_r', 'lowerarm_r', 'hand_r',
          'thigh_l', 'calf_l', 'foot_l', 'ball_l', 'thigh_r', 'calf_r', 'foot_r', 'ball_r']
    stick = {'name': name, 'dt': DT, 'bones': SB, 'frames': [[[round(x, 1) for x in cw(b, f)] for b in SB] for f in range(len(frames))],
             'steps': [{k: v for k, v in st.items()} for st in steps], 't_stop': TS}
    (SD / 'stick' / (name + '.json')).write_text(json.dumps(stick))
    # curves
    cur = {'SHM_StopSettle': [], 'footspeed_l': [], 'footspeed_r': [], 'pbi_authoredforwardlean': []}
    t_settle = t_end + 0.1
    for f in range(len(frames)):
        t = f * DT
        cur['SHM_StopSettle'].append(1.0 if t <= t_settle else max(0.0, 1.0 - (t - t_settle) / 0.1))
        for s in 'lr':
            a = cw('ball_' + s, max(0, f - 1)); b_ = cw('ball_' + s, min(len(frames) - 1, f + 1))
            sp = math.hypot(b_[0] - a[0], b_[1] - a[1]) / (DT * (min(len(frames) - 1, f + 1) - max(0, f - 1)))
            cur['footspeed_' + s].append(sp * FS_SCALE)
        cur['pbi_authoredforwardlean'].append(PBI_LEAN * (1.0 - mj(t / TRUNK_T)))
    return local, info, cur
# full-skeleton FK helper (all ancestors of the bones we rotate)
clip_full = ae.Clip(loop, ['root', 'pelvis', 'foot_l', 'foot_r', 'ball_l', 'ball_r', 'calf_l', 'calf_r', 'head', 'neck_01', 'spine_03', 'spine_05', 'hand_l', 'hand_r',
                           'lowerarm_l', 'lowerarm_r', 'upperarm_l', 'upperarm_r', 'clavicle_l', 'clavicle_r', 'thigh_l', 'thigh_r'] + [b for b in ('ik_foot_l', 'ik_foot_r', 'ik_foot_root') if b in NAMES])
# loop curve units: footspeed vs the planned ball speed of the loop itself; authored lean value
def _loop_curve(name):
    try: return [AL.get_float_value(loop, name, k * T1 / NK1) for k in range(NK1)]
    except Exception: return None
FS_LOOP = _loop_curve('footspeed_l'); PBI_LOOP = _loop_curve('pbi_authoredforwardlean')
_bs = []
for k in range(NK1):
    a = rel(loop_local(k * T1 / NK1), 'ball_l')[0]; b_ = rel(loop_local((k + 1) * T1 / NK1), 'ball_l')[0]
    _bs.append(math.hypot(b_[0] - a[0], b_[1] - a[1] + VLOOP * T1 / NK1) / (T1 / NK1))
FS_SCALE = (max(FS_LOOP) / max(_bs)) if FS_LOOP and max(_bs) > 0 else 1.0
PBI_LEAN = (sum(PBI_LOOP) / len(PBI_LOOP)) if PBI_LOOP else 0.0
def write(name, local, cur):
    path = OUTDIR + '/' + name
    ae.leg_guard(loop, local, label=name)
    seq = u.load_asset(path) if EAL.does_asset_exist(path) else EAL.duplicate_asset(LOOP, path)
    for tr in [str(t) for t in AL.get_animation_notify_track_names(seq)]:
        AL.remove_animation_notify_events_by_track(seq, tr)
        try: AL.remove_animation_notify_track(seq, tr)
        except Exception: pass
    n = len(local['root']); c = ae.controller(seq)
    try: c.open_bracket(u.Text('SHME V2.36 jog stop ' + name), True)
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
# ---- bins
LANDALL = sorted([(t, s) for s in 'lr' for t in LANDS[s]])
phases = cfg.get('phases')
if not phases:
    nph = int(cfg.get('nph', 2)); phases = []
    if nph == 2:                                           # representative: release 0.15 s of loop time before each foot's landing
        for s in 'lr': phases.append([(LANDS[s][0] - 0.15) % T1, 'SHM236_JogStop_B%s_P0' % s])
    else:
        for k in range(nph): phases.append([k * T1 / nph, k])            # bins over the whole loop (its two strides differ slightly)
out = {'ext_idle': EXT_IDLE, 'loop_land_ahead': LAND_AHEAD, 'idle_ball_fwd': {s: round(ae.vdot(IDLE_BALL[s], FWD), 1) for s in 'lr'}, 'planted_keys': {s: ''.join('1' if x else '.' for x in PL[s]) for s in 'lr'}, 'loop': LOOP, 'T1': round(T1, 4), 'NK1': NK1, 'vloop': round(VLOOP, 1), 'lands': LANDS, 'step_t': round(STEP_T, 3), 'BZ0': BZ0,
       'fs_scale': round(FS_SCALE, 4), 'pbi_lean': round(PBI_LEAN, 3), 't_stop': round(TS, 3), 'd_stop': round(DFIN, 1), 'clips': {}}
for tau0, name in phases:
    tau0 = float(tau0)
    if not isinstance(name, str):
        B_, _, _, _, _ = plan(tau0); name = 'SHM236_JogStop_B%s_P%02d' % (B_, int(name))
    if ONLY and name not in ONLY: continue
    local, info, cur = build(tau0, name)
    if not DRY: info['saved'], info['path'] = write(name, local, cur)
    out['clips'][name] = info
(SD / ('gen236_stop_%s.json' % ('dry' if DRY else 'write'))).write_text(json.dumps(out, indent=1, default=str))
print('G236S ' + json.dumps(out, default=str))
