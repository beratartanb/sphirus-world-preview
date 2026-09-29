"""Offline skin-weight transfer for the garments (Blender 5.2 python: numpy + BVH), deterministic and independent of the
engine's inpaint solver: closest point on the BR body surface -> barycentric blend of the body's per-vertex bone weights,
two Laplacian smoothing passes over the garment mesh, top-8 influences, normalised.
usage: blender -b --factory-startup --python blender_outfit_weights.py -- <sculpt_package.json.gz> <outfit_geometry.json.gz> <out_weights.json.gz>"""
import bpy, sys, json, gzip, time
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--')+1:]; PKG, GEO, OUT = a
P = json.loads(gzip.open(PKG, 'rb').read()); NB, NH = P['NB'], P['NH']
BODY = np.asarray(P['br_neutral'])[:NB]; TRI = np.asarray(P['body']['triangles']); W = P['weights'][:NB]
bvh = BVHTree.FromPolygons([Vector(p*0.01) for p in BODY], [list(t) for t in TRI])
G = json.loads(gzip.open(GEO, 'rb').read())
def bary(p, a, b, c):
    v0 = b-a; v1 = c-a; v2 = p-a; d00 = v0 @ v0; d01 = v0 @ v1; d11 = v1 @ v1; d20 = v2 @ v0; d21 = v2 @ v1
    den = d00*d11-d01*d01
    if abs(den) < 1e-12: return (1.0, 0.0, 0.0)
    v = (d11*d20-d01*d21)/den; w = (d00*d21-d01*d20)/den; u = 1-v-w
    u, v, w = max(u, 0), max(v, 0), max(w, 0); s = u+v+w; return (u/s, v/s, w/s)
out = {}
for g in ['henley', 'trousers', 'henley_lod1', 'trousers_lod1']:
    t0 = time.time(); X = np.asarray(G[g]['positions']); T = np.asarray(G[g]['triangles']); n = len(X)
    raw = []
    for p in X:
        loc, nrm, idx, dist = bvh.find_nearest(Vector(p*0.01))
        t = TRI[idx]; q = np.asarray(loc)*100; u, v, w = bary(q, BODY[t[0]], BODY[t[1]], BODY[t[2]])
        acc = {}
        for k, wt in ((t[0], u), (t[1], v), (t[2], w)):
            for b, x in W[k].items(): acc[b] = acc.get(b, 0.0)+wt*x
        raw.append(acc)
    # Laplacian smoothing over the garment mesh (2 passes, 0.5) keeps neighbouring vertices on the same bones
    nbr = [set() for _ in range(n)]
    for a_, b_, c_ in T: nbr[a_] |= {b_, c_}; nbr[b_] |= {a_, c_}; nbr[c_] |= {a_, b_}
    import os
    cur = raw
    for _ in range(int(os.environ.get('SPH_W_SMOOTH', '6'))):   # wide, smooth blends across the armhole/crotch: no tearing at 180 deg
        nxt = []
        for i in range(n):
            acc = {b: 0.5*x for b, x in cur[i].items()}; m = len(nbr[i])
            for j in nbr[i]:
                for b, x in cur[j].items(): acc[b] = acc.get(b, 0.0)+0.5*x/m
            nxt.append(acc)
        cur = nxt
    final = []
    for acc in cur:
        top = sorted(acc.items(), key=lambda kv: -kv[1])[:8]; s = sum(x for _, x in top) or 1.0
        final.append({b: round(x/s, 6) for b, x in top if x/s > 1e-4})
    out[g] = final; print(g, n, 'verts weighted in %.1fs' % (time.time()-t0), 'mean influences %.2f' % np.mean([len(f) for f in final]), flush=True)
with gzip.open(OUT, 'wt') as f: json.dump(out, f)
print('WEIGHTS_OK')
