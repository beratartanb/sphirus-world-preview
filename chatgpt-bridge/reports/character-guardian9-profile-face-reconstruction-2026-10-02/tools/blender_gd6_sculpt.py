"""GUARDIAN-6 sculpt brushes on a DNA-order head (npy, UE cm), guided by the Tier A overlays. Skin + cartilage only; collar guard (no change
below z 146.5, smooth to 148.5) keeps the head/body weld exact; eyeballs / lids-attached meshes follow skin via the MetaHuman fit.
modes:
  project <head.npy> <out.json>           : back-project the Tier A nasolabial tracker curves (front + ~33 deg 3/4 solved cameras) onto the
                                            head surface -> 3D polylines {'front': {'crv_nasolabial_l': [[x,y,z]..]}, 'close': {...}}
  sculpt  <in.npy> <brushes.json> <out.npy>: apply brushes in order. Brush types:
    line_step : {"pts": [[x,y,z]..], "w": cm, "amp": cm, "side": [sx,sy,sz], "ext": cm}  plane step across a surface line: displacement
                along the vertex normal = amp*tanh(d/w)*exp(-(d/(3w))^2) (d = signed in-surface distance, + toward 'side'), faded at the ends
    line_groove: {"pts": .., "w": cm, "depth": cm, "bulge": cm, "side": [..], "ext": cm}  soft trough (-depth gaussian) with an optional
                bulge on the 'side' half (tissue above a tear trough) -- no sharp crease (widths >= 0.25 cm)
    region    : {"c": [..], "r": [..], "amt": cm (along normal) , "d": [..] (move), "p": falloff power}
    scale     : {"c", "r", "s": [sx,sy,sz], "pivot": [..]}
    smooth    : {"c", "r", "iters", "lam"}   Taubin (volume-preserving) local smoothing
usage: blender -b -P blender_gd6_sculpt.py -- project <head.npy> <out.json> | sculpt <in.npy> <brushes.json> <out.npy>"""
import sys, os, json, math, numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from id_common import pkg, SEG
a = sys.argv[sys.argv.index('--')+1:]; MODE = a[0]
P = pkg(); TRI = np.asarray(P['head']['triangles']); MID = np.asarray(P['head']['material_ids']); TS = TRI[MID == 0]
SOFT = np.r_[np.arange(*SEG['skin']), np.arange(*SEG['cartilage'])]
def sstep(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
def normals(X):
    N = np.zeros_like(X); fn = -np.cross(X[TRI[:, 1]]-X[TRI[:, 0]], X[TRI[:, 2]]-X[TRI[:, 0]])
    for k in range(3): np.add.at(N, TRI[:, k], fn)
    return N/np.maximum(np.linalg.norm(N, axis=1), 1e-9)[:, None]
if MODE == 'project':
    from gd_common import ray
    X = np.load(a[1]); bvh = BVHTree.FromPolygons([Vector(p) for p in X], [list(t) for t in TS]); out = {}
    for view, f in (('front', 'ref_front.json'), ('close', 'ref_close.json')):
        R = json.load(open('Saved/Codex/CharacterGuardian_20261001/track/'+f)); out[view] = {}
        for k in ('crv_nasolabial_l', 'crv_nasolabial_r'):
            pts = []
            for px, py in R[k]:
                o, d = ray(view, px, py); hit = bvh.ray_cast(Vector(o), Vector(d))
                if hit[0] is not None: pts.append([round(c, 4) for c in hit[0]])
            out[view][k] = pts
    json.dump(out, open(a[2], 'w'), indent=1); print('PROJECT_OK', {v: {k: len(p) for k, p in d.items()} for v, d in out.items()})
    sys.exit(0)
X = np.load(a[1]).copy(); BR = json.load(open(a[2])); OUT = a[3]; log = []
E_ = np.r_[TRI[:, [0, 1]], TRI[:, [1, 2]], TRI[:, [2, 0]]]; E_ = np.r_[E_, E_[:, ::-1]]; DEG = np.bincount(E_[:, 0], minlength=len(X)).astype(float)
def line_dist(S, pts, side):
    """signed in-surface distance of S to polyline pts (+ toward 'side'), arc parameter t in [0,1], unsigned distance"""
    pts = np.asarray(pts, float); seg0, seg1 = pts[:-1], pts[1:]; v = seg1-seg0; L = np.linalg.norm(v, axis=1); cum = np.r_[0, np.cumsum(L)]
    best = np.full(len(S), 1e9); bt = np.zeros(len(S)); bc = np.zeros_like(S); btan = np.zeros_like(S)
    for i in range(len(v)):
        u = np.clip(((S-seg0[i])@v[i])/max(L[i]**2, 1e-12), 0, 1); c = seg0[i]+u[:, None]*v[i]; dd = np.linalg.norm(S-c, axis=1); m = dd < best
        best[m] = dd[m]; bt[m] = (cum[i]+u[m]*L[i])/cum[-1]; bc[m] = c[m]; btan[m] = v[i]/max(L[i], 1e-9)
    return best, bt, bc, btan
for b in BR:
    S = X[SOFT]; N = normals(X)[SOFT]; guard = sstep((S[:, 2]-146.5)/2.0); disp = np.zeros_like(S); t = b['type']
    if t in ('line_step', 'line_groove'):
        bvh = BVHTree.FromPolygons([Vector(q) for q in X], [list(tr) for tr in TS]); pts = np.asarray(b['pts'], float)
        sc = np.r_[0, np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))]; ss = np.linspace(0, sc[-1], 40); pts = np.stack([np.interp(ss, sc, pts[:, k]) for k in range(3)], 1)
        for _ in range(int(b.get('smooth_line', 6))): pts[1:-1] = 0.5*pts[1:-1]+0.25*(pts[:-2]+pts[2:])
        b['pts'] = [list(bvh.find_nearest(Vector(q))[0]) for q in pts]
        dist, tt, cc, tan = line_dist(S, b['pts'], b['side']); w = b['w']; ext = b.get('ext', 3.0*w)
        side = np.asarray(b['side'], float); side = side/np.linalg.norm(side); lat = side[None]-tan*(tan@side)[:, None]; lat = lat-N*np.sum(lat*N, 1)[:, None]
        lat /= np.maximum(np.linalg.norm(lat, axis=1), 1e-6)[:, None]
        d = np.sum((S-cc)*lat, 1); e0, e1 = b.get('fade', [0.18, 0.18]); endf = sstep(tt/e0)*sstep((1-tt)/e1)*sstep((ext-dist)/(0.3*ext))
        if t == 'line_step': amt = b['amp']*np.tanh(d/w)*np.exp(-(d/(3*w))**2)
        else: amt = -b['depth']*np.exp(-(d/w)**2)+b.get('bulge', 0.0)*np.exp(-((d-1.6*w)/(1.2*w))**2)
        disp = N*(amt*endf*guard)[:, None]
    elif t == 'region':
        c = np.asarray(b['c'], float); r = np.asarray(b['r'], float); q = np.linalg.norm((S-c)/r, axis=1); wv = sstep(1-q)**b.get('p', 1.0)*guard
        if 'amt' in b: disp += N*(wv*b['amt'])[:, None]
        if 'd' in b: disp += wv[:, None]*np.asarray(b['d'], float)
    elif t == 'scale':
        c = np.asarray(b['c'], float); r = np.asarray(b['r'], float); q = np.linalg.norm((S-c)/r, axis=1); wv = sstep(1-q)**b.get('p', 1.0)*guard
        pv = np.asarray(b.get('pivot', b['c']), float); disp = wv[:, None]*((S-pv)*(np.asarray(b['s'], float)-1))
    elif t == 'smooth':
        c = np.asarray(b['c'], float); r = np.asarray(b['r'], float); q = np.linalg.norm((S-c)/r, axis=1); wv = sstep(1-q)*guard
        W = np.zeros(len(X)); W[SOFT] = wv; Y = X.copy()
        for it in range(b.get('iters', 8)):
            for lam in (b.get('lam', 0.5), -b.get('lam', 0.5)-0.03):
                acc = np.zeros_like(Y); np.add.at(acc, E_[:, 0], Y[E_[:, 1]]); Lp = acc/np.maximum(DEG, 1)[:, None]-Y; Y = Y+(lam*W)[:, None]*Lp
        disp = (Y-X)[SOFT]
    X[SOFT] += disp; dn = np.linalg.norm(disp, axis=1); log.append((b.get('name', t), round(float(dn.max()*10), 2), int((dn > 0.005).sum())))
np.save(OUT, X); print('SCULPT_OK', OUT, json.dumps(log))
