"""chin-bottom row check: the same window (2x panel px) from the reference panel and from images in that frame, with a row grid every 10 px (labels = row numbers via tick length: long tick every 50). usage: -- <out.jpg> <y0> <y1> <x0> <x1> <scale> <ref panel> <img1> [...]"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; OUT = a[0]; y0, y1, x0, x1 = [int(v) for v in a[1:5]]; S = float(a[5]); R = gi.load(a[6]); R = gi.resize(R, R.shape[1]*2, R.shape[0]*2)
tiles = [R] + [gi.load(p) for p in a[7:]]; W = int((x1-x0)*S); H = int((y1-y0)*S); row = []; sep = np.ones((H, 6, 4), np.float32)
for T in tiles:
    C = gi.resize(T[y0:y1, x0:x1], W, H).copy()
    for y in range(y0 - y0 % 10 + 10, y1, 10):
        yy = int((y-y0)*S); L = 40 if y % 50 == 0 else 14; C[yy:yy+1, :L, :3] = [1, 1, 0]; C[yy:yy+1, W-L:, :3] = [1, 1, 0]
        if y % 50 == 0: C[yy:yy+1, :, :3] = C[yy:yy+1, :, :3]*0.4 + np.array([0.6, 0.6, 0.0])
    row += [C, sep]
gi.save(OUT, np.concatenate(row[:-1], 1)); print('ROWS_OK', OUT, 'grid: long tick = rows', [y for y in range(y0 - y0 % 50 + 50, y1, 50)])
