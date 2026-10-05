"""GD11 refinement O: FAMILY-SPECIFIC re-routing of the main lock guides (prim:*) and nape spines -> layer-2 guides json (v2 of the N editor).
Each front/side primary is assigned a family by its root azimuth theta (deg from the front, around the head axis at y=2.5) and height:
  F1 forehead-corner (theta 18-42, z > 165):  shallow sweep back-down over the temple top (A1), then rise; stand-off +S1 (outer layer)
  F2 temple (theta 42-66):                      strong diagonal down-back to the ear top (A2), late rise; stand-off -S2 (hugs, inner layer)
  F3 side above ear (theta 66-92, z 161-169):   nearly horizontal back along the upper ear (A3 small), lateral outward push LX3, rise late
  F4 behind ear (theta 92-125, z < 168):        from behind the ear UP-back into the bun (lift early), stand-off +S4
  nape spines: lateral / lift / entry variation (as N), plus every third spine enters the bun higher.
The sweep is applied to the first TS fraction of the centreline; the moved points keep their original scalp stand-off (BVH re-projection) plus
the family stand-off offset; tails blend back over 5 points. Prints which guides changed per family.
usage: blender -b --factory-startup --python blender_g11ro_guides_edit.py -- <in guides.json> <out guides.json> <head.npy>
env: GO_A1=1.4 GO_A2=3.0 GO_A3=0.8 GO_A4=1.2 GO_TS1=0.35 GO_TS2=0.45 GO_TS3=0.4 GO_TS4=0.3 GO_S1=0.35 GO_S2=0.2 GO_S4=0.3 GO_LX3=0.5 GO_DY=1.0 GO_NAPE_LAT=0.7 GO_NAPE_LIFT=0.35 GO_NAPE_ENTRY=0.6"""
import bpy, sys, os, json, math, numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import head_topology
a = sys.argv[sys.argv.index('--')+1:]; IN, OUT, HEAD = a[0], a[1], a[2]; E = lambda k, d: float(os.environ.get(k, d))
A1, A2, A3, A4 = E('GO_A1', '1.4'), E('GO_A2', '3.0'), E('GO_A3', '0.8'), E('GO_A4', '1.2'); TS = {1: E('GO_TS1', '0.35'), 2: E('GO_TS2', '0.45'), 3: E('GO_TS3', '0.4'), 4: E('GO_TS4', '0.3')}
S1, S2, S4, LX3, DY = E('GO_S1', '0.35'), E('GO_S2', '0.2'), E('GO_S4', '0.3'), E('GO_LX3', '0.5'), E('GO_DY', '1.0'); NL, NLIFT, NENT = E('GO_NAPE_LAT', '0.7'), E('GO_NAPE_LIFT', '0.35'), E('GO_NAPE_ENTRY', '0.6')
G = json.load(open(IN)); X = np.load(HEAD)[:24049]; T, MI = head_topology(); TT = T[(MI == 0) & (T.max(1) < 24049)]
bvh = BVHTree.FromPolygons([tuple(map(float, p)) for p in X], [tuple(int(i) for i in t) for t in TT]); fn = np.cross(X[TT[:, 1]]-X[TT[:, 0]], X[TT[:, 2]]-X[TT[:, 0]]); fn = -fn/np.maximum(np.linalg.norm(fn, axis=1), 1e-9)[:, None]
def nearest(p): loc, nrm, idx, d = bvh.find_nearest(Vector(p)); return np.asarray(loc), np.asarray(fn[idx])
def standoff(p): loc, n = nearest(p); return float(np.dot(p-loc, n))
def sstep(t): t = min(max(t, 0.0), 1.0); return t*t*(3-2*t)
def family(r):
    th = math.degrees(math.atan2(abs(r[0]+0.23), r[1]-2.5)); z = r[2]
    if 18 <= th < 42 and z > 165: return 1
    if 42 <= th < 66: return 2
    if 66 <= th < 92 and 161 < z < 169.5: return 3
    if 92 <= th < 125 and z < 168 and r[1] < 0.5: return 4
    return 0
log = {1: [], 2: [], 3: [], 4: [], 'nape': []}
for k, v in G.items():
    if not isinstance(v, dict): continue
    if k.startswith('prim:') and v.get('group') in ('front_to_bun', 'side_to_bun', 'top_to_bun'):
        c = np.asarray(v['ctrl'], float); r = c[0]; n = len(c); sd = 1.0 if r[0] > -0.25 else -1.0; fam = family(r)
        if fam == 0: continue
        amp = {1: A1, 2: A2, 3: A3, 4: -A4}[fam]; ts = TS[fam]; soff = {1: S1, 2: -S2, 3: 0.0, 4: S4}[fam]; lx = {1: 0.15, 2: 0.25, 3: LX3, 4: 0.1}[fam]; new = c.copy(); it = int(ts*(n-1))
        for i in range(1, n):
            t = i/(n-1)
            if t >= ts: break
            w = math.sin(math.pi*t/ts); h0 = standoff(c[i])
            q = c[i]+np.array([sd*lx*abs(amp)*w, -DY*w*(0.6 if fam == 4 else 1.0), -amp*w])   # fam 4: amp negative -> moves UP early
            loc, nrm = nearest(q); new[i] = loc+nrm*max(h0+soff*w, 0.15)
        for i in range(it, min(n, it+5)):
            f = 1-sstep((i-it)/4.0); new[i] = c[i]+(new[max(1, it-1)]-c[max(1, it-1)])*f*0.5
        v['ctrl'] = [[round(float(x), 4) for x in p] for p in new]; log[fam].append(k)
    if k.startswith('nape_spine:'):
        j = int(k.split(':')[1]); c = np.asarray(v['ctrl'], float)
        if len(c) >= 3:
            mid = c[1].copy(); sgn = 1.0 if j % 2 == 0 else -1.0; mid[0] += sgn*NL; mid[2] += (0.5 if j % 3 == 0 else -0.5)*NLIFT*2
            loc, nrm = nearest(mid); h0 = standoff(c[1]); c[1] = loc+nrm*(max(h0, 0.1)+(NLIFT if j % 2 == 0 else 0.0))
            c[-1][2] += sgn*NENT+(0.5 if j % 3 == 0 else 0.0); v['ctrl'] = [[round(float(x), 4) for x in p] for p in c]; log['nape'].append(k)
json.dump(G, open(OUT, 'w')); print('GUIDES_EDIT2_OK', json.dumps({str(k): len(v) for k, v in log.items()}), json.dumps({str(k): v for k, v in log.items()})[:700])
