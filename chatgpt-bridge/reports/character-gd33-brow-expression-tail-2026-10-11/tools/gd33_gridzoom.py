"""GD33: zoomed crops with a labelled pixel grid (2x panel frame coordinates) for hand-reading brow-tail stations on the reference and on the
captures in the same solved camera. Grid every 10 px (every 50 px brighter). usage: blender -b --python gd33_gridzoom.py -- <out.png> <x0,y0,x1,y1> <scale> label=img ..."""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'GD13_Identity_20261009', 'tools')); import gd13_img as gi; from gd13_common import ROOT
a = sys.argv[sys.argv.index('--')+1:]; OUT = a[0]; x0, y0, x1, y1 = [int(v) for v in a[1].split(',')]; S = int(a[2]); tiles = []
for it in a[3:]:
    lab, p = it.split('=', 1)
    if p.startswith('REF:'):
        I = gi.load(f'{ROOT}/SourceAssets/Characters/GD13_IdentityMaster_20261009/references/GD13_REF_panel_{p[4:]}.png'); I = gi.resize(I, I.shape[1]*2, I.shape[0]*2)
    else: I = gi.load(p)
    T = gi.resize(I[y0:y1, x0:x1, :4].copy(), (x1-x0)*S, (y1-y0)*S)
    for x in range((x0//10+1)*10, x1, 10):
        X = (x-x0)*S; T[:, X, :3] = T[:, X, :3]*0.6+(np.array([1, 1, 0.2]) if x % 50 == 0 else np.array([0.2, 0.9, 1]))*0.4
    for y in range((y0//10+1)*10, y1, 10):
        Y = (y-y0)*S; T[Y, :, :3] = T[Y, :, :3]*0.6+(np.array([1, 1, 0.2]) if y % 50 == 0 else np.array([0.2, 0.9, 1]))*0.4
    tiles.append(T); tiles.append(np.ones((6, T.shape[1], 4), np.float32))
gi.save(OUT, np.concatenate(tiles, 0)); print('GRIDZOOM_OK', OUT)
