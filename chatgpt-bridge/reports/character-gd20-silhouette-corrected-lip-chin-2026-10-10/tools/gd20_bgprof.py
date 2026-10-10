"""GD20 background-key profile silhouette: per row of the reference prof_faceL panel (1x px) the first column from the left whose colour differs from the
row's background (median of the leftmost 30 px) by > thr; the same on candidate alpha renders made with the solved profile camera (2x -> /2).
Robust at the lips (the skin classifier of contours_auto drops the dark vermilion / mouth line). Residual = ref_x - cand_x (+ = model in front, px ~0.71 mm).
usage: -- <ref panel png> <row0> <row1> label=alpha.png [label2=alpha2.png ...]"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; R = gi.load(a[0]); r0, r1 = int(a[1]), int(a[2]); C = {}
for s in a[3:]:
    lab, p = s.split('=', 1); A = gi.load(p); al = A[..., 3] > 0.5; C[lab] = al
def ref_edge(y):
    row = R[y, :, :3]; bg = np.median(row[:30], 0); d = np.abs(row-bg).max(1); idx = np.nonzero(d > 0.10)[0]
    # skip hair strands: require a run of >= 6 face px
    for i in idx:
        if i+6 < row.shape[0] and (d[i:i+6] > 0.10).all(): return i+0.5
    return None
def cand_edge(al, y):
    rows = al[2*y:2*y+2]; cols = np.nonzero(rows.any(0))[0]; return cols.min()/2.0 if cols.size else None
print('row | ref x | ' + ' | '.join('%s x  res' % k for k in C))
for y in range(r0, r1):
    rx = ref_edge(y); out = []
    for k, al in C.items():
        cx = cand_edge(al, y); out.append('%5.1f %+5.2f' % (cx, rx-cx) if (cx is not None and rx is not None) else '   .     . ')
    print('%4d | %5.1f | %s' % (y, rx if rx is not None else float('nan'), ' | '.join(out)))
