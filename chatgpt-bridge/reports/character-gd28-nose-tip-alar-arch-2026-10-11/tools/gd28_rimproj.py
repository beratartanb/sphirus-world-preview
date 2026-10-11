"""GD28 projected nostril opening: 3D alar rim (lowest down-facing skin per y bin in the camera-side ala band |x-MX| in [RB0, RB1], x on the camera
side) and columella / nostril-floor bottom (|x-MX| < 0.35) are projected with the solved prof_faceL camera; between them is the opening seen from
the side. Prints both curves in panel px (1x) per y, the opening height (rim above columella, px) and the rim's arch height above its end chord,
normalised by the projected tip->subnasale distance; also the reference blob boundaries (dark-blob segmentation, same as gd28_nostril.py) for
comparison. usage: -- <cams json> <ref panel> label=head.npy [...]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); from gd13_common import NS, MX, project, skin_normals; import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; C = json.load(open(a[0]))['prof_faceL']; REF = gi.load(a[1]); H = [s.split('=', 1) for s in a[2:]]
RB0, RB1 = 0.9, 2.0
# reference blob (same ROI / percentile as gd28_nostril.py)
x0, x1, y0, y1 = 44, 92, 238, 268; Lm = REF[y0:y1, x0:x1, :3].mean(-1); thr = np.percentile(Lm, 14); m = Lm < thr
from collections import deque
lab = np.zeros(m.shape, int); best = None; n = 0
for r in range(m.shape[0]):
    for c in range(m.shape[1]):
        if m[r, c] and not lab[r, c]:
            n += 1; dq = deque([(r, c)]); lab[r, c] = n; cnt = 0
            while dq:
                rr, cc = dq.popleft(); cnt += 1
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    q = (rr+dr, cc+dc)
                    if 0 <= q[0] < m.shape[0] and 0 <= q[1] < m.shape[1] and m[q] and not lab[q]: lab[q] = n; dq.append(q)
            if best is None or cnt > best[1]: best = (n, cnt)
Bm = lab == best[0]; cols = np.nonzero(Bm.any(0))[0]; Rtsn = np.hypot(65.0-42.0, 267.4-242.7)
ru = np.array([y0+np.nonzero(Bm[:, c])[0].min() for c in cols]); rl = np.array([y0+np.nonzero(Bm[:, c])[0].max() for c in cols])
print('REF blob: x %d..%d (length %.2f x tip-sn), upper-boundary rows front->back: %s' % (x0+cols[0], x0+cols[-1], (cols[-1]-cols[0])/Rtsn, ' '.join('%.0f' % v for v in ru[::3])))
print('          lower-boundary rows: %s | max opening height %.2f x tip-sn' % (' '.join('%.0f' % v for v in rl[::3]), (rl-ru).max()/Rtsn))
for lb, p in H:
    X = np.load(p); S = X[:NS]; NN = skin_normals(X); x = S[:, 0]-MX; Pp = project(C, S)
    side = -1.0   # camera side (silhouette sources were at negative x offsets)
    tipi = np.argmax(S[:, 1]*((np.abs(x) < 0.3) & (S[:, 2] > 158.0) & (S[:, 2] < 159.6))); sni = None
    rim, col = [], []
    for y in np.arange(15.0, 12.4, -0.1):
        q = (x*side > RB0) & (x*side < RB1) & (np.abs(S[:, 1]-y) < 0.05) & (S[:, 2] > 157.3) & (S[:, 2] < 159.2) & (NN[:, 2] < -0.3)
        if q.any(): i = np.nonzero(q)[0][np.argmin(S[q, 2])]; rim.append((y, Pp[i, 0], Pp[i, 1], S[i, 2]))
        q = (np.abs(x) < 0.35) & (np.abs(S[:, 1]-y) < 0.05) & (S[:, 2] > 157.2) & (S[:, 2] < 159.2) & (NN[:, 2] < -0.3)
        if q.any(): i = np.nonzero(q)[0][np.argmin(S[q, 2])]; col.append((y, Pp[i, 0], Pp[i, 1], S[i, 2]))
    rim = np.array(rim); col = np.array(col)
    snq = (np.abs(x) < 0.2) & (S[:, 2] > 157.2) & (S[:, 2] < 157.8) & (S[:, 1] > 12.8); sn = Pp[snq][np.argmax(Pp[snq][:, 0])] if snq.any() else Pp[tipi]
    tsn = np.hypot(*(Pp[tipi]-sn))
    # opening: per panel column, rim row vs columella row (interpolated)
    ou = np.linspace(max(rim[:, 1].min(), col[:, 1].min()), min(rim[:, 1].max(), col[:, 1].max()), 12)
    rr = np.interp(ou, rim[np.argsort(rim[:, 1]), 1], rim[np.argsort(rim[:, 1]), 2]); cr = np.interp(ou, col[np.argsort(col[:, 1]), 1], col[np.argsort(col[:, 1]), 2])
    op = cr-rr; vis = op > 0.3
    print('%-6s rim rows (front->back by panel x): %s' % (lb, ' '.join('%.1f' % v for v in rr)))
    print('       col rows                        : %s' % ' '.join('%.1f' % v for v in cr))
    print('       opening (col-rim, px)           : %s | visible length %.2f x tip-sn, max height %.2f x tip-sn' % (' '.join('%+.1f' % v for v in op), (ou[vis].max()-ou[vis].min())/tsn if vis.sum() > 1 else 0, op.max()/tsn))
