"""GD14: compact image grid (row-major, each cell scaled to the cell width, rows padded to the tallest cell, 6 px separators). usage: -- <out.jpg> <ncol> <cell width> <img...>"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'GD13_Identity_20261009', 'tools')); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; OUT = a[0]; NC = int(a[1]); CW = int(a[2]); IM = [gi.load(p) for p in a[3:]]; IM = [gi.resize(I, CW, int(round(I.shape[0]*CW/I.shape[1]))) for I in IM]
bg = np.array([0.12, 0.12, 0.12, 1.0], np.float32); rows = []
for r in range(0, len(IM), NC):
    cells = IM[r:r+NC]; h = max(c.shape[0] for c in cells); row = []
    for c in cells: pad = np.tile(bg, (h-c.shape[0], CW, 1)); row += [np.concatenate([c, pad], 0), np.tile(bg, (h, 6, 1))]
    while len(row) < 2*NC: row += [np.tile(bg, (h, CW, 1)), np.tile(bg, (h, 6, 1))]
    rows += [np.concatenate(row[:-1], 1), np.tile(bg, (6, NC*CW+6*(NC-1), 1))]
gi.save(OUT, np.concatenate(rows[:-1], 0), 90); print('GRID_OK', OUT)
