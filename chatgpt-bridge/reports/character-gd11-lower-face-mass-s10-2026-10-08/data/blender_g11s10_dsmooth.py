"""pass S10: HARMONIC SMOOTHING OF THE DISPLACEMENT field D = cand - base inside a box (not of the shape): removes local dips / bumps that a
masked or protected edit leaves in D (they read as new hollows), while the shape detail of the base is kept. Lip vermilion + mouth interior
(and optionally the lower lid band) are pinned to D = 0; the box edge fades over FADE cm.
usage: blender -b --python blender_g11s10_dsmooth.py -- <base.npy> <cand.npy> <out.npy> "ax0,ax1,z0,z1,ymin" [ITERS=60] [FADE=0.6]"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from id_common import pkg
a = sys.argv[sys.argv.index('--')+1:]; Bs = np.load(a[0]); C = np.load(a[1]); AX0, AX1, Z0, Z1, YM = [float(v) for v in a[3].split(',')]
IT = int(a[4]) if len(a) > 4 else 60; FD = float(a[5]) if len(a) > 5 else 0.6; NH = 24049; MX = -0.23
def ss(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
H = Bs[:NH]; ax = np.abs(H[:, 0]-MX); y = H[:, 1]; z = H[:, 2]
box = ss((ax-AX0)/FD+0.5)*(1-ss((ax-AX1)/FD+0.5))*ss((z-Z0)/FD+0.5)*(1-ss((z-Z1)/FD+0.5))*ss((y-YM)/FD+0.5)
lips = (ax < 2.55) & (z > 153.75) & (z < 155.75) & (y > 11.6)
T = np.asarray(pkg()['head']['triangles']); T = T[(T < NH).all(1)]
n = np.cross(H[T[:, 1]]-H[T[:, 0]], H[T[:, 2]]-H[T[:, 0]]); N = np.zeros((NH, 3))
for k in range(3): np.add.at(N, T[:, k], -n)
N /= np.maximum(np.linalg.norm(N, axis=1), 1e-9)[:, None]
mouth_in = (ax < 2.8) & (z > 153.5) & (z < 156.0) & (N[:, 1] < 0.25)
pin = lips | mouth_in
E = np.r_[T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]]; E = np.r_[E, E[:, ::-1]]; DEG = np.bincount(E[:, 0], minlength=NH).astype(float)
D0 = (C-Bs)[:NH].copy(); D = D0.copy(); D[pin] = D0[pin]
act = box > 1e-3
for _ in range(IT):
    acc = np.zeros((NH, 3)); np.add.at(acc, E[:, 0], D[E[:, 1]]); L = acc/np.maximum(DEG, 1)[:, None]
    D[act] = D[act]+0.5*(L[act]-D[act]); D[pin] = D0[pin]
Dn = D0*(1-box)[:, None]+D*box[:, None]
O = C.copy(); O[:NH] = Bs[:NH]+Dn
ch = np.linalg.norm(Dn-D0, axis=1)*10; print('DSMOOTH box verts %d, change max %.2f mm mean(box) %.3f mm, lips change max %.3f mm' % (int((box > 0.5).sum()), ch.max(), ch[box > 0.5].mean(), ch[lips].max()))
np.save(a[2], O)
