"""GD15 lower-face region metrics for a set of heads vs a base (DNA order, project cm). Support tool; the eye decides.
Per head: front-silhouette half-width change (mm, mean of both sides, verts ahead of the ear y > 3) per z slice, and signed NORMAL displacement
(mm, + = outward) averaged in anatomical spots (snapped to the base surface), plus 'rel' = spot minus its surrounding ring (negative = reads as a
relative hollow even if nothing moved inward) - the lesson of S5/S9 (gonial push, caved mid cheek).
usage: blender -b --python gd15_cheekmetrics.py -- <base.npy|.f32> <topo.npz> <out.json> <head1|list.txt> [head2 ...]"""
import sys, json, numpy as np
a = sys.argv[sys.argv.index('--')+1:]
def L(p): return np.load(p) if p.endswith('.npy') else np.fromfile(p, np.float32).reshape(-1, 3).astype(float)
B = L(a[0]); TP = np.load(a[1]); OUT = a[2]; HS = a[3:]; NS = 24049; MX = -0.23
HS = sum(([l.strip() for l in open(h) if l.strip()] if h.endswith(".txt") else [h] for h in HS), [])   # a .txt arg = list of heads
T = TP['loops'].reshape(-1, 3); T = T[(T < NS).all(1)]   # head_topo loops are already outward-wound (verified: mean N.(S-c) > 0)
S = B[:NS]; fn = np.cross(S[T[:, 1]]-S[T[:, 0]], S[T[:, 2]]-S[T[:, 0]]); N = np.zeros((NS, 3))
for k in range(3): np.add.at(N, T[:, k], fn)
N /= np.maximum(np.linalg.norm(N, axis=1), 1e-9)[:, None]
SPOTS = {'gonial': (5.3, 2.5, 151.8, 0.9), 'masseter': (5.2, 5.2, 153.6, 0.9), 'midcheek': (4.3, 8.5, 156.4, 0.9), 'malar': (4.0, 9.8, 159.2, 0.8),
         'buccal': (4.6, 7.2, 155.0, 0.8), 'prejowl': (2.9, 10.6, 152.6, 0.6), 'jawborder': (4.2, 7.0, 151.4, 0.7), 'chin': (0.0, 12.3, 152.4, 0.6), 'menton': (0.0, 11.0, 151.0, 0.5)}
def spot_idx(x, y, z, r, side):
    p = np.array([MX+side*x, y, z]); c = S[np.argmin(np.linalg.norm(S-p, axis=1))]; d = np.linalg.norm(S-c, axis=1)
    return d < r, (d >= r*1.4) & (d < r*2.6)
ZS = [150.5, 151.5, 152.5, 153.5, 154.5, 155.5, 156.5, 157.5, 158.5]
def hw(X, z, side):
    m = (np.abs(X[:NS, 2]-z) < 0.2) & (X[:NS, 1] > 3.0) & ((X[:NS, 0]-MX)*side > 0)
    return np.abs(X[:NS][m, 0]-MX).max() if m.any() else np.nan
res = {}
for h in HS:
    X = L(h); D = X[:NS]-S; dn = (D*N).sum(1)*10; r = {'w': {}, 's': {}}
    for z in ZS: r['w'][str(z)] = round(float(np.mean([(hw(X, z, s)-hw(B, z, s))*10 for s in (1, -1)])), 2)
    for k, (x, y, z, rad) in SPOTS.items():
        vals = []; rels = []
        for s in ((1, -1) if x > 0 else (1,)):
            ins, ring = spot_idx(x, y, z, rad, s); v = dn[ins].mean(); vals.append(v); rels.append(v-dn[ring].mean())
        r['s'][k] = [round(float(np.mean(vals)), 2), round(float(np.mean(rels)), 2)]
    r['max'] = round(float(np.linalg.norm(D, axis=1).max()*10), 2); res[h.replace('\\', '/').rsplit('/', 1)[-1]] = r
json.dump(res, open(OUT, 'w'), indent=1); print('CHEEKMET', len(res))
