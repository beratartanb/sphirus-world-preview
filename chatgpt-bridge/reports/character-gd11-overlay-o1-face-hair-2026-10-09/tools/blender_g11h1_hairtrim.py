"""pass H1 / H2: POST-PROCESS of a built hair (strands.npz + strand_tags.json of blender_g11rq_hair.py) without a rebuild (a rebuild re-clusters
every lock). Writes a new hair dir (hair_main.abc / hair_loose.abc / strands.npz / strand_tags.json / build_env.txt copy) for gd11rcc_hair_cycle.sh SKIP_BUILD=1.
H1 (TRIM): lateral thinning of the hair layer outside the scalp, roots fixed: for every strand point behind the face plane (fade y 4 -> 7)
  |x - MX| = r_scalp(y, z) + (|x - MX| - r_scalp) * k(z), k from TRIM_K "k_upper,k_ear,k_nape" (z bands 166-176 / 158-166 / <158, smooth),
  weighted along the strand (0 at the root, 1 from 25 % of its length); r_scalp = head half-width in (y, z) bins from SPH_HEAD_NPY.
H2 (WISPS): adds separated fine strands: copies WISP_FRAC of the loose 'fly' / 'mess_face' / 'mess_ear' / 'mess_bun' strands with a small rotation
  about the root (<= WISP_DEG), length 0.75..1.05 and a fine lateral wave, tagged 'wisp'.
usage: blender -b --python blender_g11h1_hairtrim.py -- <src hair dir> <dst hair dir>   env TRIM_K, WISP_FRAC (0 = off), WISP_DEG, SEED"""
import bpy, sys, os, json, math, shutil, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; SRC, DST = a[0], a[1]; os.makedirs(DST, exist_ok=True); MX = -0.23
Z = np.load(os.path.join(SRC, 'strands.npz')); TG = json.load(open(os.path.join(SRC, 'strand_tags.json'))); M = Z['main'].astype(np.float64); L = Z['loose'].astype(np.float64)
env = {l.split('=', 1)[0]: l.split('=', 1)[1] for l in open(os.path.join(SRC, 'build_env.txt'), encoding='utf-8').read().splitlines() if '=' in l}
H = np.load(env.get('SPH_HEAD_NPY', 'Saved/Codex/CharacterGuardian7_20261002/headC8.npy'))[:24049]
def ss(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
# scalp half-width map r(y, z): 0.5 cm bins, filled by nearest neighbours where empty
yb = np.arange(-12.0, 14.0, 0.5); zb = np.arange(146.0, 180.0, 0.5); RS = np.full((len(yb), len(zb)), np.nan)
iy = np.clip(((H[:, 1]-yb[0])/0.5).astype(int), 0, len(yb)-1); iz = np.clip(((H[:, 2]-zb[0])/0.5).astype(int), 0, len(zb)-1); ax = np.abs(H[:, 0]-MX)
for i, j, v in zip(iy, iz, ax): RS[i, j] = v if np.isnan(RS[i, j]) else max(RS[i, j], v)
ok = ~np.isnan(RS); P_ = np.argwhere(ok); V_ = RS[ok]
for i, j in np.argwhere(~ok): k_ = np.argmin(((P_-[i, j])**2).sum(1)); RS[i, j] = V_[k_]
def rscalp(p): i = np.clip(((p[..., 1]-yb[0])/0.5).astype(int), 0, len(yb)-1); j = np.clip(((p[..., 2]-zb[0])/0.5).astype(int), 0, len(zb)-1); return RS[i, j]
KU, KE, KN = [float(v) for v in os.environ.get('TRIM_K', '1,1,1').split(',')]
def kz(z): return KN+(KE-KN)*ss((z-157.0)/2.0)+(KU-KE)*ss((z-165.0)/2.0)
def trim(A):
    if (KU, KE, KN) == (1, 1, 1): return A, 0.0
    n, np_, _ = A.shape; seg = np.linalg.norm(np.diff(A, axis=1), axis=2); s = np.c_[np.zeros(n), np.cumsum(seg, 1)]; s /= np.maximum(s[:, -1:], 1e-6)
    ws = ss(s/0.25); wy = 1-ss((A[..., 1]-4.0)/3.0); w = ws*wy
    r = rscalp(A); d = np.abs(A[..., 0]-MX); out = np.maximum(d-r, 0); k = kz(A[..., 2]); dn = np.where(d > r, r+out*(1-(1-k)*w), d)
    B = A.copy(); B[..., 0] = MX+np.sign(A[..., 0]-MX)*dn; return B, float(np.abs(B-A).max())
M2, mm = trim(M); L2, ml = trim(L)
print('H1TRIM k %.2f/%.2f/%.2f max move main %.2f loose %.2f cm' % (KU, KE, KN, mm, ml))
LT = list(TG['loose']); WF = float(os.environ.get('WISP_FRAC', '0'))
if WF > 0:
    rng = np.random.default_rng(int(os.environ.get('SEED', '909'))); src = [i for i, t in enumerate(LT) if t in ('fly', 'mess_face', 'mess_ear', 'mess_bun')]
    pick = rng.choice(src, int(len(src)*WF), replace=False); NW = []
    DEG = math.radians(float(os.environ.get('WISP_DEG', '8')))
    for i in pick:
        S = L2[i].copy(); r0 = S[0]; ax_ = rng.normal(size=3); ax_ /= np.linalg.norm(ax_); th = rng.uniform(-DEG, DEG)
        K = np.array([[0, -ax_[2], ax_[1]], [ax_[2], 0, -ax_[0]], [-ax_[1], ax_[0], 0]]); Rm = np.eye(3)+math.sin(th)*K+(1-math.cos(th))*K@K
        S = r0+(S-r0)@Rm.T; f = rng.uniform(0.75, 1.05); S = r0+(S-r0)*f
        t = np.linspace(0, 1, len(S))[:, None]; S = S+np.c_[np.sin(t[:, 0]*math.pi*rng.uniform(2, 4)+rng.uniform(0, 6.28)), np.zeros(len(S)), np.zeros(len(S))]*0.12*t
        NW.append(S)
    L2 = np.concatenate([L2, np.asarray(NW)], 0); LT += ['wisp']*len(NW); print('H2WISP added %d separated strands (from %d candidates, %.0f deg)' % (len(NW), len(src), math.degrees(DEG)))
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
export(M2, 'hair_main'); export(L2, 'hair_loose')
np.savez_compressed(os.path.join(DST, 'strands.npz'), main=M2.astype(np.float32), loose=L2.astype(np.float32)); json.dump({'main': TG['main'], 'loose': LT}, open(os.path.join(DST, 'strand_tags.json'), 'w'))
shutil.copy(os.path.join(SRC, 'build_env.txt'), os.path.join(DST, 'build_env.txt'))
json.dump({'src': SRC, 'TRIM_K': [KU, KE, KN], 'WISP_FRAC': WF, 'WISP_DEG': os.environ.get('WISP_DEG', '8'), 'main': len(M2), 'loose': len(L2)}, open(os.path.join(DST, 'postprocess.json'), 'w'))
print('H1_OK', DST)
