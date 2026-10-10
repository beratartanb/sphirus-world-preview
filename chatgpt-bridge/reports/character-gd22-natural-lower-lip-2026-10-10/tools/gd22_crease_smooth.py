"""GD22 targeted crease rounding: positional Laplacian smoothing of the OUTER skin inside an ellipsoid zone (plateau + smooth edge), only for vertices whose
normal faces forward (n_y > NY0, so the inner mucosa / vestibule is untouched); tangential-plus-normal Laplacian (true smoothing, rounds a crease), k per
iteration. usage: -- <in.npy> <topo.npz> <out.npy> <zone json [x,y,z,rx,ry,rz,plateau_x,plateau_y,plateau_z]> <iters> <k> [NY0=0.0]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); from gd13_common import NS, MX, skin_normals
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]).astype(float); TP = np.load(a[1]); OUT = a[2]; Z = json.loads(a[3]); IT = int(a[4]); K = float(a[5]); NY0 = float(a[6]) if len(a) > 6 else 0.0
T = TP['loops'].reshape(-1, 3); T = T[(T < NS).all(1)]; E = np.unique(np.sort(np.r_[T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]], 1), axis=0)
I0 = np.r_[E[:, 0], E[:, 1]]; I1 = np.r_[E[:, 1], E[:, 0]]; DEG = np.bincount(I0, minlength=NS).astype(float)
def lap(F): acc = np.zeros_like(F); np.add.at(acc, I0, F[I1]); return acc/np.maximum(DEG, 1)[:, None]
def ss(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
S = X[:NS].copy(); c = np.array(Z[:3]); r = np.array(Z[3:6]); p = np.array(Z[6:9]); NN = skin_normals(X)
w = np.prod(ss((r-np.abs(S-c))/np.maximum(r-p, 1e-6)), axis=1) * ss((NN[:, 1]-NY0)/0.3)
for _ in range(IT): S = S + (K*w)[:, None]*(lap(S)-S)
Y = X.copy(); Y[:NS] = S; np.save(OUT, Y); d = np.linalg.norm(Y-X, axis=1)*10
print('CREASE_SMOOTH verts w>0.05: %d, max move %.2f mm, mean (w>0.05) %.3f mm' % ((w > 0.05).sum(), d.max(), d[:NS][w > 0.05].mean()))
