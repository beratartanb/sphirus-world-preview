"""GD16 brow SHAPE board: the reference brow stations measured on the user's front panel (medial head, first third, body, arch apex,
lateral tail: top and bottom hair boundary per station, data/brow_stations_v2.json, panel-original px) drawn as markers on the reference
and on each candidate's solved-front-camera capture (warped onto the same 2x panel frame), zoomed. Medial head = green, apex = yellow,
tail = magenta, other stations = cyan; top and bottom boundary points joined per station. Same frame for every tile -> shape, not only height.
usage: blender -b --python gd16_browstations.py -- <ref panel png> <stations json> <out.jpg> <label=capture.png> [...]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'GD13_Identity_20261009', 'tools')); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; R = gi.load(a[0]); ST = json.load(open(a[1])); OUT = a[2]; CAND = [x.split('=', 1) for x in a[3:]]
R = gi.resize(R, R.shape[1]*2, R.shape[0]*2)
X0, X1, Y0, Y1, S = 330, 700, 320, 420, 3
def tile(img):
    T = gi.resize(img[Y0:Y1, X0:X1].copy(), (X1-X0)*S, (Y1-Y0)*S)
    for side, L in ST.items():
        n = len(L)
        for k, (c, t, b) in enumerate(L):
            med = k == 0; tail = k == n-1; apex = (k == int(np.argmin([q[1] for q in L])))
            col = (0.2, 1, 0.2) if med else (1, 1, 0.1) if apex else (1, 0.2, 1) if tail else (0.2, 0.9, 1)
            x = int((2*c-X0)*S); yt = int((2*t-Y0)*S); yb = int((2*b-Y0)*S)
            T[max(0, yt):yb+1, max(0, x-1):x+2, :3] = T[max(0, yt):yb+1, max(0, x-1):x+2, :3]*0.35+np.array(col)*0.65
            for y in (yt, yb): T[max(0, y-3):y+4, max(0, x-3):x+4, :3] = col
    return T
tiles = [tile(R)]+[tile(gi.load(p)) for _, p in CAND]
sep = np.ones((8, tiles[0].shape[1], 4), np.float32)
rows = []
for t in tiles: rows += [t, sep]
gi.save(OUT, np.concatenate(rows[:-1], 0)); print('BROWSTATIONS_OK', OUT, ['REF']+[l for l, _ in CAND])
