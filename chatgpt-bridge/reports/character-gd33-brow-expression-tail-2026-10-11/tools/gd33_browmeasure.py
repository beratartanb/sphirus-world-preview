"""GD33 brow / eye measurement on the 2x front panel frame (reference panel resized 2x, UE captures already warped onto that frame by the
solved front camera). Brow band per column = the GD16 gd16_browref.py method (local skin level = 85th percentile, brow = darker than
skin*RATIO, largest dark run, core = darker than PK x peak, darkness-weighted centre; outlier rejection + light smoothing). Pupil = darkest
5x5 mean inside each eye window. Reports per brow: medial / apex / lateral centre rows, the medial-head slope (medial row - apex row; > 0 =
the inner head sits LOWER than the arch = frowning read), thickness (medial / body / tail), darkness, brow-to-pupil distance (centre row at
the pupil column and at the medial head), inter-brow gap. 1 px = about 0.08 mm at the front camera (2x frame). Also a check image.
usage: blender -b --factory-startup --python gd33_browmeasure.py -- <out.json> <check.jpg> label=image[ ...] (image 'REF' = reference)"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'GD13_Identity_20261009', 'tools')); import gd13_img as gi; from gd13_common import ROOT
a = sys.argv[sys.argv.index('--')+1:]; OUT, CHK = a[0], a[1]; ITEMS = [x.split('=', 1) for x in a[2:]]
RT = float(os.environ.get('BR_RATIO', '0.80')); PK = float(os.environ.get('BR_PK', '0.45'))
Y0, Y1 = 330, 400; SIDES = {'imgL': (362, 486), 'imgR': (556, 684)}; EYES = {'imgL': (390, 480, 380, 470), 'imgR': (560, 650, 380, 470)}   # c0, c1, r0, r1
def load(p):
    if p == 'REF':
        R = gi.load(f'{ROOT}/SourceAssets/Characters/GD13_IdentityMaster_20261009/references/GD13_REF_panel_front.png'); return gi.resize(R, R.shape[1]*2, R.shape[0]*2)
    return gi.load(p)
def brow(L, c0, c1):
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
        dd = (sk-w[i:j]).clip(0); core = np.nonzero(dd > PK*dd.max())[0]; i2, j2 = i+core[0], i+core[-1]+1
        dd2 = (sk-w[i2:j2]).clip(0); cen = Y0+i2+float((np.arange(j2-i2)*dd2).sum()/dd2.sum())
        rows.append([c, Y0+i2, cen, Y0+j2, float(dd2.mean()/sk)])
    A = np.array(rows, float); keep = np.ones(len(A), bool)
    for k in range(len(A)):
        nb = A[max(0, k-6):k+7]; med = np.median(nb[:, 2]); th = np.median(nb[:, 3]-nb[:, 1])
        if abs(A[k, 2]-med) > 4 or (A[k, 3]-A[k, 1]) > th*1.6+3: keep[k] = False
    A = A[keep]
    for j_ in (1, 2, 3): A[:, j_] = np.convolve(np.pad(A[:, j_], 3, mode='edge'), np.ones(7)/7, 'valid')
    return A
def pupil(L, c0, c1, r0, r1):
    W = L[r0:r1, c0:c1]; k = np.ones(5)/5; B = np.apply_along_axis(lambda v: np.convolve(v, k, 'same'), 0, W); B = np.apply_along_axis(lambda v: np.convolve(v, k, 'same'), 1, B)
    B[:3] = B[-3:] = 9; B[:, :3] = B[:, -3:] = 9; r, c = np.unravel_index(np.argmin(B), B.shape); return c0+c, r0+r
res = {}; tiles = []
for lab, p in ITEMS:
    I = load(p); L = I[..., :3] @ np.array([0.30, 0.59, 0.11]); out = {}
    for side, (c0, c1) in SIDES.items():
        A = brow(L, c0, c1); med_first = (side == 'imgR')   # imgR: medial end = low columns; imgL: medial end = high columns
        Am = A[:8] if med_first else A[-8:]; Al = A[-8:] if med_first else A[:8]
        px, py = pupil(L, *EYES[side]); ip = np.argmin(np.abs(A[:, 0]-px))
        out[side] = {'cols': [int(A[0, 0]), int(A[-1, 0])], 'medial_row': round(float(Am[:, 2].mean()), 1), 'apex_row': round(float(A[:, 2].min()), 1), 'apex_col': int(A[np.argmin(A[:, 2]), 0]),
                     'lateral_row': round(float(Al[:, 2].mean()), 1), 'medial_minus_apex': round(float(Am[:, 2].mean()-A[:, 2].min()), 1),
                     'thick_medial': round(float((Am[:, 3]-Am[:, 1]).mean()), 1), 'thick_body': round(float(np.median(A[:, 3]-A[:, 1])), 1), 'thick_tail': round(float((Al[:, 3]-Al[:, 1]).mean()), 1),
                     'darkness': round(float(A[:, 4].mean()), 3), 'darkness_medial': round(float(Am[:, 4].mean()), 3), 'pupil': [int(px), int(py)],
                     'brow_to_pupil_at_pupil': round(float(py-A[ip, 2]), 1), 'brow_to_pupil_medial': round(float(py-Am[:, 2].mean()), 1), 'bottom_to_pupil_at_pupil': round(float(py-A[ip, 3]), 1),
                     'curve': A[:, :4].round(1).tolist()}
    out['gap_px'] = int(min(r[0] for r in out['imgR']['curve']) - max(r[0] for r in out['imgL']['curve']))
    res[lab] = out
    T = I[300:480, 340:700].copy(); S = 3; T = gi.resize(T, T.shape[1]*S, T.shape[0]*S)
    for side in SIDES:
        for c, t, m, b in out[side]['curve']:
            for y, colr in ((t, (0.2, 1, 1)), (m, (1, 1, 0.2)), (b, (1, 0.3, 1))):
                X_, Y_ = int((c-340)*S), int((y-300)*S)
                if 0 <= X_ < T.shape[1]-2 and 0 <= Y_ < T.shape[0]-2: T[Y_:Y_+2, X_:X_+2, :3] = colr
        px, py = out[side]['pupil']; X_, Y_ = int((px-340)*S), int((py-300)*S); T[max(Y_-4, 0):Y_+5, max(X_-4, 0):X_+5, :3] = (1, 0.1, 0.1)
    tiles.append(T)
gi.save(CHK, np.concatenate(tiles, 0))
json.dump(res, open(OUT, 'w'), indent=1)
for lab, out in res.items():
    for side in SIDES:
        o = out[side]; print('BROW %-10s %s medial %.1f apex %.1f lateral %.1f | med-apex %+.1f | thick %.1f/%.1f/%.1f | dark %.3f (med %.3f) | brow->pupil %.1f (medial %.1f, lower edge %.1f) | gap %d' % (
            lab, side, o['medial_row'], o['apex_row'], o['lateral_row'], o['medial_minus_apex'], o['thick_medial'], o['thick_body'], o['thick_tail'], o['darkness'], o['darkness_medial'],
            o['brow_to_pupil_at_pupil'], o['brow_to_pupil_medial'], o['bottom_to_pupil_at_pupil'], out['gap_px']))
