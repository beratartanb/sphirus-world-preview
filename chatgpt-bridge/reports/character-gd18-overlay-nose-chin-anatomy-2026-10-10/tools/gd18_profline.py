"""GD18 nose profile lines: the reference profile edge (automatic skin-key contour of the user's prof_faceL panel, the same 'prof_front' rows the
GD13 fit uses) and each candidate's projected profile edge (outermost model vertex per row in the FIXED solved profile camera, from a
gd13_fit.py iters-0 dump) drawn on the reference panel, zoomed. Anatomical points are located on the REFERENCE curve itself:
nasion = most posterior point between brow and dorsum, pronasale = most anterior point of the tip, subnasale = most posterior point
below the tip, dorsal hump / rhinion = most anterior dorsum point above the supratip, supratip = most posterior point between hump and tip.
Also writes per-row residuals (px, + = model in FRONT of the reference) in anatomical bands. Profile panel ~14 px/cm (1 px ~ 0.71 mm);
the panel is ~9 % smaller than front and its neck pose differs - read the nose band, not the lip/chin bands, as shape evidence.
usage: blender -b --python gd18_profline.py -- <ref panel png> <out.jpg> <out.json> <label=dumpF.json> [label=dumpF.json ...]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'GD13_Identity_20261009', 'tools')); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; R = gi.load(a[0]); OUT, OJ = a[1], a[2]; CANDS = [x.split('=', 1) for x in a[3:]]
COL = [(1.0, 0.2, 0.9), (0.1, 0.95, 1.0), (0.3, 1.0, 0.3), (1.0, 0.6, 0.1)]
def rows_of(path):
    D = json.load(open(path)); out = {}
    for d in D.get('prof_faceL', []):
        if d[0] == 'prof_front': out[round(d[1][1]*2)/2] = (np.array(d[1]), np.array(d[2]), d[3])
    return out
C = {lab: rows_of(p) for lab, p in CANDS}; any_ = next(iter(C.values()))
ys = np.array(sorted(y for y in any_ if 140 <= y <= 300)); RX = np.array([any_[y][0][0] for y in ys])   # reference edge x per row (face looks to -x)
def amax(lo, hi, f):
    m = (ys >= lo) & (ys <= hi); i = np.nonzero(m)[0]; return int(i[np.argmax(f(RX[i]))])
i_nas = amax(176, 205, lambda x: x); i_tip = amax(236, 262, lambda x: -x); i_sub = amax(ys[i_tip]+2, 285, lambda x: x)
i_hump = amax(ys[i_nas]+4, ys[i_tip]-8, lambda x: -x - 0.08*(np.arange(len(x)))*0)   # most anterior dorsum point
i_supra = amax(ys[i_hump]+1, ys[i_tip]-1, lambda x: x) if ys[i_tip]-ys[i_hump] > 3 else i_hump
LM = {'nasion': i_nas, 'dorsal_hump_rhinion': i_hump, 'supratip': i_supra, 'pronasale_tip': i_tip, 'subnasale': i_sub}
# dorsal convexity: max anterior deviation of the dorsum from the nasion->tip chord (px; + = convex hump)
def convex(X):
    y0, y1 = ys[i_nas], ys[i_tip]; m = (ys >= y0) & (ys <= y1); x0, x1 = X[i_nas], X[i_tip]
    chord = x0+(x1-x0)*(ys[m]-y0)/(y1-y0); return float(np.max(chord-X[m]))
res = {'landmarks_ref_px': {k: [float(RX[i]), float(ys[i])] for k, i in LM.items()}, 'ref_dorsal_convexity_px': round(convex(RX), 2), 'cands': {}}
BANDS = {'radix_nasion': (ys[i_nas]-8, ys[i_nas]+6), 'upper_dorsum': (ys[i_nas]+6, ys[i_hump]+2), 'lower_dorsum_supratip': (ys[i_hump]+2, ys[i_tip]-3),
         'tip': (ys[i_tip]-3, ys[i_tip]+5), 'columella_subnasale': (ys[i_tip]+5, ys[i_sub]+2)}
for lab, rows in C.items():
    r = {}
    for b, (lo, hi) in BANDS.items():
        v = [rows[y][2] for y in rows if lo <= y <= hi]; r[b] = [round(float(np.mean(v)), 2), round(float(np.sqrt(np.mean(np.square(v)))), 2), len(v)] if v else None
    MX = np.array([rows[y][1][0] if y in rows else np.nan for y in ys]); r['dorsal_convexity_px'] = round(convex(MX), 2) if not np.isnan(MX[[i_nas, i_tip]]).any() else None
    res['cands'][lab] = r
json.dump(res, open(OJ, 'w'), indent=1)
# ---- drawing: crop around the nose, x4
x0, x1, y0, y1 = int(RX.min())-40, int(RX.min())+110, 150, 300; S = 4
T = R[y0:y1, x0:x1].copy(); T = gi.resize(T, (x1-x0)*S, (y1-y0)*S); T[..., :3] *= 0.85
def dot(img, x, y, col, r=2):
    X_, Y_ = int(round((x-x0)*S)), int(round((y-y0)*S))
    if not (r <= Y_ < img.shape[0]-r and r <= X_ < img.shape[1]-r): return   # 2026-10-10 fix: points outside the crop made negative slices (full-height bars)
    img[Y_-r:Y_+r+1, X_-r:X_+r+1, :3] = col
def poly(img, P, col, r=2):
    for (xa, ya), (xb, yb) in zip(P[:-1], P[1:]):
        n = int(max(abs(xb-xa), abs(yb-ya))*S)+1
        for t in np.linspace(0, 1, n): dot(img, xa+(xb-xa)*t, ya+(yb-ya)*t, col, r)
poly(T, [(any_[y][0][0], y) for y in ys], (1.0, 0.92, 0.2), 2)
for k, (lab, rows) in enumerate(C.items()):
    yy = [y for y in ys if y in rows]; poly(T, [(rows[y][1][0], y) for y in yy], COL[k % len(COL)], 1)
for k, i in LM.items():
    for d in range(-6, 7): dot(T, RX[i]-3+d*0.5, ys[i], (1, 1, 1), 1)
gi.save(OUT, T); print('PROFLINE_OK', json.dumps(res['landmarks_ref_px']), 'ref convexity', res['ref_dorsal_convexity_px'])
for lab, r in res['cands'].items(): print('PROFLINE', lab, json.dumps(r))
