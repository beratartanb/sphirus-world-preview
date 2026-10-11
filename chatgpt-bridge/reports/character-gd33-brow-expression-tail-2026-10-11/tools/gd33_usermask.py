"""GD33: the user's red brow outlines (drawn on the GD33 grid-zoom crops r/tail_prof.png = prof_faceL origin (120,280) x4, r/tailZ_q3R.png =
q3_faceR origin (520,340) x7; REF tile only) -> filled masks in 2x panel coordinates, then the REFERENCE brow band measured ONLY inside the
mask (hair outside the outline ignored): per column, skin level = 90th percentile of the column inside mask +-12 px, brow = darker than
skin x RATIO, darkness-weighted centre + core top / bottom (> 0.45 x column peak darkness). Writes data/usermask_<view>.npz (mask, path) and
r/usermask_<view>_check.png (outline + measured band on the reference crop).
usage: blender -b --factory-startup --python gd33_usermask.py -- <view> <annotated.jpg> <x0> <y0> <scale> <tile_h> <seed_x> <seed_y> <out_dir>"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'GD13_Identity_20261009', 'tools')); import gd13_img as gi; from gd13_common import ROOT
a = sys.argv[sys.argv.index('--')+1:]; VIEW, ANN = a[0], a[1]; X0, Y0, SC, TH, SX, SY = (int(v) for v in a[2:8]); OUT = a[8]; RATIO = float(os.environ.get('UM_RATIO', '0.86'))
A = gi.load(ANN)[:TH, :, :3]; H, W = A.shape[:2]
red = (A[..., 0] > 0.55) & (A[..., 0]-A[..., 1] > 0.30) & (A[..., 0]-A[..., 2] > 0.25)
R = red.copy()
for _ in range(4): R = R | np.roll(R, 1, 0) | np.roll(R, -1, 0) | np.roll(R, 1, 1) | np.roll(R, -1, 1)   # close small gaps
F = np.zeros_like(R); st = [(SY, SX)]; F[SY, SX] = True
while st:
    y, x = st.pop()
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        yy, xx = y+dy, x+dx
        if 0 <= yy < H and 0 <= xx < W and not F[yy, xx] and not R[yy, xx]: F[yy, xx] = True; st.append((yy, xx))
leak = F.mean() > 0.45
if leak:   # open outline (runs off the crop edge): inside = between the upper and the lower red stroke per column; one stroke only -> from the crop
    F = np.zeros_like(R)          # top edge down to it when the upper stroke has left the crop (x beyond the last two-stroke column), else skipped
    two = []
    for x in range(W):
        r = np.nonzero(red[:, x])[0]
        if len(r) == 0: continue
        cl = np.split(r, np.nonzero(np.diff(r) > 8)[0]+1)
        if len(cl) >= 2: F[cl[0].max()+1:cl[-1].min(), x] = True; two.append(x)
    if two:
        for x in range(max(two)+1, W):
            r = np.nonzero(red[:, x])[0]
            if len(r): F[:r.min(), x] = True
M = F | (R & ~np.roll(~F, 0, 0))   # filled interior (outline band excluded)
# to 2x panel coordinates
ys, xs = np.nonzero(M); px = X0+xs/SC; py = Y0+ys/SC
REF = gi.load(f'{ROOT}/SourceAssets/Characters/GD13_IdentityMaster_20261009/references/GD13_REF_panel_{VIEW}.png'); REF = gi.resize(REF, REF.shape[1]*2, REF.shape[0]*2)
L = REF[..., :3] @ np.array([0.30, 0.59, 0.11]); Mp = np.zeros(L.shape, bool); Mp[np.round(py).astype(int).clip(0, L.shape[0]-1), np.round(px).astype(int).clip(0, L.shape[1]-1)] = True
path = []
for c in range(int(px.min()), int(px.max())+1):
    rows = np.nonzero(Mp[:, c])[0]
    if len(rows) < 4: continue
    r0, r1 = rows.min(), rows.max(); win = L[max(r0-12, 0):r1+13, c-1:c+2].mean(1); sk = np.percentile(win, 90)
    w = L[r0:r1+1, c-1:c+2].mean(1); d = (sk*RATIO-w).clip(0)
    if d.max() <= 0.01: continue
    core = np.nonzero(d > 0.45*d.max())[0]; cen = r0+float((np.arange(len(d))*d).sum()/d.sum())
    path.append([c, r0+core[0], cen, r0+core[-1], float(d.mean()), int(r0), int(r1)])
P = np.array(path, float)
for j in (1, 2, 3): P[:, j] = np.convolve(np.pad(P[:, j], 4, mode='edge'), np.ones(9)/9, 'valid')
np.savez(f'{OUT}/usermask_{VIEW}.npz', px=px, py=py, path=P, leak=leak)
# check: reference crop with outline (red) and measured band (yellow centre, cyan top/bottom)
x0, x1, y0, y1 = int(px.min())-20, int(px.max())+20, int(py.min())-20, int(py.max())+20; S = 4
T = gi.resize(REF[y0:y1, x0:x1].copy(), (x1-x0)*S, (y1-y0)*S)
ry, rx = np.nonzero(red); T[((Y0+ry/SC-y0)*S).astype(int).clip(0, T.shape[0]-1), ((X0+rx/SC-x0)*S).astype(int).clip(0, T.shape[1]-1), :3] = (1, 0.1, 0.1)
for c, t, m, b, _, _, _ in P:
    for y, col in ((t, (0.2, 1, 1)), (m, (1, 1, 0.2)), (b, (0.2, 1, 1))):
        X_, Y_ = int((c-x0)*S), int((y-y0)*S)
        if 0 <= X_ < T.shape[1]-2 and 0 <= Y_ < T.shape[0]-2: T[Y_:Y_+3, X_:X_+3, :3] = col
gi.save(f'{OUT}/usermask_{VIEW}_check.png', T)
print('USERMASK', VIEW, 'leak', leak, 'mask px', int(M.sum()), 'panel cols %.0f..%.0f rows %.0f..%.0f' % (px.min(), px.max(), py.min(), py.max()), 'path n', len(P),
      'lateral tip col %.0f cen %.1f (top %.1f bot %.1f)' % ((P[0, 0], P[0, 2], P[0, 1], P[0, 3]) if VIEW == 'q3_faceR' else (P[-1, 0], P[-1, 2], P[-1, 1], P[-1, 3])))
