"""GD11 refinement N: programmatic edit of the MAIN lock guides (prim:*) and the nape spines of a guides.json -> layer-2 guides json.
(1) front-side / temple primaries (root in the front-side hairline zone: y > YMIN, |x| > XMIN, z < ZMAX, excluding the part-top): the first
    part of the centreline is swept DOWN-BACK diagonally across the temple toward the ear top (crossing flow) before it rises to the bun:
    dz(t) = -A * sin(pi * t/TS) for t < TS (TS = sweep fraction), plus a backward push dy; each moved point keeps its original stand-off from the
    scalp (re-projected on the build head). (2) behind-ear side primaries (root y < -1, |x| > 5): a shallower down-back sweep (A*0.5) so the
    behind-ear mass gathers from below. (3) nape_spine:j: alternate lateral / lift offsets on the middle control point and alternate bun-entry
    heights so sub-locks cross and layer instead of one sheet. Writes <out.json> (same keys; only edited entries differ -> the builder's layer-2
    tolerance picks them up) and prints what changed.
usage: blender -b --factory-startup --python blender_g11rn_guides_edit.py -- <in guides.json> <out guides.json> <head.npy>  env: GE_A=2.6 GE_TS=0.42 GE_DY=0.9 GE_XMIN=3.4 GE_YMIN=1.5 GE_ZMAX=171 GE_NAPE_LAT=0.7 GE_NAPE_LIFT=0.35 GE_NAPE_ENTRY=0.6"""
import bpy, sys, os, json, math, numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import head_topology
a = sys.argv[sys.argv.index('--')+1:]; IN, OUT, HEAD = a[0], a[1], a[2]; E = lambda k, d: float(os.environ.get(k, d))
A, TS, DY, XMIN, YMIN, ZMAX = E('GE_A', '2.6'), E('GE_TS', '0.42'), E('GE_DY', '0.9'), E('GE_XMIN', '3.4'), E('GE_YMIN', '1.5'), E('GE_ZMAX', '171')
NL, NLIFT, NENT = E('GE_NAPE_LAT', '0.7'), E('GE_NAPE_LIFT', '0.35'), E('GE_NAPE_ENTRY', '0.6')
G = json.load(open(IN)); X = np.load(HEAD)[:24049]; T, MI = head_topology(); TT = T[(MI == 0) & (T.max(1) < 24049)]
bvh = BVHTree.FromPolygons([tuple(map(float, p)) for p in X], [tuple(int(i) for i in t) for t in TT]); fn = np.cross(X[TT[:, 1]]-X[TT[:, 0]], X[TT[:, 2]]-X[TT[:, 0]]); fn = -fn/np.maximum(np.linalg.norm(fn, axis=1), 1e-9)[:, None]
def nearest(p): loc, nrm, idx, d = bvh.find_nearest(Vector(p)); return np.asarray(loc), np.asarray(fn[idx])
def standoff(p): loc, n = nearest(p); return float(np.dot(p-loc, n))
def sstep(t): t = min(max(t, 0.0), 1.0); return t*t*(3-2*t)
log = {'front_side_sweep': [], 'behind_ear_sweep': [], 'nape_spine': []}
for k, v in G.items():
    if not isinstance(v, dict): continue
    if k.startswith('prim:') and v.get('group') in ('front_to_bun', 'side_to_bun'):
        c = np.asarray(v['ctrl'], float); r = c[0]; n = len(c); sd = 1.0 if r[0] > -0.25 else -1.0
        front_side = (r[1] > YMIN) and (abs(r[0]) > XMIN) and (r[2] < ZMAX)
        behind = (r[1] < -1.0) and (abs(r[0]) > 5.0) and (r[2] < 168.0)
        if not (front_side or behind): continue
        amp = A if front_side else 0.5*A; new = c.copy()
        for i in range(1, n):
            t = i/(n-1)
            if t >= TS: break
            w = math.sin(math.pi*t/TS); h0 = standoff(c[i])
            q = c[i]+np.array([sd*0.25*amp*w, -DY*w, -amp*w])          # down, back, slightly outward
            loc, nrm = nearest(q); new[i] = loc+nrm*max(h0, 0.15)      # keep the original stand-off on the new scalp position
        for i in range(int(TS*(n-1)), min(n, int(TS*(n-1))+5)):        # blend back into the untouched tail
            f = 1-sstep((i-TS*(n-1))/4.0); new[i] = c[i]+(new[max(1, int(TS*(n-1))-1)]-c[max(1, int(TS*(n-1))-1)])*f*0.5
        v['ctrl'] = [[round(float(x), 4) for x in p] for p in new]; (log['front_side_sweep'] if front_side else log['behind_ear_sweep']).append(k)
    if k.startswith('nape_spine:'):
        j = int(k.split(':')[1]); c = np.asarray(v['ctrl'], float)
        if len(c) >= 3:
            mid = c[1].copy(); sgn = 1.0 if j % 2 == 0 else -1.0; mid[0] += sgn*NL; mid[2] += (0.5 if j % 3 == 0 else -0.5)*NLIFT*2
            loc, nrm = nearest(mid); h0 = standoff(c[1]); c[1] = loc+nrm*(max(h0, 0.1)+(NLIFT if j % 2 == 0 else 0.0))
            c[-1][2] += sgn*NENT; v['ctrl'] = [[round(float(x), 4) for x in p] for p in c]; log['nape_spine'].append(k)
json.dump(G, open(OUT, 'w')); print('GUIDES_EDIT_OK', json.dumps({k: len(v) for k, v in log.items()}), json.dumps(log)[:600])
