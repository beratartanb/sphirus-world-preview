"""GD46: quality check of a settled posed Henley vs its posed start: flipped triangles (normal reversed vs start), edge-length outliers,
sleeve-vs-torso proximity (self-intersection proxy: sleeve vertices closer than `near` cm to torso triangles, both in the posed state),
and per-region clearance to the posed body. usage: blender -b --python gd46_meshcheck.py -- <build_dir> <g17e_build_dir>"""
import bpy, sys, os, json, gzip, numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--')+1:]; BD, GDIR = a[0], a[1]
GEO = json.loads(gzip.open(os.path.join(GDIR, 'outfit_geometry.json.gz'), 'rb').read()); H = GEO['henley']; T = np.asarray(H['triangles'], np.int64); PART = np.asarray(H['part']); X0 = np.asarray(H['positions'])
S0 = np.asarray(json.loads(gzip.open(os.path.join(BD, 'henley_posed_start.json.gz'), 'rt').read())['positions']); S1 = np.asarray(json.loads(gzip.open(os.path.join(BD, 'henley_posed_settled.json.gz'), 'rt').read())['positions'])
B = np.asarray(json.loads(gzip.open(os.path.join(BD, 'body_posed.json.gz'), 'rt').read())['positions'])
P = json.loads(gzip.open(sys.argv[sys.argv.index('--')+3], 'rb').read()) if len(a) > 2 else None
main = PART == 'SPH_Henley'; Tm = T[np.all(main[T], axis=1)]
def nrm(X, Tt): n = np.cross(X[Tt[:, 1]]-X[Tt[:, 0]], X[Tt[:, 2]]-X[Tt[:, 0]]); return n/np.maximum(np.linalg.norm(n, axis=1), 1e-9)[:, None]
flip = (np.einsum('ij,ij->i', nrm(S0, Tm), nrm(S1, Tm)) < 0); rep = {'tris_main': int(len(Tm)), 'flipped': int(flip.sum())}
E = np.unique(np.sort(np.concatenate([Tm[:, [0, 1]], Tm[:, [1, 2]], Tm[:, [2, 0]]]), axis=1), axis=0); L0 = np.linalg.norm(X0[E[:, 1]]-X0[E[:, 0]], axis=1); L1 = np.linalg.norm(S1[E[:, 1]]-S1[E[:, 0]], axis=1); r = L1/np.maximum(L0, 1e-6)
rep['edges'] = {'n': int(len(E)), 'ratio_gt_1.5': int((r > 1.5).sum()), 'ratio_lt_0.5': int((r < 0.5).sum()), 'p95': round(float(np.percentile(r, 95)), 3)}
sl = main & (np.abs(X0[:, 0]) > 24); to = main & (np.abs(X0[:, 0]) <= 24)          # sleeves vs torso panels (bind-space split)
Tt = Tm[np.all(to[Tm], axis=1)]; bvh = BVHTree.FromPolygons([tuple(v) for v in S1], [list(t) for t in Tt]) if len(Tt) else None
near = 0.4; cnt = 0; inside = 0
if bvh is not None:
    for i in np.nonzero(sl)[0]:
        loc, n_, idx, d = bvh.find_nearest(Vector(S1[i]))
        if loc is not None and d < near: cnt += 1
rep['sleeve_torso_near_lt_%.1fcm' % near] = int(cnt)
# clearance per region (posed body, outward normal from body triangles)
TB = None
if P is not None:
    NB = P['NB']; TB = np.asarray([list(t) for t in P['body']['triangles']]+[[x+NB, y+NB, z+NB] for x, y, z in P['head']['triangles']], np.int64)
    bl = lambda p_: (p_[0], -p_[1], p_[2]); bb = BVHTree.FromPolygons([bl(v) for v in B], [list(t) for t in TB]); sd = np.full(len(S1), 9.9)
    for i in np.nonzero(main)[0]:
        q_ = Vector(bl(S1[i])); loc, n_, idx, d = bb.find_nearest(q_)
        if loc is not None: sd[i] = (q_-loc).dot(n_)
    zb = X0[:, 2]; rep['clearance_by_region'] = {}
    for nm, m_ in (('yoke_z>136', main & (zb > 136)), ('shoulder_cap_128-136_|x|>12', main & (zb > 128) & (zb <= 136) & (np.abs(X0[:, 0]) > 12)), ('upper_back_122-136_|x|<12', main & (zb > 122) & (zb <= 136) & (np.abs(X0[:, 0]) <= 12)), ('torso_<122', main & (zb <= 122) & (np.abs(X0[:, 0]) <= 24)), ('sleeves', sl)):
        v = sd[m_]; rep['clearance_by_region'][nm] = {'n': int(m_.sum()), 'p05': round(float(np.percentile(v, 5)), 2), 'p50': round(float(np.percentile(v, 50)), 2), 'p95': round(float(np.percentile(v, 95)), 2), 'max': round(float(v.max()), 2), 'inside': int((v < 0).sum())}
    sd0 = np.full(len(S0), 9.9)
    for i in np.nonzero(main)[0]:
        q_ = Vector(bl(S0[i])); loc, n_, idx, d = bb.find_nearest(q_)
        if loc is not None: sd0[i] = (q_-loc).dot(n_)
    rep['clearance_start_by_region'] = {}
    for nm, m_ in (('yoke_z>136', main & (zb > 136)), ('shoulder_cap_128-136_|x|>12', main & (zb > 128) & (zb <= 136) & (np.abs(X0[:, 0]) > 12)), ('upper_back_122-136_|x|<12', main & (zb > 122) & (zb <= 136) & (np.abs(X0[:, 0]) <= 12)), ('torso_<122', main & (zb <= 122) & (np.abs(X0[:, 0]) <= 24)), ('sleeves', sl)):
        v = sd0[m_]; rep['clearance_start_by_region'][nm] = {'p05': round(float(np.percentile(v, 5)), 2), 'p50': round(float(np.percentile(v, 50)), 2), 'p95': round(float(np.percentile(v, 95)), 2), 'max': round(float(v.max()), 2), 'inside': int((v < 0).sum())}
json.dump(rep, open(os.path.join(BD, 'meshcheck.json'), 'w'), indent=1); print('MESHCHECK', json.dumps(rep))
