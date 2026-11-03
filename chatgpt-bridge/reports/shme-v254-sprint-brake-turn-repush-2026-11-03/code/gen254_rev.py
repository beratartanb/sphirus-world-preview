"""gen254_rev.py (editor job): V2.54 physics-planned BRAKE -> PIVOT -> TRANSFER -> RE-PUSH turn-around (180 deg, also 135) from any loop
phase of the SPRINT (default) or jog loop - new candidate assets (never in place). Generalises gen238_cut.py (jog 90).
Why (v254a60 s54_rev / j54_rev, fixed 60, redir254.py on the visible mesh, production V2.53):
  * an opposite request at sprint plays the vendor A_LR_Run_Pivot_F_B (route SHM_RedirectDB_SRL/SRR) and then backward walk / run loops:
    CR_Backpedal is true from the request frame (LookDrivenLocomotion: the opposite input is 'backward' in the body frame LocoYaw), the
    body never faces the new direction in 2.2 s, travels backward 1.0 s with the trunk upright (lean +43 -> 0 deg); jog reversal = SHM236
    F_B content + back-run (1.7 s backward). Nothing brakes, plants, turns the body and re-pushes.
Plan (the gen238 rules, contact by contact, roles decided from the simulated state, never a table of angles):
  * the swing in progress lands at its natural loop time (no delay); while the speed along the old travel is above V_PIV x v0 every contact
    is an in-line BRAKE (A_BRK per contact period, the foot lands ahead on the facing line, the trunk leans back with the braking share);
  * the first OUTSIDE-foot contact below that speed is the PIVOT plant: it stops the body and starts the new direction a little
    (VEX_PIVOT), the body (facing) turns over it; an inside foot below the speed takes one more settling brake step instead;
  * TRANSFER: the inside foot lands toward the new travel (A_CUT), then PUSH contacts re-accelerate at A_PUSH on the new line until the
    clip hands over to the loop at EXIT_V x v0 (the loop's own acceleration finishes it - the cost of the reversal is visible);
  * the body facing is a separate signal from the velocity heading: 0 through the brake (head and chest begin to lead at the request),
    turning 0 -> ANG from the pivot plant to the transfer, then the travel heading.
Curves: SHM226_V = signed speed along the facing (V2.28 clip-speed contract), SHM226_W; SHM238_Turn = facing x 90 / ANG with SHM238_W (V2.38
yaw contract: Cmd = Yaw0 + Delta x Turn / 90), SHM254_Side = +1 right / -1 left turn while W (fixes the sign of a +-180 request), SHM254_W;
SHM237_FPPelvisOff, loop curves. builtins.G254REV = {'dry_run': True, 'clips': [{'name', 'tau0', 'side'}], 'loop': ..., knobs}.
Prints G254REV {...}."""
import unreal as u, json, math, builtins, pathlib, importlib, sys
P = pathlib.Path(u.Paths.project_dir()).resolve(); sys.path.insert(0, str(P / 'Tools/SHME_V1_20260925'))
import v137_animedit as ae; importlib.reload(ae)
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'G254REV', {})); DRY = bool(cfg.get('dry_run', True))
K = lambda k, d: float(cfg.get(k, d))
BLOCK_T = K('block_t', 0.12); OWN_TAIL = K('own_tail', 0.05)
LOOP = cfg.get('loop', '/Game/GraceRanger/SHME/Animations/V233/SprintCalm/SHM233_Calm_A_LB_Sprint_Fwd')   # the gait loop the cut leaves and returns to
OUTDIR = cfg.get('outdir', '/Game/GraceRanger/SHME/Animations/V254'); SD = P / 'Saved/Codex/SHME_V254_20261104'; (SD / 'stick').mkdir(parents=True, exist_ok=True)
FPS = 30.0; DT = 1.0 / FPS; G = 981.0
A_CUT = K('a_cut', 0.55 * G); A_BR = K('a_br', 410.0); A_PUSH = K('a_push', 300.0); A_WEAK = K('a_weak', 0.5)
VEX_PLANT = K('vex_plant', 0.55); VEX_TR = K('vex_tr', 0.80); AIM_T0 = K('aim_t0', 0.06); AIM_T = K('aim_t', 0.20); XOVER = K('xover', 0.2)
ST_BRAKE = K('st_brake', 0.33); ST_TR = K('st_tr', 0.31); D_PLANT = K('d_plant', 38.0); BRAKE_EXTRA = K('brake_extra', 6.0); OUT_LAT = K('out_lat', 6.0)
HEAD_LEAD = K('head_lead', 0.45); HEAD_MAX = K('head_max', 30.0); CHEST_LEAD = K('chest_lead', 10.0); PELV_LEAD = K('pelv_lead', 8.0)
LEAN_BACK = K('lean_back', 14.0); UPRIGHT = K('upright', 12.0); LEAN_TAU = K('lean_tau', 0.25); FACE_TAIL = K('face_tail', 0.25); LEAN_LAT = K('lean_lat', 0.55); LEAN_LAT_MAX = K('lean_lat_max', 9.0); ARM_DAMP = K('arm_damp', 0.6)
DIP_CM = K('dip_cm', 1.8); PLANT_YAW = K('plant_yaw', 0.30); TR_YAW = K('tr_yaw', 0.30)
HEEL_CAP = K('heel_cap', 50.0); HEEL_PUSH0 = K('heel_push0', 18.0); HEEL_PUSHV = K('heel_pushv', 14.0); PUSH_T = K('push_t', 0.16); TOE_MAX = K('toe_max', 85.0)
KNEE_MARGIN = K('knee_margin', 0.4); HEEL_MARGIN = K('heel_margin', 1.5); LOOPDEV = K('loopdev', 0.55); APEX_MIN = K('apex_min', 4.5); LANDC = K('landc', 2.5)
TAIL = K('tail', 0.45); SMOOTH_F = int(K('smooth_f', 4)); NSTEP_MAX = int(K('nstep_max', 11)); REACH0 = K('reach0', 14.0); REACH_V = K('reach_v', 0.07)
ANG = K('ang', 180.0); A_BRK = K('a_brk', 0.50 * G); V_PIV = K('v_piv', 0.30); VEX_PIVOT = K('vex_pivot', 0.10); PIV_T = K('piv_t', 0.36); EXIT_V = K('exit_v', 0.85); FACE_LEAD = K('face_lead', 0.06); D_PIV = K('d_piv', 20.0); PIV_LAG = K('piv_lag', 25.0)
VPIV = V_PIV if ANG >= 135.0 else K('v_piv90', 0.55); VEXP = VEX_PIVOT if ANG >= 135.0 else VEX_PLANT; PIV_T_ = PIV_T if ANG >= 135.0 else ST_TR
loop = u.load_asset(LOOP)
NAMES = [str(n) for n in AL.get_animation_track_names(loop)]
NK1 = ae.num_frames(loop) - 1; T1 = float(loop.get_play_length())
Lk = ae.read_local(loop, NAMES, list(range(NK1 + 1)))
BONES = ['root', 'pelvis', 'foot_l', 'foot_r', 'ball_l', 'ball_r', 'calf_l', 'calf_r', 'head', 'neck_01', 'spine_01', 'spine_03', 'spine_05', 'hand_l', 'hand_r',
         'lowerarm_l', 'lowerarm_r', 'upperarm_l', 'upperarm_r', 'clavicle_l', 'clavicle_r', 'thigh_l', 'thigh_r'] + [b for b in ('ik_foot_l', 'ik_foot_r', 'ik_foot_root') if b in NAMES]
clip = ae.Clip(loop, BONES)
D = ae.vsub(Lk['root'][NK1][0], Lk['root'][0][0]); VLOOP = ae.vlen(D) / T1; FWD = ae.vnorm(D); LEFT = ae.vnorm(ae.vcross(FWD, (0.0, 0.0, 1.0))); RIGHT = ae.vsc(LEFT, -1.0)
ZAX = (0.0, 0.0, 1.0)
def qyaw(h): return ae.qaxis(ZAX, h)
_chk = ae.qrot(qyaw(90.0), FWD); assert ae.vdot(_chk, RIGHT) > 0.99, ('yaw sign', _chk, RIGHT)   # +h turns FWD toward RIGHT
def slerp(a, b, t):
    d = sum(a[i] * b[i] for i in range(4))
    if d < 0: b = tuple(-x for x in b); d = -d
    if d > 0.9995: return ae.qnorm(tuple(a[i] + (b[i] - a[i]) * t for i in range(4)))
    th = math.acos(min(d, 1.0)); s = math.sin(th)
    return tuple((math.sin((1 - t) * th) * a[i] + math.sin(t * th) * b[i]) / s for i in range(4))
def lerp(a, b, t): return tuple(a[i] + (b[i] - a[i]) * t for i in range(len(a)))
def mj(x): x = min(1.0, max(0.0, x)); return x * x * x * (10 - 15 * x + 6 * x * x)
def bell(x): return math.sin(math.pi * min(1.0, max(0.0, x))) ** 2
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
# ---- loop contact table (the V2.36/V2.37 rule: ball low and nearly still in the world; short runs / gaps cleaned)
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
SEQ = sorted([(t, s) for s in 'lr' for t in LANDS[s]]); STEP_T = T1 / len(SEQ)
def next_event(lst, tau):                                                     # first event >= tau (absolute loop time, cycles unrolled)
    c = math.floor(tau / T1); best = None
    for k in (c, c + 1, c + 2):
        for x in lst:
            v = x + k * T1
            if v >= tau - 1e-6 and (best is None or v < best): best = v
    return best
def prev_event(lst, tau):
    c = math.floor(tau / T1); best = None
    for k in (c - 1, c):
        for x in lst:
            v = x + k * T1
            if v < tau - 1e-6 and (best is None or v > best): best = v
    return best
LOOP_BALL = lambda s, tau: rel(loop_local(tau), 'ball_' + s)[0]
LOOP_FOOT = lambda s, tau: rel(loop_local(tau), 'foot_' + s)
def fpitch(foot, ball, fwd): return math.degrees(math.atan2(foot[2] - ball[2], ae.vdot(ae.vsub(ball, foot), fwd)))
FLATL = {s: min(fpitch(LOOP_FOOT(s, x)[0], LOOP_BALL(s, x), FWD) for x in LANDS[s]) for s in 'lr'}
TOE_EXTRA = {s: max(0.0, max(fpitch(LOOP_FOOT(s, x)[0], LOOP_BALL(s, x), FWD) for x in LIFTS[s]) - FLATL[s]) for s in 'lr'}
BALL_LOCAL = {s: Lk['ball_' + s][0][0] for s in 'lr'}
def foot_at_ball(s, ball, q): return ae.vsub(ball, ae.qrot(q, BALL_LOCAL[s]))
LATL = {s: ae.vdot(LOOP_BALL(s, LANDS[s][0]), LEFT) for s in 'lr'}          # the loop's track (signed, left +)
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
def _loop_curve(name):
    try: return [AL.get_float_value(loop, name, k * T1 / NK1) for k in range(NK1)]
    except Exception: return None
FS_LOOP = _loop_curve('footspeed_l')
_bs = [math.hypot(_BW['l'][(k + 1) % NK1][0] - _BW['l'][k][0], _BW['l'][(k + 1) % NK1][1] - _BW['l'][k][1] + VLOOP * T1 / NK1) / (T1 / NK1) for k in range(NK1)]
FS_SCALE = (max(FS_LOOP) / max(_bs)) if FS_LOOP and max(_bs) > 0 else 1.0
def loop_swing(s, tl):
    t0 = prev_event(LIFTS[s], tl); n = 24; pts = []
    for i in range(n + 1):
        tau = t0 + (tl - t0) * i / n; pts.append(ae.vadd(LOOP_BALL(s, tau), ae.vsc(FWD, VLOOP * (tau - t0))))
    a, b = pts[0], pts[-1]; dev = [ae.vsub(pts[i], lerp(a, b, i / n)) for i in range(n + 1)]
    return dev, ae.vlen(ae.vsub(b, a))
def dev_at(dev, x):
    n = len(dev) - 1; f = min(max(x, 0.0), 1.0) * n; i = min(int(f), n - 1); w = f - i
    return lerp(dev[i], dev[i + 1], w)
def reach(v): return REACH0 + REACH_V * v
# ---- the physics plan (local frame: x = old travel, y = toward the turn)
def plan(tau0, side):
    sgn = 1.0 if side == 'R' else -1.0; OUT = 'l' if side == 'R' else 'r'; IN = 'r' if side == 'R' else 'l'; v0 = VLOOP
    # V2.54: contacts and velocity are simulated TOGETHER - each contact's role comes from the state at its touchdown
    ang = math.radians(ANG); DN = (math.cos(ang), math.sin(ang))            # the new travel direction (local: x old travel, y toward the turn)
    nl = min([(next_event(LANDS[s], tau0 + 1e-4), s) for s in 'lr'])
    t1 = nl[0] - tau0; F = nl[1]; contacts = []; phase = 'brake'; k = 0; t = t1
    h = 0.002; ts = [0.0]; vx = [v0]; vy = [0.0]; px = [0.0]; py = [0.0]; ci = []; tend = None
    def run(t_end, c):
        while ts[-1] < t_end - 1e-9:
            tt = ts[-1] + h; x, y = vx[-1], vy[-1]; ax = ay = 0.0
            if c is not None:
                rl = c['role']; sp = math.hypot(x, y)
                if rl == 'brake':
                    if sp > 1e-6: s_ = min(A_BRK, sp / h) / sp; ax, ay = -x * s_, -y * s_
                else:
                    f_ = {'plant': VEXP, 'transfer': VEX_TR, 'push': 1.0}[rl]; tgt = (DN[0] * f_ * v0, DN[1] * f_ * v0)
                    cap = {'plant': A_CUT * (A_WEAK + (1.0 - A_WEAK) * c['aim']), 'transfer': A_CUT, 'push': A_PUSH}[rl]
                    dx, dy = tgt[0] - x, tgt[1] - y; dl = math.hypot(dx, dy)
                    if dl > 1e-6: s_ = min(cap, dl / h) / dl; ax, ay = dx * s_, dy * s_
            nx, ny = x + ax * h, y + ay * h; ts.append(tt); vx.append(nx); vy.append(ny)
            px.append(px[-1] + 0.5 * (x + nx) * h); py.append(py[-1] + 0.5 * (y + ny) * h); ci.append((ax, ay))
    run(t1, None)
    while k < NSTEP_MAX:
        x, y = vx[-1], vy[-1]; along_old = x
        aim = min(1.0, max(0.0, (t - AIM_T0) / AIM_T)) if k == 0 else 1.0
        if phase == 'brake':
            if along_old > VPIV * v0 or (F != OUT and along_old > 0.12 * v0) or aim < 0.25: role = 'brake'
            else: role = 'plant'; phase = 'turned'
        elif phase == 'turned': role = 'transfer'; phase = 'push'
        else: role = 'push'
        c = {'foot': F, 't': round(t, 4), 'role': role, 'steer': aim > 0.0, 'aim': aim}; contacts.append(c); k += 1
        per = ST_BRAKE if role == 'brake' else (PIV_T_ if role == 'plant' else (ST_TR if role == 'transfer' else STEP_T))
        run(t + per, c); F = 'r' if F == 'l' else 'l'; t += per
        x, y = vx[-1], vy[-1]
        if role == 'push' and x * DN[0] + y * DN[1] >= EXIT_V * v0: break
    tend = ts[-1]
    ci.append(ci[-1])
    def at(tt):
        j = min(int(max(tt, 0.0) / h), len(ts) - 2); w = (tt - ts[j]) / h if tt < ts[-1] else 1.0
        if tt >= ts[-1]:
            return (px[-1] + vx[-1] * (tt - ts[-1]), py[-1] + vy[-1] * (tt - ts[-1]), vx[-1], vy[-1], 0.0, 0.0)
        return (px[j] + (px[j + 1] - px[j]) * w, py[j] + (py[j + 1] - py[j]) * w, vx[j] + (vx[j + 1] - vx[j]) * w, vy[j] + (vy[j + 1] - vy[j]) * w, ci[j][0], ci[j][1])
    # trim contacts: keep those up to the first push contact whose landing velocity is ~aligned and fast (that one is the loop handover)
    keep = list(contacts)
    tp_ = [c['t'] for c in keep if c['role'] == 'plant']; ttr_ = [c['t'] for c in keep if c['role'] == 'transfer']
    t_pl = tp_[0] if tp_ else keep[0]['t']; t_tr = ttr_[0] if ttr_ else t_pl + PIV_T
    def face(tt):                                     # body facing (deg toward the turn): 0 through the brake, turning over the pivot
        return ANG * mj((tt - (t_pl - FACE_LEAD)) / max(0.1, (t_tr + FACE_TAIL) - (t_pl - FACE_LEAD)))
    return {'sgn': sgn, 'OUT': OUT, 'IN': IN, 't1': t1, 'contacts': keep, 'at': at, 'tend': tend, 'face': face, 't_pl': t_pl, 't_tr': t_tr}
def hdg(vx_, vy_): return math.degrees(math.atan2(vy_, max(vx_, -1e9))) if math.hypot(vx_, vy_) > 1e-3 else 0.0
def world(sgn, x, y): return ae.vadd(ae.vsc(FWD, x), ae.vsc(RIGHT, sgn * y))
def build(spec):
    name = spec['name']; tau0 = float(spec['tau0']); side = spec.get('side', 'R')
    PLN = plan(tau0, side); sgn = PLN['sgn']; at = PLN['at']; C = PLN['contacts']; OUT = PLN['OUT']
    v0 = VLOOP
    FACE = PLN['face']
    def state(t):
        x, y, vx_, vy_, ax, ay = at(t); h_ = FACE(t); hv = hdg(vx_, vy_)
        vl = vx_ * math.cos(math.radians(h_)) + vy_ * math.sin(math.radians(h_))       # signed speed along the facing
        return {'p': world(sgn, x, y), 'h': h_, 'hv': hv, 'v': math.hypot(vx_, vy_), 'vl': vl, 'ax': ax, 'ay': ay, 'vx': vx_, 'vy': vy_}
    # loop phase clock: each contact <-> the loop landing of that foot (in order); linear between; root-consistent after the last contact
    taus = []; last = tau0
    for c in C:
        tl = next_event(LANDS[c['foot']], last + 0.02); taus.append(tl); last = tl
    tN = C[-1]['t']; tauN = taus[-1]
    def clock(t):
        if t <= C[0]['t']: return tau0 + (taus[0] - tau0) * (t / max(C[0]['t'], 1e-3))
        for j in range(1, len(C)):
            if t <= C[j]['t']: return taus[j - 1] + (taus[j] - taus[j - 1]) * (t - C[j - 1]['t']) / (C[j]['t'] - C[j - 1]['t'])
        return tauN + (t - tN) * (state(t)['v'] / VLOOP)
    def t_of_tau(target, t0):
        t = t0
        while t < t0 + 3.0 and clock(t) < target: t += 0.004
        return t
    # contact placements (ball positions, world) + landing foot rotations
    for j, c in enumerate(C):
        s = state(c['t']); hh = s['h']; ah = math.hypot(s['ax'], s['ay'])
        lat = LATL[c['foot']]; latv = ae.qrot(qyaw(sgn * hh), ae.vsc(LEFT, lat))
        if c['role'] in ('brake', 'weak'):
            p = ae.vadd(ae.vadd(s['p'], ae.vsc(world(sgn, math.cos(math.radians(hh)), math.sin(math.radians(hh))), reach(s['v']) + BRAKE_EXTRA)), latv); yaw = hh
            pass
        elif c['role'] == 'plant':
            # force from the foot to the CoM: the foot goes opposite the acceleration it must deliver (ahead and outside)
            ua = world(sgn, -s['ax'] / max(ah, 1e-3), -s['ay'] / max(ah, 1e-3)) if ah > 1.0 else world(sgn, 1.0, 0.0)
            p = ae.vadd(s['p'], ae.vsc(ua, D_PIV if ANG >= 135.0 else D_PLANT))
            out_lat = ae.vdot(ae.vsub(p, s['p']), world(sgn, 0.0, -1.0))          # outward of the turn (+)
            need = abs(lat) + OUT_LAT
            if out_lat < need: p = ae.vadd(p, ae.vsc(world(sgn, 0.0, -1.0), need - out_lat))
            yaw = hh + PLANT_YAW * (ANG - hh)
        else:
            dirh = world(sgn, math.cos(math.radians(hh)), math.sin(math.radians(hh)))
            p = ae.vadd(ae.vadd(s['p'], ae.vsc(dirh, reach(s['v']))), latv); yaw = hh + (TR_YAW * (ANG - hh) if c['role'] == 'transfer' else 0.0)
        if c['aim'] < 1.0:                           # little time to re-aim: between where the loop puts it and the plan
            pr = ae.vadd(s['p'], ae.qrot(qyaw(sgn * hh), LOOP_BALL(c['foot'], taus[j])))
            if j == 0 and planted(c['foot'], tau0) and c['t'] < 0.1: pr = rel(loop_local(tau0), 'ball_' + c['foot'])[0]   # already down at frame 0
            down0 = j == 0 and planted(c['foot'], tau0) and c['t'] < 0.1
            p = pr if down0 else lerp(pr, p, c['aim']); yaw = hh if down0 else hh + (yaw - hh) * c['aim']
        c['p'] = (p[0], p[1], BZ0[c['foot']]); c['yaw'] = yaw; c['v'] = round(s['v'], 1); c['h'] = round(hh, 1); c['tau'] = round(taus[j], 3)
        ql = LOOP_FOOT(c['foot'], taus[j])[1]; c['q'] = ae.qnorm(ae.qmul(qyaw(sgn * yaw), ql))
    L = tN + TAIL; N = int(math.ceil(L / DT)) + 1
    # frame-0 state of each foot (loop at tau0, root at the origin)
    P0 = loop_local(tau0)
    tl = {s: [] for s in 'lr'}
    for s in 'lr':
        mine = [c for c in C if c['foot'] == s]; b0 = rel(P0, 'ball_' + s)[0]; q0 = rel(P0, 'foot_' + s)[1]
        if planted(s, tau0) and mine and mine[0]['t'] < 0.1 and C.index(mine[0]) == 0:   # its first contact IS the stance it is in
            cur, curq, tcur, first_sw = mine[0]['p'], q0, 0.0, False; mine = mine[1:]
        elif planted(s, tau0):
            cur, curq, tcur, first_sw = b0, q0, 0.0, False
        else:
            ta = tau0 - 1.0 / NK1 * T1; tb = tau0 + 1.0 / NK1 * T1
            vel = ae.vsc(ae.vsub(ae.vadd(LOOP_BALL(s, tb), ae.vsc(FWD, VLOOP * (tb - tau0))), ae.vadd(LOOP_BALL(s, ta), ae.vsc(FWD, VLOOP * (ta - tau0)))), 1.0 / (tb - ta))
            cur, curq, tcur, first_sw = b0, q0, 0.0, True
        for c in mine:
            j = C.index(c)
            if not first_sw and tcur == 0.0 and planted(s, tau0):   # the stance it is in at the request ends where the loop lifts it
                lt = max(DT, min(t_of_tau(next_event(LIFTS[s], tau0 + 1e-4), 0.0), c['t'] - 0.15))
                tl[s].append(('plant', tcur, lt, cur, curq)); ta_ = lt; vel0 = None
            elif not first_sw:
                lt = t_of_tau(prev_event(LIFTS[s], taus[j]) if prev_event(LIFTS[s], taus[j]) > clock(tcur) else clock(tcur) + 0.05, tcur)
                lt = max(tcur + 0.12, min(lt, c['t'] - 0.18))
                tl[s].append(('plant', tcur, lt, cur, curq)); ta_ = lt; vel0 = None
            else:                                       # the swing already in the air: its loop path (turned with the heading) + offset to the plan
                ta_ = 0.0; s_ = state(c['t']); pred = ae.vadd(s_['p'], ae.qrot(qyaw(sgn * s_['h']), LOOP_BALL(s, taus[j])))
                vel0 = {'pred': pred}
            dev, lnL = loop_swing(s, taus[j] % T1 if any(abs(taus[j] % T1 - x) < 1e-6 for x in LANDS[s]) else min(LANDS[s], key=lambda x: abs(x - taus[j] % T1)))
            tl[s].append(('swing', ta_, c['t'], cur, curq, c['p'], c['q'], dev, lnL, vel0))
            first_sw = False; cur, curq, tcur = c['p'], c['q'], c['t']
        # the last stance of this foot: until its loop lift after the handover, then it joins the loop path (rotated to the new heading)
        nlift = next_event(LIFTS[s], clock(tcur) + 0.02); lt = t_of_tau(nlift, tcur)
        tl[s].append(('plant', tcur, lt, cur, curq)); tl[s].append(('join', lt, 99.0, cur, curq))
    def seg_at(s, t):
        for sg in tl[s]:
            if sg[1] <= t + 1e-9 and t <= sg[2] + 1e-9: return sg
        raise RuntimeError('timeline gap %s %.3f %s' % (s, t, [(x[0], round(x[1], 3), round(x[2], 3)) for x in tl[s]]))
    LEGL = {s: ae.vlen(Lk['calf_' + s][0][0]) + ae.vlen(Lk['foot_' + s][0][0]) - HEEL_MARGIN for s in 'lr'}
    hN = state(L)['h']
    frames = []; HO = {s: {'mode': 'pin'} for s in 'lr'}; LASTQ = {s: rel(P0, 'foot_' + s)[1] for s in 'lr'}
    tp = [c['t'] for c in C if c['role'] in ('plant', 'weak')]; t_pl = tp[0] if tp else C[0]['t']
    t_tr = ([c['t'] for c in C if c['role'] == 'transfer'] or [t_pl + ST_TR])[0]
    # the plan's acceleration is piecewise constant (it jumps at each touchdown); the body answers it over ~0.1 s on both sides of the
    # contact (anticipation, then absorption): the layer inputs use a centred raised-cosine mean of +-SMOOTH_F frames (no lag, no one-frame step)
    AX0 = [state(f * DT)['ax'] for f in range(N)]; AY0 = [state(f * DT)['ay'] for f in range(N)]
    def csm(a):
        o = []
        for f in range(N):
            ws = [(0.5 + 0.5 * math.cos(math.pi * k / (SMOOTH_F + 1)), a[min(max(f + k, 0), N - 1)]) for k in range(-SMOOTH_F, SMOOTH_F + 1)]
            o.append(sum(w * v for w, v in ws) / sum(w for w, _ in ws))
        return o
    AXS = csm(AX0); AYS = csm(AY0)
    for f in range(N):
        t = f * DT; tau = clock(t); Lp = loop_local(tau); st = state(t); hh = st['h']
        rq = ae.qnorm(ae.qmul(qyaw(sgn * hh), Lk['root'][0][1]))
        pose = {b: Lp[b] for b in NAMES}; pose['root'] = (st['p'], rq, Lk['root'][0][2])
        # arms: swing amplitude damps with the braking share of the acceleration (no mechanical loop swing through the brake)
        _vv = math.hypot(st['vx'], st['vy']); brake = min(1.0, max(0.0, -(AXS[f] * st['vx'] + AYS[f] * st['vy']) / max(_vv, 1.0)) / A_CUT) if _vv > 20.0 else 0.0; amp = 1.0 - ARM_DAMP * brake
        for b in ARMS:
            dq = ae.qmul(ae.qinv(MEAN[b]), Lp[b][1])
            if dq[3] < 0: dq = tuple(-x for x in dq)
            pose[b] = (lerp(MEANT[b], Lp[b][0], amp), ae.qnorm(ae.qmul(MEAN[b], slerp((0.0, 0.0, 0.0, 1.0), dq, amp))), Lp[b][2])
        frames.append({'pose': pose, 'st': st, 'tau': tau, 'brake': brake})
    local = {b: [fr['pose'][b] for fr in frames] for b in NAMES}
    # whole-body layers (component-space deltas, children follow): gaze leads, chest leads the pelvis, the pelvis follows the plant
    rem = lambda h_: max(0.0, ANG - h_)
    _lpb = []; _lpu = []; _b = 0.0; _u = 0.0; _k = 1.0 - math.exp(-DT / max(LEAN_TAU, 1e-3))
    for f in range(N):
        st_ = frames[f]['st']; hh_ = st_['h']; vv_ = max(st_['v'], 1.0)
        a_lon_ = AXS[f] * math.cos(math.radians(hh_)) + AYS[f] * math.sin(math.radians(hh_))
        _b += _k * (min(1.0, max(0.0, -a_lon_) / A_CUT) - _b); _u += _k * (max(0.0, 1.0 - st_['v'] / VLOOP) - _u); _lpb.append(_b); _lpu.append(_u)
    lead_info = []
    for f in range(N):
        t = f * DT; st = frames[f]['st']; hh = st['h']
        w_on = mj(t / 0.20)                                                    # the head starts turning at the request
        head = min(HEAD_MAX, HEAD_LEAD * rem(hh)) * w_on
        chest = CHEST_LEAD * bell((t - (t_pl - 0.12)) / (t_tr + 0.30 - (t_pl - 0.12)))
        pelv = PELV_LEAD * bell((t - (t_pl - 0.05)) / (t_tr + 0.25 - (t_pl - 0.05)))
        a_lat = AYS[f] * math.cos(math.radians(hh)) - AXS[f] * math.sin(math.radians(hh))      # acceleration toward the turn side of the heading
        a_lon = AXS[f] * math.cos(math.radians(hh)) + AYS[f] * math.sin(math.radians(hh))
        lat_lean = max(-LEAN_LAT_MAX, min(LEAN_LAT_MAX, LEAN_LAT * math.degrees(math.atan2(a_lat, G))))
        back = LEAN_BACK * _lpb[f] + UPRIGHT * _lpu[f]                         # braking share + the slower body stands taller (both low-passed)
        fwd_h, left_h = ae.heading_axes(clip, f, local)
        ae.apply_bone_delta(clip, local, 'pelvis', f, qyaw(sgn * pelv))
        ae.apply_bone_delta(clip, local, 'spine_01' if 'spine_01' in NAMES else 'spine_03', f, ae.qnorm(ae.qmul(ae.qaxis(fwd_h, sgn * lat_lean), ae.qaxis(left_h, back))))
        ae.apply_bone_delta(clip, local, 'spine_03', f, qyaw(sgn * (chest - pelv * 0.5)))
        ae.apply_bone_delta(clip, local, 'neck_01', f, qyaw(sgn * max(0.0, head - chest) * 0.4))
        ae.apply_bone_delta(clip, local, 'head', f, qyaw(sgn * max(0.0, head - chest) * 0.6))
        lead_info.append((round(t, 2), round(head, 1), round(chest, 1), round(pelv, 1), round(lat_lean, 1), round(back, 1)))
    # feet: targets per frame
    ft = []; pn_ = []; EXA = {s: [] for s in 'lr'}
    PIVC = next((c for c in C if c['role'] == 'plant'), None) if ANG >= 135.0 else None
    def reach_roll(s, ball, q, a_min, cap, f, t, fwdv):
        hip = clip.comp('thigh_' + s, f, local)[0]
        ex0 = max(0.0, fpitch(foot_at_ball(s, ball, q), ball, fwdv) - FLATL[s]); a_min = max(0.0, min(a_min, cap - ex0)); cap = max(a_min, cap - ex0)
        latax = ae.vnorm(ae.vcross(fwdv, ZAX))
        for kk in range(int(a_min), int(cap) + 1):
            q2 = ae.qnorm(ae.qmul(ae.qaxis(latax, -kk), q)) if kk else q
            if ae.vlen(ae.vsub(hip, foot_at_ball(s, ball, q2))) <= LEGL[s]: return q2, float(kk)
        return ae.qnorm(ae.qmul(ae.qaxis(latax, -cap), q)), float(cap)
    for f in range(N):
        t = f * DT; tau = frames[f]['tau']; st = frames[f]['st']; F_ = {}; PN = {}
        for s in 'lr':
            sg = seg_at(s, t); ex = 0.0
            if sg[0] == 'join':
                rq = local['root'][f][1]; lf = LOOP_FOOT(s, tau); lb = ae.vadd(st['p'], ae.qrot(ae.qmul(rq, ae.qinv(Lk['root'][0][1])), LOOP_BALL(s, tau)))
                lq = ae.qnorm(ae.qmul(ae.qmul(rq, ae.qinv(Lk['root'][0][1])), lf[1]))
                h_ = HO[s]
                if h_['mode'] == 'pin':
                    nxt = next_event(LANDS[s], tau + 1e-4); h_.update({'mode': 'fade', 'off': ae.vsub(sg[3], lb), 'tau0': tau, 'tau1': nxt, 'q0': LASTQ[s]})
                x_ = (tau - h_['tau0']) / max(h_['tau1'] - h_['tau0'], 1e-3) if h_['mode'] == 'fade' else 1.0
                w = 1.0 - mj(x_)
                if w <= 0.0: h_['mode'] = 'loop'
                q = slerp(h_['q0'], lq, mj(x_ / 0.3)) if h_['mode'] == 'fade' else lq
                bp = ae.vadd(ae.vadd(lb, ae.vsc(h_.get('off', (0.0, 0.0, 0.0)), max(w, 0.0))), (0.0, 0.0, APEX_MIN * math.sin(math.pi * min(1.0, x_)) * w))
                F_[s] = (foot_at_ball(s, bp, q), q); PN[s] = planted(s, tau) and w <= 0.0; EXA[s].append(0.0); continue
            hv = st['h']; fwdv = ae.vnorm(world(sgn, math.cos(math.radians(hv)), math.sin(math.radians(hv))))
            if sg[0] == 'plant':
                _, ta, tb, p0, q0 = sg; PN[s] = True; hp = 0.0
                if PIVC is not None and math.hypot(p0[0] - PIVC['p'][0], p0[1] - PIVC['p'][1]) < 0.5:   # the pivot foot turns on its pinned ball, behind the body
                    dy_ = max(0.0, st['h'] - PIV_LAG - PIVC['yaw']); q0 = ae.qnorm(ae.qmul(qyaw(sgn * dy_), q0))
                if tb < 99.0: hp = (HEEL_PUSH0 + HEEL_PUSHV * st['v'] / VLOOP) * mj((t - (tb - PUSH_T)) / PUSH_T)
                cap = HEEL_CAP + (max(0.0, min(TOE_EXTRA[s], TOE_MAX) - HEEL_CAP) * mj((t - (tb - PUSH_T)) / PUSH_T) if tb < 99.0 else 0.0)
                q, ex = reach_roll(s, p0, q0, hp, cap, f, t, fwdv); LASTQ[s] = q; F_[s] = (foot_at_ball(s, p0, q), q); EXA[s].append(ex)
            else:
                _, ta, tb, p0, q0, p1, q1, dev, lnL, vel0 = sg; PN[s] = False
                x = (t - ta) / max(tb - ta, 1e-3); ln = math.hypot(p1[0] - p0[0], p1[1] - p0[1]); sc = min(1.0, ln / max(lnL, 1.0))
                qa = LASTQ[s] if vel0 is None else q0
                if vel0 is not None:
                    lq_ = ae.qnorm(ae.qmul(qyaw(sgn * st['h']), LOOP_FOOT(s, tau)[1]))
                    lb_ = ae.vadd(st['p'], ae.qrot(qyaw(sgn * st['h']), LOOP_BALL(s, tau)))
                    off = ae.vsc(ae.vsub(p1, vel0['pred']), mj(x))
                    bp = ae.vadd(lb_, off); q = slerp(lq_, q1, mj((x - 0.6) / 0.4))
                    fp_ = foot_at_ball(s, bp, q); hip = clip.comp('thigh_' + s, f, local)[0]; dh = ae.vsub(fp_, hip); lh = ae.vlen(dh)
                    if lh > LEGL[s] - 0.5: fp_ = ae.vadd(hip, ae.vsc(dh, (LEGL[s] - 0.5) / lh))
                    F_[s] = (fp_, q); EXA[s].append(0.0); LASTQ[s] = q; continue
                base = lerp(p0, p1, mj(x))
                # the loop's swing shape, turned onto this swing's own direction
                sdir = ae.vnorm((p1[0] - p0[0], p1[1] - p0[1], 0.0)) if ln > 1.0 else fwdv
                ang = math.degrees(math.atan2(ae.vdot(ae.vcross(FWD, sdir), ZAX), ae.vdot(FWD, sdir)))
                dv = ae.qrot(ae.qaxis(ZAX, ang), dev_at(dev, x)); zd = dv[2] * (sc ** LOOPDEV); zmin = APEX_MIN * math.sin(math.pi * x)
                wa_ = mj((x - 0.78) / 0.22)
                xy = (base[0] + dv[0] * sc * (1 - wa_), base[1] + dv[1] * sc * (1 - wa_))
                zc = p1[2] + LANDC * (1.0 - mj((x - 0.8) / 0.2)) if x > 0.55 else -1e9
                bp = (xy[0], xy[1], max(base[2] + max(zd, zmin), zc))
                q = slerp(qa, q1, mj((x - 0.25) / 0.75))
                fp_ = foot_at_ball(s, bp, q); hip = clip.comp('thigh_' + s, f, local)[0]; dh = ae.vsub(fp_, hip); lh = ae.vlen(dh)
                if lh > LEGL[s] - 0.5: fp_ = ae.vadd(hip, ae.vsc(dh, (LEGL[s] - 0.5) / lh))
                F_[s] = (fp_, q); EXA[s].append(0.0)
        ft.append(F_); pn_.append(PN)
    PLN_ = {s: [pn_[f][s] for f in range(N)] for s in 'lr'}
    # pelvis height: drop only as much as a planted leg needs to reach its foot (+ a small absorption on the plant stance)
    need = []
    for f in range(N):
        dm = 0.0
        for s in 'lr':
            if not PLN_[s][f]: continue
            hip = clip.comp('thigh_' + s, f, local)[0]; fp = ft[f][s][0]
            Lm = ae.vlen(local['calf_' + s][f][0]) + ae.vlen(local['foot_' + s][f][0]) - KNEE_MARGIN
            hz = hip[2] - fp[2]; hor = math.hypot(hip[0] - fp[0], hip[1] - fp[1])
            if hz * hz + hor * hor > Lm * Lm: dm = max(dm, hz - math.sqrt(max(Lm * Lm - hor * hor, 0.0)))
        need.append(dm + DIP_CM * bell((f * DT - t_pl) / max(t_tr + 0.1 - t_pl, 0.2)))
    mx = [max(need[max(0, f - 4):f + 5]) for f in range(N)]; drop = [max(sum(mx[max(0, f - 4):f + 5]) / len(mx[max(0, f - 4):f + 5]), need[f]) for f in range(N)]
    for f in range(N):
        pt, pq, ps = local['pelvis'][f]; local['pelvis'][f] = ((pt[0], pt[1], pt[2] - drop[f]), pq, ps)
    for f in range(N):
        for s in 'lr':
            kh = clip.comp('calf_' + s, f, local)[0]; ae.solve_leg(clip, local, s, f, ft[f][s][0], ft[f][s][1], kh)
    for s in 'lr':
        b = 'ik_foot_' + s
        if b in NAMES and 'ik_foot_root' in NAMES:
            for f in range(N):
                fp, fq = clip.comp('foot_' + s, f, local); pp, pq = clip.comp('ik_foot_root', f, local)
                local[b][f] = (ae.qrot(ae.qinv(pq), ae.vsub(fp, pp)), ae.qnorm(ae.qmul(ae.qinv(pq), fq)), local[b][f][2])
    # ---- checks (component incl. root = the clip's world)
    def cw(b, f): return clip.comp(b, f, local)[0]
    ferr = max(ae.vlen(ae.vsub(cw('foot_' + s, f), ft[f][s][0])) for f in range(N) for s in 'lr')
    drift = {s: 0.0 for s in 'lr'}; zjump = 0.0
    for s in 'lr':
        for f in range(1, N):
            a, b_ = cw('ball_' + s, f - 1), cw('ball_' + s, f); zjump = max(zjump, abs(b_[2] - a[2]))
            if PLN_[s][f] and PLN_[s][f - 1]: drift[s] += math.hypot(b_[0] - a[0], b_[1] - a[1])
    def yaw_of(v): return math.degrees(math.atan2(ae.vdot(v, RIGHT), ae.vdot(v, FWD)))
    body = []
    for f in range(0, N, 2):
        tl_, tr_ = cw('thigh_l', f), cw('thigh_r', f); cl_, cr_ = cw('clavicle_l', f), cw('clavicle_r', f)
        pv = ae.vcross(ZAX, ae.vsub(tr_, tl_)); cv = ae.vcross(ZAX, ae.vsub(cr_, cl_))
        body.append((round(f * DT, 2), round(frames[f]['st']['v']), round(frames[f]['st']['h']), round(sgn * yaw_of(ae.vsc(pv, -1.0)) if False else yaw_of(ae.vsub(cw('pelvis', f), cw('pelvis', f))), 0)))
    # pelvis / chest yaw from the hip and shoulder lines (forward = the normal of the line), signed toward the turn
    def lineyaw(a, b):
        d = ae.vsub(b, a); n_ = ae.vcross(d, ZAX)                                   # left->right line, n = forward
        return sgn * yaw_of(ae.vsc(n_, -1.0))
    body = [(round(f * DT, 2), round(frames[f]['st']['v']), round(frames[f]['st']['h']), round(lineyaw(cw('thigh_l', f), cw('thigh_r', f))), round(lineyaw(cw('clavicle_l', f), cw('clavicle_r', f))),
             round(cw('pelvis', f)[2] - local['root'][f][0][2], 1)) for f in range(0, N, 2)]
    info = {'tau0': tau0, 'side': side, 't1': round(PLN['t1'], 3), 'contacts': [{k: ([round(x, 1) for x in v] if k == 'p' else v) for k, v in c.items() if k != 'q'} for c in C],
            'n_contacts_to_new_line': len(C), 'len': round(L, 3), 'frames': N, 'foot_err': round(ferr, 2), 'planted_drift': {s: round(drift[s], 2) for s in 'lr'},
            'ball_z_jump_max': round(zjump, 2), 'pelvis_drop_max': round(max(drop), 1), 'tend': PLN['tend'],
            'body_t_v_h_pel_chest_pz': body, 'leads': lead_info[::3]}
    SB = ['pelvis', 'spine_03', 'spine_05', 'neck_01', 'head', 'clavicle_l', 'upperarm_l', 'lowerarm_l', 'hand_l', 'clavicle_r', 'upperarm_r', 'lowerarm_r', 'hand_r',
          'thigh_l', 'calf_l', 'foot_l', 'ball_l', 'thigh_r', 'calf_r', 'foot_r', 'ball_r']
    (SD / 'stick' / (name + '.json')).write_text(json.dumps({'name': name, 'dt': DT, 'bones': SB, 'fwd': FWD, 'right': RIGHT, 'sgn': sgn,
        'root': [[round(x, 1) for x in local['root'][f][0]] for f in range(N)], 'planted': PLN_, 'contacts': info['contacts'],
        'frames': [[[round(x, 1) for x in cw(b, f)] for b in SB] for f in range(N)]}))
    cur = {'footspeed_l': [], 'footspeed_r': []}
    for f in range(N):
        for s in 'lr':
            a = cw('ball_' + s, max(0, f - 1)); b_ = cw('ball_' + s, min(N - 1, f + 1))
            cur['footspeed_' + s].append(FS_SCALE * math.hypot(b_[0] - a[0], b_[1] - a[1]) / (DT * (min(N - 1, f + 1) - max(0, f - 1))))
    cur['SHM226_V'] = [frames[f]['st']['vl'] for f in range(N)]; cur['SHM226_W'] = [1.0] * N
    # the authored redirect owns the capsule heading (and holds its route) until its planned turn is done (89.5 deg); the loop tail is free
    t_done = next((f * DT for f in range(N) if frames[f]['st']['h'] >= ANG - 0.5), L)
    # Turn and W drop TOGETHER (the contract reads Turn / W: an interpolated W between keys with Turn held would read up to 2 x the turn)
    cur['SHM238_W'] = [1.0 if f * DT <= t_done else 0.0 for f in range(N)]; cur['SHM238_Turn'] = [frames[f]['st']['h'] * 90.0 / ANG * cur['SHM238_W'][f] for f in range(N)]
    cur['SHM254_W'] = list(cur['SHM238_W']); cur['SHM254_Side'] = [sgn * w for w in cur['SHM238_W']]
    cur['SHM254_Own'] = [1.0 if f * DT <= L - OWN_TAIL else 0.0 for f in range(N)]   # the route stays on this clip through the re-push (V2.54 hold) until the speed is past the push route (SHM211_PushMaxSpeed 400)
    t_last = max([c['t'] for c in C if c['role'] != 'push'] or [t_tr])
    cur['SHM237_FPPelvisOff'] = [mj((f * DT - (C[0]['t'] - 0.1)) / 0.1) * (1.0 - mj((f * DT - (t_last + 0.25)) / 0.3)) for f in range(N)]
    for cn in ('Enable_OrientationWarping', 'Disable_FootLock', 'pbi_authoredforwardlean'):
        try: cur[cn] = [AL.get_float_value(loop, cn, frames[f]['tau'] % T1) for f in range(N)]
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
    try: c.open_bracket(u.Text('SHME V2.54 ' + name), True)
    except Exception: c.open_bracket('SHME V2.54 ' + name, True)
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
    # V2.54 add254_block: a brake/plant/transfer is only valid from its own beginning - Motion Matching may enter only in [0, BLOCK_T)
    AL.add_animation_notify_track(seq, 'SHME_V254_Block')
    AL.add_animation_notify_state_event(seq, 'SHME_V254_Block', BLOCK_T, seq.get_play_length() - BLOCK_T, u.AnimNotifyState_PoseSearchBlockTransition)
    return EAL.save_loaded_asset(seq, False), path
specs = cfg.get('clips') or []
out = {'loop': LOOP, 'T1': T1, 'vloop': round(VLOOP, 1), 'step_t': round(STEP_T, 3), 'lands': LANDS, 'lifts': LIFTS, 'latl': LATL, 'clips': {}}
for spec in specs:
    try: name, local, info, cur = build(spec)
    except Exception as e:
        import traceback; out['clips'][spec['name']] = {'error': traceback.format_exc()[-900:]}; continue
    if not DRY:
        try: info['saved'], info['path'] = write(name, local, cur)
        except Exception as e: info['write_error'] = str(e)[:300]
    out['clips'][name] = info
(SD / 'data' / ('gen254_rev_%s.json' % ('dry' if DRY else 'write'))).write_text(json.dumps(out, indent=1, default=str))
print('G254REV ' + json.dumps({k: v for k, v in out.items() if k != 'clips'}, default=str)[:600])
for n_, c_ in out['clips'].items(): print('G254REV_CLIP ' + n_ + ' ' + json.dumps({k: v for k, v in c_.items() if k not in ('body_t_v_h_pel_chest_pz', 'leads')}, default=str)[:1500])
