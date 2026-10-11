"""GD38: locate the most compressed / stretched skin triangles of a head vs a base head (area ratio), with centroid and per-vertex motion.
usage: blender -b --factory-startup --python gd38_arealoc.py -- <head.npy> <base.npy> [N=10]"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); from gd13_common import NS, MX, pkg
a = sys.argv[sys.argv.index('--')+1:]; A = np.load(a[0])[:NS]; B = np.load(a[1])[:NS]; n = int(a[2]) if len(a) > 2 else 10
T = np.asarray(pkg()['head']['triangles']); T = T[(T < NS).all(1)]
def area(Q): return 0.5*np.linalg.norm(np.cross(Q[T[:, 1]]-Q[T[:, 0]], Q[T[:, 2]]-Q[T[:, 0]]), axis=1)
r = area(A)/np.maximum(area(B), 1e-12); o = np.argsort(r)
for t in list(o[:n])+list(o[-3:]):
    c = B[T[t]].mean(0); d = (A[T[t]]-B[T[t]]).mean(0)*10
    print('AREALOC ratio %.3f at x %+.2f y %.2f z %.2f | base area %.4f cm2 | mean move %+.2f %+.2f %+.2f mm' % (r[t], c[0]-MX, c[1], c[2], area(B)[t], *d))
