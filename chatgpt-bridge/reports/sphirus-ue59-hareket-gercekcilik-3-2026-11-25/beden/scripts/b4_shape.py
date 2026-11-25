# b4_shape.py (exec'd inside b4_body.py, mode 'shape'): body form delta for the B4 pass.
# Uses V0/T0 (body LOD0 bind pose, cm, forward +Y, left +X), RA (region weights from skin weights), bones, FV (face, for the seam guard).
# Torso: width / front-depth / back-depth factors per height about the section centre, scaled by the torso skin weight.
# Limbs: radial factors per bone parameter t about the local section centroid (centroids from t-bins of the region's own vertices),
#        medial side reduced on the thighs, falloff with distance from the limb axis (axilla / groin protection), scaled by skin weight.
# Local fields: lower belly, trochanter / hip-thigh mass, scapula / upper back, glute. Neck seam guard, graph diffusion, flip check.
import numpy as np, json, os
from mathutils.kdtree import KDTree
S = A['shape']; Vn = V0.copy(); n = len(V0); D = np.zeros((n, 3))
def pl(z, pts):  # piecewise linear in z
    zz = [p[0] for p in pts]; return np.interp(z, zz, [p[1] for p in pts])
x, y, z = V0[:, 0], V0[:, 1], V0[:, 2]
# ---- torso section centre (front/back midpoint) per z from the measured profile (holes skipped), smoothed
prof = [s_ for s_ in Mb['torso_profile'] if s_['front'] > 4 and s_['back'] < -4 and 14 < s_['w'] < 45]
pz = np.array([s_['z'] for s_ in prof]); pc = np.array([(s_['front'] + s_['back']) / 2 for s_ in prof]) + mid[1]
cy = np.interp(z, pz, pc)
wt = RA['torso'] + RA['torso_l'] + RA['torso_r']
sw = pl(z, S['torso_w']); sf = pl(z, S['torso_front']); sb = pl(z, S['torso_back'])
dyt = np.where(y > cy, (sf - 1) * (y - cy), (sb - 1) * (y - cy))
D[:, 0] += wt * (sw - 1) * x; D[:, 1] += wt * dyt
# ---- limbs
def limb(a, b, reg, prof_t, medial_k=1.0, side=1):
    global D
    A_, B_ = bones[a], bones[b]; L = np.linalg.norm(B_ - A_); nax = (B_ - A_) / L
    t = ((V0 - A_) @ nax) / L; w = RA[reg]
    sel = w > 0.3; tb = np.clip((t * 20).astype(int), -4, 24); cen = {}
    for k in np.unique(tb[sel]):
        m = sel & (tb == k)
        if m.sum() > 8: cen[k] = V0[m].mean(axis=0)
    ks = np.array(sorted(cen)); C = np.array([cen[k] for k in ks])
    c = np.stack([np.interp(tb, ks, C[:, i]) for i in range(3)], axis=1)
    r = V0 - c; r -= np.outer(r @ nax, nax); rl = np.linalg.norm(r, axis=1) + 1e-6
    md = {k: (float(np.median(rl[sel & (tb == k)])) if (sel & (tb == k)).sum() > 8 else None) for k in np.unique(tb)}
    kk = np.array(sorted(k for k, v in md.items() if v)); vv = np.array([md[k] for k in kk]); rmed = np.interp(tb, kk, vv)
    g = np.clip(1.0 - (rl - 1.35 * rmed) / (0.5 * rmed), 0, 1)       # falloff away from the limb (chest / groin)
    s = np.interp(t, [p[0] for p in prof_t], [p[1] for p in prof_t]) - 1
    if medial_k != 1.0:
        med = np.clip(-(r[:, 0] * side) / rl, 0, 1); s = s * (1 - (1 - medial_k) * med)
    D += (w * g * s)[:, None] * r
for sd_, sg in (('l', 1), ('r', -1)):
    limb('upperarm_' + sd_, 'lowerarm_' + sd_, 'uarm_' + sd_, S['uarm'])
    limb('lowerarm_' + sd_, 'hand_' + sd_, 'forearm_' + sd_, S['forearm'])
    limb('thigh_' + sd_, 'calf_' + sd_, 'thigh_' + sd_, S['thigh'], S.get('thigh_medial', 0.35), sg)
    limb('calf_' + sd_, 'foot_' + sd_, 'calf_' + sd_, S['calf'], S.get('calf_medial', 0.7), sg)
# ---- local fields (gaussian, mirrored) : {'c': [x,y,z], 'r': [rx,ry,rz], 'd': [dx,dy,dz], 'sym': true}
for fd in S.get('fields', []):
    for sg in ((1, -1) if fd.get('sym') else (1,)):
        c = np.array([fd['c'][0] * sg, fd['c'][1], fd['c'][2]]); rr = np.array(fd['r']); q = (((V0 - c) / rr) ** 2).sum(axis=1)
        w = np.exp(-2.0 * q) * (q < 2.5); d = np.array([fd['d'][0] * sg, fd['d'][1], fd['d'][2]])
        if fd.get('normal'):
            pass
        D += w[:, None] * d[None, :] * (1 - ARMW[:, None] * fd.get('armless', 1.0))
# ---- neck seam guard: distance to the face mesh
kd = KDTree(len(FV))
for i, p in enumerate(FV): kd.insert(p.tolist(), i)
kd.balance()
dseam = np.array([kd.find(p.tolist())[2] for p in V0]); seam = dseam < 0.15
ks2 = KDTree(int(seam.sum()))
for j, i in enumerate(np.where(seam)[0]): ks2.insert(V0[i].tolist(), j)
ks2.balance()
ds = np.array([ks2.find(p.tolist())[2] for p in V0])
G = np.clip((ds - S.get('seam_in', 2.0)) / (S.get('seam_out', 9.0) - S.get('seam_in', 2.0)), 0, 1); G = G * G * (3 - 2 * G)
D *= G[:, None]
# ---- graph diffusion of the delta (no new shape, removes steps between fields)
nb = [[] for _ in range(n)]
for a_, b_, c_ in T0:
    nb[a_] += [b_, c_]; nb[b_] += [a_, c_]; nb[c_] += [a_, b_]
nb = [np.array(sorted(set(v))) for v in nb]
for it in range(S.get('diffuse', 10)):
    Dn = np.array([D[v].mean(axis=0) if len(v) else D[i] for i, v in enumerate(nb)]); D = 0.5 * D + 0.5 * Dn; D *= G[:, None]
D[:, 2] *= S.get('keep_z', 1.0)
Vn = V0 + D
# ---- checks
def tri_n(V):
    a = V[T0]; c = np.cross(a[:, 1] - a[:, 0], a[:, 2] - a[:, 0]); return c
c0 = tri_n(V0); c1 = tri_n(Vn); ar0 = np.linalg.norm(c0, axis=1); ar1 = np.linalg.norm(c1, axis=1)
flips = int(((c0 * c1).sum(axis=1) < 0).sum()); arr = ar1 / np.maximum(ar0, 1e-9)
mag = np.linalg.norm(D, axis=1)
log('SHAPE delta max %.2f cm p99 %.2f mean(moved) %.2f | flips %d | area ratio min %.2f p1 %.2f max %.2f | seam verts %d max delta at seam %.4f' % (mag.max(), np.percentile(mag, 99), mag[mag > 0.01].mean(), flips, arr.min(), np.percentile(arr, 1), arr.max(), seam.sum(), mag[seam].max()))
Ma = measure(Vn, 'after'); json.dump(Ma, open(os.path.join(OUT, 'measure_after.json'), 'w'), indent=1)
log('MEASURE after', json.dumps({k: v for k, v in Ma.items() if k != 'torso_profile'}))
np.save(os.path.join(OUT, 'delta_lod0.npy'), D)
if A.get('render'): render('after', Vn, FV)
# ---- LOD transfer (nearest LOD0 vertex, inverse-distance over 4 neighbours)
kd0 = KDTree(n)
for i, p in enumerate(V0): kd0.insert(p.tolist(), i)
kd0.balance(); out = {'lods': {'0': np.round(D, 4).tolist()}}
for k, Ld in B['lods'].items():
    if k == '0': continue
    VL = np.array(Ld['v']); DL = np.zeros_like(VL)
    for i, p in enumerate(VL):
        nn = kd0.find_n(p.tolist(), 4); ws = np.array([1.0 / (max(d_, 1e-3)) for _, _, d_ in nn]); ids = [j for _, j, _ in nn]
        DL[i] = (D[ids] * ws[:, None]).sum(axis=0) / ws.sum()
    out['lods'][k] = np.round(DL, 4).tolist(); log('LOD', k, 'verts', len(VL), 'max', round(float(np.linalg.norm(DL, axis=1).max()), 2))
json.dump(out, open(os.path.join(OUT, 'delta_body.json'), 'w'))
# ---- garments: delta of the nearest body surface point (barycentric on LOD0), all garment LODs
from mathutils.bvhtree import BVHTree
bvh = BVHTree.FromPolygons([tuple(p) for p in V0], [tuple(t) for t in T0])
for gpath in A.get('garments', []):
    G_ = json.load(open(gpath)); go = {'lods': {}}; rep = []
    for k, Ld in G_['lods'].items():
        VG = np.array(Ld['v']); DG = np.zeros_like(VG); far = 0
        for i, p in enumerate(VG):
            loc, nrm, ti, dist = bvh.find_nearest(Vector(p.tolist()))
            if ti is None: continue
            a_, b_, c_ = T0[ti]; P3 = V0[[a_, b_, c_]]; q = np.array(loc)
            v0_, v1_, v2_ = P3[1] - P3[0], P3[2] - P3[0], q - P3[0]; d00, d01, d11, d20, d21 = v0_ @ v0_, v0_ @ v1_, v1_ @ v1_, v2_ @ v0_, v2_ @ v1_
            den = d00 * d11 - d01 * d01 or 1e-9; bv = (d11 * d20 - d01 * d21) / den; bw = (d00 * d21 - d01 * d20) / den; bu = 1 - bv - bw
            dd = bu * D[a_] + bv * D[b_] + bw * D[c_]
            fall = 1.0 if dist < 12 else max(0.0, 1 - (dist - 12) / 18.0); far += dist > 12
            DG[i] = dd * fall
        go['lods'][k] = np.round(DG, 4).tolist(); rep.append((k, len(VG), round(float(np.linalg.norm(DG, axis=1).max()), 2), far))
    nm = os.path.basename(gpath).replace('dump_', 'delta_'); json.dump(go, open(os.path.join(OUT, nm), 'w')); log('GARMENT', nm, rep)
