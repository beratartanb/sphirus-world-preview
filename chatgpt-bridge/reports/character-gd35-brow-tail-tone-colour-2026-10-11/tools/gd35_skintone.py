"""GD35 skin tone patches on the 2x front panel frame (reference resized 2x, UE captures warped by the solved front camera): forehead, left /
right cheek, chin, neck. Per patch the median colour (robust to freckles / speculars: pixels between the 20th and 80th luminance percentile),
reported as luminance, R/G, B/G and HSV saturation; the mean over the face patches is the skin tone summary. Writes a patch check image.
usage: blender -b --factory-startup --python gd35_skintone.py -- <out.json> <check.jpg> label=image ..."""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'GD13_Identity_20261009', 'tools')); import gd13_img as gi; from gd13_common import ROOT
a = sys.argv[sys.argv.index('--')+1:]; OUT, CHK = a[0], a[1]; ITEMS = [x.split('=', 1) for x in a[2:]]
PATCH = {'forehead': (450, 600, 285, 325), 'cheekL': (350, 410, 500, 565), 'cheekR': (620, 680, 500, 565), 'undereyeL': (390, 450, 470, 500), 'undereyeR': (600, 660, 470, 500), 'nose': (505, 545, 470, 530), 'neck': (440, 600, 900, 960)}
def load(p):
    if p == 'REF': R = gi.load(f'{ROOT}/SourceAssets/Characters/GD13_IdentityMaster_20261009/references/GD13_REF_panel_front.png'); return gi.resize(R, R.shape[1]*2, R.shape[0]*2)
    return gi.load(p)
res = {}; tiles = []
for lab, p in ITEMS:
    I = load(p)[..., :3]; out = {}
    for k, (c0, c1, r0, r1) in PATCH.items():
        P = I[r0:r1, c0:c1].reshape(-1, 3); L = P @ np.array([0.30, 0.59, 0.11]); lo, hi = np.percentile(L, [20, 80]); Q = P[(L >= lo) & (L <= hi)]
        m = np.median(Q, 0); mx, mn = m.max(), m.min()
        out[k] = {'lum': round(float(m @ np.array([0.30, 0.59, 0.11])), 4), 'R/G': round(float(m[0]/m[1]), 3), 'B/G': round(float(m[2]/m[1]), 3), 'sat': round(float((mx-mn)/max(mx, 1e-4)), 3), 'rgb': [round(float(v), 4) for v in m]}
    face = [out[k] for k in ('forehead', 'cheekL', 'cheekR', 'undereyeL', 'undereyeR', 'nose')]
    out['face_mean'] = {q: round(float(np.mean([f[q] for f in face])), 3) for q in ('lum', 'R/G', 'B/G', 'sat')}
    res[lab] = out
    T = I[220:1000, 280:760].copy()
    for k, (c0, c1, r0, r1) in PATCH.items():
        T[r0-220:r1-220, c0-280:c0-278] = (1, 0, 0); T[r0-220:r1-220, c1-282:c1-280] = (1, 0, 0); T[r0-220:r0-218, c0-280:c1-280] = (1, 0, 0); T[r1-222:r1-220, c0-280:c1-280] = (1, 0, 0)
    tiles.append(gi.resize(T, T.shape[1]//2, T.shape[0]//2))
gi.save(CHK, np.concatenate(tiles, 1)); json.dump(res, open(OUT, 'w'), indent=1)
for lab, out in res.items():
    print('SKIN %-8s face lum %.3f R/G %.3f B/G %.3f sat %.3f | ' % (lab, *(out['face_mean'][q] for q in ('lum', 'R/G', 'B/G', 'sat'))) + ' '.join('%s %.2f/%.2f' % (k, out[k]['R/G'], out[k]['B/G']) for k in PATCH))
