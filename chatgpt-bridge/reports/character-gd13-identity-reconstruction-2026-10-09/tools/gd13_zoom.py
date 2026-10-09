"""GD13 close-up comparison: the same pixel window (2x panel coordinates) cut from the reference panel and from renders made with that panel's
solved camera, stacked side by side, upscaled. usage: -- <out.jpg> <x0> <y0> <x1> <y1> <scale> <view> <render1.png> [render2.png ...]"""
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); import gd13_img as gi; from gd13_common import ROOT
a = sys.argv[sys.argv.index('--')+1:]; OUT = a[0]; x0, y0, x1, y1 = [int(v) for v in a[1:5]]; S = float(a[5]); V = a[6]; RS = a[7:]
R = gi.load(f'{ROOT}/SourceAssets/Characters/GD13_IdentityMaster_20261009/references/GD13_REF_panel_{V}.png'); R = gi.resize(R, R.shape[1]*2, R.shape[0]*2)
tiles = [R[y0:y1, x0:x1]]+[gi.load(p)[y0:y1, x0:x1] for p in RS]
W = int((x1-x0)*S); H = int((y1-y0)*S); sep = np.ones((H, 6, 4), np.float32)
row = []
for t in tiles: row += [gi.resize(t, W, H), sep]
gi.save(OUT, np.concatenate(row[:-1], 1)); print('ZOOM_OK')
