"""GD28 nostril arch (side view): in a region of interest around the nostril (panel px, given for the reference; the candidate image is 2x and
is sampled at 2x coordinates), the darkest connected blob (luminance below the P-th percentile of the ROI) is taken as the visible nostril
opening; its UPPER boundary (alar rim margin) and lower boundary are traced per column. Both curves are normalised to the nostril's own
front/back extent (u = 0 front .. 1 back) and to the tip->subnasale distance of each image, so arch shapes are comparable; a 6x overlay with
the blobs outlined is written. usage: -- <out.jpg> <x0 x1 y0 y1 (panel px)> <P> label=img.png:scale:tipx,tipy,snx,sny[:x0,x1,y0,y1[:alpha.png]] [...] (optional per-item ROI override and an alpha render masking out the background)"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; OUT = a[0]; x0, x1, y0, y1 = [int(v) for v in a[1:5]]; PCT = float(a[5]); ITEMS = a[6:]
def blob(L, thr):
    m = L < thr; lab = np.zeros(m.shape, int); n = 0; best = None
    for r in range(m.shape[0]):
        for c in range(m.shape[1]):
            if m[r, c] and not lab[r, c]:
                n += 1; st = [(r, c)]; lab[r, c] = n; cnt = 0
                while st:
                    rr, cc = st.pop(); cnt += 1
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        q = (rr+dr, cc+dc)
                        if 0 <= q[0] < m.shape[0] and 0 <= q[1] < m.shape[1] and m[q] and not lab[q]: lab[q] = n; st.append(q)
                if best is None or cnt > best[1]: best = (n, cnt)
    return lab == best[0]
tiles = []; print('label  u:   ' + ' '.join('%5.2f' % u for u in np.linspace(0, 1, 11)) + '   (upper boundary height above the blob bottom-chord, / tip-sn length)')
for it in ITEMS:
    lab, spec = it.split('=', 1); parts = spec.split('|'); path, sc, lm = parts[0].rsplit(':', 2); sc = float(sc); tx, ty, sx, sy = [float(v) for v in lm.split(',')]
    roi = [int(v) for v in parts[1].split(',')] if len(parts) > 1 and parts[1] else [x0, x1, y0, y1]; AL = gi.load(parts[2])[..., 3] if len(parts) > 2 else None
    I = gi.load(path); X0, X1, Y0, Y1 = [int(round(v*sc)) for v in roi]; C = I[Y0:Y1, X0:X1, :3]; Lm = C.mean(-1)
    if AL is not None: Lm = np.where(AL[Y0:Y1, X0:X1] > 0.5, Lm, 9.0)
    B = blob(Lm, np.percentile(Lm[Lm < 5], PCT)); cols = np.nonzero(B.any(0))[0]
    up = np.array([np.nonzero(B[:, c])[0].min() for c in cols], float); lo = np.array([np.nonzero(B[:, c])[0].max() for c in cols], float)
    L = np.hypot(sx-tx, sy-ty)*sc; u = (cols-cols[0])/max(cols[-1]-cols[0], 1)
    # arch height of the upper boundary above the straight line joining its two ends, normalised by tip-sn length (+ = arched up)
    chord = up[0]+(up[-1]-up[0])*u; h = (chord-up)/L
    print('%-8s     ' % lab + ' '.join('%+5.3f' % np.interp(v, u, h) for v in np.linspace(0, 1, 11)) + '   width %.2f height %.2f (x tip-sn)' % ((cols[-1]-cols[0])/L, (lo.max()-up.min())/L))
    T = gi.resize(I[Y0:Y1, X0:X1].copy(), (roi[1]-roi[0])*6, (roi[3]-roi[2])*6); Bz = np.kron(B, np.ones((int(6/sc), int(6/sc)), bool)) if sc < 6 else B
    Bz = gi.resize(np.dstack([B.astype(float)]*3+[np.ones(B.shape)]), T.shape[1], T.shape[0])[..., 0] > 0.5
    edge = Bz ^ (np.roll(Bz, 1, 0) & np.roll(Bz, -1, 0) & np.roll(Bz, 1, 1) & np.roll(Bz, -1, 1)); T[edge, :3] = (1.0, 0.2, 0.2); tiles.append(T)
H = max(t.shape[0] for t in tiles); W = sum(t.shape[1] for t in tiles)+6*(len(tiles)-1); O = np.zeros((H, W, 4)); O[..., 3] = 1; x = 0
for t in tiles: O[:t.shape[0], x:x+t.shape[1]] = t; x += t.shape[1]+6
gi.save(OUT, O); print('NOSTRIL_OK', OUT)
