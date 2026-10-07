"""pass UU: the ACTUAL baked face in DNA order = postrig + low-passed residual (same diffusion as blender_g11uu_residual3.py), for measuring
the shipped candidate (uu31c) with the npy-based tools. usage: blender -b --python blender_g11uu_actual.py -- <target.npy> <postrig.npy> <out.npy> [lowpass_iters]"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from id_common import pkg
a = sys.argv[sys.argv.index('--')+1:]; T0 = np.load(a[0]); P0 = np.load(a[1]); NL = int(a[3]) if len(a) > 3 else 60; NH = 24049
T = T0[:NH]; P = P0[:NH]; R = T-P
TRI = np.asarray(pkg()['head']['triangles']); T3 = TRI[(TRI < NH).all(1)]; E = np.r_[T3[:, [0, 1]], T3[:, [1, 2]], T3[:, [2, 0]]]; E = np.r_[E, E[:, ::-1]]; DEG = np.bincount(E[:, 0], minlength=NH).astype(float)
for _ in range(NL):
    acc = np.zeros_like(R); np.add.at(acc, E[:, 0], R[E[:, 1]]); R = R+0.5*(acc/np.maximum(DEG, 1)[:, None]-R)
out = T0.copy(); out[:NH] = P+R
if len(P0) >= len(T0): out[NH:] = P0[NH:len(T0)]
np.save(a[2], out); print('ACTUAL saved', a[2], 'max resid %.2f mm' % (np.linalg.norm(R, axis=1).max()*10))
