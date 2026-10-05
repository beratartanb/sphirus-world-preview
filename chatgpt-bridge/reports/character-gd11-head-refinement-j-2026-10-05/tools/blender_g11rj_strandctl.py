"""GD11 refinement J: strand-generation CONTROL (does the dense result keep the guide/flow shape?). Measured on strand geometry, per build.
For the nape / behind-ear families: strand counts; root height relative to the soft back hairline zh_back (roots below the hairline = on neck skin);
tip z spread and tip-to-bun-centre distance (same-level tips = low spread); root-to-root spacing (islands in a row); mid-length distance to the head
surface (surface flattening = ~0, lifted sheet = large); strand length; ear pinna hits (points inside the ear box) for the loose behind-ear families.
usage: blender -b --factory-startup --python blender_g11rj_strandctl.py -- <out.json> <head.npy> <hair_dir1> [<hair_dir2> ...]"""
import bpy, sys, os, json, math, numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--')+1:]; OUT, HEAD = a[0], a[1]; DIRS = a[2:]
hd = np.load(HEAD)[:24049]
def sstep(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
def zh_back(x, y):
    th = abs(math.degrees(math.atan2(x, y-2.5))); zc = 151.2+2.2*(abs(x)/6.0)**2+0.35*math.sin(x*2.3+0.7); zs = float(np.interp(th, [112, 122, 132, 142, 152], [161.0, 159.2, 157.4, 155.6, 153.4]))
    w = sstep((abs(x)-3.4)/1.6); return (1-w)*zc+w*zs
# head surface distance via nearest head vertex (DNA-order npy is dense enough: ~1 mm spacing)
from mathutils.kdtree import KDTree
kd = KDTree(len(hd))
for i, p in enumerate(hd): kd.insert(Vector(p), i)
kd.balance()
def surf_d(P):
    return np.array([kd.find(Vector(p))[2] for p in P])
def in_ear(P):
    return (np.abs(P[:, 0]) > 7.3) & (P[:, 1] > -0.8) & (P[:, 1] < 4.4) & (P[:, 2] > 156.0) & (P[:, 2] < 167.0)
FAM_MAIN = ['nape_field:join', 'nape_field:free', 'nape_field:wisp', 'nape_lock', 'nape_fine', 'nape_to_bun', 'corner_to_bun']
FAM_LOOSE = ['ear_frame', 'under_ear', 'behind_ear', 'ear_lock', 'nape_free', 'temple_veil']
res = {}
for HD in DIRS:
    d = np.load(os.path.join(HD, 'strands.npz')); M, L = d['main'], d['loose']; tg = json.load(open(os.path.join(HD, 'strand_tags.json')))
    tm = np.array(tg['main']); tl = np.array(tg['loose']); r = {'main_total': int(len(M)), 'loose_total': int(len(L))}
    bun = json.load(open(os.path.join(HD, 'hair_build.json'))).get('bun_centre') if os.path.exists(os.path.join(HD, 'hair_build.json')) else None
    for fam, S, T in [(f, M, tm) for f in FAM_MAIN]+[(f, L, tl) for f in FAM_LOOSE]:
        sel = np.array([t.startswith(fam) for t in T]); P = S[sel]
        if len(P) == 0: continue
        roots = P[:, 0]; tips = P[:, -1]
        dz_root = np.array([p[2]-zh_back(p[0], p[1]) for p in roots])
        seg = np.linalg.norm(np.diff(P, axis=1), axis=2).sum(1)
        mid = P[:, P.shape[1]//2]; sd_mid = surf_d(mid[::max(1, len(mid)//400)])
        sd_q = surf_d(P[::max(1, len(P)//200), P.shape[1]//4]); sd_3q = surf_d(P[::max(1, len(P)//200), 3*P.shape[1]//4])
        # nearest other root distance (islands / rows read as clustered roots with empty gaps)
        rk = KDTree(len(roots))
        for i, p in enumerate(roots): rk.insert(Vector(p), i)
        rk.balance(); nn = np.array([rk.find_n(Vector(p), 2)[-1][2] for p in roots[::max(1, len(roots)//600)]])
        ear_hits = int(in_ear(P.reshape(-1, 3)).sum())
        e = {'n': int(len(P)), 'root_dz_hairline_min_med_max': [round(float(dz_root.min()), 2), round(float(np.median(dz_root)), 2), round(float(dz_root.max()), 2)],
             'roots_below_hairline_frac': round(float((dz_root < -0.05).mean()), 3), 'roots_within_1cm_of_hairline_frac': round(float((np.abs(dz_root) < 1.0).mean()), 3),
             'root_x_range': [round(float(roots[:, 0].min()), 1), round(float(roots[:, 0].max()), 1)], 'root_z_range': [round(float(roots[:, 2].min()), 1), round(float(roots[:, 2].max()), 1)],
             'root_nn_spacing_med_p90_cm': [round(float(np.median(nn)), 3), round(float(np.percentile(nn, 90)), 3)],
             'length_cm_min_med_max': [round(float(seg.min()), 1), round(float(np.median(seg)), 1), round(float(seg.max()), 1)],
             'tip_z_med_std': [round(float(np.median(tips[:, 2])), 2), round(float(tips[:, 2].std()), 2)],
             'tip_x_std': round(float(tips[:, 0].std()), 2),
             'surf_dist_cm_q1_mid_q3_med': [round(float(np.median(sd_q)), 2), round(float(np.median(sd_mid)), 2), round(float(np.median(sd_3q)), 2)],
             'surf_dist_mid_p90': round(float(np.percentile(sd_mid, 90)), 2), 'ear_box_point_hits': ear_hits}
        if bun is not None:
            bc = np.asarray(bun); e['tip_to_bun_centre_med_std'] = [round(float(np.median(np.linalg.norm(tips-bc, axis=1))), 2), round(float(np.linalg.norm(tips-bc, axis=1).std()), 2)]
        r[fam] = e
    res[os.path.basename(HD.rstrip('/\\'))] = r
json.dump(res, open(OUT, 'w'), indent=1); print('STRANDCTL_OK', list(res))
