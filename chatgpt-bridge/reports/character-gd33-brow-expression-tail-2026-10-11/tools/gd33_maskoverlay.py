"""GD33: the user's red brow outline drawn onto model captures in the same solved camera (q3_faceR: identical panel frame; prof_faceL: the
reference outline mapped into the model frame about the lateral canthus with scale 1/PK, the profile panel scale difference). Crops x S.
usage: blender -b --factory-startup --python gd33_maskoverlay.py -- <out.png> <view> <annotated.jpg> <x0> <y0> <scale> <tile_h> <crop x0,y0,x1,y1> <S> label=img ..."""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'GD13_Identity_20261009', 'tools')); import gd13_img as gi; from gd13_common import ROOT
a = sys.argv[sys.argv.index('--')+1:]; OUT, VIEW, ANN = a[:3]; X0, Y0, SC, TH = (int(v) for v in a[3:7]); cx0, cy0, cx1, cy1 = (int(v) for v in a[7].split(',')); S = int(a[8])
A = gi.load(ANN)[:TH, :, :3]; red = (A[..., 0] > 0.55) & (A[..., 0]-A[..., 1] > 0.30) & (A[..., 0]-A[..., 2] > 0.25); ry, rx = np.nonzero(red)
px, py = X0+rx/SC, Y0+ry/SC; K = float(os.environ.get('PK', '1.087'))
tiles = []
for it in a[9:]:
    lab, p = it.split('=', 1)
    if p == 'REF': I = gi.load(f'{ROOT}/SourceAssets/Characters/GD13_IdentityMaster_20261009/references/GD13_REF_panel_{VIEW}.png'); I = gi.resize(I, I.shape[1]*2, I.shape[0]*2); qx, qy = px, py
    else:
        I = gi.load(p); qx, qy = px, py
        if VIEW == 'prof_faceL': qx = 252.0+(px-247.5)/K; qy = 397.0+(py-390.0)/K
    T = gi.resize(I[cy0:cy1, cx0:cx1, :3].copy(), (cx1-cx0)*S, (cy1-cy0)*S)
    X_ = ((qx-cx0)*S).astype(int); Y_ = ((qy-cy0)*S).astype(int); ok = (X_ >= 0) & (X_ < T.shape[1]) & (Y_ >= 0) & (Y_ < T.shape[0]); T[Y_[ok], X_[ok]] = (1, 0.1, 0.1)
    tiles.append(T); tiles.append(np.ones((5, T.shape[1], 3), np.float32))
gi.save(OUT, np.concatenate(tiles, 0)); print('MASKOVL_OK', OUT)
