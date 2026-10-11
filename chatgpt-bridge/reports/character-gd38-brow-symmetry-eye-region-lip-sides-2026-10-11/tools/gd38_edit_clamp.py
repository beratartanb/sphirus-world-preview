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
# PS mode CLAMP (default): every vertex in front of the teeth moves back by min(PS x weight, clearance to the teeth behind it - 0.5 mm);
# clearance from a dilated (x, z) grid of the teeth front envelope; vertices behind the teeth front (mouth bag) do not move.
TE = X[24049:28295]; CS_ = 0.05; gx = np.floor((TE[:, 0]-MX)/CS_).astype(int); gz = np.floor(TE[:, 2]/CS_).astype(int); env = {}
for i_, j_, yy in zip(gx, gz, TE[:, 1]):
    for di in (-2, -1, 0, 1, 2):
        for dj in (-2, -1, 0, 1, 2):
            k_ = (i_+di, j_+dj); env[k_] = max(env.get(k_, -99.0), yy)
vx = np.floor(x/CS_).astype(int); vz = np.floor(z/CS_).astype(int); ty = np.array([env.get((i_, j_), -99.0) for i_, j_ in zip(vx, vz)])
infront = ss((y-ty+0.02)/0.08); clear = np.where(ty > -50, y-ty, 9.9)
wP = wl*wz*infront*(y > 9.0)
for _ in range(int(os.environ.get('PS_SMOOTH', '12'))): wP = 0.5*wP+0.5*lap(wP[:, None])[:, 0]
dyP = -np.minimum(PS*wP, np.maximum(clear-0.05, 0.0))
for _ in range(3):   # smooth the clamped field, re-clamp (no vertex closer than 0.5 mm to the teeth behind it)
    dyP = 0.5*dyP+0.5*lap(dyP[:, None])[:, 0]; dyP = -np.minimum(-dyP, np.maximum(clear-0.05, 0.0))
D[:, 1] += dyP
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
D += UB*wU[:, None]*(MA-S)
for _ in range(K): D = 0.5*D+0.5*lap(D)   # PS is symmetric; UB acts on -x only (its zone is > 1.2 cm from the midline)
Y = X.copy(); Y[:NS] = S+D; np.save(OUT, Y)
d = np.linalg.norm(D, axis=1)*10; zb = wU > 0.5
print('GD38E eyes: eyeR(-x) - aligned mirror(eyeL) = %s mm' % np.round((eyeR_c-eyeL_m)*10, 2))
print('GD38E PS %.1f mm (clamped to teeth clearance): moved>0.1mm %d, max dy %.2f mm | UB %.2f: bag zone verts %d, mean |mirror - X| there %.2f mm (p95 %.2f), max move %.2f mm' % (PS*10, int((-dyP*10 > 0.1).sum()), -D[:, 1].min()*10, UB, int(zb.sum()), np.linalg.norm(MA-S, axis=1)[zb].mean()*10, np.percentile(np.linalg.norm(MA-S, axis=1)[zb]*10, 95), d[wU > 0].max() if (wU > 0).any() else 0))
print('GD38E total moved>0.1mm %d max %.2f mm, +x side max %.3f mm (PS only, symmetric)' % (int((d > 0.1).sum()), d.max(), d[x > 0.6].max()))
json.dump({'PS_mm': PS*10, 'UB': UB, 'K': K, 'eyeR_minus_mirror_eyeL_mm': ((eyeR_c-eyeL_m)*10).tolist(), 'bag_zone_verts': int(zb.sum()), 'max_mm': float(d.max())}, open(OUT.replace('.npy', '_edit.json'), 'w'), indent=1)
