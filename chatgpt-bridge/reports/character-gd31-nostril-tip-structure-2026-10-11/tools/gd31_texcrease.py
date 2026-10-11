"""GD31 baked-texture vs geometry check: reads per-vertex UVs of the GD13 scene HEAD mesh (DNA vertex order), crops the baked base-colour texture
around the nose base, and draws on it the most concave vertices (alar-facial / supra-alar crease) of up to three heads in different colours,
so a dark band baked into the texture can be compared with where each head's geometric crease actually lies.
usage: blender -b --python gd31_texcrease.py -- <texture.png> <out.jpg> <topo.npz> label=head.npy:color [...]   (colors r g c y m)"""
import bpy, sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); import gd13_img as gi; from gd13_common import NS, MX, skin_normals
a = sys.argv[sys.argv.index('--')+1:]; TEX, OUT, TOPO = a[0], a[1], a[2]; HEADS = a[3:]
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from id_common import pkg
UVr = np.asarray(pkg()['head']['uv'], float); print('TEXCREASE uv array', UVr.shape)
TRI = np.asarray(pkg()['head']['triangles'], int); UV = np.zeros((int(TRI.max())+1, 2)); cntv = np.zeros(len(UV))
for k in range(3): np.add.at(UV, TRI[:, k], UVr[:, k]); np.add.at(cntv, TRI[:, k], 1)
UV /= np.maximum(cntv, 1)[:, None]
TP = np.load(TOPO); T = TP['loops'].reshape(-1, 3); T = T[(T < NS).all(1)]; E = np.unique(np.sort(np.r_[T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]], 1), axis=0)
I0 = np.r_[E[:, 0], E[:, 1]]; I1 = np.r_[E[:, 1], E[:, 0]]; DEG = np.bincount(I0, minlength=NS).astype(float)
I = gi.load(TEX); H, W = I.shape[:2]
COL = {'r': (1, 0.2, 0.2), 'g': (0.2, 1, 0.2), 'c': (0.1, 0.9, 1), 'y': (1, 1, 0.2), 'm': (1, 0.2, 1)}
first = np.load(HEADS[0].split('=', 1)[1].rsplit(':', 1)[0])[:NS]; x = first[:, 0]-MX
reg = (first[:, 1] > 11.8) & (first[:, 2] > 157.2) & (first[:, 2] < 160.4) & (x > 0.4) & (x < 2.8)     # +x side nose base
cavm = np.zeros(NS, bool); cavm[np.load(os.path.join(os.path.dirname(TOPO), 'cavity_idx.npy'))] = True; reg &= ~cavm
u = UV[:NS][reg, 0]; v = UV[:NS][reg, 1]; pad = 0.004
u0, u1, v0, v1 = np.percentile(u, 3)-pad, np.percentile(u, 97)+pad, np.percentile(v, 3)-pad, np.percentile(v, 97)+pad
c0, c1 = int(u0*W), int(u1*W); r0, r1 = int((1-v1)*H), int((1-v0)*H)
crop = I[r0:r1, c0:c1].copy(); S = max(1, int(900/max(c1-c0, r1-r0)))
T2 = gi.resize(crop, (c1-c0)*S, (r1-r0)*S); base = T2.copy()
print('TEXCREASE uv box u %.3f-%.3f v %.3f-%.3f -> px cols %d-%d rows %d-%d, zoom %d' % (u0, u1, v0, v1, c0, c1, r0, r1, S))
tiles = [base]
for h in HEADS:
    lb, spec = h.split('=', 1); p, col = spec.rsplit(':', 1); X = np.load(p); P = X[:NS]; NN = skin_normals(X)
    acc = np.zeros((NS, 3)); np.add.at(acc, I0, P[I1]); L = acc/np.maximum(DEG, 1)[:, None]-P
    el = np.linalg.norm(P[E[:, 0]]-P[E[:, 1]], axis=1); mel = np.zeros(NS); np.add.at(mel, E[:, 0], el); np.add.at(mel, E[:, 1], el); mel /= np.maximum(DEG, 1)
    cv = (L*NN).sum(1)/np.maximum(mel, 1e-6)**2; m = reg & (cv > np.percentile(cv[reg], 85))
    Tt = base.copy()
    for i in np.nonzero(m)[0]:
        cc = int(round((UV[i, 0]*W-c0)*S)); rr = int(round(((1-UV[i, 1])*H-r0)*S))
        if 2 <= cc < Tt.shape[1]-2 and 2 <= rr < Tt.shape[0]-2: Tt[rr-2:rr+3, cc-2:cc+3, :3] = COL[col]
    tiles.append(Tt); print('TEXCREASE %s concave verts %d' % (lb, m.sum()))
Hh = max(t.shape[0] for t in tiles); O = np.zeros((Hh, sum(t.shape[1] for t in tiles)+6*(len(tiles)-1), 4)); O[..., 3] = 1; xo = 0
for t in tiles: O[:t.shape[0], xo:xo+t.shape[1]] = t; xo += t.shape[1]+6
gi.save(OUT, O); print('TEXCREASE_OK', OUT)
