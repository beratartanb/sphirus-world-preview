import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); from gd13_common import NS, MX, pkg
X = np.load(sys.argv[sys.argv.index('--')+1])[:NS]; P = pkg()['head']; T = np.asarray(P['triangles']); UVc = np.asarray(P['uv'], float); sk = (T < NS).all(1); T = T[sk]; UVc = UVc[sk]
U = np.zeros((NS, 2)); C = np.zeros(NS)
for k in range(3): np.add.at(U, T[:, k], UVc[:, k]); np.add.at(C, T[:, k], 1)
U = U/np.maximum(C, 1)[:, None]; ax = np.abs(X[:, 0]-MX); face = (X[:, 1] > 3) & (X[:, 2] > 150) & (X[:, 2] < 168)
mid = face & (ax < 0.03); print('UVAXIS midline verts', mid.sum(), 'u median %.4f mean %.4f std %.4f' % (np.median(U[mid, 0]), U[mid, 0].mean(), U[mid, 0].std()))
for zlo, zhi in ((150, 154), (154, 158), (158, 162), (162, 168)):
    mm = mid & (X[:, 2] > zlo) & (X[:, 2] < zhi); print('  z %d-%d n %d u %.4f' % (zlo, zhi, mm.sum(), np.median(U[mm, 0]) if mm.any() else -1))
# u vs x linear fit over the face: u = a + b*(x-MX)
A = np.c_[np.ones(face.sum()), X[face, 0]-MX]; cf, *_ = np.linalg.lstsq(A, U[face, 0], rcond=None); print('UVAXIS fit u = %.4f + %.4f*(x-MX)' % tuple(cf))
