# scalp_region.py (Blender -b, numpy): which Sph8 face vertices lie under the bun's strand roots -> scalp cover region.
# Roots from strands.npz (C49/GD38 UE frame) moved by the measured head offset (top-of-skull alignment, scalp nn p50 0.24 cm).
# Region = vertices within 0.7 cm of a root, then eroded by 1.6 cm (edge distance along the mesh) so the cover edge stays under hair.
import sys, json, traceback, numpy as np
from mathutils import kdtree
A = sys.argv[sys.argv.index('--') + 1:]; out = A[0]
try:
    Z = np.load(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/SourceAssets/Characters/CharacterCohesion_C49_20261104/Hair/h1/strands.npz')
    R = np.concatenate([Z['main'][:, 0], Z['loose'][:, 0]]).astype(float) + np.array([0.22, -2.31, 1.45])
    F = json.load(open(r'C:/Users/berat/Documents/Unreal Projects/sphirus_UE59/Saved/UE59Work/b4/dump_face.json'))['lods']['0']; V = np.array(F['v']); T = np.array(F['t'])
    kd = kdtree.KDTree(len(R))
    for i, p in enumerate(R): kd.insert(p, i)
    kd.balance()
    nd = np.array([kd.find(p)[2] for p in V]); cnt = np.array([len(kd.find_range(p, 1.0)) for p in V])
    R0 = (nd < 0.7)
    nb = [set() for _ in range(len(V))]
    for a, b, c in T:
        for x, y in ((a, b), (b, c), (c, a)): nb[x].add(y); nb[y].add(x)
    # interior gaps (part lines, whorls: no roots within 0.7 cm but enclosed by rooted scalp) belong to the region; only the outer
    # hairline counts as edge. Complement components that are small (<= 200 verts) and within 1.5 cm of roots everywhere are filled.
    comp = -np.ones(len(V), int); sizes = []
    for s0 in np.where(~R0)[0]:
        if comp[s0] >= 0: continue
        st = [s0]; comp[s0] = len(sizes); n = 0
        while st:
            v = st.pop(); n += 1
            for x in nb[v]:
                if not R0[x] and comp[x] < 0: comp[x] = len(sizes); st.append(x)
        sizes.append(n)
    gap = np.zeros(len(V), bool)
    for k, n in enumerate(sizes):
        m = comp == k
        if n <= 200 and float(nd[m].max()) < 1.5: gap |= m   # small and close to roots on every vertex: a part line / whorl
    filled = int(gap.sum()); R0 = R0 | gap
    # distance from the region boundary (Dijkstra-lite over edges)
    import heapq
    dist = np.full(len(V), 1e9); hq = []
    for v in np.where(R0)[0]:
        if any(not R0[x] for x in nb[v]): dist[v] = 0.0; heapq.heappush(hq, (0.0, v))
    while hq:
        d, v = heapq.heappop(hq)
        if d > dist[v] or d > 3.0: continue
        for x in nb[v]:
            if R0[x]:
                nd2 = d + float(np.linalg.norm(V[x] - V[v]))
                if nd2 < dist[x]: dist[x] = nd2; heapq.heappush(hq, (nd2, x))
    keep = R0 & (dist >= 1.6)
    tri = [t.tolist() for t in T if keep[t].all()]
    rep = {'filled_gaps': filled, 'gap_components': len(sizes) - 1, 'roots': len(R), 'face_v': len(V), 'R0': int(R0.sum()), 'keep': int(keep.sum()), 'tris': len(tri), 'keep_z': [float(V[keep, 2].min()), float(V[keep, 2].max())], 'keep_y': [float(V[keep, 1].min()), float(V[keep, 1].max())],
           'roots_per_cm2_crown': float(np.median(cnt[keep]) / 3.14), 'nd_p50_keep': float(np.median(nd[keep]))}
    json.dump({'v': np.where(keep)[0].tolist(), 't': tri, 'rep': rep}, open(out, 'w'))
except BaseException: open(out, 'w').write('ERR ' + traceback.format_exc())
