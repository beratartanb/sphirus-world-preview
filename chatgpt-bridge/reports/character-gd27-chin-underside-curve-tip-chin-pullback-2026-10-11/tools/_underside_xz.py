"""Chin / submental underside: lowest down-facing skin z per (lateral x-MX, y) cell, to see the shape across the width. usage: -- label=head.npy [...]"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); from gd13_common import NS, MX, skin_normals
H = [s.split('=', 1) for s in sys.argv[sys.argv.index('--')+1:]]; XO = [0, 0.8, 1.6, 2.4, 3.2, 4.0]; YS = np.arange(13.0, 6.49, -0.5)
for lab, p in H:
    X = np.load(p); S = X[:NS]; NN = skin_normals(X); print(lab + '   y \ |x-MX| ' + ' '.join('%6.1f' % o for o in XO))
    for y in YS:
        row = []
        for o in XO:
            q = (np.abs(np.abs(S[:, 0]-MX)-o) < 0.25) & (np.abs(S[:, 1]-y) < 0.25) & (S[:, 2] < 153.0) & (S[:, 2] > 146.0) & (NN[:, 2] < -0.3)
            row.append('%6.2f' % S[q, 2].min() if q.any() else '    . ')
        print('   %5.1f        ' % y + ' '.join(row))
