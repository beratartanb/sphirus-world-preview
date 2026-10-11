"""GD30 groove fill (fill-only soften): moves skin vertices OUTWARD along their normal by up to AMP mm, weighted by their concavity
(c = (mean(neighbours) - v) . n / mean_edge^2, only c > C0 counts, full at C1) inside an ellipsoid zone with a plateau, so a deep crease
(supra-alar / alar-facial groove) gets shallower while convex forms (ala lobule crest, rim, cheek) are not moved. The displacement is
smoothed by K graph-Laplacian passes so the fill is a soft band, not a ridge. Iterates IT times (concavity re-evaluated each time).
usage: -- <in.npy> <topo.npz> <out.npy> <zones json [[cx,cy,cz, rx,ry,rz, px,py,pz, amp_mm], ...]> [C0=0.3] [C1=1.5] [IT=3] [K=3]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); from gd13_common import NS, MX, skin_normals
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]).astype(float); TP = np.load(a[1]); OUT = a[2]; ZONES = json.loads(a[3])
C0 = float(a[4]) if len(a) > 4 else 0.3; C1 = float(a[5]) if len(a) > 5 else 1.5; IT = int(a[6]) if len(a) > 6 else 3; K = int(a[7]) if len(a) > 7 else 3
def ss(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
T = TP['loops'].reshape(-1, 3); T = T[(T < NS).all(1)]; E = np.unique(np.sort(np.r_[T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]], 1), axis=0)
I0 = np.r_[E[:, 0], E[:, 1]]; I1 = np.r_[E[:, 1], E[:, 0]]; DEG = np.bincount(I0, minlength=NS).astype(float)
def lap(F): acc = np.zeros_like(F); np.add.at(acc, I0, F[I1]); return acc/np.maximum(DEG, 1)[:, None]
Y = X.copy(); S0 = X[:NS].copy(); tot = np.zeros(NS)
for it in range(IT):
    S = Y[:NS]; NN = skin_normals(Y); L = lap(S)-S
    el = np.linalg.norm(S[E[:, 0]]-S[E[:, 1]], axis=1); me = np.zeros(NS); np.add.at(me, E[:, 0], el); np.add.at(me, E[:, 1], el); me /= np.maximum(DEG, 1)
    cv = (L*NN).sum(1)/np.maximum(me, 1e-6)**2; cw = ss((cv-C0)/max(C1-C0, 1e-6))
    D = np.zeros((NS, 3))
    for Z in ZONES:
        c = np.array(Z[:3]); r = np.array(Z[3:6]); p = np.array(Z[6:9]); amp = Z[9]/10.0/IT
        wz = np.prod(ss((r-np.abs(S-c))/np.maximum(r-p, 1e-6)), axis=1)
        D += (wz*cw*amp)[:, None]*NN
    for _ in range(K): D = 0.5*D+0.5*lap(D)
    Y[:NS] = S+D; tot = np.linalg.norm(Y[:NS]-S0, axis=1)*10
np.save(OUT, Y); print('GROOVEFILL verts moved >0.05mm: %d, max %.2f mm, mean of moved %.2f mm' % ((tot > 0.05).sum(), tot.max(), tot[tot > 0.05].mean() if (tot > 0.05).any() else 0))
