"""GD37 horizontal profiles of the outer face surface: for z bands, the front-most skin y per |x| bin (0.1 cm), averaged left/right, plus
redness. Used to locate the alar crease / alar lobule and the lip corners. usage: ... -- <head.npy> <tex.png> z1 z2 ..."""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); import gd13_img as gi; from gd13_common import NS, MX, pkg
a = sys.argv[sys.argv.index('--')+1:]; S = np.load(a[0])[:NS].astype(float); TEX = a[1]; ZS = [float(v) for v in a[2:]]
P = pkg()['head']; T = np.asarray(P['triangles']); UVc = np.asarray(P['uv'], float); sk = (T < NS).all(1); T = T[sk]; UVc = UVc[sk]
U = np.zeros((NS, 2)); C = np.zeros(NS)
for k in range(3): np.add.at(U, T[:, k], UVc[:, k]); np.add.at(C, T[:, k], 1)
U = U/np.maximum(C, 1)[:, None]; TX = gi.load(TEX)[..., :3]; H, W = TX.shape[:2]
col = TX[(U[:, 1]*(H-1)).astype(int).clip(0, H-1), (U[:, 0]*(W-1)).astype(int).clip(0, W-1)]; red = col[:, 0]/np.maximum(col[:, 1], 1e-4)
x = S[:, 0]-MX; y, z = S[:, 1], S[:, 2]
for zc in ZS:
    out = []
    for b in np.arange(0, 3.4, 0.1):
        vals = []
        for sgn in (1, -1):
            m = (np.abs(z-zc) < 0.06) & (sgn*x >= b) & (sgn*x < b+0.1) & (y > 8)
            if m.sum(): j = np.nonzero(m)[0][np.argmax(y[m])]; vals.append((y[j], red[j]))
        if vals: out.append('%.1f:%.2f/%.2f' % (b, np.mean([v[0] for v in vals]), np.mean([v[1] for v in vals])))
    print('XPROF z %.2f  ' % zc + ' '.join(out))
