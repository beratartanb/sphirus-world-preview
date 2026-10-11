"""GD38 brow-head gap measurement in the front 2x panel frame (reference resized 2x; UE captures warped by the solved front camera).
Brow pixels = luminance below BD x the skin level (median of the band between the brows and the upper lids). For each image side the brow head
= the medial-most column (counted from the frame midline = mean of the two iris centres given) where the column holds >= NMIN brow pixels in the
brow band; also the tail end (lateral-most such column) and the mean brow row (centroid) per 10-column bin. All in 2x frame px (~0.32 mm).
usage: blender -b --factory-startup --python gd38_browgap.py -- <out.json> <check.png> <midcol> label=image ...   (REF = reference panel)"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'GD13_Identity_20261009', 'tools')); import gd13_img as gi; from gd13_common import ROOT
a = sys.argv[sys.argv.index('--')+1:]; OUT, CHK, MID = a[0], a[1], float(a[2]); ITEMS = [x.split('=', 1) for x in a[3:]]
BD = float(os.environ.get('BG_BD', '0.72')); NMIN = int(os.environ.get('BG_NMIN', '3')); R0, R1 = int(os.environ.get('BG_R0', '330')), int(os.environ.get('BG_R1', '410')); C0, C1 = int(os.environ.get("BG_C0", "300")), int(os.environ.get("BG_C1", "740"))
def load(p):
    if p == 'REF': I = gi.load(f'{ROOT}/SourceAssets/Characters/GD13_IdentityMaster_20261009/references/GD13_REF_panel_front.png'); return gi.resize(I, I.shape[1]*2, I.shape[0]*2)
    return gi.load(p)
res = {}; tiles = []
for lab, p in ITEMS:
    I = load(p)[..., :3]; Ht = I.shape[0]; L = I @ np.array([0.30, 0.59, 0.11])
    Iv = I   # gi.load rows are top-down in the frame (same indexing as gd33_gridzoom)
    skin = np.median(L[R1+5:R1+25, int(MID)-40:int(MID)+40]); B = L[R0:R1, C0:C1] < BD*skin
    cnt = B.sum(0); cols = np.arange(C0, C1); o = {'skin': round(float(skin), 3)}
    for side, sel in (('imgL', cols < MID), ('imgR', cols > MID)):
        c = cols[sel & (cnt >= NMIN)]
        if not len(c): continue
        if side == 'imgL': head, tail = int(c.max()), int(c.min())
        else: head, tail = int(c.min()), int(c.max())
        o[side] = {'head_col': head, 'tail_col': tail, 'head_off': round(abs(head-MID), 1), 'tail_off': round(abs(tail-MID), 1)}
        prof = []
        for c0 in range(min(head, tail), max(head, tail), 10):
            m = B[:, c0-C0:c0-C0+10]
            if m.sum() > 5: rr = np.nonzero(m)[0]; prof.append([c0+5, round(float(R0+rr.mean()), 1), int(rr.max()-rr.min()+1)])
        o[side]['profile'] = prof
    if 'imgL' in o and 'imgR' in o: o['gap_px'] = o['imgR']['head_col']-o['imgL']['head_col']
    res[lab] = o
    T = Iv[R0-20:R1+30, C0:C1].copy(); T[20:-30][B] = T[20:-30][B]*0.4+np.array([1, 0, 1])*0.6
    for side in ('imgL', 'imgR'):
        if side in o: T[:, o[side]['head_col']-C0] = (0, 1, 1); T[:, o[side]['tail_col']-C0] = (1, 1, 0)
    T[:, int(MID)-C0] = (1, 1, 1); tiles.append(T)
gi.save(CHK, np.concatenate(tiles, 0)); json.dump(res, open(OUT, 'w'), indent=1)
for lab, o in res.items():
    print('BROWGAP %-8s gap %s | imgL head off %s tail off %s | imgR head off %s tail off %s' % (lab, o.get('gap_px'), o.get('imgL', {}).get('head_off'), o.get('imgL', {}).get('tail_off'), o.get('imgR', {}).get('head_off'), o.get('imgR', {}).get('tail_off')))
