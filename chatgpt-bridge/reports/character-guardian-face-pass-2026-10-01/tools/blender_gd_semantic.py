"""GUARDIAN face pass: bind the MetaHuman tracker curves of a candidate RENDER to the candidate mesh (ray cast from the reference-solved
camera through every curve point -> triangle + barycentric). The bound curves can then be re-projected from any deformed version of the
same topology, giving the tracker-equivalent curves without rendering.
usage: blender -b --factory-startup --python blender_gd_semantic.py -- <head.npy> <cand prefix (track/<p>_front.json)> <out semantic.json>"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import *
from mathutils import Vector
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]); PFX = a[1]; OUT = a[2]
T, MI = head_topology(); keep = np.isin(MI, [0, 3, 4]); TT = T[keep]
bvh = BVHTree.FromPolygons([Vector(p) for p in X], [list(t) for t in TT])
out = {}
for view in VIEWS:
    C = json.load(open(f'{G}/track/{PFX}_{view}.json')); res = {}
    for k, pts in C.items():
        lst = []
        for px, py in pts:
            o, d = ray(view, px, py); loc, nrm, idx, dist = bvh.ray_cast(Vector(o), Vector(d))
            if loc is None: lst.append(None); continue
            tri = TT[idx]; A, B, Cc = X[tri]; p = np.asarray(loc)
            v0, v1, v2 = B-A, Cc-A, p-A; d00, d01, d11, d20, d21 = v0@v0, v0@v1, v1@v1, v2@v0, v2@v1; den = d00*d11-d01*d01
            w1 = (d11*d20-d01*d21)/den; w2 = (d00*d21-d01*d20)/den; w0 = 1-w1-w2
            if not (tri < 24049).all():   # eyeball hit (lid margin seen against the globe): snap to the nearest skin vertex
                j = int(np.argmin(np.linalg.norm(X[:24049]-p, axis=1))); lst.append([[j, j, j], [1.0, 0.0, 0.0]])
            else: lst.append([tri.tolist(), [float(w0), float(w1), float(w2)]])
        res[k] = lst
    out[view] = res
    # self check: re-project and compare with the tracked points
    err = []
    for k, lst in res.items():
        for (px, py), e in zip(C[k], lst):
            if e is None: continue
            q = topix(view, [np.asarray(e[1])@X[e[0]]])[0]; err.append(np.hypot(q[0]-px, q[1]-py))
    print('SEM', view, 'curves', len(res), 'points', sum(len(v) for v in res.values()), 'missing', sum(e is None for v in res.values() for e in v), 'reproj err px median %.2f max %.2f' % (np.median(err), np.max(err)))
json.dump(out, open(OUT, 'w')); print('SEMANTIC_OK', OUT)
