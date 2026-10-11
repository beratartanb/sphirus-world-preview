"""GD37 midline profile dump: skin vertices near the midline (|x-MX| < W) on the front of the lower face, sorted by z, with y, texture redness
and the gd37_edit vermilion flag logic. usage: blender -b --factory-startup --python gd37_midprof.py -- <head.npy> <tex.png> [W=0.12] [ref.npy]"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); import gd13_img as gi; from gd13_common import NS, MX, pkg
a = sys.argv[sys.argv.index('--')+1:]; S = np.load(a[0])[:NS].astype(float); TEX = a[1]; Wd = float(a[2]) if len(a) > 2 else 0.12; R = np.load(a[3])[:NS] if len(a) > 3 else None
P = pkg()['head']; T = np.asarray(P['triangles']); UVc = np.asarray(P['uv'], float); sk = (T < NS).all(1); T = T[sk]; UVc = UVc[sk]
U = np.zeros((NS, 2)); C = np.zeros(NS)
for k in range(3): np.add.at(U, T[:, k], UVc[:, k]); np.add.at(C, T[:, k], 1)
U = U/np.maximum(C, 1)[:, None]; TX = gi.load(TEX)[..., :3]; H, W = TX.shape[:2]
col = TX[(U[:, 1]*(H-1)).astype(int).clip(0, H-1), (U[:, 0]*(W-1)).astype(int).clip(0, W-1)]; red = col[:, 0]/np.maximum(col[:, 1], 1e-4)
ax = np.abs(S[:, 0]-MX); m = np.nonzero((ax < Wd) & (S[:, 2] > 152.5) & (S[:, 2] < 160.5) & (S[:, 1] > 9.5))[0]; m = m[np.argsort(-S[m, 2])]
for i in m: print('MID v%5d z %.2f y %.2f red %.3f%s' % (i, S[i, 2], S[i, 1], red[i], '' if R is None else '  dy %+.2f mm' % ((S[i, 1]-R[i, 1])*10)))
