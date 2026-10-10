"""nose-base crop strip: REF front panel (4x) + 4x clay renders of heads in the same solved front camera. usage: -- <out.jpg> <ref panel png> <render1.png> [...]"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; OUT = a[0]; R = gi.load(a[1]); R = gi.resize(R, R.shape[1]*4, R.shape[0]*4)
tiles = [R[1000:1240, 860:1180]] + [gi.load(p)[2000:2480, 1720:2360] for p in a[2:]]
sep = np.ones((480, 6, 4), np.float32); row = []
for T in tiles: row += [gi.resize(T, 640, 480), sep]
gi.save(OUT, np.concatenate(row[:-1], 1)); print('STRIP_OK', OUT)
