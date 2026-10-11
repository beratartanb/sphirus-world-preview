"""GD31 like-for-like nostril-opening check on REAL renders: the darkest connected blob in the ROI is segmented the same way on the reference
panel (1x) and on UE captures warped into the panel frame (2x, downsampled to 1x), masked by the candidate's alpha so background never counts.
Prints extents, area and IoU vs the reference, and writes REF | candidates zooms with the reference blob outline (orange) and each
candidate blob (cyan outline). usage: -- <out.jpg> <ref panel> <x0,x1,y0,y1> <S> <pct> label=capture2x.png|alpha2x.png [...]"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; OUT, REF = a[0], a[1]; x0, x1, y0, y1 = [int(v) for v in a[2].split(',')]; S = int(a[3]); PCT = float(a[4]); CANDS = a[5:]
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
R = gi.load(REF)[y0:y1, x0:x1, :3]; RL = R.mean(-1); RB = blob(RL, np.percentile(RL, PCT))
def ext(B): rr, cc = np.nonzero(B); return cc.min()+x0, cc.max()+x0, rr.min()+y0, rr.max()+y0, B.sum()
print('%-9s cols %d-%d rows %d-%d area %d px^2' % (('REF',)+ext(RB)))
W, H = (x1-x0)*S, (y1-y0)*S
def outline(T, B, col):
    Bz = gi.resize(np.dstack([B.astype(float)]*3+[np.ones(B.shape)]), W, H)[..., 0] > 0.5
    e = Bz ^ (np.roll(Bz, 1, 0) & np.roll(Bz, -1, 0) & np.roll(Bz, 1, 1) & np.roll(Bz, -1, 1)); T[e, :3] = col
T0 = gi.resize(np.dstack([R, np.ones(R.shape[:2])]), W, H).copy(); outline(T0, RB, (1, 0.55, 0)); tiles = [T0]
for c in CANDS:
    lb, spec = c.split('=', 1); p, al = spec.split('|'); I = gi.load(p); A = gi.load(al)[..., 3]
    C = gi.resize(I[y0*2:y1*2, x0*2:x1*2], x1-x0, y1-y0)[..., :3]; Am = gi.resize(np.dstack([A[y0*2:y1*2, x0*2:x1*2]]*4), x1-x0, y1-y0)[..., 0] > 0.9
    CL = np.where(Am, C.mean(-1), 9.0); CB = blob(CL, np.percentile(CL[Am], PCT)); iou = (CB & RB).sum()/max((CB | RB).sum(), 1)
    rc = np.nonzero(RB); cc = np.nonzero(CB)
    print('%-9s cols %d-%d rows %d-%d area %d px^2 | IoU %.3f | centre d(col,row) %+.1f %+.1f' % ((lb,)+ext(CB)+(iou, cc[1].mean()-rc[1].mean(), cc[0].mean()-rc[0].mean())))
    T = gi.resize(I[y0*2:y1*2, x0*2:x1*2].copy(), W, H); outline(T, RB, (1, 0.55, 0)); outline(T, CB, (0.1, 0.9, 1)); tiles.append(T)
O = np.zeros((H, len(tiles)*(W+6)-6, 4)); O[..., 3] = 1
for i, T in enumerate(tiles): O[:, i*(W+6):i*(W+6)+W] = T
gi.save(OUT, O); print('REALOPEN_OK', OUT)
