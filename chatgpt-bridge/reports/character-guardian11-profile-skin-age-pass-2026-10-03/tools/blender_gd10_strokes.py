"""GUARDIAN-10 stroke sculpting on a DNA-order head (npy, UE cm), the scripted equivalent of Blender sculpt-mode brushes with X symmetry.
A stroke = polyline of points on/near the surface; dabs are spaced along it (spacing = 0.25*radius); each dab applies the brush to the skin
+ cartilage vertices within its radius with a smooth falloff (1-(d/r)^2)^2 * strength. Eyeballs / teeth untouched; collar guard below z 148.5.
Brushes:
  inflate : move along each vertex normal (+ adds flesh, - deflates)
  clay    : move along the AVERAGE normal of the dab area (builds a soft plane/mass, keeps forms readable)
  grab    : move by a fixed vector 'd' (cm) per stroke (applied once with the stroke-union falloff, not per dab)
  smooth  : relax toward the neighbour average (Taubin, volume-preserving)
  flatten : move toward the dab's average plane (reduces bumps / ridges)
Each stroke: {"brush", "pts": [[x,y,z],..], "r": cm, "s": strength (cm per dab for inflate/clay, 0..1 for smooth/flatten), "d": [..] (grab),
  "sym": true (mirror about x = MX)}.  Points are snapped to the surface before applying.
usage: blender -b -P blender_gd10_strokes.py -- <in.npy> <strokes.json> <out.npy>    env MX (facial midline x, default -0.25)"""
import sys, os, json, numpy as np
from mathutils import Vector, kdtree
from mathutils.bvhtree import BVHTree
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from id_common import pkg, SEG
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]).copy(); STK = json.load(open(a[1])); OUT = a[2]; MX = float(os.environ.get('MX', '-0.25'))
P = pkg(); TRI = np.asarray(P['head']['triangles']); MID = np.asarray(P['head']['material_ids']); TS = TRI[MID == 0]
SOFT = np.r_[np.arange(*SEG['skin']), np.arange(*SEG['cartilage'])]
E_ = np.r_[TRI[:, [0, 1]], TRI[:, [1, 2]], TRI[:, [2, 0]]]; E_ = np.r_[E_, E_[:, ::-1]]; DEG = np.bincount(E_[:, 0], minlength=len(X)).astype(float)
def sstep(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
def normals(X):
    N = np.zeros_like(X); fn = -np.cross(X[TRI[:, 1]]-X[TRI[:, 0]], X[TRI[:, 2]]-X[TRI[:, 0]])
    for k in range(3): np.add.at(N, TRI[:, k], fn)
    return N/np.maximum(np.linalg.norm(N, axis=1), 1e-9)[:, None]
def dabs(pts, r):
    pts = np.asarray(pts, float)
    if len(pts) == 1: return pts
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1); s = np.r_[0, np.cumsum(seg)]; n = max(2, int(s[-1]/(0.25*r))+1); t = np.linspace(0, s[-1], n)
    return np.stack([np.interp(t, s, pts[:, k]) for k in range(3)], 1)
log = []
for st in STK:
    variants = [np.asarray(st['pts'], float)]
    if st.get('sym'):
        m = variants[0].copy(); m[:, 0] = 2*MX-m[:, 0]; variants.append(m)
    tot = 0.0
    for vi, pts in enumerate(variants):
        bvh = BVHTree.FromPolygons([Vector(q) for q in X], [list(t) for t in TS])
        pts = np.array([list(bvh.find_nearest(Vector(q))[0]) for q in pts]); r = st['r']; b = st['brush']; S = X[SOFT]
        guard = sstep((S[:, 2]-146.5)/2.0)
        if b == 'grab':
            w = np.zeros(len(S))
            for c in dabs(pts, r): w = np.maximum(w, (1-np.clip(np.linalg.norm(S-c, axis=1)/r, 0, 1)**2)**2)
            d = np.asarray(st['d'], float)*(np.array([-1.0, 1, 1]) if vi == 1 else 1.0)
            disp = (w*guard)[:, None]*d; X[SOFT] += disp; tot = max(tot, float(np.linalg.norm(disp, axis=1).max())); continue
        for c in dabs(pts, r):
            S = X[SOFT]; dist = np.linalg.norm(S-c, axis=1); w = (1-np.clip(dist/r, 0, 1)**2)**2*guard; idx = np.nonzero(w > 1e-4)[0]
            if len(idx) == 0: continue
            if b in ('inflate', 'clay', 'flatten'):
                N = normals(X)[SOFT]
            if b == 'inflate': disp = N[idx]*(w[idx]*st['s'])[:, None]
            elif b == 'clay': an = (N[idx]*w[idx, None]).sum(0); an /= np.linalg.norm(an)+1e-9; disp = an[None]*(w[idx]*st['s'])[:, None]
            elif b == 'flatten':
                an = (N[idx]*w[idx, None]).sum(0); an /= np.linalg.norm(an)+1e-9; cen = (S[idx]*w[idx, None]).sum(0)/w[idx].sum(); h = (S[idx]-cen)@an
                disp = -an[None]*(h*w[idx]*st['s'])[:, None]
            elif b == 'smooth':
                acc = np.zeros_like(X); np.add.at(acc, E_[:, 0], X[E_[:, 1]]); Lp = (acc/np.maximum(DEG, 1)[:, None]-X)[SOFT]
                disp = Lp[idx]*(w[idx]*st['s'])[:, None]
            X[SOFT[idx]] += disp; tot = max(tot, float(np.linalg.norm(disp, axis=1).max()))
    log.append((st.get('name', st['brush']), round(tot*10, 2)))
np.save(OUT, X); print('STROKES_OK', OUT, json.dumps(log))
