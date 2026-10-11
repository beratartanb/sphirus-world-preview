"""GD30 soft normal push (alar wing volume): outer-skin vertices inside an ellipsoid zone (plateau + smooth edge) move along their own vertex normal by
AMOUNT mm, weighted by a SOFT direction gate ss((n . u - G0)/0.4) so only the surface facing the direction u (e.g. the outer lateral alar wing) moves and
the nostril interior / rim inner face stays - a thin rim thickens smoothly instead of splitting. Displacements are then smoothed over the mesh graph
(2 Laplacian passes on the displacement field) to avoid vertex-level ripple.
usage: -- <in.npy> <topo.npz> <out.npy> <zone json [x,y,z,rx,ry,rz,px,py,pz]> <amount mm> <u json [ux,uy,uz]> [G0=0.2] [move json [mx,my,mz]: translate the gated surface along this unit direction instead of the vertex normal]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); from gd13_common import NS, MX, skin_normals
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]).astype(float); TP = np.load(a[1]); OUT = a[2]; Z = json.loads(a[3]); AMT = float(a[4])/10.0; U = np.array(json.loads(a[5]), float); U /= np.linalg.norm(U); G0 = float(a[6]) if len(a) > 6 else 0.2; MV = np.array(json.loads(a[7]), float) if len(a) > 7 else None
T = TP['loops'].reshape(-1, 3); T = T[(T < NS).all(1)]; E = np.unique(np.sort(np.r_[T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]], 1), axis=0)
I0 = np.r_[E[:, 0], E[:, 1]]; I1 = np.r_[E[:, 1], E[:, 0]]; DEG = np.bincount(I0, minlength=NS).astype(float)
def lap(F): acc = np.zeros_like(F); np.add.at(acc, I0, F[I1]); return acc/np.maximum(DEG, 1)[:, None]
def ss(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
S = X[:NS]; c = np.array(Z[:3]); r = np.array(Z[3:6]); p = np.array(Z[6:9]); NN = skin_normals(X)
w = np.prod(ss((r-np.abs(S-c))/np.maximum(r-p, 1e-6)), axis=1) * ss((NN@U-G0)/0.4)
D = (np.tile(MV/np.linalg.norm(MV), (NS, 1)) if MV is not None else NN)*(AMT*w)[:, None]
for _ in range(2): D = 0.5*D + 0.5*lap(D)
Y = X.copy(); Y[:NS] = S + D; np.save(OUT, Y); d = np.linalg.norm(D, axis=1)*10
print('NORMAL_PUSH verts w>0.05: %d, max %.2f mm, mean (w>0.05) %.3f mm' % ((w > 0.05).sum(), d.max(), d[w > 0.05].mean() if (w > 0.05).any() else 0))
