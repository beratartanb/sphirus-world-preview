"""GD11 refinement O: PROCEDURAL EYEBROW groom (editable, pipeline-compatible Alembic) rooted on the given DNA-order head npy.
Each brow is a band along an authored centre curve (head frame, UE cm): inner head -> body -> arch peak -> tail; per-section half-height
(thickness), hair length, direction angle (deg from horizontal outward; + = up), density and curl are interpolated along the curve.
Roots are sampled on the head surface (BVH projection) inside the band, hairs grow along the surface-tangent direction with a slight lift,
3 noise layers break symmetry; left/right differ slightly (asymmetry seed). Writes <out>/brow_main.abc (+ brow_strands.npz, brow_build.json).
usage: blender -b --factory-startup --python blender_g11ro_brow.py -- <head.npy> <out_dir>
env (all optional): BR_N=900 (hairs per brow)  BR_LEN=0.62 (cm, body)  BR_WIDTH=0.52 (cm, body half-height*2)  BR_Z=0.0 (global height offset cm)
     BR_INNER_X=1.25 BR_INNER_Z=164.55  BR_PEAK_X=3.55 BR_PEAK_Z=165.55  BR_TAIL_X=5.55 BR_TAIL_Z=164.45  BR_TAIL_W=0.22  BR_INNER_W=0.58
     BR_ANG_INNER=58 BR_ANG_BODY=14 BR_ANG_TAIL=-22 (deg)  BR_LIFT=0.06 (cm stand-off growth)  BR_CURL=0.25  BR_ASYM=0.12  BR_SEED=7"""
import bpy, sys, os, json, math, numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import head_topology
a = sys.argv[sys.argv.index('--')+1:]; HEAD, OUT = a[0], a[1]; os.makedirs(OUT, exist_ok=True); E = lambda k, d: float(os.environ.get(k, d))
X = np.load(HEAD)[:24049]; T, MI = head_topology(); TT = T[(MI == 0) & (T.max(1) < 24049)]; MX = -0.23
bvh = BVHTree.FromPolygons([tuple(map(float, p)) for p in X], [tuple(int(i) for i in t) for t in TT]); fn = np.cross(X[TT[:, 1]]-X[TT[:, 0]], X[TT[:, 2]]-X[TT[:, 0]]); fn = -fn/np.maximum(np.linalg.norm(fn, axis=1), 1e-9)[:, None]
def nearest(p): loc, nrm, idx, d = bvh.find_nearest(Vector(p)); return np.asarray(loc), np.asarray(fn[idx])
def sstep(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
rng = np.random.default_rng(int(E('BR_SEED', '7'))); N = int(E('BR_N', '900')); NPTS = 8
LEN, WID, DZ = E('BR_LEN', '0.62'), E('BR_WIDTH', '0.52'), E('BR_Z', '0.0')
P_IN, P_PK, P_TL = (E('BR_INNER_X', '1.25'), E('BR_INNER_Z', '164.55')+DZ), (E('BR_PEAK_X', '3.55'), E('BR_PEAK_Z', '165.55')+DZ), (E('BR_TAIL_X', '5.55'), E('BR_TAIL_Z', '164.45')+DZ)
W_IN, W_TL = E('BR_INNER_W', '0.58'), E('BR_TAIL_W', '0.22'); A_IN, A_BD, A_TL = E('BR_ANG_INNER', '58'), E('BR_ANG_BODY', '14'), E('BR_ANG_TAIL', '-22'); LIFT, CURL, ASYM = E('BR_LIFT', '0.06'), E('BR_CURL', '0.25'), E('BR_ASYM', '0.12')
def centre(u, sd):   # u in [0,1] along the brow (0 = inner head, 1 = tail tip); quadratic through inner / peak (at u=0.62) / tail
    xi, zi = P_IN; xp, zp = P_PK; xt, zt = P_TL; up = 0.62
    if u < up: s = u/up; x = xi+(xp-xi)*s; z = zi+(zp-zi)*(1-(1-s)**2)
    else: s = (u-up)/(1-up); x = xp+(xt-xp)*s; z = zp+(zt-zp)*(s**1.6)
    x += ASYM*0.25*sd*math.sin(u*3.0); z += ASYM*0.5*(0.5-abs(sd-0.5))*math.sin(u*5.0+sd)
    return x, z
def half_w(u):   # band half-height (cm)
    w = np.interp(u, [0.0, 0.18, 0.62, 0.86, 1.0], [W_IN, WID, WID*0.92, WID*0.55, W_TL]); return 0.5*w
def ang(u): return float(np.interp(u, [0.0, 0.14, 0.3, 0.62, 0.85, 1.0], [A_IN, A_IN*0.75, A_BD+6, A_BD, A_BD*0.4+A_TL*0.6, A_TL]))
def hlen(u): return LEN*float(np.interp(u, [0.0, 0.2, 0.62, 1.0], [0.9, 1.05, 1.0, 0.7]))
def dens(u): return float(np.interp(u, [0.0, 0.08, 0.25, 0.7, 0.9, 1.0], [E('BR_IN_DENS', '0.35'), 0.8, 1.0, 1.0, 0.5+0.5*E('BR_TAIL_DENS', '0.3'), E('BR_TAIL_DENS', '0.3')]))
strands = []; tags = []
for side in (1.0, -1.0):
    sd = 0.5+0.5*side*ASYM
    for k in range(N):
        u = rng.random()
        if rng.random() > dens(u): continue
        x0, z0 = centre(u, sd); hw = half_w(u); v = rng.uniform(-1, 1); zr = z0+v*hw*(1-0.25*abs(v))
        xr = MX+side*(x0+rng.normal(0, 0.05)); q0 = np.array([xr, 14.0, zr]); loc, nrm = nearest(q0)            # project onto the brow skin (front-facing)
        # growth direction: outward (+side x) rotated by ang(u) upward, in the tangent plane
        th = math.radians(ang(u)+rng.normal(0, 7)); d = np.array([side*math.cos(th), 0.0, math.sin(th)]); d -= nrm*np.dot(d, nrm); d /= np.linalg.norm(d)
        L = hlen(u)*(0.75+0.5*rng.random()); pts = []; p = loc.copy()+nrm*0.02; b = np.cross(nrm, d); curl = CURL*rng.normal(0, 1)
        for i in range(NPTS):
            t = i/(NPTS-1); p_ = loc+d*L*t+nrm*(0.02+LIFT*math.sin(math.pi*min(t*1.3, 1.0))*(0.6+0.8*rng.random()))+b*curl*L*t*t
            l2, n2 = nearest(p_); h_ = float(np.dot(p_-l2, n2)); p_ = l2+n2*max(h_, 0.015)   # stay on the skin, never inside
            pts.append(p_)
        strands.append(np.asarray(pts)); tags.append('brow:%s:%.2f' % ('L' if side > 0 else 'R', u))
S = np.asarray(strands); np.savez_compressed(os.path.join(OUT, 'strands.npz'), main=S, loose=np.zeros((0, NPTS, 3))); json.dump({'main': tags, 'loose': []}, open(os.path.join(OUT, 'strand_tags.json'), 'w')); json.dump({'n': len(S), 'params': {k: v for k, v in os.environ.items() if k.startswith('BR_')}}, open(os.path.join(OUT, 'brow_build.json'), 'w'))
cu = bpy.data.curves.new('brow_main', 'CURVE'); cu.dimensions = '3D'
for s in S:
    sp = cu.splines.new('POLY'); sp.points.add(len(s)-1)
    for i, (x, y, z) in enumerate(s): sp.points[i].co = (x, -z, y, 1)
ob = bpy.data.objects.new('brow_main', cu); bpy.context.scene.collection.objects.link(ob)
for o in bpy.context.scene.objects: o.select_set(o == ob)
fp = os.path.join(OUT, 'brow_main.abc'); bpy.ops.wm.alembic_export(filepath=fp, selected=True, start=1, end=1, curves_as_mesh=False, global_scale=1.0); print('BROW_OK', len(S), fp)
