"""pass YY: UNFOLD a candidate head against a fold-free reference (same topology, DNA order). Triangles whose normal turned by more than
~70 deg relative to the reference (cos < COS) are folds created by the edits (ww/xx ops near the nasal sidewall pin, mouth corner, lips).
The displacement field D = cand - ref is relaxed (Laplacian of D, not of the shape) on the folded triangles' vertices plus RING rings of
neighbours, repeated until no folded triangle is left (or MAXIT): the edits stay, only the folded strip gets a smooth transition.
usage: blender -b --python blender_g11yy_unfold.py -- <ref.npy> <cand.npy> <out.npy> [COS=0.35] [RING=2] [MAXIT=400]"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from id_common import pkg
a = sys.argv[sys.argv.index('--')+1:]; R = np.load(a[0]); C = np.load(a[1]); OUT = a[2]
COS = float(a[3]) if len(a) > 3 else 0.35; RING = int(a[4]) if len(a) > 4 else 2; MAXIT = int(a[5]) if len(a) > 5 else 400
NH = 24049; T = np.asarray(pkg()['head']['triangles']); T = T[(T < NH).all(1)]
E = np.r_[T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]]; E = np.r_[E, E[:, ::-1]]; DEG = np.bincount(E[:, 0], minlength=NH).astype(float)
def nrm(X):
    n = np.cross(X[T[:, 1]]-X[T[:, 0]], X[T[:, 2]]-X[T[:, 0]]); return n/np.maximum(np.linalg.norm(n, axis=1), 1e-12)[:, None]
nR = nrm(R[:NH]); X = C.copy(); D = (C-R)[:NH].copy()
def folded(X): return np.where((nrm(X[:NH])*nR).sum(1) < COS)[0]
f0 = folded(X); print('UNFOLD start folded tris', len(f0)); it = 0
while it < MAXIT:
    f = folded(X)
    if len(f) == 0: break
    act = np.zeros(NH, bool); act[np.unique(T[f])] = True
    for _ in range(RING): nb = np.zeros(NH, bool); nb[E[:, 1][act[E[:, 0]]]] = True; act |= nb
    for _ in range(4):
        acc = np.zeros((NH, 3)); np.add.at(acc, E[:, 0], D[E[:, 1]]); L = acc/np.maximum(DEG, 1)[:, None]
        D[act] = D[act]+0.5*(L[act]-D[act])
    X[:NH] = R[:NH]+D; it += 1
f = folded(X); moved = np.linalg.norm(X[:NH]-C[:NH], axis=1)
print('UNFOLD done it %d folded tris %d -> %d, changed verts %d, max change %.2f mm' % (it, len(f0), len(f), int((moved > 1e-4).sum()), moved.max()*10))
np.save(OUT, X)
