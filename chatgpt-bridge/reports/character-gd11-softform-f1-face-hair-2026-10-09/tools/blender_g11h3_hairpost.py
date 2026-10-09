"""pass F (hair stages 2 / 3): POST-PROCESS of a built hair dir (strands.npz + strand_tags.json) without a rebuild (a rebuild re-clusters locks).
Stage 2 (mass / silhouette):
  BACK_K   k: thins the hair layer behind the head: every strand point p moves toward its nearest scalp point q, p' = q + (p - q) * (1 - (1 - k) w),
           w = along-strand weight (0 at the root, 1 from 25 %) * region weight (back: y < BACK_Y0, fading over 3 cm; above z BACK_Z0 fading over 2 cm)
  BACK_DROP f: removes a random fraction f of the MAIN strands whose root lies in the back mass (root y < BACK_Y0 and z > BACK_Z0), so the outer shell
           becomes airier and the bun reads as its own form (loose groom untouched)
  BUN_S s / BUN_PULL cm: loose 'mess_bun' / 'mess_loop' strands scaled about the bun centre (median of their points) and moved toward the head
Stage 3 (separated fine strands): WISPS = JSON list of {"tags": [...], "frac": f, "deg": d, "lmin": a, "lmax": b, "wave": cm, "box": [x0,x1,y0,y1,z0,z1] (root, |x|),
           "droop": cm} - copies of matching strands (main or loose, by tag prefix) rotated about the root <= deg, length a..b (extrapolated beyond 1 along the
           last segment + droop), fine lateral wave; tagged 'wisp:<first tag>' and written to the LOOSE groom.
usage: blender -b --python blender_g11h3_hairpost.py -- <src hair dir> <dst hair dir>   env BACK_K BACK_Y0 BACK_Z0 BACK_DROP BUN_S BUN_PULL WISPS SEED"""
import bpy, sys, os, json, math, shutil, numpy as np
from mathutils.kdtree import KDTree
a = sys.argv[sys.argv.index('--')+1:]; SRC, DST = a[0], a[1]; os.makedirs(DST, exist_ok=True); MX = -0.23
Z = np.load(os.path.join(SRC, 'strands.npz')); TG = json.load(open(os.path.join(SRC, 'strand_tags.json'))); M = Z['main'].astype(np.float64); L = Z['loose'].astype(np.float64)
MT, LT = list(TG['main']), list(TG['loose'])
env = {l.split('=', 1)[0]: l.split('=', 1)[1] for l in open(os.path.join(SRC, 'build_env.txt'), encoding='utf-8').read().splitlines() if '=' in l}
H = np.load(env.get('SPH_HEAD_NPY', 'Saved/Codex/CharacterGuardian7_20261002/headC8.npy'))[:24049]
rng = np.random.default_rng(int(os.environ.get('SEED', '4242'))); E = lambda k, d: float(os.environ.get(k, d))
def ss(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
def sparam(A):
    seg = np.linalg.norm(np.diff(A, axis=1), axis=2); s = np.c_[np.zeros(len(A)), np.cumsum(seg, 1)]; return s/np.maximum(s[:, -1:], 1e-6)
rep = {}
BK, BY0, BZ0 = E('BACK_K', 1.0), E('BACK_Y0', 1.0), E('BACK_Z0', 156.0)
if BK < 1.0:
    hv = H[(H[:, 1] < 6.0) & (H[:, 2] > 150.0)]; kd = KDTree(len(hv))
    for i, p in enumerate(hv): kd.insert(p.tolist(), i)
    kd.balance()
    def thin(A):
        if not len(A): return A, 0.0
        P = A.reshape(-1, 3); Q = np.array([kd.find(p.tolist())[0] for p in P]).reshape(A.shape)
        w = ss(sparam(A)/0.25)*ss((BY0-A[..., 1])/3.0)*ss((A[..., 2]-BZ0)/2.0)
        B = Q+(A-Q)*(1-(1-BK)*w)[..., None]; return B, float(np.linalg.norm(B-A, axis=2).max())
    M, m1 = thin(M); L, m2 = thin(L); rep['back_thin'] = dict(k=BK, max_move_main=round(m1, 2), max_move_loose=round(m2, 2)); print('BACKTHIN k %.2f max move main %.2f loose %.2f cm' % (BK, m1, m2))
BD = E('BACK_DROP', 0.0)
if BD > 0:
    r0 = M[:, 0]; cand = np.nonzero((r0[:, 1] < BY0) & (r0[:, 2] > BZ0))[0]; drop = rng.choice(cand, int(len(cand)*BD), replace=False); keep = np.ones(len(M), bool); keep[drop] = False
    M = M[keep]; MT = [t for t, k_ in zip(MT, keep) if k_]; rep['back_drop'] = dict(frac=BD, candidates=int(len(cand)), removed=int(len(drop))); print('BACKDROP removed %d of %d back-mass main strands' % (len(drop), len(cand)))
BS, BPULL = E('BUN_S', 1.0), E('BUN_PULL', 0.0)
if BS != 1.0 or BPULL:
    bi = [i for i, t in enumerate(LT) if t in ('mess_bun', 'mess_loop')]; Pb = L[bi]; c = np.median(Pb.reshape(-1, 3), 0); hc = np.array([MX, 3.0, 162.0]); dv = (hc-c)/np.linalg.norm(hc-c)
    w = ss(sparam(Pb)/0.3)[..., None]; L[bi] = Pb+((c+(Pb-c)*BS+dv*BPULL)-Pb)*w; rep['bun'] = dict(scale=BS, pull_cm=BPULL, centre=c.round(2).tolist(), n=len(bi)); print('BUN scale %.2f pull %.2f cm centre %s (%d strands)' % (BS, BPULL, c.round(2).tolist(), len(bi)))
WS = json.loads(os.environ.get('WISPS', '[]')); NW = []; NWT = []
for sp in WS:
    pool = [(M, MT, i) for i, t in enumerate(MT) if any(t.startswith(p) for p in sp['tags'])]+[(L, LT, i) for i, t in enumerate(LT) if any(t.startswith(p) for p in sp['tags'])]
    if 'box' in sp:
        x0, x1, y0, y1, z0, z1 = sp['box']; pool = [(A, T_, i) for A, T_, i in pool if x0 <= abs(A[i, 0, 0]-MX) <= x1 and y0 <= A[i, 0, 1] <= y1 and z0 <= A[i, 0, 2] <= z1]
    n = int(len(pool)*sp['frac']); pick = rng.choice(len(pool), n, replace=False) if n else []; DEG = math.radians(sp.get('deg', 8))
    for j in pick:
        A, T_, i = pool[j]; S = A[i].copy(); r0 = S[0]; ax_ = rng.normal(size=3); ax_ /= np.linalg.norm(ax_); th = rng.uniform(-DEG, DEG)
        K = np.array([[0, -ax_[2], ax_[1]], [ax_[2], 0, -ax_[0]], [-ax_[1], ax_[0], 0]]); Rm = np.eye(3)+math.sin(th)*K+(1-math.cos(th))*K@K; S = r0+(S-r0)@Rm.T
        f = rng.uniform(sp.get('lmin', 0.8), sp.get('lmax', 1.05)); s = sparam(S[None])[0]
        if f <= 1.0:
            tt = np.linspace(0, f, len(S)); S = np.c_[np.interp(tt, s, S[:, 0]), np.interp(tt, s, S[:, 1]), np.interp(tt, s, S[:, 2])]
        else:   # extend beyond the tip along the last direction + droop
            Ltot = np.linalg.norm(np.diff(S, axis=0), axis=1).sum(); d_ = S[-1]-S[-3]; d_ /= max(np.linalg.norm(d_), 1e-6); ext = (f-1)*Ltot
            tail = S[-1]+np.outer(np.linspace(0, 1, 9)[1:], d_*ext)+np.outer(np.linspace(0, 1, 9)[1:]**2, [0, 0, -sp.get('droop', 0.4)])
            S2 = np.r_[S, tail]; s2 = sparam(S2[None])[0]; tt = np.linspace(0, 1, len(S)); S = np.c_[np.interp(tt, s2, S2[:, 0]), np.interp(tt, s2, S2[:, 1]), np.interp(tt, s2, S2[:, 2])]
        if sp.get('fall'):   # turn the strand about its root so it falls forward / down over the hairline edge (keeps its own curl)
            v0 = S[-1]-S[0]; v0 /= max(np.linalg.norm(v0), 1e-6); lat = np.sign(S[0, 0]-MX)*sp.get('fall_lat', 0.35)
            tg = np.array([lat, sp.get('fall_fwd', 0.55), -1.0])+rng.normal(size=3)*0.12; tg /= np.linalg.norm(tg); ax2 = np.cross(v0, tg); sn = np.linalg.norm(ax2)
            if sn > 1e-6:
                ax2 /= sn; ang = math.atan2(sn, float(v0@tg)); K2 = np.array([[0, -ax2[2], ax2[1]], [ax2[2], 0, -ax2[0]], [-ax2[1], ax2[0], 0]])
                R2 = np.eye(3)+math.sin(ang)*K2+(1-math.cos(ang))*K2@K2; S = S[0]+(S-S[0])@R2.T
            S[:, 1] = np.maximum(S[:, 1], S[0, 1]-0.1+np.linspace(0, 0.25, len(S)))   # stay in front of the root (no strands into the scalp)
            below = np.nonzero(S[:, 2] < sp.get('zmin', 164.6))[0]                     # never below the brow line: shorten the strand there (no clamped flat run)
            if len(below) and below[0] >= 3:
                S2 = S[:below[0]]; s2 = sparam(S2[None])[0]; tt = np.linspace(0, 1, len(S)); S = np.c_[np.interp(tt, s2, S2[:, 0]), np.interp(tt, s2, S2[:, 1]), np.interp(tt, s2, S2[:, 2])]
            elif len(below): continue
        t = np.linspace(0, 1, len(S)); side = np.cross(S[-1]-S[0], [0, 0, 1.0]); side /= max(np.linalg.norm(side), 1e-6)
        S = S+np.outer(np.sin(t*math.pi*rng.uniform(2, 4)+rng.uniform(0, 6.28))*sp.get('wave', 0.12)*t, side)
        NW.append(S); NWT.append('wisp:'+sp['tags'][0])
    rep.setdefault('wisps', []).append(dict(tags=sp['tags'], pool=len(pool), added=int(n))); print('WISPS %s pool %d added %d' % (sp['tags'], len(pool), n))
if NW: L = np.concatenate([L, np.asarray(NW)], 0); LT += NWT
def export(strands, name):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'
    for s in strands:
        sp = cu.splines.new('POLY'); sp.points.add(len(s)-1)
        for i, (x, y, z) in enumerate(s): sp.points[i].co = (x, -z, y, 1)
    ob = bpy.data.objects.new(name, cu); bpy.context.scene.collection.objects.link(ob)
    for o in bpy.context.scene.objects: o.select_set(o == ob)
    bpy.ops.wm.alembic_export(filepath=os.path.join(DST, name+'.abc'), selected=True, start=1, end=1, curves_as_mesh=False, global_scale=1.0)
    bpy.data.objects.remove(ob, do_unlink=True); print('EXPORTED', name, len(strands))
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
export(M, 'hair_main'); export(L, 'hair_loose')
np.savez_compressed(os.path.join(DST, 'strands.npz'), main=M.astype(np.float32), loose=L.astype(np.float32)); json.dump({'main': MT, 'loose': LT}, open(os.path.join(DST, 'strand_tags.json'), 'w'))
shutil.copy(os.path.join(SRC, 'build_env.txt'), os.path.join(DST, 'build_env.txt'))
rep.update(src=SRC, main=len(M), loose=len(L), env={k: os.environ.get(k) for k in ('BACK_K', 'BACK_Y0', 'BACK_Z0', 'BACK_DROP', 'BUN_S', 'BUN_PULL', 'WISPS', 'SEED')})
json.dump(rep, open(os.path.join(DST, 'postprocess.json'), 'w'), indent=1); print('H3_OK', DST, json.dumps({k: v for k, v in rep.items() if k != 'env'}))
