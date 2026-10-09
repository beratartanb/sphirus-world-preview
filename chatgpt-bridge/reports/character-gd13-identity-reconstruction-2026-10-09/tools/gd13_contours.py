"""GD13: automatic reference contours from the 6-view sheet panels (panel-original px), by a skin classifier with run-length strand rejection.
  prof_faceL : 'prof_front'   leftmost skin run per row (forehead below the hairline -> brow -> nose -> lips -> chin), rows Y0..Y1
               'prof_under'   per column, the skin -> background transition below the chin (under-chin line), cols X0..X1
  q3_faceR   : 'far_R'        rightmost skin run per row (far cheek / nose / lips / chin against the background)
  q3_faceL   : 'far_L'        leftmost skin run per row
  front      : 'cheek_imgL' / 'cheek_imgR'  outermost skin run per row on each side (cheek / jaw contour against hair / background)
Row / column ranges come from a json {view: {name: [a, b]}}. Writes contours json {view: {name: [[x, y], ...]}} + a check image.
usage: blender -b --factory-startup --python gd13_contours.py -- <panel dir> <ranges.json> <out.json> <check.jpg>"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; PD, RG, OUT, CHK = a[0], json.load(open(a[1])), a[2], a[3]
def skin(I):
    r, g, b = I[..., 0], I[..., 1], I[..., 2]; return (r > 0.42) & (r-b > 0.13) & (r-g > 0.06) & ((r+g+b)/3 > 0.33)
def run_ok(m, i, step, n=5):
    j = i+np.arange(n)*step; j = j[(j >= 0) & (j < len(m))]; return len(j) == n and m[j].all()
out = {}; imgs = []
for v, spec in RG.items():
    I = gi.load(f'{PD}/GD13_REF_panel_{v}.png'); S = skin(I); H, W = S.shape; out[v] = {}; C = I.copy()
    for name, (lo, hi) in spec.items():
        pts = []
        if name in ('prof_front', 'far_L', 'cheek_imgL'):
            for y in range(lo, hi+1):
                x0 = 0 if name != 'cheek_imgL' else 60
                xs = [x for x in range(x0, W//2+120) if S[y, x] and run_ok(S[y], x, 1, 6)]
                if xs: pts.append([xs[0]+0.5, y+0.5])
        elif name in ('far_R', 'cheek_imgR'):
            for y in range(lo, hi+1):
                x1 = W-1 if name != 'cheek_imgR' else W-60
                xs = [x for x in range(x1, W//2-120, -1) if S[y, x] and run_ok(S[y], x, -1, 6)]
                if xs: pts.append([xs[0]+0.5, y+0.5])
        elif name == 'prof_under':
            for x in range(lo, hi+1):
                col = S[:, x]; ys = [y for y in range(300, H-5) if col[y] and run_ok(col, y, -1, 6) and not col[y+1:y+4].any()]
                if ys: pts.append([x+0.5, ys[0]+0.5])
        out[v][name] = pts
        for p in pts: C[int(p[1]), max(int(p[0])-1, 0):int(p[0])+2, :3] = [1, 0, 1]
    imgs.append(gi.resize(C, 483, 545))
json.dump(out, open(OUT, 'w'), indent=0); gi.save(CHK, np.concatenate([gi.resize(x, 483*2, 545*2) for x in imgs], 1)); print('CONTOURS_OK', {v: {k: len(p) for k, p in d.items()} for v, d in out.items()})
