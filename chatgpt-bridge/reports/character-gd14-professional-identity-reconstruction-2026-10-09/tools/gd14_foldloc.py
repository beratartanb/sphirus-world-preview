"""GD14: locate folded edges (dihedral > 120 deg) that are NEW vs a base head, and the triangles with extreme area change; prints project-frame
positions (x offset from the midline). usage: -- <head.npy> <base.npy> <topo.npz>"""
import sys, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]); B = np.load(a[1]); TP = np.load(a[2]); NS = 24049; MX = -0.23
T = TP['loops'].reshape(-1, 3); T = T[(T < NS).all(1)]
def folds(Y):
    E = np.r_[T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]]; F = np.r_[np.arange(len(T)), np.arange(len(T)), np.arange(len(T))]
    key = np.sort(E, 1); o = np.lexsort((key[:, 1], key[:, 0])); ks = key[o]; fs = F[o]; same = (ks[1:] == ks[:-1]).all(1); pr = np.c_[fs[:-1][same], fs[1:][same]]; ek = ks[:-1][same]
    n = np.cross(Y[T[:, 1]]-Y[T[:, 0]], Y[T[:, 2]]-Y[T[:, 0]]); n /= np.maximum(np.linalg.norm(n, axis=1), 1e-12)[:, None]
    ang = np.degrees(np.arccos(np.clip((n[pr[:, 0]]*n[pr[:, 1]]).sum(1), -1, 1))); m = ang > 120
    return {tuple(e): g for e, g in zip(map(tuple, ek[m]), ang[m])}
fb, fx = folds(B), folds(X); new = [e for e in fx if e not in fb]
print('folds base', len(fb), 'cand', len(fx), 'new', len(new), 'removed', len([e for e in fb if e not in fx]))
for e in new: p = X[list(e)].mean(0); print('  NEW fold %.0f deg at x%+.2f y %.2f z %.2f' % (fx[e], p[0]-MX, p[1], p[2]))
ar = lambda Y: np.linalg.norm(np.cross(Y[T[:, 1]]-Y[T[:, 0]], Y[T[:, 2]]-Y[T[:, 0]]), axis=1)
r = ar(X)/np.maximum(ar(B), 1e-12); i = np.argsort(r)
for j in list(i[:4])+list(i[-4:]): p = X[T[j]].mean(0); print('  area ratio %.2f at x%+.2f y %.2f z %.2f' % (r[j], p[0]-MX, p[1], p[2]))
