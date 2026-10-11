"""GD38: brow stations (top / bottom band lines) of two brow3d json files projected with the solved front camera onto the 2x reference front
panel (crop), for the process board: old = yellow, new = cyan; midline (nasion) white.
usage: blender -b --factory-startup --python gd38_browplot.py -- <cams.json> <old.json> <new.json> <head.npy> <out.png>"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); import gd13_img as gi; from gd13_common import NS, MX, project, load_cams, ROOT
a = sys.argv[sys.argv.index('--')+1:]; C = load_cams(a[0])['front']; OLD, NEW = json.load(open(a[1])), json.load(open(a[2])); X = np.load(a[3])[:NS]; OUT = a[4]
I = gi.load(f'{ROOT}/SourceAssets/Characters/GD13_IdentityMaster_20261009/references/GD13_REF_panel_front.png'); I = gi.resize(I, I.shape[1]*2, I.shape[0]*2)[..., :3].copy()
def line(P, col):
    q = project(C, np.asarray(P))*2
    for (x0, y0), (x1, y1) in zip(q[:-1], q[1:]):
        for t in np.linspace(0, 1, 40):
            xx, yy = int(round(x0+(x1-x0)*t)), int(round(y0+(y1-y0)*t))
            if 0 <= yy < I.shape[0]-1 and 0 <= xx < I.shape[1]-1: I[yy:yy+2, xx:xx+2] = col
for B, col in ((OLD, (1, 1, 0)), (NEW, (0, 1, 1))):
    for side in ('imgL', 'imgR'):
        line([s['top'] for s in B[side]], col); line([s['bot'] for s in B[side]], col)
mid = X[(np.abs(X[:, 0]-MX) < 0.05) & (X[:, 2] > 162.5) & (X[:, 2] < 164.5)]; mid = mid[np.argmax(mid[:, 1])]; mx = int(project(C, mid[None])[0][0]*2); I[300:470, mx:mx+1] = (1, 1, 1)
gi.save(OUT, gi.resize(I[300:470, 330:710].copy(), 760, 340)); print('BROWPLOT_OK')
