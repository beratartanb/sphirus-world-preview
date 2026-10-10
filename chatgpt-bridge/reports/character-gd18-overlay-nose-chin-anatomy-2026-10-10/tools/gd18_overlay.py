"""GD18 overlay board: the reference panel and candidate images that are ALREADY in the panel's 2x pixel frame (UE captures warped with the
solved panel camera = gd18_warp.py, or Blender renders made with CAM_REF_<view> = gd13_render) - no image is deformed, scaled or shifted to fit:
same solved camera, same scale. Per candidate one row: REF | candidate | 50 % blend | red-cyan difference (ref = red, candidate = cyan;
where the two agree the pixel is grey, where only the ref has skin it is red, where only the candidate has skin it is cyan).
Overlays carry the reference auto skin-key contours (yellow, GD13 contours_auto.json) and the candidate silhouette from its alpha render (magenta).
usage: -- <out.jpg> <view> <x0> <y0> <x1> <y1> <tile w> label=image.png[|alpha.png] [label2=...]   (crop in 2x panel px)"""
import sys, os, json, numpy as np
ROOT = os.getcwd(); G = os.path.join(ROOT, 'Saved/Codex/GD13_Identity_20261009'); sys.path.insert(0, os.path.join(G, 'tools')); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; OUT = a[0]; V = a[1]; x0, y0, x1, y1 = [int(v) for v in a[2:6]]; TW = int(a[6]); C = a[7:]
R = gi.load(f'{ROOT}/SourceAssets/Characters/GD13_IdentityMaster_20261009/references/GD13_REF_panel_{V}.png'); R = gi.resize(R, R.shape[1]*2, R.shape[0]*2)
AU = json.load(open(os.path.join(G, 'data/contours_auto.json'))).get(V, {})
def gray(I): return I[..., :3] @ np.array([0.299, 0.587, 0.114], np.float32)
def draw_pts(I, P, col, r=1):
    for x, y in P:
        xi, yi = int(round(x)), int(round(y))
        if 0 <= yi < I.shape[0] and 0 <= xi < I.shape[1]: I[max(0, yi-r):yi+r+1, max(0, xi-r):xi+r+1, :3] = col
    return I
def edge(al):
    e = al ^ (np.roll(al, 1, 0) & np.roll(al, -1, 0) & np.roll(al, 1, 1) & np.roll(al, -1, 1)); return e & al
def tile(I): return gi.resize(I[y0:y1, x0:x1], TW, int(TW*(y1-y0)/(x1-x0)))
def label(I, txt):
    I = I.copy(); I[:18, :, :3] *= 0.25; return I
rows = []
for c in C:
    lab, spec = c.split('=', 1); p = spec.split('|'); Im = gi.load(p[0]); Im = gi.resize(Im, R.shape[1], R.shape[0]) if Im.shape[:2] != R.shape[:2] else Im
    al = None
    if len(p) > 1: A = gi.load(p[1]); A = gi.resize(A, R.shape[1], R.shape[0]) if A.shape[:2] != R.shape[:2] else A; al = A[..., 3] > 0.5
    B = R*0.5+Im*0.5; gR, gC = gray(R), gray(Im); D = np.stack([gR, gC, gC, np.ones_like(gR)], -1)
    for I in (B, D):
        for k, P in AU.items(): draw_pts(I, np.asarray(P)*2, [1, 1, 0], 1)
        if al is not None: I[edge(al), :3] = [1, 0.1, 0.85]
    rows.append(np.concatenate([tile(R), tile(Im), tile(B), tile(D)], 1)); print('OVL', lab, V)
sep = np.zeros((6, rows[0].shape[1], 4), np.float32); sep[..., 3] = 1
out = rows[0]
for r in rows[1:]: out = np.concatenate([out, sep, r], 0)
gi.save(OUT, out); print('OVERLAY_OK', OUT)
