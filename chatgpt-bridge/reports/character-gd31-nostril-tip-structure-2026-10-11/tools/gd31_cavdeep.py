"""GD31 nostril-cavity deepening: the fixed cavity vertex set (data/cavity_idx.npy, inner walls / roof facing the nostril axis) is pushed AWAY from
the cavity (opposite to the vertex normal, i.e. into the nose tissue) by AMT mm, weighted along y (full at y <= Y0, 0 at y >= Y1: posterior
emphasis), with a 2-ring soft falloff onto neighbouring vertices and K Laplacian passes on the displacement, so the posterior vestibule becomes
deep enough to stay dark like the photo. Reports the minimum distance between the moved cavity wall and the outer alar skin (wall thickness).
usage: -- <in.npy> <topo.npz> <cavity idx.npy> <out.npy> <AMT mm> [Y0=13.6] [Y1=14.4] [K=3]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); from gd13_common import NS, MX, skin_normals
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]).astype(float); TP = np.load(a[1]); CAV = np.load(a[2]); OUT = a[3]; AMT = float(a[4])/10.0
Y0 = float(a[5]) if len(a) > 5 else 13.6; Y1 = float(a[6]) if len(a) > 6 else 14.4; K = int(a[7]) if len(a) > 7 else 3
def ss(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
T = TP['loops'].reshape(-1, 3); T = T[(T < NS).all(1)]; E = np.unique(np.sort(np.r_[T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]], 1), axis=0)
I0 = np.r_[E[:, 0], E[:, 1]]; I1 = np.r_[E[:, 1], E[:, 0]]; DEG = np.bincount(I0, minlength=NS).astype(float)
def lap(F): acc = np.zeros_like(F); np.add.at(acc, I0, F[I1]); return acc/np.maximum(DEG, 1)[:, None]
S = X[:NS]; NN = skin_normals(X); w = np.zeros(NS); w[CAV] = 1.0
for _ in range(2): w = np.maximum(w, 0.5*lap(w[:, None])[:, 0])   # soft 2-ring falloff
w *= ss((Y1-S[:, 1])/max(Y1-Y0, 1e-6))
D = -NN*(AMT*w)[:, None]
for _ in range(K): D = 0.5*D+0.5*lap(D)
Y = X.copy(); Y[:NS] = S+D; np.save(OUT, Y); d = np.linalg.norm(D, axis=1)*10
# wall thickness: cavity vertex to nearest outer alar skin vertex (non-cavity, |x-MX| 0.8..2.3, facing away from the axis)
cav = np.zeros(NS, bool); cav[CAV] = True; P = Y[:NS]; x = np.abs(P[:, 0]-MX)
outer = (~cav) & (x > 0.8) & (x < 2.3) & (P[:, 1] > 12.6) & (P[:, 1] < 14.8) & (P[:, 2] > 157.6) & (P[:, 2] < 159.4)
ci = np.nonzero(cav & (w > 0.3))[0]; oi = np.nonzero(outer)[0]
if len(ci) and len(oi):
    dist = np.min(np.linalg.norm(P[ci][:, None, :]-P[oi][None, :, :], axis=2), axis=1)*10
    print('CAVDEEP moved >0.05mm %d, max %.2f mm | min wall distance cavity->outer %.2f mm (p5 %.2f)' % ((d > 0.05).sum(), d.max(), dist.min(), np.percentile(dist, 5)))
