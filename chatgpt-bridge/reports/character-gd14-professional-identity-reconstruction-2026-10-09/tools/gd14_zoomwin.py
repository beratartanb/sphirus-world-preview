"""GD14: close-up windows (2x panel px) per reference view, from E's anatomical points projected with the solved cameras -> data/zoomwin.json"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'GD13_Identity_20261009', 'tools')); from gd13_common import project
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]); C = json.load(open(a[1])); OUT = a[2]; MX = -0.23; S = X[:24049]
def fpt(xo, z):
    for w in (0.12, 0.25, 0.5, 1.0):
        m = (np.abs(S[:, 0]-(MX+xo)) < w) & (np.abs(S[:, 2]-z) < w) & (S[:, 1] > -2)
        if m.any(): return S[m][np.argmax(S[m, 1])]
P = {'eyeL': X[28955:29725].mean(0), 'eyeR': X[29725:30495].mean(0), 'browL': fpt(2.6, 164.3), 'browR': fpt(-2.6, 164.3), 'glabella': fpt(0, 164.0), 'forehead': fpt(0, 167.0),
     'tip': fpt(0, 159.0), 'subn': fpt(0, 157.9), 'stom': fpt(0, 155.6), 'cornerL': fpt(2.35, 155.3), 'cornerR': fpt(-2.35, 155.3), 'chin': fpt(0, 152.5), 'menton': fpt(0, 151.2),
     'malarL': fpt(3.3, 159.4), 'malarR': fpt(-3.3, 159.4), 'buccL': fpt(4.4, 156.5), 'buccR': fpt(-4.4, 156.5), 'jawL': fpt(4.0, 153.0), 'jawR': fpt(-4.0, 153.0)}
REG = {'eye': ['eyeL', 'eyeR'], 'brow': ['browL', 'browR', 'glabella', 'eyeL', 'eyeR'], 'cheek': ['malarL', 'malarR', 'buccL', 'buccR'], 'nose': ['tip', 'subn', 'glabella'], 'lips': ['stom', 'cornerL', 'cornerR', 'subn'], 'chin': ['chin', 'menton', 'stom', 'jawL', 'jawR']}
PAD = {'eye': 70, 'brow': 60, 'cheek': 70, 'nose': 60, 'lips': 55, 'chin': 70}
out = {}
for v, c in C.items():
    if v not in ('front', 'q3_faceR', 'q3_faceL', 'prof_faceL'): continue
    W, H = (966, 1082) if v != 'prof_faceL' else (966, 1090); out[v] = {}
    for r, keys in REG.items():
        pts = project(c, np.array([P[k] for k in keys]))*2
        far = {'q3_faceR': 'L', 'q3_faceL': 'R', 'prof_faceL': 'R'}.get(v)   # camera on the subject's right (q3_faceR) / left side: drop far-side cheek/jaw points
        if far: keep = [i for i, k in enumerate(keys) if not (k.endswith(far) and (k[:-1] in ('malar', 'bucc', 'jaw', 'corner') or v == 'prof_faceL'))]; pts = pts[keep]
        x0, y0 = pts.min(0)-PAD[r]; x1, y1 = pts.max(0)+PAD[r]; cx, cy = (x0+x1)/2, (y0+y1)/2; h = max(y1-y0, (x1-x0)*0.55); w = max(x1-x0, h*1.6)
        out[v][r] = [int(max(0, cx-w/2)), int(max(0, cy-h/2)), int(min(W, cx+w/2)), int(min(H, cy+h/2))]
json.dump(out, open(OUT, 'w'), indent=1); print(json.dumps(out))
