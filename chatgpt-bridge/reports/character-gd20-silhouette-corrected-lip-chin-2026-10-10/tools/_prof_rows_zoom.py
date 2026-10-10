"""6x zoom of the reference profile panel rows r0..r1 (cols c0..c1) with the background-key edge (orange) and row ticks every 5 rows (long every 10),
next to candidate renders (2x frame) cropped to the same window. usage: -- <out.jpg> <r0> <r1> <c0> <c1> <ref panel> label=render.png ..."""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; OUT = a[0]; r0, r1, c0, c1 = [int(v) for v in a[1:5]]; R = gi.load(a[5]); S = 6
def edge(row):
    bg = np.median(row[:30], 0); d = np.abs(row-bg).max(1); idx = np.nonzero(d > 0.10)[0]
    for i in idx:
        if i+6 < row.shape[0] and (d[i:i+6] > 0.10).all(): return i
    return None
tiles = []
C = gi.resize(R[r0:r1, c0:c1], (c1-c0)*S, (r1-r0)*S).copy()
for y in range(r0, r1):
    e = edge(R[y, :, :3]); yy = (y-r0)*S
    if e is not None and c0 <= e < c1: C[yy:yy+S, (e-c0)*S:(e-c0)*S+2, :3] = [1, 0.5, 0]
    if y % 5 == 0: L = 30 if y % 10 == 0 else 12; C[yy:yy+1, :L, :3] = [1, 1, 0]
tiles.append(C)
for s in a[6:]:
    lab, p = s.split('=', 1); I = gi.load(p); Cc = gi.resize(I[2*r0:2*r1, 2*c0:2*c1], (c1-c0)*S, (r1-r0)*S).copy()
    for y in range(r0, r1):
        if y % 5 == 0: yy = (y-r0)*S; L = 30 if y % 10 == 0 else 12; Cc[yy:yy+1, :L, :3] = [1, 1, 0]
    tiles.append(Cc)
sep = np.ones((tiles[0].shape[0], 6, 4), np.float32); row = []
for t in tiles: row += [t, sep]
gi.save(OUT, np.concatenate(row[:-1], 1)); print('ZOOM_OK', OUT)
