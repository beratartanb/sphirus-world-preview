"""GD33 eye-opening measure on the 2x front panel frame (reference panel resized 2x; UE captures warped onto the same frame, hair hidden).
Per eye window: skin level = 85th percentile luminance. Sclera = desaturated (HSV s < SAT) and bright (lum > SCL x skin) pixels; iris+pupil =
pixels darker than IRI x skin inside the sclera's horizontal extent; the visible eye = sclera | iris, largest connected blob. Reports the
visible-eye area, its height at the iris centre column (vertical opening) and the iris height (rows of iris pixels in the 5 centre columns)
relative to the eye width (the scale-free openness = height / width). Writes a mask check image.
usage: blender -b --factory-startup --python gd33_eyeopen.py -- <out.json> <check.jpg> label=image[ ...] (image 'REF' = reference)"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'GD13_Identity_20261009', 'tools')); import gd13_img as gi; from gd13_common import ROOT
a = sys.argv[sys.argv.index('--')+1:]; OUT, CHK = a[0], a[1]; ITEMS = [x.split('=', 1) for x in a[2:]]
SAT = float(os.environ.get('EO_SAT', '0.30')); SCL = float(os.environ.get('EO_SCL', '0.80')); IRI = float(os.environ.get('EO_IRI', '0.62'))
EYES = {'imgL': (370, 500, 385, 455), 'imgR': (545, 675, 385, 455)}   # c0, c1, r0, r1 (2x front frame)
def load(p):
    if p == 'REF':
        R = gi.load(f'{ROOT}/SourceAssets/Characters/GD13_IdentityMaster_20261009/references/GD13_REF_panel_front.png'); return gi.resize(R, R.shape[1]*2, R.shape[0]*2)
    return gi.load(p)
def blobs(M):
    lab = np.zeros(M.shape, int); n = 0
    for y, x in zip(*np.nonzero(M)):
        if lab[y, x]: continue
        n += 1; st = [(y, x)]; lab[y, x] = n
        while st:
            cy, cx = st.pop()
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                yy, xx = cy+dy, cx+dx
                if 0 <= yy < M.shape[0] and 0 <= xx < M.shape[1] and M[yy, xx] and not lab[yy, xx]: lab[yy, xx] = n; st.append((yy, xx))
    return lab, n
res = {}; tiles = []
for lab_, p in ITEMS:
    I = load(p)[..., :3]; L = I @ np.array([0.30, 0.59, 0.11]); mx = I.max(2); mn = I.min(2); S = np.where(mx > 1e-4, (mx-mn)/np.maximum(mx, 1e-4), 0); out = {}
    T = I[370:470, 360:690].copy()
    for side, (c0, c1, r0, r1) in EYES.items():
        Lw, Sw = L[r0:r1, c0:c1], S[r0:r1, c0:c1]; sk = np.percentile(Lw, 85)
        scl = (Sw < SAT) & (Lw > SCL*sk); cols = np.nonzero(scl.any(0))[0]
        if len(cols) == 0: out[side] = None; continue
        iris = (Lw < IRI*sk); iris[:, :cols.min()] = False; iris[:, cols.max()+1:] = False
        V = scl | iris; lb, n = blobs(V)
        if n == 0: out[side] = None; continue
        sizes = np.bincount(lb.ravel())[1:]; k = 1+int(np.argmax(sizes)); B = lb == k
        ys, xs = np.nonzero(B); w = xs.max()-xs.min()+1
        ir = iris & B; ic = int(np.median(np.nonzero(ir)[1])) if ir.any() else int(xs.mean())
        hc = [np.nonzero(B[:, c])[0] for c in range(max(ic-2, 0), min(ic+3, B.shape[1]))]; hgt = float(np.median([h.max()-h.min()+1 for h in hc if len(h)]))
        ih = [np.nonzero(ir[:, c])[0] for c in range(max(ic-2, 0), min(ic+3, B.shape[1]))]; ihgt = float(np.median([h.max()-h.min()+1 for h in ih if len(h)])) if any(len(h) for h in ih) else 0.0
        out[side] = {'area_px': int(B.sum()), 'sclera_px': int((scl & B).sum()), 'width_px': int(w), 'open_height_px': hgt, 'iris_height_px': ihgt, 'open_ratio': round(hgt/w, 3)}
        Tm = T[r0-370:r1-370, c0-360:c1-360]; Tm[B & scl] = Tm[B & scl]*0.5+np.array([0, 0.5, 0.5]); Tm[B & iris] = Tm[B & iris]*0.5+np.array([0.5, 0, 0.5])
    res[lab_] = out; tiles.append(gi.resize(T, T.shape[1]*3, T.shape[0]*3))
gi.save(CHK, np.concatenate(tiles, 0)); json.dump(res, open(OUT, 'w'), indent=1)
for lab_, out in res.items():
    print('EYEOPEN %-12s ' % lab_ + ' | '.join('%s open %.0f px / w %d = %.3f  iris h %.0f  sclera %d' % (s, o['open_height_px'], o['width_px'], o['open_ratio'], o['iris_height_px'], o['sclera_px']) if o else s+' none' for s, o in out.items()))
