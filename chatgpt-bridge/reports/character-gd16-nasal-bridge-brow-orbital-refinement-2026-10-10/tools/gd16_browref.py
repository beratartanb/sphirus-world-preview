"""GD16 reference brow measurement on the user's FRONT panel (2x panel px, the frame the solved front camera renders into).
Per image column inside each brow: luminance profile over the brow window, local skin level = 85th percentile of the column window,
brow pixels = darker than skin*ratio; the largest dark run gives the top / bottom hair boundary, the darkness-weighted centroid the centre
line. Columns with hair strands / lid shadow ambiguities are rejected (run too thick / thin, jump vs. neighbours) and the curves are lightly
smoothed. Writes json {side: [[col, top, centre, bottom, darkness], ...]} + a check image (detected band drawn on the zoomed crop).
side 'imgL' = image-left brow = the subject's RIGHT brow; 'imgR' = subject's LEFT brow.
usage: blender -b --python gd16_browref.py -- <panel png> <out.json> <check.jpg> [ratio=0.80] [peak fraction=0.45]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'GD13_Identity_20261009', 'tools')); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; R = gi.load(a[0]); OUT, CHK = a[1], a[2]; RT = float(a[3]) if len(a) > 3 else 0.80; PK = float(a[4]) if len(a) > 4 else 0.45
R = gi.resize(R, R.shape[1]*2, R.shape[0]*2); L = R[..., :3] @ np.array([0.30, 0.59, 0.11])
Y0, Y1 = 330, 400
SIDES = {'imgL': (362, 486), 'imgR': (556, 684)}   # lateral limits stop before the loose hair strands
res = {}
for side, (c0, c1) in SIDES.items():
    rows = []
    for c in range(c0, c1):
        col = L[Y0-30:Y1+10, c-1:c+2].mean(1); col = np.convolve(col, np.ones(3)/3, 'same'); sk = np.percentile(col, 85)
        w = col[30:30+(Y1-Y0)]; dark = w < sk*RT
        if not dark.any(): continue
        runs = []; i = 0
        while i < len(dark):
            if dark[i]:
                j = i
                while j < len(dark) and dark[j]: j += 1
                runs.append((i, j)); i = j
            else: i += 1
        i, j = max(runs, key=lambda r: (sk-w[r[0]:r[1]]).clip(0).sum())
        if j-i < 4: continue
        dd = (sk-w[i:j]).clip(0); core = np.nonzero(dd > PK*dd.max())[0]; i2, j2 = i+core[0], i+core[-1]+1   # hair band = darker than PK x peak
        dd2 = (sk-w[i2:j2]).clip(0); cen = Y0+i2+float((np.arange(j2-i2)*dd2).sum()/dd2.sum())
        rows.append([c, Y0+i2, round(cen, 2), Y0+j2, round(float(dd2.mean()/sk), 3)])
    A = np.array(rows, float)
    # reject outliers vs a running median (hair strands, lid crease)
    keep = np.ones(len(A), bool)
    for k in range(len(A)):
        nb = A[max(0, k-6):k+7]; med = np.median(nb[:, 2]); th = np.median(nb[:, 3]-nb[:, 1])
        if abs(A[k, 2]-med) > 4 or (A[k, 3]-A[k, 1]) > th*1.6+3: keep[k] = False
    A = A[keep]
    for j_ in (1, 2, 3):   # light smoothing of top / centre / bottom
        A[:, j_] = np.convolve(np.pad(A[:, j_], 3, mode='edge'), np.ones(7)/7, 'valid')
    res[side] = A.round(2).tolist()
json.dump(res, open(OUT, 'w'), indent=1)
# check image
T = R[315:415, 330:710].copy(); S = 4; T = gi.resize(T, T.shape[1]*S, T.shape[0]*S)
def dot(x, y, col):
    X_, Y_ = int((x-330)*S), int((y-315)*S)
    if 0 <= X_ < T.shape[1] and 0 <= Y_ < T.shape[0]: T[max(0, Y_-1):Y_+2, max(0, X_-1):X_+2, :3] = col
for side, A in res.items():
    for c, t, m, b, d in A: dot(c, t, (0.2, 1, 1)); dot(c, m, (1, 1, 0.2)); dot(c, b, (1, 0.3, 1))
gi.save(CHK, T)
for side, A in res.items():
    A = np.array(A); print('BROWREF', side, 'cols %d..%d n %d' % (A[0, 0], A[-1, 0], len(A)), 'centre rows: medial %.1f apex %.1f (col %d) lateral %.1f | thickness medial %.1f body %.1f tail %.1f' % (
        A[0, 2] if side == 'imgR' else A[-1, 2], A[:, 2].min(), A[np.argmin(A[:, 2]), 0], A[-1, 2] if side == 'imgR' else A[0, 2],
        (A[-1, 3]-A[-1, 1]) if side == 'imgL' else (A[0, 3]-A[0, 1]), np.median(A[:, 3]-A[:, 1]), (A[0, 3]-A[0, 1]) if side == 'imgL' else (A[-1, 3]-A[-1, 1])))
