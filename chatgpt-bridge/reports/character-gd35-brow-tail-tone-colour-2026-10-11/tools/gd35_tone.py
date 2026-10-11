"""GD34 brow tone along the brow (user: 'renk farki var gibi'): front view, 2x panel frame, hair hidden. Per column the brow core band is found
as in gd16_browref / gd33_browmeasure (darker than skin x RATIO, core > 0.45 x peak); the columns are split into medial head (first 20 % of
the brow from the nose), body (20-75 %) and tail (last 25 %). Per segment: darkness = 1 - brow core luminance / local skin luminance, and the
core colour as R/G and B/G ratios (warm-red vs neutral-brown). Windows include the temple tails.
usage: blender -b --factory-startup --python gd34_tone.py -- <out.json> label=image ... (image 'REF' = reference)"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'GD13_Identity_20261009', 'tools')); import gd13_img as gi; from gd13_common import ROOT
a = sys.argv[sys.argv.index('--')+1:]; OUT = a[0]; ITEMS = [x.split('=', 1) for x in a[1:]]; RT = 0.82; PK = 0.45; Y0, Y1 = 330, 405
SIDES = {'imgL': (322, 486, 'desc'), 'imgR': (556, 722, 'asc')}   # medial end: imgL = high columns, imgR = low columns
def load(p):
    if p == 'REF': R = gi.load(f'{ROOT}/SourceAssets/Characters/GD13_IdentityMaster_20261009/references/GD13_REF_panel_front.png'); return gi.resize(R, R.shape[1]*2, R.shape[0]*2)
    return gi.load(p)
res = {}
for lab, p in ITEMS:
    I = load(p)[..., :3]; L = I @ np.array([0.30, 0.59, 0.11]); out = {}
    for side, (c0, c1, order) in SIDES.items():
        rows = []
        for c in range(c0, c1):
            col = L[Y0-30:Y1+10, c-1:c+2].mean(1); sk = np.percentile(col, 85); w = col[30:30+(Y1-Y0)]; d = (sk*RT-w).clip(0)
            if d.max() <= 0.01: continue
            core = np.nonzero(d > PK*d.max())[0]
            if len(core) < 3: continue
            rs = slice(Y0+core[0], Y0+core[-1]+1); rgb = I[rs, c].mean(0); lum = L[rs, c].mean()
            rows.append([c, 1-lum/sk, rgb[0]/max(rgb[1], 1e-4), rgb[2]/max(rgb[1], 1e-4)])
        A = np.array(rows); A = A[np.argsort(A[:, 0])] if order == 'asc' else A[np.argsort(-A[:, 0])]   # medial -> lateral
        n = len(A); seg = {'head': A[:int(0.2*n)], 'body': A[int(0.2*n):int(0.75*n)], 'tail': A[int(0.75*n):]}
        out[side] = {k: {'dark': round(float(v[:, 1].mean()), 3), 'R/G': round(float(v[:, 2].mean()), 3), 'B/G': round(float(v[:, 3].mean()), 3)} for k, v in seg.items()}
        out[side]['tail_minus_body_dark'] = round(out[side]['tail']['dark']-out[side]['body']['dark'], 3); out[side]['head_minus_body_dark'] = round(out[side]['head']['dark']-out[side]['body']['dark'], 3)
    res[lab] = out
json.dump(res, open(OUT, 'w'), indent=1)
for lab, out in res.items():
    for s in SIDES:
        o = out[s]; print('TONE %-7s %s ' % (lab, s) + ' | '.join('%s dark %.3f R/G %.2f B/G %.2f' % (k, o[k]['dark'], o[k]['R/G'], o[k]['B/G']) for k in ('head', 'body', 'tail')) + ' | tail-body %+.3f head-body %+.3f' % (o['tail_minus_body_dark'], o['head_minus_body_dark']))
