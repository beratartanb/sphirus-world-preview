"""GD44: silhouette profiles of the user's body reference sheet (5 views, 1500x844; local-only reference). Figure = luminance above a
threshold over the dark studio background (floor shadow excluded below the soles). For a figure column window: per row the run that contains
the figure's body axis (front/back: torso centre run; side: the run spanning the body axis), giving left/right (front/back) or front/back
(side) contour x. Rows are normalised by the figure height (top of head = 0, sole = 1). Writes JSON + a check image.
usage: blender -b --factory-startup --python gd44_refsil.py -- <sheet.jpg> <out.json> <check.png> name:x0:x1[:axis_x] ..."""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; I = gi.load(a[0])[..., :3]; OUT, CHK = a[1], a[2]
TH = float(os.environ.get('RS_TH', '0.20'))
L = I @ np.array([0.30, 0.59, 0.11]); H, W = L.shape
if np.median(L[:20]) > np.median(L[-20:]) and False: L = L[::-1]
res = {}; C = I.copy()
for spec in a[3:]:
    p = spec.split(':'); name, x0, x1 = p[0], int(p[1]), int(p[2]); M = L[:, x0:x1] > TH
    GAP = int(os.environ.get('RS_GAP', '8'))
    for r in range(M.shape[0]):   # close dark crease gaps inside the figure (spine groove, glute fold) up to GAP px
        c = np.nonzero(M[r])[0]
        if len(c) > 1:
            g = np.nonzero((np.diff(c) > 1) & (np.diff(c) <= GAP+1))[0]
            for k in g: M[r, c[k]:c[k+1]] = True
    rows = np.nonzero(M.sum(1) > 2)[0]
    # vertical extent: top = first row with figure pixels; sole = last row before the floor (rows with a wide flat shadow are dark anyway)
    top, bot = int(rows.min()), int(rows.max()); hgt = bot-top
    axis = float(p[3]) if len(p) > 3 else None
    if axis is None:   # body axis = median centre of the rows between 35 % and 55 % of the height (torso)
        cs = []
        for r in range(top+int(0.35*hgt), top+int(0.55*hgt)):
            c = np.nonzero(M[r])[0]
            if len(c): cs.append(0.5*(c.min()+c.max()))
        axis = float(np.median(cs))+x0
    prof = []
    for r in range(top, bot+1):
        c = np.nonzero(M[r])[0]
        if not len(c): prof.append(None); continue
        runs = np.split(c, np.nonzero(np.diff(c) > 1)[0]+1); ax_ = axis-x0
        best = min(runs, key=lambda q: 0 if q[0] <= ax_ <= q[-1] else min(abs(q[0]-ax_), abs(q[-1]-ax_)))
        prof.append([int(best[0]+x0), int(best[-1]+x0)])
        C[r, best[0]+x0] = (1, 0, 0); C[r, best[-1]+x0] = (0, 1, 1)
    res[name] = {'x0': x0, 'x1': x1, 'top': top, 'bottom': bot, 'height_px': hgt, 'axis_x': axis, 'rows': prof}
    C[top, x0:x1] = (1, 1, 0); C[bot, x0:x1] = (1, 1, 0)
gi.save(CHK, C); json.dump(res, open(OUT, 'w'))
for k, v in res.items():
    hp = v['height_px']; out = []
    for f in (0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.70, 0.80, 0.90):
        r = v['rows'][int(f*hp)]
        out.append('%.2f:%s' % (f, '-' if r is None else '%.3f' % ((r[1]-r[0])/hp)))
    print('REFSIL %-8s top %d bottom %d height %d axis %.1f | width/height at rows: %s' % (k, v['top'], v['bottom'], hp, v['axis_x'], ' '.join(out)))
