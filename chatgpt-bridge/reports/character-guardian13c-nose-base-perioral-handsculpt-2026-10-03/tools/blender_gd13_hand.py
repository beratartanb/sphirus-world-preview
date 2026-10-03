"""GUARDIAN-13 localized sculpt with TOPOLOGY-AWARE brushes (Blender sculpt-mode equivalents: mask + grab/move + smooth with
'connected / topology' falloff). Unlike the euclidean ellipsoid ops, influence spreads only ALONG THE SURFACE (geodesic distance
over mesh edges, Dijkstra), so a grab on the alar rim cannot pull nostril-interior or columella vertices across the opening.
Global protect mask (never moves): teeth / mouth interior (non-skin segments), lip seam band, jaw / chin (z < 153.2), nose dorsum
above z 159.6, everything outside the nose-base / perioral boxes.
Stroke = {"name", "type": "grab"|"smooth", "sel": {"box": {"ax": [a0, a1], "y": [..], "z": [..]}, "n": {"axis": "x_med"|"x_lat"|"y"|"z", "min": v}},
          "d": [dx_lat, dy, dz] (grab; dx_lat is mirrored: + = away from the midline), "r": geodesic radius cm, "iters": n (smooth)}
Seeds = vertices passing sel on both sides (mirror). Weight = (1-(g/r)^2)^2, g = geodesic distance to the nearest seed (0 at seeds).
usage: blender -b -P blender_gd13_hand.py -- <in.npy> <strokes.json> <out.npy>"""
import sys, os, json, heapq, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import head_topology
a = sys.argv[sys.argv.index('--')+1:]; X0 = np.load(a[0]); X = X0.copy(); C = json.load(open(a[1])); OUT = a[2]
MX = -0.25; NH = 24049; T, MI = head_topology(); TT = T[(MI == 0) & (T.max(1) < NH)]
E_ = np.r_[TT[:, [0, 1]], TT[:, [1, 2]], TT[:, [2, 0]]]; E_ = np.unique(np.sort(E_, 1), axis=0)
ADJ = [[] for _ in range(NH)]
for i, j in E_: ADJ[i].append(j); ADJ[j].append(i)
H0 = X0[:NH]; ax0 = np.abs(H0[:, 0]-MX)
ZONE = (((ax0 < 3.0) & (H0[:, 2] > 157.3) & (H0[:, 2] < 159.7) & (H0[:, 1] > 11.8)) |          # nose base
        ((ax0 < 3.6) & (H0[:, 2] > 153.2) & (H0[:, 2] < 157.6) & (H0[:, 1] > 10.8)))           # perioral
def normals(X):
    N = np.zeros((NH, 3)); fn = -np.cross(X[TT[:, 1]]-X[TT[:, 0]], X[TT[:, 2]]-X[TT[:, 0]])
    for k in range(3): np.add.at(N, TT[:, k], fn)
    return N/np.maximum(np.linalg.norm(N, axis=1), 1e-9)[:, None]
def select(X, sel):
    H = X[:NH]; ax = np.abs(H[:, 0]-MX); s = np.sign(H[:, 0]-MX); b = sel['box']
    m = (ax >= b['ax'][0]) & (ax <= b['ax'][1]) & (H[:, 1] >= b['y'][0]) & (H[:, 1] <= b['y'][1]) & (H[:, 2] >= b['z'][0]) & (H[:, 2] <= b['z'][1])
    if 'n' in sel:
        N = normals(X); c = sel['n']; v = {'x_med': -N[:, 0]*s, 'x_lat': N[:, 0]*s, 'y': N[:, 1], 'z': N[:, 2], '-z': -N[:, 2]}[c['axis']]; m &= v >= c['min']
    return np.nonzero(m & ZONE)[0]
def geodesic(X, seeds, r):
    d = np.full(NH, np.inf); d[seeds] = 0.0; pq = [(0.0, int(i)) for i in seeds]; heapq.heapify(pq)
    while pq:
        g, i = heapq.heappop(pq)
        if g > d[i] or g > r: continue
        for j in ADJ[i]:
            ng = g+float(np.linalg.norm(X[i]-X[j]))
            if ng < d[j] and ng <= r: d[j] = ng; heapq.heappush(pq, (ng, j))
    return d
log = []
for st in C['strokes']:
    seeds = select(X, st['sel'])
    if len(seeds) == 0: log.append({st['name']: 'NO SEEDS'}); continue
    g = geodesic(X, seeds, st['r']); w = np.where(np.isfinite(g), (1-np.clip(g/st['r'], 0, 1)**2)**2, 0.0)*ZONE
    Nn = normals(X); w = w*np.where(X[:NH, 2] < 157.6, (Nn[:, 1] > 0.0).astype(float), 1.0)   # lip seam / inner lips (back-facing) never move
    if st['type'] == 'grab':
        s = np.sign(X[:NH, 0]-MX); dv = np.asarray(st['d'], float); D = np.stack([dv[0]*s, np.full(NH, dv[1]), np.full(NH, dv[2])], 1)
        X[:NH] += w[:, None]*D
    elif st['type'] == 'smooth':
        Ei = np.r_[E_, E_[:, ::-1]]; deg = np.bincount(Ei[:, 0], minlength=NH).astype(float)
        for k in range(st.get('iters', 2)):
            for lam in (0.5, -0.53):
                acc = np.zeros((NH, 3)); np.add.at(acc, Ei[:, 0], X[Ei[:, 1]]); L = acc/np.maximum(deg, 1)[:, None]-X[:NH]; X[:NH] += lam*st.get('s', 1.0)*w[:, None]*L
    log.append({st['name']: [int(len(seeds)), int((w > 0.01).sum()), round(10*float(np.linalg.norm(X-X0, axis=1).max()), 2)]})
np.save(OUT, X); print('HAND_OK', json.dumps(log))
