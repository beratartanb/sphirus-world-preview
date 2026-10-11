"""GD38 face edit of a DNA-order head (user, after GD37: lip sides still look odd and swollen in the side view; under-eye bags differ left/right).
 PS : perioral sides ("muzzle") pushed back: thickness ramp from the teeth front envelope (0 within 0.5 mm, full 3.5 mm in front), lateral weight 0 at |x| 0.8 -> 1 at 2.0..2.6 -> 0 at 3.7 cm,
      vertical 1 over z 154.4..157.0 fading to 153.4 / 158.0; dy = -PS mm (the inner lip lining in front of the teeth stays).
 UB : under-eye bags: the subject's RIGHT (-x) infraorbital / lower-lid bag zone replaced by UB x the aligned UV-continuous mirror of the LEFT (+x)
      side (GD36 good side); zone z 159.5..161.95, |x| 1.2..4.8 with ramps; the lower-lid margin stays (vertices within 2.5 mm of the right
      eyeball fixed, ramp to 6 mm); +x untouched.
Then K Laplacian passes on the displacement. Prints eyeball asymmetry (aligned) and the zone stats.
usage: blender -b --factory-startup --python gd38_edit.py -- <in.npy> <mirror_uv.npy (aligned mirror of in.npy)> <out.npy> [PS=2.5 mm] [UB=1.0] [K=4]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); from gd13_common import NS, MX, pkg, mirror_map
import mathutils
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]).astype(float); MA = np.load(a[1])[:NS].astype(float); OUT = a[2]
PS = (float(a[3]) if len(a) > 3 else 2.5)/10; UB = float(a[4]) if len(a) > 4 else 1.0; K = int(a[5]) if len(a) > 5 else 4
S = X[:NS]; T = np.asarray(pkg()['head']['triangles']); T = T[(T < NS).all(1)]
x = S[:, 0]-MX; ax = np.abs(x); y, z = S[:, 1], S[:, 2]
E = np.unique(np.sort(np.r_[T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]], 1), axis=0); I0 = np.r_[E[:, 0], E[:, 1]]; I1 = np.r_[E[:, 1], E[:, 0]]; DEG = np.bincount(I0, minlength=NS).astype(float)
def lap(F): acc = np.zeros_like(F); np.add.at(acc, I0, F[I1]); return acc/np.maximum(DEG, 1)[:, None]
def ss(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
bvh = BVHTree.FromPolygons([tuple(p) for p in S], [tuple(int(i) for i in t) for t in T]); dirv = mathutils.Vector((0, 1, 0))
occl = np.zeros(NS, bool)
for i in np.nonzero((y > 9.0) & (z > 152.6) & (z < 158.8) & (ax < 4.4))[0]:
    occl[i] = bvh.ray_cast(mathutils.Vector((S[i, 0], S[i, 1]+0.01, S[i, 2])), dirv, 4.0)[0] is not None
ow = np.where((y > 9.0) & ~occl, 1.0, 0.0)[:, None]
for _ in range(3): ow = np.minimum(ow, 0.5*ow+0.5*lap(ow)+0.2)   # soften the outer/inner boundary at the lip roll without spreading inward
ow = ow[:, 0]
D = np.zeros_like(S)
# PS perioral sides
wl = ss((ax-0.8)/1.2)*ss((3.7-ax)/1.1); wz = ss((z-153.4)/1.0)*ss((158.0-z)/1.0)
# PS: thickness ramp from the teeth front envelope (0 within 0.5 mm, full 3.5 mm in front), weight smoothed across the lip contact seam, and the
# mouth-corner pockets (occluded vertices around the commissure next to the canines) kept with a soft falloff (PK_R0 core, PK_R1 ramp).
TE = X[24049:28295]; tax = np.abs(TE[:, 0]-MX); tb = np.arange(0.0, 3.6, 0.1); tyb = np.full(len(tb), np.nan)
for i, b in enumerate(tb):
    mt = (tax >= b) & (tax < b+0.1) & (TE[:, 2] > 154.0) & (TE[:, 2] < 157.0)
    if mt.any(): tyb[i] = TE[mt, 1].max()
okt = ~np.isnan(tyb); yt = np.interp(ax, tb[okt]+0.05, tyb[okt], right=np.nan); yt = np.where(np.isnan(yt), 6.0, yt)
wth = ss((y-yt-0.05)/0.30)*(y > 9.0); wP = wl*wz*wth
for _ in range(int(os.environ.get('PS_SMOOTH', '12'))): wP = 0.5*wP+0.5*lap(wP[:, None])[:, 0]
from mathutils.kdtree import KDTree as _KD
pocket = occl & (ax > 1.7) & (ax < 2.7) & (z > 155.0) & (z < 156.1) & (y > 11.0); kdp = _KD(int(pocket.sum()))
for j, i in enumerate(np.nonzero(pocket)[0]): kdp.insert(tuple(S[i]), j)
kdp.balance(); dp = np.array([kdp.find(tuple(p))[2] if wP[i] > 1e-4 else 9.0 for i, p in enumerate(S)])
PK_R0, PK_R1 = float(os.environ.get('PK_R0', '0.15')), float(os.environ.get('PK_R1', '0.45')); wP = wP*ss((dp-PK_R0)/PK_R1)
D[:, 1] -= PS*wP
# UB under-eye bag mirror (-x side from +x)
ER = X[29725:30495]; EL = X[28955:29725]   # eyeR = subject's right (-x)
MM = mirror_map()[:NS]; Mr = S[MM].copy(); Mr[:, 0] = 2*MX-Mr[:, 0]; face = (y > 3) & (z > 148.5) & (z < 168) & ~((ax > 6.2) & (y < 4.6))
P, Q = Mr[face], S[face]; pc, qc = P.mean(0), Q.mean(0); U_, s_, Vt = np.linalg.svd((P-pc).T@(Q-qc)); dd = np.sign(np.linalg.det(Vt.T@U_.T)); R = Vt.T@np.diag([1, 1, dd])@U_.T
def amir(p): q = np.atleast_2d(p).copy(); q[:, 0] = 2*MX-q[:, 0]; return (q-pc)@R.T+qc
eyeR_c = ER.mean(0); eyeL_m = amir(EL.mean(0))[0]
from mathutils.kdtree import KDTree
kd = KDTree(len(ER))
for i, p in enumerate(ER): kd.insert(tuple(p), i)
kd.balance(); de = np.array([kd.find(tuple(p))[2] if (x[i] < 0 and z[i] > 159.0 and z[i] < 163.0 and ax[i] < 5.0) else 9.0 for i, p in enumerate(S)])
wU = ss((161.95-z)/0.35)*ss((z-159.5)/0.6)*ss((ax-1.2)/0.4)*ss((4.8-ax)/0.5)*ss((de-0.25)/0.35)*ss((y-8.0)/0.8)*(x < -0.6)
EYE = float(os.environ.get('EYE', '0'))   # EYE mode: the whole right eye region (eyeball + lids + bag + lower brow ridge) from the aligned mirror of the left
if EYE > 0:
    tE = eyeL_m-eyeR_c; Y_EYE = X[29725:30495]+EYE*tE   # eyeball moved rigidly onto the aligned mirror of the left eyeball
    dc = np.linalg.norm(S-eyeR_c, axis=1); R_IN, R_OUT = float(os.environ.get('EYE_RIN', '1.5')), float(os.environ.get('EYE_ROUT', '2.4'))
    wE = ss((R_OUT-dc)/(R_OUT-R_IN))*ss((-x-0.4)/0.5)*ss((y-7.0)/1.0)
    if os.environ.get('EYE_MODE', 'rigidbag') == 'mirror':
        D += EYE*wE[:, None]*(MA-S); wU = wE   # full mirror of the region (flips in the upper-lid fold / lateral canthus)
    else:   # rigid: the whole region follows the eyeball translation (lid shapes kept, lid margins stay on the eye); bag: below the lower lid
        wB = ss((eyeR_c[2]-0.55-z)/0.35)*ss((z-159.5)/0.6)*ss((ax-1.2)/0.4)*ss((4.8-ax)/0.5)*ss((de-0.25)/0.35)*ss((y-8.0)/0.8)*(x < -0.6)
        Dr = EYE*wE[:, None]*tE[None, :]; D += Dr+UB*wB[:, None]*((MA-S)-Dr); wU = wB
        BRW = float(os.environ.get('BRW', '0'))   # brow ridge above the upper-lid fold: mirror shape (the fold itself stays rigid)
        if BRW > 0:
            wBR = ss((z-163.2)/0.5)*ss((165.8-z)/0.7)*ss((ax-float(os.environ.get("BR_M0", "0.3")))/float(os.environ.get("BR_MW", "1.0")))*ss((5.6-ax)/0.6)*(x < 0)*ss((y-7.0)/1.0)
            D += BRW*wBR[:, None]*((MA-S)-Dr)
else:
    D += UB*wU[:, None]*(MA-S)
for _ in range(K): D = 0.5*D+0.5*lap(D)   # PS is symmetric; UB acts on -x only (its zone is > 1.2 cm from the midline)
Y = X.copy(); Y[:NS] = S+D
if EYE > 0:   # extra eye meshes (shell / edge / cartilage / lashes, 30495+) near the right eye follow the same rigid translation (render consistency)
    XE = X[30495:]; dce = np.linalg.norm(XE-eyeR_c, axis=1); wx = ss((R_OUT-dce)/(R_OUT-R_IN))*((XE[:, 0]-MX) < 0); Y[30495:] = XE+EYE*wx[:, None]*tE[None, :]
if EYE > 0: Y[29725:30495] = Y_EYE; print('GD38E EYE %.2f: right eyeball moved %s mm' % (EYE, np.round(EYE*tE*10, 2)))
np.save(OUT, Y)
d = np.linalg.norm(D, axis=1)*10; zb = wU > 0.5
print('GD38E eyes: eyeR(-x) - aligned mirror(eyeL) = %s mm' % np.round((eyeR_c-eyeL_m)*10, 2))
print('GD38E PS %.1f mm: moved>0.1mm %d, max dy %.2f mm | UB %.2f: bag zone verts %d, mean |mirror - X| there %.2f mm (p95 %.2f), max move %.2f mm' % (PS*10, int((wP*PS*10 > 0.1).sum()), -D[:, 1].min()*10, UB, int(zb.sum()), np.linalg.norm(MA-S, axis=1)[zb].mean()*10, np.percentile(np.linalg.norm(MA-S, axis=1)[zb]*10, 95), d[wU > 0].max() if (wU > 0).any() else 0))
print('GD38E total moved>0.1mm %d max %.2f mm, +x side max %.3f mm (PS only, symmetric)' % (int((d > 0.1).sum()), d.max(), d[x > 0.6].max()))
json.dump({'PS_mm': PS*10, 'UB': UB, 'K': K, 'eyeR_minus_mirror_eyeL_mm': ((eyeR_c-eyeL_m)*10).tolist(), 'bag_zone_verts': int(zb.sum()), 'max_mm': float(d.max())}, open(OUT.replace('.npy', '_edit.json'), 'w'), indent=1)
