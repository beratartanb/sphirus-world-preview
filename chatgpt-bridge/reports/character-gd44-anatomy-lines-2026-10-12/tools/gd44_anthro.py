"""GD44: anthropometric verification of a body candidate against literature norms (adult female, scaled to our stature) and the private
reference silhouette. Measures from the mesh: segment lengths / landmark heights from the bind skeleton, horizontal section breadth / depth /
perimeter at anatomical levels (torso, legs), bone-perpendicular sections for the arms (A-pose), breast point distance, shoulder breadths.
Perimeter = closed polygon of the true plane section (edge/plane intersections, angle-ordered around the centroid; sections are convex-ish).
usage: blender -b --python gd44_anthro.py -- <libdir> <pkg> <lk> <extra|-> <label> <out.json>
Norms: approximate ranges for a lean athletic adult woman of ~173 cm (ANSUR-II female means scaled by stature, lean adjustment); labelled
approximate on purpose — they bound plausibility, they are not a target to the millimetre."""
import sys, os, json, numpy as np
sys.path.insert(0, sys.argv[sys.argv.index('--')+1]); from gd44_lib import Body, MX
a = sys.argv[sys.argv.index('--')+2:]; PKG, LKJ, EXTRA, LAB, OUT = a[:5]
B = Body(PKG, LKJ, extra=None if EXTRA == '-' else EXTRA); XR = B.XR; x, y, z = XR.T; NB = B.NB; E = B.E; W8 = B.P['weights']
def chain(pre): return np.asarray([sum(w for b_, w in W8[v].items() if b_.startswith(pre)) for v in range(NB)])
clav = chain(('clavicle',)); arm = B.arm-clav; uarm = B.uarm; larm = chain(('lowerarm',)); hand = B.hand; leg = B.leg
H = 173.27; bone = B.bone
def hull2d(Q):
    Q = Q[np.lexsort((Q[:, 1], Q[:, 0]))]
    def half(pts):
        h = []
        for q in pts:
            while len(h) >= 2 and np.cross(h[-1]-h[-2], q-h[-2]) <= 0: h.pop()
            h.append(q)
        return h
    lo = half(Q); up = half(Q[::-1]); return np.asarray(lo[:-1]+up[:-1])
def plane_section(p0, n, mask):
    n = np.asarray(n, float); n = n/np.linalg.norm(n); s = (XR-p0)@n; e = E[mask[E[:, 0]] & mask[E[:, 1]]]
    s0, s1 = s[e[:, 0]], s[e[:, 1]]; c = (s0*s1 < 0); e = e[c]; s0, s1 = s0[c], s1[c]; t = s0/(s0-s1)
    P = XR[e[:, 0]]+(XR[e[:, 1]]-XR[e[:, 0]])*t[:, None]
    if len(P) < 6: return None
    u = np.cross(n, [0, 0, 1.0]) if abs(n[2]) < 0.9 else np.cross(n, [1.0, 0, 0]); u /= np.linalg.norm(u); v = np.cross(n, u)
    Q = np.stack([(P-p0)@u, (P-p0)@v], 1); Hh = hull2d(Q); per = float(np.sum(np.linalg.norm(np.roll(Hh, -1, 0)-Hh, axis=1)))   # convex hull = tape measure
    return {'perimeter': per, 'w': float(Q[:, 0].max()-Q[:, 0].min()), 'd': float(Q[:, 1].max()-Q[:, 1].min()), 'n': int(len(Q)), 'P': P}
def hsec(zz, mask):
    r = plane_section(np.array([0, 0, zz]), [0, 0, 1.0], mask)
    if r is None: return None
    P = r['P']; r['w'] = float(P[:, 0].max()-P[:, 0].min()); r['d'] = float(P[:, 1].max()-P[:, 1].min()); r['front'] = float(P[:, 1].max()); r['back'] = float(P[:, 1].min()); return r
TR = (arm < 0.3) & (hand < 0.1); LL = (leg > 0.4) & (x > 0); RL = (leg > 0.4) & (x < 0); ALLM = np.ones(NB, bool)
def best(zs, mask, pick):
    out = None
    for zz in zs:
        r = hsec(zz, mask)
        if r is None: continue
        if out is None or (pick == 'min' and r['perimeter'] < out[1]['perimeter']) or (pick == 'max' and r['perimeter'] > out[1]['perimeter']): out = (zz, r)
    return out
M = {}
# ---- skeleton lengths / heights (bind, cm)
J = {k: bone(k) for k in ('upperarm_l', 'lowerarm_l', 'hand_l', 'thigh_l', 'calf_l', 'foot_l', 'ball_l', 'clavicle_l', 'neck_01', 'pelvis')}
M['stature'] = H; M['acromion_z_est'] = float(J['upperarm_l'][2]+2.0); M['shoulder_joint_z'] = float(J['upperarm_l'][2]); M['hip_joint_z'] = float(J['thigh_l'][2]); M['knee_joint_z'] = float(J['calf_l'][2]); M['ankle_joint_z'] = float(J['foot_l'][2])
M['upper_arm_len'] = float(np.linalg.norm(J['lowerarm_l']-J['upperarm_l'])); M['forearm_len'] = float(np.linalg.norm(J['hand_l']-J['lowerarm_l'])); M['thigh_len'] = float(np.linalg.norm(J['calf_l']-J['thigh_l'])); M['shank_len'] = float(np.linalg.norm(J['foot_l']-J['calf_l']))
PLAN = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'shape_plan.json'))); M['crotch_z'] = float(PLAN['landmarks_our_z']['crotch'])
# ---- torso levels
bust_z = 127.5; r = hsec(bust_z, TR); M['bust_circ'] = r['perimeter']; M['bust_w'] = r['w']; M['bust_d'] = r['d']
ub = best(np.arange(118.0, 124.1, 0.5), TR, 'min'); M['underbust_z'], M['underbust_circ'] = ub[0], ub[1]['perimeter']
wz = best(np.arange(100.0, 118.1, 0.5), TR, 'min'); M['waist_z'], M['waist_circ'], M['waist_w'], M['waist_d'] = wz[0], wz[1]['perimeter'], wz[1]['w'], wz[1]['d']
r = hsec(104.0, TR); M['navel_circ'], M['navel_w'], M['navel_d'] = r['perimeter'], r['w'], r['d']
hz = best(np.arange(M['crotch_z']+5.0, 100.1, 0.5), TR | (leg > 0.4), 'max'); M['hip_z'], M['hip_circ'], M['hip_w'], M['hip_d'] = hz[0], hz[1]['perimeter'], hz[1]['w'], hz[1]['d']
# ---- legs (left)
zt = M['crotch_z']-2.5; r = hsec(zt, (leg > 0.5) & (x > 0)); M['thigh_upper_z'], M['thigh_upper_circ'] = zt, r['perimeter']
zm = 0.5*(M['hip_joint_z']+M['knee_joint_z']); r = hsec(zm, LL); M['thigh_mid_z'], M['thigh_mid_circ'] = zm, r['perimeter']
r = hsec(M['knee_joint_z']+1.0, LL); M['knee_circ'] = r['perimeter']
cz = best(np.arange(26.0, 44.1, 0.5), LL, 'max'); M['calf_z'], M['calf_circ'] = cz[0], cz[1]['perimeter']
az = best(np.arange(9.0, 17.1, 0.5), LL, 'min'); M['ankle_z'], M['ankle_circ'] = az[0], az[1]['perimeter']
# ---- arms (left, sections perpendicular to the bone axis)
def arm_best(j0, j1, mask, t0, t1, pick):
    ax = j1-j0; L = np.linalg.norm(ax); n = ax/L; out = None
    for t in np.arange(t0, t1+1e-6, 0.03):
        r = plane_section(j0+t*ax, n, mask)
        if r is None: continue
        if out is None or (pick == 'max' and r['perimeter'] > out[1]) or (pick == 'min' and r['perimeter'] < out[1]): out = (float(t), r['perimeter'])
    return out
UA = (uarm > 0.55) & (x > 0); FA = (larm > 0.55) & (x > 0) & (hand < 0.2); WR = ((larm > 0.3) | (hand > 0.3)) & (x > 0) & (B.hand < 0.985)
ua = arm_best(J['upperarm_l'], J['lowerarm_l'], UA, 0.30, 0.60, 'max'); M['upper_arm_t'], M['upper_arm_circ'] = ua
fa = arm_best(J['lowerarm_l'], J['hand_l'], FA, 0.15, 0.45, 'max'); M['forearm_t'], M['forearm_circ'] = fa
def slab_perimeter(j0, j1, t, mask, rmax=6.0, half=0.8):   # fallback: vertex slab perpendicular to the axis, convex hull perimeter
    ax = j1-j0; L = np.linalg.norm(ax); n = ax/L; d = XR-(j0+t*ax); tt = d@n; perp = d-np.outer(tt, n); sel = mask & (np.abs(tt) < half) & (np.linalg.norm(perp, axis=1) < rmax)
    if sel.sum() < 6: return None
    u = np.cross(n, [0, 0, 1.0]); u /= np.linalg.norm(u); v = np.cross(n, u); Q = np.stack([perp[sel]@u, perp[sel]@v], 1); Hh = hull2d(Q); return float(np.sum(np.linalg.norm(np.roll(Hh, -1, 0)-Hh, axis=1)))
wr = arm_best(J['lowerarm_l'], J['hand_l'], WR, 0.86, 1.0, 'min')   # styloid level
if wr is None:
    cands = [(t, slab_perimeter(J['lowerarm_l'], J['hand_l'], t, (x > 0) & (B.hand < 0.985))) for t in np.arange(0.86, 1.001, 0.02)]; cands = [c for c in cands if c[1] is not None]
    wr = min(cands, key=lambda c: c[1]) if cands else (None, None)
M['wrist_t'], M['wrist_circ'] = wr
# ---- shoulders / chest breadth / breast points
sel = (np.abs(z-M['acromion_z_est']) < 1.0) & (hand < 0.1); M['shoulder_w_at_acromion'] = float(x[sel].max()-x[sel].min()) if sel.any() else None
chest = (z > 118) & (z < 134) & (y > 3) & (arm < 0.45) & (x > 3)
k = np.argmax(np.where(chest, y, -99)); M['breast_apex_left'] = [float(x[k]), float(y[k]), float(z[k])]; M['bust_point_distance'] = float(2*x[k])
M['chest_w_at_bust'] = M['bust_w']; M['waist_wd_ratio'] = M['waist_w']/M['waist_d']; M['hip_wd_ratio'] = M['hip_w']/M['hip_d']
# ---- norms (lean athletic woman ~173 cm; approximate literature-based ranges)
NORM = {'bust_circ': (86, 92), 'underbust_circ': (73, 78), 'waist_circ': (66, 73), 'navel_circ': (70, 78), 'hip_circ': (93, 99), 'thigh_upper_circ': (54, 59), 'thigh_mid_circ': (47, 52), 'knee_circ': (35, 38.5), 'calf_circ': (34, 37.5), 'ankle_circ': (20.5, 23),
        'upper_arm_circ': (25.5, 28.5), 'forearm_circ': (22.5, 25), 'wrist_circ': (14.8, 16.2), 'shoulder_w_at_acromion': (40, 45), 'bust_point_distance': (18, 21.5), 'waist_w': (23.5, 26.5), 'waist_d': (18, 21), 'waist_wd_ratio': (1.18, 1.42), 'hip_w': (33, 36.5), 'hip_d': (22, 26), 'hip_wd_ratio': (1.3, 1.6),
        'crotch_z': (0.46*H, 0.485*H), 'knee_joint_z': (0.27*H, 0.295*H), 'acromion_z_est': (0.80*H, 0.83*H), 'upper_arm_len': (0.16*H, 0.178*H), 'forearm_len': (0.138*H, 0.156*H), 'thigh_len': (0.235*H, 0.26*H), 'shank_len': (0.23*H, 0.255*H)}
rows = []
for k, (lo, hi) in NORM.items():
    v = M.get(k)
    if v is None: continue
    st = 'OK' if lo <= v <= hi else ('LOW %.0f%%' % (100*(v-lo)/lo) if v < lo else 'HIGH +%.0f%%' % (100*(v-hi)/hi)); rows.append((k, v, lo, hi, st)); M[k+'_status'] = st
json.dump({k: v for k, v in M.items()}, open(OUT, 'w'), indent=1)
print('ANTHRO %-24s %8s   norm %6s..%-6s  %s' % ('measure', LAB, 'lo', 'hi', 'status'))
for k, v, lo, hi, st in rows: print('ANTHRO %-24s %8.1f   norm %6.1f..%-6.1f  %s' % (k, v, lo, hi, st))
print('ANTHRO_EXTRA', json.dumps({k: (round(v, 2) if isinstance(v, float) else v) for k, v in M.items() if k not in NORM and not k.endswith('_status')}))
