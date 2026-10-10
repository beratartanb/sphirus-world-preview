"""chin-bottom edge row (2x panel frame) by the same method on every image: mean luminance of the midline columns x 470..530 per row, smoothed,
the strongest negative gradient between rows 700 and 860 (chin skin -> under-chin). Prints the row and the profile every 10 rows. usage: -- <label=img> ..."""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); import gd13_img as gi
for a in sys.argv[sys.argv.index('--')+1:]:
    lab, p = a.split('=', 1); I = gi.load(p)
    if I.shape[0] < 1000: I = gi.resize(I, I.shape[1]*2, I.shape[0]*2)
    g = (I[..., :3] @ np.array([0.299, 0.587, 0.114]))[:, 470:530].mean(1); k = np.ones(7)/7; gs = np.convolve(g, k, 'same'); d = np.diff(gs)
    seg = d[700:860]; r = 700+int(np.argmin(seg)); top = np.argsort(seg)[:3]+700
    print('%-6s chin-bottom edge row %d (top-3 drops %s)  lum every 10 rows from 700: %s' % (lab, r, sorted(top.tolist()), ' '.join('%.2f' % v for v in gs[700:860:10])))
