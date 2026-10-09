"""GD13 board parts: batch crops (2x-panel pixel rects) from reference panels and renders, optional outline overlay, written as JPG.
spec json: [{"src": path | "REF:<view>", "rect": [x0,y0,x1,y1] | null, "w": width, "out": path, "ovl": optional alpha png (silhouette outline drawn on src)}]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); import gd13_img as gi; from gd13_common import ROOT
S = json.load(open(sys.argv[sys.argv.index('--')+1])); cache = {}
def img(src):
    if src not in cache:
        if src.startswith('REF:'):
            A = gi.load(f'{ROOT}/SourceAssets/Characters/GD13_IdentityMaster_20261009/references/GD13_REF_panel_{src[4:]}.png'); A = gi.resize(A, A.shape[1]*2, A.shape[0]*2)
        else: A = gi.load(src)
        cache[src] = A
    return cache[src]
for s in S:
    A = img(s['src']).copy()
    if s.get('ovl'):
        al = gi.load(s['ovl'])[..., 3] > 0.5; e = al & ~(np.roll(al, 1, 0) & np.roll(al, -1, 0) & np.roll(al, 1, 1) & np.roll(al, -1, 1))
        e = e | np.roll(e, 1, 0) | np.roll(e, 1, 1); A = gi.resize(A, al.shape[1], al.shape[0]) if A.shape[:2] != al.shape else A; A[e, :3] = [1, 0.1, 0.85]
    r = s.get('rect')
    if r: A = A[r[1]:r[3], r[0]:r[2]]
    w = s.get('w', A.shape[1]); h = int(round(A.shape[0]*w/A.shape[1])); gi.save(s['out'], gi.resize(A, w, h), 90)
print('PARTS_OK', len(S))
