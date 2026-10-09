"""GD14: vertical stack of image strips (same width, 8 px dark separators). usage: -- <out.jpg> <width> <img1> [img2 ...]"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'GD13_Identity_20261009', 'tools')); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; OUT = a[0]; WD = int(a[1]); R = []
for p in a[2:]:
    I = gi.load(p); h = int(round(I.shape[0]*WD/I.shape[1])); R.append(gi.resize(I, WD, h)); R.append(np.full((8, WD, 4), [0.12, 0.12, 0.12, 1.0], np.float32))
gi.save(OUT, np.concatenate(R[:-1], 0), 90); print('VSTACK_OK', OUT)
