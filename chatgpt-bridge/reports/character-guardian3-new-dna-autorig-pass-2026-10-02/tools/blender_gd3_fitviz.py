"""GUARDIAN-3: draw a model fit against the Tier A photos with the fit's own per-view similarity: candidate (red) vs reference (green)
tracker curves, picks (cyan ref / magenta candidate), clay silhouette outline. usage: blender -b -P blender_gd3_fitviz.py -- <head.npy> <report.json> <out prefix>"""
import bpy, sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import topix, VIEWS, ref_curves
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]); REP = json.load(open(a[1])) if a[1] != '-' else {}; OUT = a[2]
SEM = json.load(open('Saved/Codex/CharacterGuardian_20261001/semantic_j.json')); PK = json.load(open('Saved/Codex/CharacterIdentity_20260930/ref_picks.json'))
def load(p):
    im = bpy.data.images.load(os.path.abspath(p)); w, h = im.size; x = np.asarray(im.pixels[:], np.float32).reshape(h, w, im.channels)[::-1][..., :3].copy(); bpy.data.images.remove(im); return x
def save(x, p):
    h, w = x.shape[:2]; rgba = np.ones((h, w, 4), np.float32); rgba[..., :3] = x; im = bpy.data.images.new('o', w, h); im.pixels.foreach_set(np.ascontiguousarray(rgba[::-1]).ravel()); im.filepath_raw = os.path.abspath(p); im.file_format = 'PNG'; im.save()
def dot(img, p, c, r=2):
    x, y = int(round(p[0])), int(round(p[1])); h, w = img.shape[:2]; img[max(y-r, 0):min(y+r+1, h), max(x-r, 0):min(x+r+1, w)] = c
def similarity(P, Q):
    mp, mq = P.mean(0), Q.mean(0); A, Bq = P-mp, Q-mq; C = Bq.T@A/len(P); U, Sg, Vt = np.linalg.svd(C); D = np.eye(2); D[1, 1] = np.sign(np.linalg.det(U@Vt)); Rm = U@D@Vt
    s = (Sg*np.diag(D)).sum()/(A**2).sum()*len(P); return s, Rm, mq-s*Rm@mp
for view in ('front', 'close'):
    if 'sims_full' in REP: s, Rm, t = REP['sims_full'][view]
    else:   # own similarity from the bound tracker curves (near-side curves only in 3/4)
        R0 = ref_curves(view); P2, Q2 = [], []
        for crv, bind in SEM[view].items():
            if view == 'close' and crv.endswith('_l'): continue
            if len(bind) != len(R0[crv]): continue
            for b, q in zip(bind, R0[crv]):
                if b is None: continue
                P2.append((X[b[0]]*np.asarray(b[1])[:, None]).sum(0)); Q2.append(q)
        s, Rm, t = similarity(topix(view, np.asarray(P2)), np.asarray(Q2, float)); Rm = np.asarray(Rm); t = np.asarray(t)
    T = lambda P: (s*(Rm@topix(view, P).T)).T+t
    img = load(VIEWS[view]['ref'])*0.85; R = ref_curves(view)
    # clay silhouette points (skin verts) as faint red
    q = T(X[:24049:3])
    for p in q: dot(img, p, (0.55, 0.25, 0.25), 0)
    for crv, bind in SEM[view].items():
        for i, b in enumerate(bind):
            if b is None: continue
            P = (X[b[0]]*np.asarray(b[1])[:, None]).sum(0); dot(img, T(P[None])[0], (1, 0.1, 0.1), 1)
        for p in R[crv]: dot(img, p, (0.1, 1, 0.2), 1)
    for p in PK[view]['points']+PK[view]['contours']: dot(img, p['ref'], (0.1, 0.9, 1.0), 2)
    for nm, vi in REP.get('vertices', {}).items():
        if nm in [p['name'] for p in PK[view]['points']]: dot(img, T(X[[vi]])[0], (1, 0.2, 1), 2)
    save(img, f'{OUT}_{view}.png')
print('FITVIZ', OUT)
