"""GD38: where are the triangles that flip (normal reversed vs the base head) / collapse in a target head? Region histogram (gd13 regions)."""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); from gd13_common import NS, MX, pkg
a = sys.argv[sys.argv.index('--')+1:]; B = np.load(a[0])[:NS]; X = np.load(a[1])[:NS]
T = np.asarray(pkg()['head']['triangles']); T = T[(T < NS).all(1)]
def nrm(P): return np.cross(P[T[:, 1]]-P[T[:, 0]], P[T[:, 2]]-P[T[:, 0]])
nb, nx = nrm(B), nrm(X); ab, axx = np.linalg.norm(nb, axis=1), np.linalg.norm(nx, axis=1); dot = (nb*nx).sum(1)/np.maximum(ab*axx, 1e-12)
bad = (dot < 0) | (axx/np.maximum(ab, 1e-12) < 0.1); C = B[T[bad]].mean(1)
ax = np.abs(C[:, 0]-MX); y, z = C[:, 1], C[:, 2]
lab = np.where((z > 162.2) & (z <= 163.8) & (ax > 1.0) & (ax < 4.6), 'upper_lid', np.where((z > 160.6) & (z <= 162.2) & (ax > 1.0) & (ax < 4.8), 'lower_lid', np.where((z > 157.3) & (z <= 159.6) & (ax < 2.4), 'nose_base',
        np.where((z > 154.4) & (z <= 157.3) & (ax < 3.0), 'lips', np.where(ax > 6.0, 'side/ear', 'other')))))
u, c = np.unique(lab, return_counts=True); print('FLIPWHERE', len(C), dict(zip(u.tolist(), c.tolist())), '| side x<MX:', int((C[:, 0] < MX).sum()))
for k in range(min(len(C), 12)): print('   ', lab[k], np.round(C[k], 2))
