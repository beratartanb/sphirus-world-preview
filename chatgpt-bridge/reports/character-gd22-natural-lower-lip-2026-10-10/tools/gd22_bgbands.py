"""GD22 background-key profile bands: ref silhouette (first non-background run per row of the prof_faceL panel, 1x px) vs candidate alpha renders
(solved profile camera, 2x). Residual = ref_x - cand_x (+ = model in front, ~0.71 mm/px), CALIBRATED by the mean residual of the first candidate over
rows 200-235 (nasal dorsum, where the skin-key and the eye agree) so edge-detection bias cancels. Prints band means and writes per-row json.
usage: -- <ref panel png> <out json> label=alpha.png [label2=...]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; R = gi.load(a[0]); OUT = a[1]; C = {}
for s in a[2:]:
    lab, p = s.split('=', 1); C[lab] = gi.load(p)[..., 3] > 0.5
def ref_edge(y):
    row = R[y, :, :3]; bg = np.median(row[:30], 0); d = np.abs(row-bg).max(1); idx = np.nonzero(d > 0.10)[0]
    for i in idx:
        if i+6 < row.shape[0] and (d[i:i+6] > 0.10).all(): return i+0.5
    return None
def cand_edge(al, y):
    rows = al[2*y:2*y+2]; cols = np.nonzero(rows.any(0))[0]; return cols.min()/2.0 if cols.size else None
rows = range(140, 362); REF = {y: ref_edge(y) for y in rows}; RES = {k: {} for k in C}
for k, al in C.items():
    for y in rows:
        rx = REF[y]; cx = cand_edge(al, y)
        if rx is not None and cx is not None: RES[k][y] = rx-cx
k0 = list(C)[0]; cal = np.mean([RES[k0][y] for y in range(200, 236) if y in RES[k0]]); print('CALIBRATION offset (rows 200-235, %s): %+.2f px -> subtracted from every residual' % (k0, cal))
BANDS = [('forehead', 140, 170), ('radix_nasion', 184, 206), ('dorsum', 207, 232), ('tip', 233, 246), ('infratip_columella', 247, 262), ('subnasale', 263, 272), ('upper_lip_philtrum', 273, 290), ('upper_vermilion', 291, 296), ('lower_lip', 297, 306), ('sulcus_shelf', 307, 322), ('pad_top', 323, 331), ('pad_mid', 332, 340), ('pad_low', 341, 349), ('pad_bottom', 350, 353)]
print('band (rows)              ' + ' | '.join('%-14s' % k for k in C))
for nm, y0, y1 in BANDS:
    cells = []
    for k in C:
        v = [RES[k][y]-cal for y in range(y0, y1+1) if y in RES[k]]; cells.append('%+5.2f (%+5.1f..%+5.1f)' % (np.mean(v), min(v), max(v)) if v else '   .   ')
    print('%-18s %3d-%3d ' % (nm, y0, y1) + ' | '.join('%-20s' % c for c in cells))
json.dump({'calibration_px': float(cal), 'ref_x': {y: REF[y] for y in rows if REF[y] is not None}, 'residual_px_calibrated': {k: {y: float(v-cal) for y, v in RES[k].items()} for k in C}}, open(OUT, 'w'))
print('BGBANDS_OK', OUT)
