# g_tighten.py (Blender -b, numpy): pulls the B13 garments toward the B13 body where they stand off it at the BACK and SIDES (the top hung
# from the shoulder blades like a board and hid the back; the shorts ballooned at the hips / seat). Front drape (bust, belly) is kept.
# Per garment vertex: nearest B13 body point (BVH on the closed body), signed offset d along the body normal n.
#   region weight w = max(back, side): back = smoothstep((-n.y - 0.15) / 0.5), side = smoothstep((|n.x| - 0.45) / 0.35)
#   (MetaHuman bind: forward +Y, left +X); fades out above the shoulder line (straps / collar) and at the hems;
#   new offset = d0 + (d - d0) * (1 - K * w) for d > d0 (never pushes inward of d0, never moves vertices that are already close).
# The delta field is Laplacian-smoothed over the garment mesh (keeps folds, removes steps). Output = delta relative to the SOURCE garment
# (s13 delta + this delta) in the b4_apply format, plus a report.
# args: -- <garment key> <d0> <K> <zTopFade0> <zTopFade1> <zHem0> <zHem1> <out dir>
import sys, json, traceback, numpy as np
from mathutils.bvhtree import BVHTree
from mathutils import Vector
A = sys.argv[sys.argv.index('--') + 1:]; key = A[0]; d0 = float(A[1]); K = float(A[2]); zt0, zt1, zh0, zh1 = map(float, A[3:7]); OUT = A[7]
D = 'C:/Users/berat/Documents/Unreal Projects/sphirus_UE59/Saved/UE59Work/'
try:
    B = np.array(json.load(open(D + 'b11/b13_pos.json'))['pos']); BT = json.load(open(D + 'b11/tmpl.json'))['t']
    bvh = BVHTree.FromPolygons([tuple(p) for p in B], [tuple(t) for t in BT])
    G = json.load(open(D + 'b11/g13_%s.json' % key))['lods']['0']; V = np.array(G['v']); T = np.array(G['t'])
    S13 = np.array(json.load(open(D + 'b4/s13/delta_g_%s.json' % key))['lods']['0'])
    assert len(S13) == len(V), (len(S13), len(V))
    def ss(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)
    dl = np.zeros_like(V); W = np.zeros(len(V)); Dd = np.zeros(len(V))
    for i, p in enumerate(V):
        loc, nrm, idx, dist = bvh.find_nearest(Vector(p))
        if loc is None: continue
        n = np.array(nrm); L_ = np.array(loc)
        if np.dot(n, L_ - np.array([0.0, 1.0, L_[2]])) < 0: n = -n          # template winding gives inward normals: orient away from the torso axis
        d = float(np.dot(p - L_, n)); Dd[i] = d
        w = max(ss((-n[1] - 0.15) / 0.5), ss((abs(n[0]) - 0.45) / 0.35))
        w *= 1.0 - ss((p[2] - zt0) / (zt1 - zt0)) if zt1 > zt0 else 1.0     # fade toward the shoulders / waistband top
        w *= ss((p[2] - zh0) / (zh1 - zh0)) if zh1 > zh0 else 1.0          # fade toward the hem
        W[i] = w
        if d > d0 and w > 0:
            nd = d0 + (d - d0) * (1 - K * w); dl[i] = (nd - d) * n
    nb = [set() for _ in range(len(V))]
    for a, b, c in T:
        nb[a].update((b, c)); nb[b].update((a, c)); nb[c].update((a, b))
    for _ in range(6):
        dl = np.array([0.5 * dl[i] + 0.5 * np.mean([dl[j] for j in nb[i]], axis=0) if nb[i] else dl[i] for i in range(len(V))])
    mv = np.linalg.norm(dl, axis=1)
    rep = {'key': key, 'verts': len(V), 'moved>0.2cm': int((mv > 0.2).sum()), 'max_move_cm': float(mv.max()), 'p90_move': float(np.percentile(mv, 90)),
           'offset_before_back_p50': float(np.median(Dd[W > 0.5])) if (W > 0.5).any() else None, 'w>0.5': int((W > 0.5).sum())}
    # offsets after for the weighted region
    D2 = []
    for i in np.where(W > 0.5)[0][::7]:
        p = V[i] + dl[i]; loc, nrm, idx, dist = bvh.find_nearest(Vector(p)); n2 = np.array(nrm); L2 = np.array(loc)
        if np.dot(n2, L2 - np.array([0.0, 1.0, L2[2]])) < 0: n2 = -n2
        D2.append(float(np.dot(p - L2, n2)))
    rep['offset_after_back_p50'] = float(np.median(D2)) if D2 else None; rep['offset_after_back_min'] = float(np.min(D2)) if D2 else None
    json.dump({'lods': {'0': (S13 + dl).round(4).tolist()}}, open(OUT + 'delta_g_%s.json' % key, 'w'))
    json.dump(rep, open(OUT + 'tight_%s.json' % key, 'w'), indent=1)
except BaseException:
    open(OUT + 'tight_%s.json' % key, 'w').write('ERR ' + traceback.format_exc())
