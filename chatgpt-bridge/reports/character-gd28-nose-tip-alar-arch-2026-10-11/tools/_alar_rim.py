"""Alar rim / columella bottom heights: lowest down-facing skin z per y bin (0.2) in lateral bands |x-MX| (columella 0-0.3, rim bands), z 157.3-159.2,
for one or more heads. usage: -- label=head.npy [...]"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); from gd13_common import NS, MX, skin_normals
H = [s.split('=', 1) for s in sys.argv[sys.argv.index('--')+1:]]; BANDS = [(0, 0.3), (0.6, 1.0), (1.0, 1.4), (1.4, 1.8), (1.8, 2.2)]
for lab, p in H:
    X = np.load(p); S = X[:NS]; NN = skin_normals(X); ax = np.abs(S[:, 0]-MX)
    print(lab + '  y   ' + ' '.join('  |x| %.1f-%.1f' % b for b in BANDS))
    for y in np.arange(15.2, 12.19, -0.2):
        row = []
        for b0, b1 in BANDS:
            q = (ax >= b0) & (ax < b1) & (np.abs(S[:, 1]-y) < 0.1) & (S[:, 2] > 157.3) & (S[:, 2] < 159.2) & (NN[:, 2] < -0.3)
            row.append('%13.2f' % S[q, 2].min() if q.any() else '            .')
        print('     %5.1f ' % y + ' '.join(row))
