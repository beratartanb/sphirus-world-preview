# gen226_rev.py = gen225_rev.py (r3: measured capsule table + S-foot ball pin) written to V226 as SHM226_JogRev_* with NPH from cfg (32 bins: V2.26 diagnosis = the 8-bin phase quantisation left the clip foot 20-25 cm from the loop foot at the matched entry time)
"""gen225_rev.py (editor job) - V2.25 A: AUTHORED jog reversal for this character: brake -> support -> measured push -> jog loop.
Two families, both strafe (the body keeps facing forward):
  B_F  backpedal (A_RB_Jog_Rear, capsule 245 cm/s) -> forward request -> brake -> first forward step -> forward loop (A_CT_Jog_Fwd, 300)
  F_B  forward jog (A_CT_Jog_Fwd, 300) -> backward request -> brake -> first backward step -> rear loop (A_RB_Jog_Rear, 245)
Root = the MEASURED capsule profile of the production reversal (Saved/Codex/SHME_V225_20261023/capsule_rev_profiles.json, v224t9 p runs,
fixed 30): B_F brake 245 -> 0 at 720 cm/s^2 (0.33 s), re-push 261 cm/s^2 to 300; F_B brake 300 -> 0 at 680 (0.43 s), re-push 198 to 245.
Footstep plan per ENTRY PHASE tau0 of the entry loop (NPH bins; frame 0 = the exact loop pose at tau0, full speed):
  1. BRAKE on the natural cadence: the entry loop keeps running at its full-speed rate (legs do not go into slow motion) while the root
     follows the brake profile. B = the next foot to land; it is redirected from its current swing to a DESIGNED brake plant: BRAKE_BEHIND
     cm beyond the capsule's stop point in the direction of the OLD travel (the body decelerates over / behind it), landing at its natural
     remaining swing time (clamped 0.12..0.45 s). The other foot S: pinned while the loop has it planted, lifts at the loop's toe-off, keeps
     the loop's swing shape until REDIR_LEAD before B lands, then is redirected to the first step of the NEW travel.
  2. FIRST STEP by time: S lands T_FIRST after the zero crossing where the exit loop places it at its heel strike relative to the root
     (the step is SHORT because the root has moved little - no lunge, no slow motion); B stays planted until the exit loop lifts it.
  3. RE-PUSH on a rate-floored clock: the exit loop runs at rate max(v / Vexit, RATE_MIN) (cadence never below RATE_MIN of the loop's),
     planted feet are PINNED where they landed, swing feet follow the loop shape relative to the real root and land where the real root
     puts them (shortened steps while the speed is still low); the pinned-vs-loop offset of a lifting foot fades over its swing.
     The clip ends when the capsule reaches the exit loop speed (+ TAIL) on the loop pose.
Upper body: entry -> exit loop poses; arms on a PHASE-COHERENT virtual exit-loop clock from S's toe-off to its heel strike; trunk / head /
pelvis blended on the same timeline; designed additions are small: brake counter-lean BRAKE_DEG (toward the stopped travel) around B's
plant, push lean PUSH_DEG into the new travel around the zero crossing, pelvis absorb dip DIP_CM. Legs: V2.10 solve_leg + leg_guard.
builtins.G225 = {'dry_run': True, 'nph': 6, 'fam': ['B_F','F_B'], 'brake_deg': 4.0, 'push_deg': 3.0, 'dip_cm': 2.5, 'tail': 0.25,
                 't_first': 0.40, 'brake_behind': 10.0, 'rate_min': 0.75}
Output: /Game/GraceRanger/SHME/Animations/V225/SHM225_JogRev_B_F_P<k> / _F_B_P<k>. Prints G225 {...}; json in Saved/Codex/SHME_V225_20261023/."""
import unreal as u, json, math, builtins, pathlib, importlib, sys
P = pathlib.Path(u.Paths.project_dir()).resolve(); sys.path.insert(0, str(P / 'Tools/SHME_V1_20260925'))
import v137_animedit as ae; importlib.reload(ae)
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary
cfg = getattr(builtins, 'G225', {}); DRY = bool(cfg.get('dry_run', True)); NPH = int(cfg.get('nph', 6)); FAMS = cfg.get('fam', ['B_F', 'F_B']); ONLY = cfg.get('only')
BRAKE_DEG = float(cfg.get('brake_deg', 4.0)); PUSH_DEG = float(cfg.get('push_deg', 3.0)); DIP_CM = float(cfg.get('dip_cm', 2.5)); TAIL = float(cfg.get('tail', 0.25))
SWING_H = float(cfg.get('swing_h', 9.0)); FADE_LEN = float(cfg.get('fade_len', 0.40)); T_FIRST = float(cfg.get('t_first', 0.40)); TAN_CAP = float(cfg.get('tan_cap', 30.0))
REDIR_LEAD = float(cfg.get('redir_lead', 0.08)); BRAKE_BEHIND = float(cfg.get('brake_behind', 10.0)); RATE_MIN = float(cfg.get('rate_min', 0.75)); TB_MIN = float(cfg.get('tb_min', 0.12)); TB_MAX = float(cfg.get('tb_max', 0.45))
OUTDIR = '/Game/GraceRanger/SHME/Animations/V226'; FPS = 30.0; DT = 1.0 / FPS
REAR = '/Game/GraceRanger/Animations/LocomotionBehavior/RearRevision/A_RB_Jog_Rear'; FWDL = '/Game/GraceRanger/Animations/Continuity/A_CT_Jog_Fwd'
PROF = {'B_F': {'v0': 245.0, 'brake': 720.0, 'push': 261.0, 'vexit': 300.0}, 'F_B': {'v0': 300.0, 'brake': 680.0, 'push': 198.0, 'vexit': 245.0}}
PROF.update(cfg.get('prof', {}))
def slerp(a, b, t):
    d = sum(a[i] * b[i] for i in range(4))
    if d < 0: b = tuple(-x for x in b); d = -d
    if d > 0.9995: return ae.qnorm(tuple(a[i] + (b[i] - a[i]) * t for i in range(4)))
    th = math.acos(min(d, 1.0)); s = math.sin(th)
    return tuple((math.sin((1 - t) * th) * a[i] + math.sin(t * th) * b[i]) / s for i in range(4))
def lerp(a, b, t): return tuple(a[i] + (b[i] - a[i]) * t for i in range(len(a)))
def sm(x): x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)
def mj(x): x = min(1.0, max(0.0, x)); return x * x * x * (10 - 15 * x + 6 * x * x)
def bell(t, t0, t1):
    if t <= t0 or t >= t1: return 0.0
    return math.sin(math.pi * (t - t0) / (t1 - t0)) ** 2
class Loop:
    def __init__(self, path, names):
        self.seq = u.load_asset(path); assert self.seq, path
        self.NK = ae.num_frames(self.seq) - 1; self.T = float(self.seq.get_play_length()); self.names = names
        self.Lk = ae.read_local(self.seq, names, list(range(self.NK + 1)))
        self.D = ae.vsub(self.Lk['root'][self.NK][0], self.Lk['root'][0][0]); self.V = ae.vlen(self.D) / self.T
        self.clip = ae.Clip(self.seq, ['root', 'pelvis', 'foot_l', 'foot_r', 'ball_l', 'ball_r', 'calf_l', 'calf_r', 'head', 'neck_01', 'spine_05', 'spine_03', 'spine_01'] + [b for b in ('ik_foot_l', 'ik_foot_r') if b in names])
        self.BZ = {s: [self.rel(self.at(k * self.T / self.NK), 'ball_' + s)[0][2] for k in range(self.NK + 1)] for s in ('l', 'r')}
        self.BZ0 = {s: min(self.BZ[s]) for s in ('l', 'r')}
    def at(self, tau):
        c, r = divmod(tau, self.T); f = r / self.T * self.NK; i = int(math.floor(f)); w = f - i; i = min(i, self.NK - 1)
        o = {}
        for b in self.names:
            (t0, q0, s0), (t1, q1, s1) = self.Lk[b][i], self.Lk[b][i + 1]
            t = lerp(t0, t1, w); q = slerp(q0, q1, w)
            if b == 'root': t = ae.vadd(t, ae.vsc(self.D, c))
            o[b] = (t, q, lerp(s0, s1, w))
        return o
    def rel(self, loc, bone):
        tmp = {b: [loc[b]] for b in loc}; r0 = loc['root']; tmp['root'] = [((0.0, 0.0, 0.0), r0[1], r0[2])]
        return self.clip.comp(bone, 0, tmp)
    def planted(self, s, tau): k = int(round((tau % self.T) / self.T * self.NK)) % (self.NK + 1); return self.BZ[s][k] < self.BZ0[s] + 1.5
    def next_land(self, s, tau):
        for k in range(1, self.NK * 2 + 1):
            t = tau + k * self.T / self.NK
            if self.planted(s, t) and not self.planted(s, t - self.T / self.NK): return t
        return tau + self.T
    def next_lift(self, s, tau):
        for k in range(1, self.NK * 2 + 1):
            t = tau + k * self.T / self.NK
            if not self.planted(s, t) and self.planted(s, t - self.T / self.NK): return t
        return tau + self.T
    def prev_lift(self, s, tau):
        for k in range(1, self.NK * 2 + 1):
            t = tau - k * self.T / self.NK
            if not self.planted(s, t) and self.planted(s, t - self.T / self.NK): return t
        return tau - self.T
names_r = set(str(n) for n in AL.get_animation_track_names(u.load_asset(REAR))); names_f = set(str(n) for n in AL.get_animation_track_names(u.load_asset(FWDL)))
NAMES = sorted(names_r & names_f); assert 'root' in NAMES and 'pelvis' in NAMES
RL = Loop(REAR, NAMES); FL = Loop(FWDL, NAMES)
FWD = ae.vnorm((FL.D[0], FL.D[1], 0.0)); assert ae.vdot(FWD, RL.D) < 0, ('rear loop travels backward', RL.D)
ARMS = [b for b in NAMES if b.startswith(('clavicle_', 'upperarm_', 'lowerarm_', 'hand_', 'thumb_', 'index_', 'middle_', 'ring_', 'pinky_'))]
UB = [b for b in NAMES if b not in ('root', 'thigh_l', 'calf_l', 'foot_l', 'ball_l', 'thigh_r', 'calf_r', 'foot_r', 'ball_r', 'ik_foot_l', 'ik_foot_r', 'ik_foot_root') and not b.startswith(('calf_twist', 'thigh_twist'))]
TRUNK = [b for b in UB if b not in ARMS]
def blend_pose(A, Bp, w, bones):
    o = dict(A)
    for b in bones: o[b] = (lerp(A[b][0], Bp[b][0], w), slerp(A[b][1], Bp[b][1], w), lerp(A[b][2], Bp[b][2], w))
    return o
def swing(p0, v0, p1, t0, t1, t, h, z0=None):
    if t <= t0: return p0
    if t >= t1: return p1
    T = t1 - t0; x = (t - t0) / T
    vm = math.hypot(v0[0], v0[1]) * T; kv = min(1.0, TAN_CAP / vm) if vm > 1e-6 else 1.0
    h00 = 2 * x ** 3 - 3 * x * x + 1; h10 = x ** 3 - 2 * x * x + x; h01 = -2 * x ** 3 + 3 * x * x
    xy = [h00 * p0[i] + h10 * T * kv * v0[i] + h01 * p1[i] for i in range(2)]
    zb = (z0 if z0 is not None else p0[2]) * (1 - mj(x)) + p1[2] * mj(x)
    return (xy[0], xy[1], zb + h * math.sin(math.pi * x) * (1 - 0.5 * x))
BALL_LOCAL = {s: FL.Lk['ball_' + s][0][0] for s in ('l', 'r')}
def foot_at_ball(s, ball, q): return ae.vsub(ball, ae.qrot(q, BALL_LOCAL[s]))
TABLE = json.load(open(cfg['prof_table'])) if cfg.get('prof_table') else {}
for _f, _t in TABLE.items():   # V2.25 r2: measured capsule reversal (t2 runs, 5 phases averaged; t=0 = last full-speed frame)
    PROF.setdefault(_f, {}).update({'v0': -(-_t['v'][0]), 'vexit': abs(_t['v'][-1])})
def profile(fam):
    if fam in TABLE:
        dtt = TABLE[fam]['dt']; tab = [-x for x in TABLE[fam]['v']]; n = len(tab)   # canonical: -v0 (old travel) rising to +vexit
        def v(t):
            if t <= 0: return tab[0]
            k = t / dtt
            if k >= n - 1: return tab[-1]
            i = int(k); w = k - i; return tab[i] * (1 - w) + tab[i + 1] * w
        cum = [0.0]
        for i in range(1, n): cum.append(cum[-1] + 0.5 * (tab[i - 1] + tab[i]) * dtt)
        def d(t):
            if t <= 0: return tab[0] * t
            k = t / dtt
            if k >= n - 1: return cum[-1] + tab[-1] * (t - (n - 1) * dtt)
            i = int(k); w = k - i; return cum[i] + (tab[i] + 0.5 * (v(t) - tab[i])) * w * dtt
        tz = next(((i - 1 + (-tab[i - 1]) / (tab[i] - tab[i - 1])) * dtt for i in range(1, n) if tab[i - 1] < 0 <= tab[i]), None)
        tv = next((i * dtt for i in range(n) if tab[i] >= 0.97 * tab[-1]), (n - 1) * dtt)
        return v, d, tz, tv
    p = PROF[fam]; v0, A, a, ve = p['v0'], p['brake'], p['push'], p['vexit']; tz = v0 / A; tv = tz + ve / a
    def v(t):
        if t <= 0: return -v0
        if t <= tz: return -(v0 - A * t)
        return min(ve, a * (t - tz))
    def d(t):
        if t <= 0: return -v0 * t
        if t <= tz: return -(v0 * t - 0.5 * A * t * t)
        if t <= tv: return -(0.5 * v0 * tz) + 0.5 * a * (t - tz) ** 2
        return -(0.5 * v0 * tz) + 0.5 * a * (tv - tz) ** 2 + ve * (t - tv)
    return v, d, tz, tv
def build(fam, key):
    EL, XL = (RL, FL) if fam == 'B_F' else (FL, RL)          # entry loop, exit loop
    sgn = 1.0 if fam == 'B_F' else -1.0                        # + : the new travel is +FWD (clip frame = forward loop frame)
    vfun, dfun, tz, tv = profile(fam); vexit = PROF[fam]['vexit']; v0 = PROF[fam]['v0']
    vf = lambda t: sgn * vfun(t); df = lambda t: sgn * dfun(t)   # signed along FWD
    prog = lambda t: sgn * (df(t) - df(tz))                      # progress along the NEW travel after the zero crossing (>= 0)
    tau0 = key * EL.T / NPH; L0 = EL.at(tau0); root0 = (0.0, 0.0, 0.0)
    r0t = v0 / EL.V                                              # loop seconds per real second at full speed
    tauE = lambda t: tau0 + r0t * t                              # entry loop on its natural cadence
    ball0 = {s: EL.rel(L0, 'ball_' + s)[0] for s in ('l', 'r')}
    # ---- phase 1: B = the next foot to land; designed brake plant beyond the stop point in the OLD travel direction
    landt = {s: EL.next_land(s, tau0) for s in ('l', 'r')}
    B = 'l' if landt['l'] < landt['r'] else 'r'; S = 'r' if B == 'l' else 'l'
    tB = min(TB_MAX, max(TB_MIN, (landt[B] - tau0) / r0t))
    LB = EL.at(landt[B]); latB = ae.vdot(EL.rel(LB, 'ball_' + B)[0], ae.vnorm(ae.vcross((0.0, 0.0, 1.0), FWD)))
    latv = ae.vnorm(ae.vcross((0.0, 0.0, 1.0), FWD))
    stopP = ae.vsc(FWD, df(tz))
    ballB_world = ae.vadd(ae.vadd(stopP, ae.vsc(FWD, -sgn * BRAKE_BEHIND)), ae.vsc(latv, latB)); ballB_world = (ballB_world[0], ballB_world[1], EL.BZ0[B])
    qB = EL.rel(LB, 'foot_' + B)[1]
    s_planted0 = EL.planted(S, tau0); ballS0_world = (ball0[S][0], ball0[S][1], EL.BZ0[S]) if s_planted0 else None
    tS_lift = (EL.next_lift(S, tau0) - tau0) / r0t if s_planted0 else 0.0
    # ---- phase 2: S's first step (time-designed), exit loop heel strike geometry
    tauHS = XL.next_land(S, 0.02); LH = XL.at(tauHS)
    rB_hs = XL.rel(LH, 'ball_' + B)[0]; rS_hs = XL.rel(LH, 'foot_' + S); qS_hs = rS_hs[1]
    tS = max(tz + T_FIRST, tS_lift + 0.22, tB + 0.10)
    rootS = ae.vsc(FWD, df(tS)); landS = ae.vadd(rootS, rS_hs[0]); landS = (landS[0], landS[1], rS_hs[0][2])
    tauTO_S = XL.prev_lift(S, tauHS)
    L = tv + TAIL; N = int(math.ceil(L / DT)) + 1
    info = {'fam': fam, 'B': B, 'S': S, 'tau0': round(tau0, 3), 'tB': round(tB, 3), 'tz': round(tz, 3), 'tS': round(tS, 3), 'tv': round(tv, 3), 'tauHS': round(tauHS, 3),
            's_planted0': s_planted0, 'tS_lift': round(tS_lift, 3), 'ballB': [round(x, 1) for x in ballB_world], 'landS': [round(x, 1) for x in landS]}
    # B swing start (frame 0 state) / S redirect
    tRedir = max(tS_lift, tB - REDIR_LEAD)
    frames = []; tS_swing0 = None; sLiftPos = None; sLiftVel = (0.0, 0.0, 0.0); qS_lift = None
    b0 = EL.rel(L0, 'foot_' + B); bPos0 = ae.vadd(root0, b0[0]); qB0 = b0[1]
    e = DT; b1 = EL.rel(EL.at(tauE(e)), 'foot_' + B); bVel0 = tuple((ae.vadd(ae.vsc(FWD, df(e)), b1[0])[i] - bPos0[i]) / e for i in range(3))
    bTarget = foot_at_ball(B, ballB_world, qB)
    # exit-phase pin / swing bookkeeping
    pin = {}; off = {}; liftTau = {}; tauX = tauHS
    for f in range(N):
        t = f * DT; rt = ae.vsc(FWD, df(t))
        Le = EL.at(tauE(min(t, tB + 0.15)))
        # exit loop clock: virtual (arms) before tS; rate-floored time clock after
        if t < tS: tauX = tauTO_S + (tauHS - tauTO_S) * sm((t - tB) / max(tS - tB, 1e-3)); Lx = XL.at(tauX)
        else:
            if f > 0 and (f - 1) * DT >= tS: tauX += max(RATE_MIN, min(1.0, abs(vf(t)) / vexit)) * DT
            else: tauX = tauHS
            Lx = XL.at(tauX)
        wA = sm((t - (tB - 0.05)) / max(tS + 0.15 - (tB - 0.05), 1e-3))
        wT = sm((t - (tB - 0.10)) / max(tS + 0.25 - (tB - 0.10), 1e-3))
        pose = blend_pose(Le, Lx, wT, TRUNK)
        for b in ARMS: pose[b] = (lerp(Le[b][0], Lx[b][0], wA), slerp(Le[b][1], Lx[b][1], wA), lerp(Le[b][2], Lx[b][2], wA))
        dip = DIP_CM * bell(t, tB - 0.05, tS + 0.10)
        pt, pq, ps = pose['pelvis']; pose['pelvis'] = ((pt[0], pt[1], pt[2] - dip), pq, ps)
        pose['root'] = (rt, FL.Lk['root'][0][1], FL.Lk['root'][0][2])
        ft = {}
        if t < tS:
            # ---- B: designed brake swing then planted
            if t < tB: ft[B] = (swing(bPos0, bVel0, bTarget, 0.0, tB, t, SWING_H * 0.8, z0=bPos0[2]), slerp(qB0, qB, mj(t / max(tB, 1e-3))))
            else: ft[B] = (bTarget, qB)
            # ---- S: pinned / loop shape / redirected first step
            if s_planted0 and t < max(tS_lift, tRedir):   # r4: stay pinned until the redirect (the loop-shaped toe-off between tS_lift and tRedir slid 8.9 cm in F_B_P4: braking root vs full-speed loop foot)
                qs = EL.rel(Le, 'foot_' + S)[1]; ft[S] = (foot_at_ball(S, ballS0_world, qs), qs)
            elif t < tRedir:
                ls = EL.rel(Le, 'foot_' + S); ft[S] = (ae.vadd(rt, ls[0]), ls[1])
            else:
                if tS_swing0 is None:
                    tS_swing0 = t; ls = EL.rel(Le, 'foot_' + S); sLiftPos = ae.vadd(rt, ls[0]); qS_lift = ls[1]
                    ls2 = EL.rel(EL.at(tauE(min(t + e, tB + 0.15))), 'foot_' + S); sLiftVel = tuple((ae.vadd(ae.vsc(FWD, df(t + e)), ls2[0])[i] - sLiftPos[i]) / e for i in range(3))
                    if s_planted0:   # r5: the swing starts FROM THE PINNED foot (r4 pinned until the redirect but started the swing from the loop-shaped foot: 20-40 cm jump)
                        sLiftPos = foot_at_ball(S, ballS0_world, qS_lift); sLiftVel = (0.0, 0.0, 0.0)
                x = (t - tS_swing0) / max(tS - tS_swing0, 1e-3)
                ft[S] = (swing(sLiftPos, sLiftVel, landS, tS_swing0, tS, t, SWING_H, z0=sLiftPos[2]), slerp(qS_lift, qS_hs, mj(x)))
            if f == N - 1 or (f + 1) * DT >= tS:
                # r3: landS is the FOOT target; the pin is a BALL position (r1/r2 pinned the ball at the foot point -> the planted foot
                # jumped back by the ball offset, ~16 cm, in the frames after the S heel strike = the 20-29 cm push-step slide)
                bS = ae.vadd(landS, ae.qrot(qS_hs, BALL_LOCAL[S])); pin[S] = (bS[0], bS[1], XL.BZ0[S]); pin[B] = ballB_world
        else:
            for s in ('l', 'r'):
                ls = XL.rel(Lx, 'foot_' + s); loopPos = ae.vadd(rt, ls[0]); pl = XL.planted(s, tauX)
                if pl and s not in pin:
                    lb = XL.rel(Lx, 'ball_' + s)[0]; pin[s] = (rt[0] + lb[0], rt[1] + lb[1], XL.BZ0[s]); off.pop(s, None)
                if not pl and s in pin:
                    off[s] = ae.vsub(foot_at_ball(s, pin[s], ls[1]), loopPos); off[s] = (off[s][0], off[s][1], 0.0); liftTau[s] = tauX; pin.pop(s)
                if s in pin: ft[s] = (foot_at_ball(s, pin[s], ls[1]), ls[1])
                else:
                    fade = 1.0 - mj((tauX - liftTau.get(s, tauX)) / FADE_LEN) if s in off else 0.0
                    ft[s] = (ae.vadd(loopPos, ae.vsc(off.get(s, (0.0, 0.0, 0.0)), fade)), ls[1])
        frames.append((pose, ft))
    local = {b: [fr[0][b] for fr in frames] for b in NAMES}
    clip = FL.clip
    lat = ae.vnorm(ae.vcross(FWD, (0.0, 0.0, 1.0)))
    for f in range(N):
        t = f * DT
        a = sgn * (BRAKE_DEG * bell(t, tB - 0.10, tz + 0.15)) + sgn * (PUSH_DEG * bell(t, tz - 0.05, tS + 0.35))
        if abs(a) > 1e-3: ae.apply_bone_delta(clip, local, 'spine_01', f, ae.qaxis(lat, -a))
    ferr_max = 0.0; ferr_at = None
    for f, (pose, ft) in enumerate(frames):
        for s in ('l', 'r'):
            kh = clip.comp('calf_' + s, f, local)[0]
            ae.solve_leg(clip, local, s, f, ft[s][0], ft[s][1], kh)
            err = ae.vlen(ae.vsub(clip.comp('foot_' + s, f, local)[0], ft[s][0]))
            if err > ferr_max:
                ferr_max = err; pv = clip.comp('pelvis', f, local)[0]
                ferr_at = {'t': round(f * DT, 2), 's': s, 'target_rel_pelvis': [round(ft[s][0][i] - pv[i], 1) for i in range(3)]}
    for s in ('l', 'r'):
        b = 'ik_foot_' + s
        if b in NAMES and 'ik_foot_root' in NAMES:
            for f in range(N):
                fp, fq = clip.comp('foot_' + s, f, local); pp, pq = clip.comp('ik_foot_root', f, local)
                lt = ae.qrot(ae.qinv(pq), ae.vsub(fp, pp)); lq = ae.qnorm(ae.qmul(ae.qinv(pq), fq)); local[b][f] = (lt, lq, local[b][f][2])
    # ---- checks
    def bw(f, s): return clip.comp('ball_' + s, f, local)[0]
    drift = 0.0; pen = 0.0
    for s in ('l', 'r'):
        for f in range(1, N):
            a_, b_ = bw(f - 1, s), bw(f, s); pen = min(pen, b_[2] - FL.BZ0[s])
            if a_[2] < FL.BZ0[s] + 1.0 and b_[2] < FL.BZ0[s] + 1.0:
                dd = math.hypot(b_[0] - a_[0], b_[1] - a_[1]); drift += dd if dd > 0.05 else 0.0
    pz = [clip.comp('pelvis', f, local)[0][2] - local['root'][f][0][2] for f in range(N)]
    e0 = max(ae.vlen(ae.vsub(ae.vsub(clip.comp(bn, 0, local)[0], local['root'][0][0]), EL.rel(L0, bn)[0])) for bn in ('foot_l', 'foot_r', 'head', 'pelvis'))
    fin = N - 1; LF = XL.at(tauX)
    eF = max(ae.vlen(ae.vsub(ae.vsub(clip.comp(bn, fin, local)[0], local['root'][fin][0]), XL.rel(LF, bn)[0])) for bn in ('foot_l', 'foot_r', 'head', 'pelvis'))
    def pitch(f, b):
        pv = clip.comp('pelvis', f, local)[0]; x = clip.comp(b, f, local)[0]; d = ae.vsub(x, pv); return math.degrees(math.atan2(ae.vdot(d, FWD), max(d[2], 1.0)))
    p3 = [pitch(f, 'spine_03') for f in range(N)]; pn = [pitch(f, 'neck_01') for f in range(N)]
    # step table: landings in the clip (ball comes down) with positions along the travel
    steps = []
    for s in ('l', 'r'):
        for f in range(1, N):
            if bw(f, s)[2] < FL.BZ0[s] + 1.5 and bw(f - 1, s)[2] >= FL.BZ0[s] + 1.5: steps.append((round(f * DT, 2), s, round(ae.vdot(bw(f, s), FWD), 1)))
    steps.sort()
    info.update(frames=N, len=round((N - 1) * DT, 3), foot_err=round(ferr_max, 2), foot_err_at=ferr_at, planted_drift=round(drift, 2), penetration=round(pen, 2),
                pelvis_min_minus_final=round(min(pz) - pz[-1], 1), entry_err=round(e0, 2), exit_err=round(eF, 2), p3_range=[round(min(p3), 1), round(max(p3), 1)],
                pn_range=[round(min(pn), 1), round(max(pn), 1)], steps=steps, root_stop=round(df(tz), 1), root_end=round(df(fin * DT), 1), tauX_end=round(tauX, 3))
    return local, info
def write(name, local, nframes, base):
    path = OUTDIR + '/' + name
    ae.leg_guard(base.seq, local, label=name)
    if EAL.does_asset_exist(path): seq = u.load_asset(path)
    else: seq = EAL.duplicate_asset(base.seq.get_path_name().split('.')[0], path)
    for tr in [str(t) for t in AL.get_animation_notify_track_names(seq)]:
        AL.remove_animation_notify_events_by_track(seq, tr)
        try: AL.remove_animation_notify_track(seq, tr)
        except Exception: pass
    c = ae.controller(seq)
    try: c.open_bracket(u.Text('SHME V2.25 authored reversal ' + name), True)
    except Exception: c.open_bracket('SHME V2.25 ' + name, True)
    try:
        c.set_number_of_frames(u.FrameNumber(nframes - 1), True)
        for b in NAMES:
            ks = local[b]
            if not c.set_bone_track_keys(b, [u.Vector(*k[0]) for k in ks], [u.Quat(*k[1]) for k in ks], [u.Vector(*k[2]) for k in ks], True): raise RuntimeError('keys ' + b)
    finally: c.close_bracket(True)
    for cn in [str(n) for n in AL.get_animation_curve_names(seq, u.RawCurveTrackTypes.RCT_FLOAT)]: AL.remove_curve(seq, cn, False)
    try: seq.set_editor_property('loop', False)
    except Exception: pass
    return EAL.save_loaded_asset(seq, False), path
out = {'dry': DRY, 'loops': {'rear': {'T': round(RL.T, 3), 'V': round(RL.V, 1), 'NK': RL.NK}, 'fwd': {'T': round(FL.T, 3), 'V': round(FL.V, 1), 'NK': FL.NK}}, 'prof': PROF, 'cfg': {k: v for k, v in cfg.items() if k != 'only'}, 'clips': {}}
for fam in FAMS:
    for k in range(NPH):
        name = 'SHM226_JogRev_%s_P%d' % (fam, k)
        if ONLY and name not in ONLY: continue
        try:
            local, info = build(fam, k)
            if not DRY: info['saved'], info['path'] = write(name, local, len(local['root']), FL if fam == 'B_F' else RL)
        except Exception:
            import traceback; info = {'err': traceback.format_exc()[-900:]}
        out['clips'][name] = info
(P / 'Saved/Codex/SHME_V226_20261024' / ('gen226_rev_%s.json' % ('dry' if DRY else 'write'))).write_text(json.dumps(out, indent=1))
print('G225 ' + json.dumps(out, default=str))
