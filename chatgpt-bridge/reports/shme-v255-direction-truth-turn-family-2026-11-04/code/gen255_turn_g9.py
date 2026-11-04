"""gen255_turn.py (editor job): V2.55 turn-around built from REAL female motion capture, not from a planned two-bone solve.
Why: v254 side frames (sheets/v254_a_side_zoom.png) show the gen254 brake as a tip-toe mince (toes down, 0.16 s steps, no heel / no load) and a
two-feet spin at the end. Its legs were synthesised. The project owns retargeted female capture of exactly the two halves of a turn-around
(/Game/CoreMotion_Retargeted/AAMS/Walk): af_Loco_<Gait>_Fwd_Stop = a real 3-4 contact brake from gait speed (long reach, loaded knee, the body
rising as it slows) and af_Loco_<Gait>_Start_Turn<S><ANG>_<S>foot = a real pivot on the outside foot + drive into the new direction.
Method (source editing, never a procedural leg):
  segment A = stop clip from a0 to aJ (time rate c_brake after the brake begins; speed profile kept, so the strides shorten instead of speeding up)
  segment B = turn start from b0 to b1 (rate c_turn), rotated to continue A
  join = both feet on the ground (A: last brake foot just loaded, rear foot not yet lifted; B: pivot foot loaded, other foot not yet lifted)
  every bone below the root is cross-faded (slerp) over x_fade; the root path is the integral of the blended velocities;
  feet: stance intervals come from the source contacts; the BALL is pinned in the world while planted, a swing carries the remaining offset away
  smoothly, legs re-solved with the source knee as hint; foot rotation, ankle roll, pelvis, spine and arms stay the source's.
Left turn = stop clip MIRRORED (comp-space reflection with per-bone reference correction) + the source left turn start.
Curves: SHM226_V/W forward speed, SHM226_VL side speed (V2.48 ClipSpeedLat), SHM238_Turn/W, SHM254_W/Side/Own, SHM255_Phase, SHM237_FPPelvisOff, footspeed.
builtins.G255 = {'dry_run': bool, 'clips': [spec]}; spec: name, A, B, mirrorA, side (+1 right / -1 left), ang, a0, aJ, b0, b1, c_brake, c_turn, x_fade, s_brake,
pelvis_k, pelvis_ref. New assets only, stick JSON in Saved/Codex/SHME_V255_20261104/stick. Prints G255 {...}."""
import unreal as u, json, math, builtins, pathlib, importlib, sys, re
P = pathlib.Path(u.Paths.project_dir()).resolve(); sys.path.insert(0, str(P / 'Tools/SHME_V1_20260925'))
import v137_animedit as ae; importlib.reload(ae)
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
cfg = dict(getattr(builtins, 'G255', {})); DRY = bool(cfg.get('dry_run', True))
LOOP = cfg.get('loop', '/Game/GraceRanger/SHME/Animations/V233/SprintCalm/SHM233_Calm_A_LB_Sprint_Fwd')
OUTDIR = cfg.get('outdir', '/Game/GraceRanger/SHME/Animations/V255'); SD = P / 'Saved/Codex/SHME_V255_20261104'; (SD / 'stick').mkdir(parents=True, exist_ok=True)
FPS = 30.0; DT = 1.0 / FPS; ZAX = (0.0, 0.0, 1.0)
loop = u.load_asset(LOOP); NAMES = [str(n) for n in AL.get_animation_track_names(loop)]; T1 = float(loop.get_play_length())
PAR = {}
for b in NAMES:
    p = ae.bone_path(loop, b)
    for i, x in enumerate(p): PAR[x] = p[i + 1] if i + 1 < len(p) else None
ALLB = list(PAR.keys())
def depth(b):
    d = 0
    while PAR.get(b) is not None: b = PAR[b]; d += 1
    return d
ORDER = sorted(ALLB, key=depth)
L0 = ae.read_local(loop, ALLB, [0])
def mir(b):
    if b.endswith('_l'): return b[:-2] + '_r'
    if b.endswith('_r'): return b[:-2] + '_l'
    return b
def Mq(q): return (q[0], -q[1], -q[2], q[3])
def Mv(v): return (-v[0], v[1], v[2])
# reference pose in component space (symmetric): per-bone mirror correction C_b = M(Qref_b)^-1 * Qref_m(b)
sk = loop.get_editor_property('skeleton')
QR = {}
try:
    rp = u.AnimPoseExtensions.get_reference_pose(sk)
    for b in ALLB:
        tr = u.AnimPoseExtensions.get_ref_bone_pose(rp, b, u.AnimPoseSpaces.WORLD); r = tr.rotation; QR[b] = (r.x, r.y, r.z, r.w)
except Exception as e: raise RuntimeError('ref pose ' + str(e)[:200])
CM = {b: ae.qnorm(ae.qmul(ae.qinv(Mq(QR[b])), QR[mir(b)])) for b in ALLB if mir(b) in QR}
def slerp(a, b, t):
    d = sum(a[i] * b[i] for i in range(4))
    if d < 0: b = tuple(-x for x in b); d = -d
    if d > 0.9995: return ae.qnorm(tuple(a[i] + (b[i] - a[i]) * t for i in range(4)))
    th = math.acos(min(d, 1.0)); s = math.sin(th)
    return tuple((math.sin((1 - t) * th) * a[i] + math.sin(t * th) * b[i]) / s for i in range(4))
def lerp(a, b, t): return tuple(a[i] + (b[i] - a[i]) * t for i in range(len(a)))
def mj(x): x = min(1.0, max(0.0, x)); return x * x * x * (10 - 15 * x + 6 * x * x)
def heading(q):
    f = ae.qrot(q, (0.0, 1.0, 0.0)); return math.degrees(math.atan2(-f[0], f[1]))
def qyaw(h): return ae.qaxis(ZAX, h)
assert abs(heading(qyaw(37.0)) - 37.0) < 0.01 or abs(heading(qyaw(37.0)) + 37.0) < 0.01
_d = ae.qrot(ae.qaxis(ae.vcross((0.0, 1.0, 0.0), ZAX), 10.0), (0.0, 0.0, 1.0)); LS_ = 1.0 if _d[1] > 0 else -1.0   # + rotation about fw x Z leans Z toward +fw when LS_ = 1
YS = 1.0 if abs(heading(qyaw(37.0)) - 37.0) < 0.01 else -1.0
class Src:
    def __init__(self, path, s0, s1, mirror=False):
        self.seq = u.load_asset(path); assert self.seq, path; self.path = path
        nk = ae.num_frames(self.seq); L = float(self.seq.get_play_length()); dt0 = L / max(1, nk - 1)
        step = max(1, int(round((1.0 / 60.0) / dt0))); self.dt = dt0 * step
        f0 = max(0, int(s0 / dt0) - step); f1 = min(nk - 1, int(math.ceil(s1 / dt0)) + step)
        fr = list(range(f0, f1 + 1, step)); self.t0 = f0 * dt0; self.n = len(fr)
        have = set(str(x) for x in AL.get_animation_track_names(self.seq)); rd = [b for b in ALLB if b in have]
        loc = ae.read_local(self.seq, rd, fr)
        for b in ALLB:
            if b not in loc: loc[b] = [L0[b][0]] * self.n
        self.miss = [b for b in ALLB if b not in have]
        if mirror: loc = self.mirrored(loc)
        self.loc = loc
    def comp_all(self, loc, k):
        T = {}; Q = {}
        for b in ORDER:
            lt, lq, ls = loc[b][k]; p = PAR.get(b)
            if p is None: T[b] = lt; Q[b] = lq
            else: T[b] = ae.vadd(T[p], ae.qrot(Q[p], lt)); Q[b] = ae.qnorm(ae.qmul(Q[p], lq))
        return T, Q
    def mirrored(self, loc):
        out = {b: [] for b in ALLB}
        for k in range(self.n):
            T, Q = self.comp_all(loc, k); T2 = {}; Q2 = {}
            for b in ALLB:
                m = mir(b)
                if m not in T: m = b
                T2[m] = Mv(T[b]); Q2[m] = ae.qnorm(ae.qmul(Mq(Q[b]), CM.get(b, (0, 0, 0, 1))))
            for b in ALLB:
                p = PAR.get(b); ls = loc[b][k][2]
                if p is None: out[b].append((T2[b], Q2[b], ls))
                else:
                    qi = ae.qinv(Q2[p]); out[b].append((ae.qrot(qi, ae.vsub(T2[b], T2[p])), ae.qnorm(ae.qmul(qi, Q2[b])), ls))
        return out
    def idx(self, s):
        x = (s - self.t0) / self.dt; x = min(max(x, 0.0), self.n - 1.0001); i = int(x); return i, x - i
    def at(self, b, s):
        i, a = self.idx(s); A = self.loc[b][i]; B_ = self.loc[b][i + 1]
        return (lerp(A[0], B_[0], a), slerp(A[1], B_[1], a), A[2])
    def root(self, s):
        t, q, _ = self.at('root', s); return t, heading(q)
    def comp(self, b, s):
        ch = []; x = b
        while x is not None: ch.append(x); x = PAR.get(x)
        t = (0.0, 0.0, 0.0); q = (0.0, 0.0, 0.0, 1.0)
        for x in reversed(ch):
            lt, lq, ls = self.at(x, s); t = ae.vadd(t, ae.qrot(q, lt)); q = ae.qnorm(ae.qmul(q, lq))
        return t, q
    def stance(self, side, s0, s1, zthr=5.0, vthr=70.0):
        """list of frames-free contact flags sampled every 1/60 s: ball low and slow in the clip's world"""
        out = []; n = int((s1 - s0) * 60) + 1; prev = None; z = []
        for i in range(n):
            s = s0 + i / 60.0; z.append(self.comp('ball_' + side, s)[0])
        zf = min(p[2] for p in z)
        for i in range(n):
            a, b = z[max(0, i - 1)], z[min(n - 1, i + 1)]; sp = math.hypot(b[0] - a[0], b[1] - a[1]) * 30.0
            out.append((s0 + i / 60.0, z[i][2] - zf < zthr and sp < vthr))
        return out
def flag_at(fl, s):
    i = int(round((s - fl[0][0]) * 60.0)); i = min(max(i, 0), len(fl) - 1); return fl[i][1]
clip = ae.Clip(loop, ['root', 'pelvis', 'spine_01', 'foot_l', 'foot_r', 'ball_l', 'ball_r', 'calf_l', 'calf_r', 'thigh_l', 'thigh_r', 'head', 'spine_03', 'spine_05', 'neck_01', 'hand_l', 'hand_r', 'lowerarm_l', 'lowerarm_r', 'upperarm_l', 'upperarm_r', 'clavicle_l', 'clavicle_r'] + [b for b in ('ik_foot_l', 'ik_foot_r', 'ik_foot_root') if b in NAMES])
ARMB = [x + y for x in ('clavicle', 'upperarm', 'lowerarm') for y in ('_l', '_r')]
_nk = ae.num_frames(loop); _Lk = ae.read_local(loop, ARMB, list(range(0, _nk, 2))); ARMQ = {}
for _b in ARMB:
    _q0 = _Lk[_b][0][1]; _acc = [0.0, 0.0, 0.0, 0.0]
    for _k in _Lk[_b]:
        _q = _k[1]; _d = sum(_q[i] * _q0[i] for i in range(4)); _sg = 1.0 if _d >= 0 else -1.0
        for i in range(4): _acc[i] += _sg * _q[i]
    ARMQ[_b] = ae.qnorm(tuple(_acc))
SB = ['root', 'pelvis', 'spine_03', 'spine_05', 'neck_01', 'head', 'clavicle_l', 'upperarm_l', 'lowerarm_l', 'hand_l', 'clavicle_r', 'upperarm_r', 'lowerarm_r', 'hand_r', 'thigh_l', 'calf_l', 'foot_l', 'ball_l', 'thigh_r', 'calf_r', 'foot_r', 'ball_r']
def build(sp):
    name = sp['name']; side = float(sp.get('side', 1.0)); ANG = float(sp.get('ang', 180.0))
    a0, aJ, b0, b1 = float(sp['a0']), float(sp['aJ']), float(sp['b0']), float(sp['b1'])
    cB, cT, X, sB = float(sp.get('c_brake', 1.3)), float(sp.get('c_turn', 1.1)), float(sp.get('x_fade', 0.2)), float(sp.get('s_brake', 0.45))
    PK, PR = float(sp.get('pelvis_k', 0.35)), float(sp.get('pelvis_ref', 84.0))
    VLEAD, XV, VC, REACH = float(sp.get('v_lead', 0.12)), float(sp.get('x_vel', 0.4)), float(sp.get('v_center', 0.12)), float(sp.get('land_reach', 38.0))
    LSIDE = float(sp.get('land_side', 5.0)); ARMK = float(sp.get('arm_k', 0.0)); VSB = float(sp.get('v_scale_b', 1.0)); VEARLY = float(sp.get('v_early', 0.0)); VFLOOR = float(sp.get('v_floor', 0.0)); VSA, OWNT, BLK = float(sp.get('v_scale_a', 1.0)), float(sp.get('own_tail', 0.25)), float(sp.get('block_t', cfg.get('block_t', 0.5)))
    A = Src(sp['A'], a0 - 0.05, aJ + 0.45, bool(sp.get('mirrorA'))); B_ = Src(sp['B'], 0.0, b1 + 0.1, False)
    # ---- time maps
    tA = [(0.0, a0)]; t = 0.0; s = a0
    while s < aJ + 0.45:
        r = 1.0 + (cB - 1.0) * mj((s - sB) / 0.15); t += 1.0 / 240.0; s += r / 240.0; tA.append((t, s))
    tJ = next(x[0] for x in tA if x[1] >= aJ)
    def sA(t):
        i = min(int(t * 240.0), len(tA) - 1); return tA[i][1]
    def sBt(t):
        return max(0.0, b0 + (t - tJ) * cT)
    T = tJ + (b1 - b0) / cT; N = int(round(T / DT)) + 1; L = (N - 1) * DT
    w = [mj((f * DT - (tJ - X / 2)) / X) for f in range(N)]
    # ---- body below the root
    local = {b: [None] * N for b in ALLB}
    for f in range(N):
        t = f * DT; sa = sA(t); sb = sBt(t); wf = w[f]
        for b in ALLB:
            if b == 'root': continue
            if wf <= 0.0: local[b][f] = A.at(b, sa)
            elif wf >= 1.0: local[b][f] = B_.at(b, sb)
            else:
                x = A.at(b, sa); y = B_.at(b, sb); local[b][f] = (lerp(x[0], y[0], wf), slerp(x[1], y[1], wf), x[2])
    # ---- root: blended velocities, blended yaw (B rotated to continue A)
    def vel(S, s):
        e = 0.03; s = max(s, S.t0 + S.dt + e); p0, _ = S.root(s - e); p1, _ = S.root(s + e); return ((p1[0] - p0[0]) / (2 * e), (p1[1] - p0[1]) / (2 * e))
    yJa = A.root(sA(tJ))[1]; yJb = B_.root(b0)[1]; G = 0.0; gr = 0.0
    wv = [mj((f * DT - (tJ + VC - XV / 2)) / XV) for f in range(N)]
    yEnd = B_.root(b1)[1]
    def unw(a, b): return a + (((b - a) + 180.0) % 360.0 - 180.0)
    def rot(v, a): c, s_ = math.cos(a), math.sin(a); q = ae.qrot(qyaw(a * YS * 180.0 / math.pi), (v[0], v[1], 0.0)); return (q[0], q[1])
    yaw = []; pos = []; px, py = 0.0, 0.0; vels = []; yb_prev = None; yacc = 0.0
    yJb0 = B_.root(0.0)[1]; yTot = 0.0; yp = yJb0
    for k in range(1, 61):
        yq = B_.root(b1 * k / 60.0)[1]; yTot += ((yq - yp + 180.0) % 360.0) - 180.0; yp = yq
    ysc = (side * ANG * (1.0 if YS > 0 else -1.0) * -1.0 * 0 + (ANG if yTot > 0 else -ANG)) / yTot
    for f in range(N):
        t = f * DT; wf = w[f]; wq = wv[f]; uv = mj((sA(t) - 0.35) / 0.5); va = vel(A, sA(t) + VEARLY * (1.0 - uv) - VLEAD * uv);   # the speed runs AHEAD of the pose in the approach (the brake begins at once), and LAGS it at the plant (the body carries over the foot)
        vb = rot(vel(B_, sBt(t)), gr)
        vx = va[0] * VSA * (1 - wq) + vb[0] * VSB * wq; vy = va[1] * VSA * (1 - wq) + vb[1] * VSB * wq
        # a redirect keeps part of its momentum: through the cut the speed never falls under v_floor (feet are re-pinned to this path)
        sp0 = math.hypot(vx, vy); fl_ = VFLOOR * mj((t - (tJ - 0.35)) / 0.2) * (1.0 - mj((t - (tJ + 0.45)) / 0.3))
        if sp0 > 1.0 and sp0 < fl_: vx *= fl_ / sp0; vy *= fl_ / sp0
        vels.append((vx, vy))
        ya = A.root(sA(t))[1]; yb = B_.root(sBt(t))[1]
        if yb_prev is None: yacc = yb
        else: yacc += ((yb - yb_prev + 180.0) % 360.0) - 180.0
        yb_prev = yb
        yaw.append((ya * (1 - wf) + (yacc - yJb0) * ysc * wf))
        pos.append((px, py)); px += vx * DT; py += vy * DT
    local['root'] = [((pos[f][0], pos[f][1], 0.0), qyaw(yaw[f]), (1.0, 1.0, 1.0)) for f in range(N)]
    # ---- pelvis: the deep brake low point is softened (a relaxed person, not a sprinter's plant)
    for f in range(N):
        pt, pq, ps = local['pelvis'][f]; dz = PK * max(0.0, PR - pt[2])
        local['pelvis'][f] = ((pt[0], pt[1], pt[2] + dz), pq, ps)
    if ARMK > 0.0:
        for bn in ARMB:
            qm = ARMQ[bn]
            for f in range(N):
                k_ = ARMK * mj((f * DT - (tJ - 0.25)) / 0.35)
                if k_ > 0.0:
                    lt, lq, ls = local[bn][f]; local[bn][f] = (lt, slerp(lq, qm, k_), ls)
    clip.local = local
    # ---- trunk: the capture's drive lean belongs to a maximal start; a relaxed person leans less. The excess over lean_cap is taken out at spine_01 / spine_03 (legs and pelvis untouched)
    CAP = float(sp.get('lean_cap', 24.0)); ex = []
    for f in range(N):
        fw = ae.qrot(qyaw(yaw[f]), (0.0, 1.0, 0.0)); pe = clip.comp('pelvis', f, local)[0]; ch = clip.comp('spine_05', f, local)[0]; d = ae.vsub(ch, pe)
        ex.append(max(0.0, math.degrees(math.atan2(ae.vdot(d, fw), d[2])) - CAP) if w[f] > 0.0 else 0.0)
    ex = [sum(ex[max(0, f - 4):f + 5]) / len(ex[max(0, f - 4):f + 5]) for f in range(N)]
    for f in range(N):
        if ex[f] < 0.05: continue
        fw = ae.qrot(qyaw(yaw[f]), (0.0, 1.0, 0.0)); ax = ae.vcross(fw, ZAX)
        for bn, sh in (('spine_01', 0.5), ('spine_03', 0.5)):
            ae.apply_bone_delta(clip, local, bn, f, ae.qaxis(ax, -LS_ * ex[f] * sh))
    # ---- contacts in output time
    fl = {s: (A.stance(s, a0 - 0.02, aJ + 0.4), B_.stance(s, 0.0, b1)) for s in 'lr'}
    st = {s: [] for s in 'lr'}
    for s in 'lr':
        for f in range(N):
            t = f * DT; st[s].append(flag_at(fl[s][0], sA(t)) if w[f] < 0.5 else flag_at(fl[s][1], sBt(t)))
        # close gaps of <= 2 frames, drop blips of <= 2 frames
        for gap in (True, False):
            f = 0
            while f < N:
                if st[s][f] != gap: f += 1; continue
                e = f
                while e + 1 < N and st[s][e + 1] == gap: e += 1
                if e - f + 1 <= 2 and f > 0 and e < N - 1:
                    for k in range(f, e + 1): st[s][k] = not gap
                f = e + 1
    # ---- feet: pin the ball, carry the rest
    M = {s: [clip.comp('ball_' + s, f, local)[0] for f in range(N)] for s in 'lr'}
    AN = {s: [clip.comp('foot_' + s, f, local) for f in range(N)] for s in 'lr'}
    TG = {s: [None] * N for s in 'lr'}; ivs = {}
    for s in 'lr':
        ivl = []; f = 0
        while f < N:
            if st[s][f]:
                e = f
                while e + 1 < N and st[s][e + 1]: e += 1
                ivl.append((f, e)); f = e + 1
            else: f += 1
        ivs[s] = ivl
        off = {}; land = {}
        for (f0, f1) in ivl:
            Pn = M[s][f0]
            if f0 > 0:
                # the brake foot lands at the loop's own reach, never at the final spot (V2.36 rule): along the current travel, ball vs pelvis
                v = vels[f0]; sp_ = math.hypot(*v)
                if sp_ > 60.0:
                    dx, dy = v[0] / sp_, v[1] / sp_; pe = clip.comp('pelvis', f0, local)[0]; al = (Pn[0] - pe[0]) * dx + (Pn[1] - pe[1]) * dy
                    if al > REACH: Pn = (Pn[0] - dx * (al - REACH), Pn[1] - dy * (al - REACH), Pn[2])
                    rx_, ry_ = -dy, dx; sg_ = 1.0 if s == 'r' else -1.0; own_ = ((Pn[0] - pe[0]) * rx_ + (Pn[1] - pe[1]) * ry_) * sg_   # right of the travel: forward +Y, right -X
                    if own_ < LSIDE: Pn = (Pn[0] + sg_ * rx_ * (LSIDE - own_), Pn[1] + sg_ * ry_ * (LSIDE - own_), Pn[2])
            land[f0] = (Pn[0] - M[s][f0][0], Pn[1] - M[s][f0][1], 0.0)
            for f in range(f0, f1 + 1):
                d = (Pn[0] - M[s][f][0], Pn[1] - M[s][f][1], 0.0); off[f] = d
        # swing: the offset left at the lift fades to the next landing's offset
        for i, (f0, f1) in enumerate(ivl):
            nx = ivl[i + 1][0] if i + 1 < len(ivl) else N
            d = off[f1]; e = land.get(nx, (0.0, 0.0, 0.0))
            for f in range(f1 + 1, nx):
                x = (f - f1) / max(1, (nx - f1)) ; k = mj(x); off[f] = (d[0] + (e[0] - d[0]) * k, d[1] + (e[1] - d[1]) * k, 0.0)
        if ivl and ivl[0][0] > 0:
            e = land[ivl[0][0]]
            for f in range(0, ivl[0][0]):
                k = mj(f / max(1, ivl[0][0])); off[f] = (e[0] * k, e[1] * k, 0.0)
        for f in range(N):
            d = off.get(f, (0.0, 0.0, 0.0)); TG[s][f] = (ae.vadd(AN[s][f][0], d), AN[s][f][1])
    over = 0.0; hyps = {}
    for f in range(N):
        for s in 'lr':
            kh = clip.comp('calf_' + s, f, local)[0]
            H = clip.comp('thigh_' + s, f, local)[0]; l1 = ae.vlen(local['calf_' + s][f][0]); l2 = ae.vlen(local['foot_' + s][f][0]); dl = ae.vlen(ae.vsub(TG[s][f][0], H))
            over = max(over, dl - (l1 + l2))
            ae.solve_leg(clip, local, s, f, TG[s][f][0], TG[s][f][1], kh)
    for s in 'lr':
        b = 'ik_foot_' + s
        if b in NAMES and 'ik_foot_root' in NAMES:
            for f in range(N):
                fp, fq = clip.comp('foot_' + s, f, local); pp, pq = clip.comp('ik_foot_root', f, local)
                local[b][f] = (ae.qrot(ae.qinv(pq), ae.vsub(fp, pp)), ae.qnorm(ae.qmul(ae.qinv(pq), fq)), local[b][f][2])
    def cw(b, f): return clip.comp(b, f, local)[0]
    ferr = max(ae.vlen(ae.vsub(cw('foot_' + s, f), TG[s][f][0])) for f in range(N) for s in 'lr')
    drift = {s: max([0.0] + [math.hypot(cw('ball_' + s, f)[0] - cw('ball_' + s, f0)[0], cw('ball_' + s, f)[1] - cw('ball_' + s, f0)[1]) for (f0, f1) in ivs[s] for f in range(f0, f1 + 1)]) for s in 'lr'}
    # ---- curves
    VF = []; VS = []
    for f in range(N):
        v = vels[f]; fw = ae.qrot(qyaw(yaw[f]), (0.0, 1.0, 0.0)); rt = ae.qrot(qyaw(yaw[f] + 90.0), (0.0, 1.0, 0.0))   # + yaw = right (checked: qyaw(90) * +Y = -X = right)
        VF.append(v[0] * fw[0] + v[1] * fw[1]); VS.append(v[0] * rt[0] + v[1] * rt[1])
    yaw0 = yaw[0]; turn = [abs(y - yaw0) for y in yaw]
    t_done = next((f * DT for f in range(N) if turn[f] >= ANG - 0.6), L)
    cur = {'SHM226_V': VF, 'SHM226_W': [1.0] * N, 'SHM226_VL': VS}
    cur['SHM238_W'] = [1.0 if f * DT <= t_done else 0.0 for f in range(N)]; cur['SHM238_Turn'] = [turn[f] * 90.0 / ANG * cur['SHM238_W'][f] for f in range(N)]
    cur['SHM254_W'] = list(cur['SHM238_W']); cur['SHM254_Side'] = [side * x for x in cur['SHM238_W']]
    cur['SHM254_Own'] = [1.0 if f * DT <= L - OWNT else 0.0 for f in range(N)]
    cur['SHM255_Phase'] = [0.0 if f * DT < tJ - X / 2 else (1.0 if f * DT < t_done else 2.0) for f in range(N)]
    cur['SHM237_FPPelvisOff'] = [1.0] * N
    fs = {'l': [], 'r': []}
    for f in range(N):
        for s in 'lr':
            a = cw('ball_' + s, max(0, f - 1)); b_ = cw('ball_' + s, min(N - 1, f + 1))
            fs[s].append(math.hypot(b_[0] - a[0], b_[1] - a[1]) / (DT * (min(N - 1, f + 1) - max(0, f - 1))))
    cur['footspeed_l'] = fs['l']; cur['footspeed_r'] = fs['r']
    for cn in ('Enable_OrientationWarping', 'Disable_FootLock', 'pbi_authoredforwardlean'):
        try: cur[cn] = [AL.get_float_value(loop, cn, (f * DT) % T1) for f in range(N)]
        except Exception: pass
    pz = [cw('pelvis', f)[2] for f in range(N)]
    info = {'len': round(L, 3), 'frames': N, 'tJ': round(tJ, 3), 't_done': round(t_done, 3), 'foot_err': round(ferr, 2), 'overreach': round(over, 2), 'drift': {k: round(v, 2) for k, v in drift.items()},
            'pelvis': [round(min(pz), 1), round(max(pz), 1)], 'stance': {s: [(round(a * DT, 2), round(b * DT, 2)) for a, b in ivs[s]] for s in 'lr'}, 'v01': [round(math.hypot(*vels[f])) for f in range(0, N, 3)], 'yaw01': [round(yaw[f]) for f in range(0, N, 3)], 'miss': len(A.miss)}
    (SD / 'stick' / (name + '.json')).write_text(json.dumps({'name': name, 'dt': DT, 'bones': SB, 'fwd': [0.0, 1.0, 0.0], 'right': [-1.0, 0.0, 0.0], 'root': [[round(x, 2) for x in cw('root', f)] for f in range(N)],
        'planted': {s: [1 if st[s][f] else 0 for f in range(N)] for s in 'lr'}, 'frames': [[[round(x, 1) for x in cw(b, f)] for b in SB] for f in range(N)]}))
    info['blk'] = BLK
    return name, local, info, cur
def write(name, local, cur, BLK=0.5):
    path = OUTDIR + '/' + name
    ae.leg_guard(loop, local, label=name)
    seq = u.load_asset(path) if EAL.does_asset_exist(path) else EAL.duplicate_asset(LOOP, path)
    for tr in [str(t) for t in AL.get_animation_notify_track_names(seq)]:
        AL.remove_animation_notify_events_by_track(seq, tr)
        try: AL.remove_animation_notify_track(seq, tr)
        except Exception: pass
    n = len(local['root']); c = ae.controller(seq)
    try: c.open_bracket(u.Text('SHME V2.55 ' + name), True)
    except Exception: c.open_bracket('SHME V2.55 ' + name, True)
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
    bt = BLK
    AL.add_animation_notify_track(seq, 'SHME_V255_Block')
    AL.add_animation_notify_state_event(seq, 'SHME_V255_Block', bt, seq.get_play_length() - bt, u.AnimNotifyState_PoseSearchBlockTransition)
    return EAL.save_loaded_asset(seq, False), path
out = {'loop': LOOP, 'clips': {}, 'ys': YS}
for sp in cfg.get('clips', []):
    try: name, local, info, cur = build(sp)
    except Exception:
        import traceback; out['clips'][sp['name']] = {'error': traceback.format_exc()[-1200:]}; continue
    if not DRY:
        try: info['saved'], info['path'] = write(name, local, cur, info['blk'])
        except Exception as e: info['write_error'] = str(e)[:400]
    out['clips'][name] = info
(SD / 'data' / ('gen255_%s.json' % ('dry' if DRY else 'write'))).write_text(json.dumps(out, indent=1, default=str))
print('G255 ' + json.dumps(out, default=str)[:3800])
