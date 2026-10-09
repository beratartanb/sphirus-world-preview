"""GD16 CUSTOM EYEBROW groom from the REFERENCE brow measurement (gd16_browref.py stations, projected to the head skin by gd16_browproj.py).
Each brow (subject right = imgL, subject left = imgR, measured separately: natural asymmetry kept) is a band between the measured top and
bottom hair boundaries along its own 3D centre line (medial head -> body -> apex -> tail). Roots are sampled on the skin inside the band
(BVH projection); hair direction lives in the skin tangent plane and follows a brow hair-flow field:
  medial head (u < 0.14): fuzzy, upward (70-85 deg from the brow axis, slight lateral lean)
  head -> body transition: rotates toward the axis
  body (lower half of the band): up-and-out (~30 deg); (upper half): down-and-out (~-12 deg) -> hairs converge on the centre line
  apex -> tail (u > 0.7): outward and slightly down along the axis, thinning density and length to the tail tip
Hair length / density / thickness taper along u; per-hair jitter, mild curl, root stand-off (never inside the skin). Same Alembic layout as
the GD11 pass-O procedural brow (imports with HairStrandsFactory, no source mesh). Writes <out>/brow_main.abc, strands.npz, brow_build.json.
usage: blender -b --factory-startup --python gd16_brow.py -- <head.npy> <brow3d.json> <out_dir>
env: BR_N=2200 (candidate roots / brow)  BR_LEN=0.62 (cm body)  BR_SEED=11  BR_HEAD_DENS=0.62  BR_TAIL_DENS=0.45  BR_LIFT=0.035  BR_CURL=0.18
     BR_BODY_UP=30 BR_BODY_DOWN=-12 BR_HEAD_ANG=78 BR_TAIL_ANG=-14 (deg from the brow axis toward 'up')  BR_PAD=0.0 (cm band padding)  BR_ROOT_LO / BR_ROOT_HI (root sub-band, fractions bottom->top of the measured visible band; 0 / 1)  BR_HEADLEN=0.62 (head length factor)"""
import bpy, sys, os, json, math, numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import head_topology
a = sys.argv[sys.argv.index('--')+1:]; HEAD, B3D, OUT = a[0], a[1], a[2]; os.makedirs(OUT, exist_ok=True); E = lambda k, d: float(os.environ.get(k, d))
X = np.load(HEAD)[:24049]; T, MI = head_topology(); TT = T[(MI == 0) & (T.max(1) < 24049)]
bvh = BVHTree.FromPolygons([tuple(map(float, p)) for p in X], [tuple(int(i) for i in t) for t in TT])
fn = np.cross(X[TT[:, 1]]-X[TT[:, 0]], X[TT[:, 2]]-X[TT[:, 0]]); fn = -fn/np.maximum(np.linalg.norm(fn, axis=1), 1e-9)[:, None]   # outward (DNA winding inward)
def nearest(p): loc, nrm, idx, d = bvh.find_nearest(Vector(p)); return np.asarray(loc), np.asarray(fn[idx])
rng = np.random.default_rng(int(E('BR_SEED', '11'))); N = int(E('BR_N', '2200')); NPTS = 8; LEN = E('BR_LEN', '0.62'); PAD = E('BR_PAD', '0.0')
B = json.load(open(B3D)); strands = []; tags = []
def sstep(t): t = min(max(t, 0.0), 1.0); return t*t*(3-2*t)
for side in ('imgL', 'imgR'):
    st = B[side]; TOP = np.array([s['top'] for s in st]); BOT = np.array([s['bot'] for s in st]); CEN = 0.5*(TOP+BOT)
    seg = np.linalg.norm(np.diff(CEN, axis=0), axis=1); U = np.r_[0, np.cumsum(seg)]/seg.sum()   # arc-length parameter, 0 = medial head
    def at(Arr, u): return np.array([np.interp(u, U, Arr[:, k]) for k in range(3)])
    n_ok = 0
    for k in range(N):
        u = rng.random()
        dens = np.interp(u, [0.0, 0.06, 0.16, 0.7, 0.88, 1.0], [E('BR_HEAD_DENS', '0.62')*0.7, E('BR_HEAD_DENS', '0.62'), 1.0, 1.0, 0.75, E('BR_TAIL_DENS', '0.45')])
        if rng.random() > dens: continue
        v = rng.uniform(-1, 1); t_, b_ = at(TOP, u), at(BOT, u); c_ = 0.5*(t_+b_); up = t_-b_; hh = 0.5*np.linalg.norm(up)+PAD; up = up/max(np.linalg.norm(up), 1e-6)
        lo_, hi_ = E('BR_ROOT_LO', '0.0'), E('BR_ROOT_HI', '1.0'); fr = lo_+(hi_-lo_)*(v+1)/2   # roots in a sub-band: hairs grow up-out, so the VISIBLE band sits above the roots
        q0 = b_+(t_-b_)*fr+up*PAD*v; loc, nrm = nearest(q0)
        ax = at(CEN, min(u+0.02, 1.0))-at(CEN, max(u-0.02, 0.0)); ax = ax/max(np.linalg.norm(ax), 1e-6)   # medial -> lateral axis
        if u < 0.14: ang = E('BR_HEAD_ANG', '78')+rng.normal(0, 9)
        elif u < 0.3: s = sstep((u-0.14)/0.16); ang = (1-s)*E('BR_HEAD_ANG', '78')+s*(E('BR_BODY_UP', '30') if v < 0 else E('BR_BODY_DOWN', '-12'))+rng.normal(0, 7)
        elif u < 0.7: w = sstep((v+1)/2); ang = (1-w)*E('BR_BODY_UP', '30')+w*E('BR_BODY_DOWN', '-12')+rng.normal(0, 6)
        else: s = sstep((u-0.7)/0.3); w = sstep((v+1)/2); body = (1-w)*E('BR_BODY_UP', '30')+w*E('BR_BODY_DOWN', '-12'); ang = (1-s)*body+s*E('BR_TAIL_ANG', '-14')+rng.normal(0, 5)
        th = math.radians(ang); upt = up-nrm*np.dot(up, nrm); upt /= max(np.linalg.norm(upt), 1e-6); axt = ax-nrm*np.dot(ax, nrm); axt /= max(np.linalg.norm(axt), 1e-6)
        d = math.cos(th)*axt+math.sin(th)*upt; d /= np.linalg.norm(d)
        L = LEN*float(np.interp(u, [0.0, 0.1, 0.3, 0.7, 1.0], [E('BR_HEADLEN', '0.62'), 0.8, 1.0, 0.92, 0.6]))*(0.75+0.5*rng.random())
        bvec = np.cross(nrm, d); curl = E('BR_CURL', '0.18')*rng.normal(0, 1); pts = []
        for i in range(NPTS):
            t = i/(NPTS-1); p_ = loc+d*L*t+nrm*(0.015+E('BR_LIFT', '0.035')*math.sin(math.pi*min(t*1.25, 1.0))*(0.6+0.8*rng.random()))+bvec*curl*L*t*t
            l2, n2 = nearest(p_); h_ = float(np.dot(p_-l2, n2)); p_ = l2+n2*max(h_, 0.012); pts.append(p_)
        strands.append(np.asarray(pts)); tags.append('brow:%s:%.2f:%.2f' % (side, u, v)); n_ok += 1
    print('BROW_SIDE', side, n_ok)
S = np.asarray(strands); np.savez_compressed(os.path.join(OUT, 'strands.npz'), main=S, loose=np.zeros((0, NPTS, 3))); json.dump({'main': tags, 'loose': []}, open(os.path.join(OUT, 'strand_tags.json'), 'w'))
json.dump({'n': len(S), 'brow3d': B3D, 'head': HEAD, 'params': {k: v for k, v in os.environ.items() if k.startswith('BR_')}}, open(os.path.join(OUT, 'brow_build.json'), 'w'))
cu = bpy.data.curves.new('brow_main', 'CURVE'); cu.dimensions = '3D'
for s in S:
    sp = cu.splines.new('POLY'); sp.points.add(len(s)-1)
    for i, (x, y, z) in enumerate(s): sp.points[i].co = (x, -z, y, 1)
ob = bpy.data.objects.new('brow_main', cu); bpy.context.scene.collection.objects.link(ob)
for o in bpy.context.scene.objects: o.select_set(o == ob)
fp = os.path.join(OUT, 'brow_main.abc'); bpy.ops.wm.alembic_export(filepath=fp, selected=True, start=1, end=1, curves_as_mesh=False, global_scale=1.0); print('BROW_OK', len(S), fp)
