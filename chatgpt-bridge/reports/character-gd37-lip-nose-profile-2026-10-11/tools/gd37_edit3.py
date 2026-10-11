"""GD37 lip / nose edit v3 (= v2 + F4 lower-nose scale + F5 mouth-line raise) of a DNA-order head. Diagnosis (REF | GD36 profile clay + texture, same solved camera, gz_prof_lips*.png): the upper
lip's vermilion border ridge (white roll / Cupid's-bow peaks) projects as a pointed 'beak' at the TOP of the vermilion, the reference's upper
vermilion is rounded with its most forward point lower; in 3/4 the lateral upper lip stays thick to the corner (reference tapers); alar base
~8-12 % wider than the reference in the front view.
Classification on the OUTER skin only (front-most surface per (x, z) cell; the inner lip lining / mouth bag sits behind it) and the vermilion from
the face base-colour texture (redness at the vertex UV; gd13_img rows are bottom-up -> py = v*(H-1)).
Fields (smooth, symmetric about MX, outer-weighted, then K Laplacian passes on the displacement):
 F1 BP   : border-ridge push-back (-y), 1 on the band [-0.8, +0.4] mm around the vermilion border, fading 4.5 mm down into the vermilion (0 at the
           stomion) and 4 mm up into the skin; amplitude x (1 + LATB ramp to the lateral lip), faded past the mouth corner.
 F2 CT   : lateral vertical taper of the upper vermilion: z compressed toward the stomion line by c(ax) (0 in the middle, CT laterally); the skin
           above follows with a 6 mm fade.
 F4 NSC  : lower nose (tip, columella, alae) scaled by (1 - NSC) about the nose-base centre (MX, 12.9, 158.1), fading into the dorsum, cheeks
           and lip (aligned profile: tip-sn segment ~7-10 % longer than the reference).
 F5 MU   : mouth line raised by MU mm: hinge field 1 at the stomion line (both lips + contact loops, y-ramp 12.25-12.65 so the mouth bag stays),
           0 at the upper border (>= 5 mm fade) and 4.5 mm down the lower lip (aligned profile: sto 1.2 mm low, li 0.7 mm high vs the reference).
 F6 PH   : upper-lip skin between the vermilion border and the subnasale pushed back by PH mm at its middle (sin profile, philtrum width,
           fading by |x| 1.6) -> deeper sn-ls concavity (aligned profile sag -0.05 vs reference -0.083).
 F3 ALAR : alar lobules / alar base x-scaled toward the midline (crease shift ALAR x 1.78 cm), cheek fade 8 mm; TIPX: dome narrowing.
usage: blender -b --factory-startup --python gd37_edit2.py -- <in.npy> <out.npy> <tex.png> [BP=0.7 mm] [LATB=0.4] [CT=0.20] [ALAR=0.09] [TIPX=0.04] [K=4] [MU=0.8 mm] [NSC=0.035] [PH=0.0 mm]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); import gd13_img as gi; from gd13_common import NS, MX, pkg
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]).astype(float); OUT, TEX = a[1], a[2]
def arg(i, d): return float(a[i]) if len(a) > i else d
BP = arg(3, 0.7)/10; LATB = arg(4, 0.4); CT = arg(5, 0.20); ALAR = arg(6, 0.09); TIPX = arg(7, 0.04); K = int(arg(8, 4)); MU = arg(9, 0.8)/10; NSC = arg(10, 0.035); PH = arg(11, 0.0)/10
S = X[:NS]; P = pkg()['head']; T = np.asarray(P['triangles']); UVc = np.asarray(P['uv'], float); sk = (T < NS).all(1); T = T[sk]; UVc = UVc[sk]
U = np.zeros((NS, 2)); C = np.zeros(NS)
for k in range(3): np.add.at(U, T[:, k], UVc[:, k]); np.add.at(C, T[:, k], 1)
U = U/np.maximum(C, 1)[:, None]
TX = gi.load(TEX)[..., :3]; H, W = TX.shape[:2]
col = TX[(U[:, 1]*(H-1)).astype(int).clip(0, H-1), (U[:, 0]*(W-1)).astype(int).clip(0, W-1)]; red = col[:, 0]/np.maximum(col[:, 1], 1e-4)
x = S[:, 0]-MX; ax = np.abs(x); y, z = S[:, 1], S[:, 2]; sg = np.sign(x)
E = np.unique(np.sort(np.r_[T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]], 1), axis=0); I0 = np.r_[E[:, 0], E[:, 1]]; I1 = np.r_[E[:, 1], E[:, 0]]; DEG = np.bincount(I0, minlength=NS).astype(float)
def lap(F): acc = np.zeros_like(F); np.add.at(acc, I0, F[I1]); return acc/np.maximum(DEG, 1)[:, None]
def ss(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
# outer skin: a ray from the vertex toward the front (+y) must not hit the head again (inner lip lining / mouth bag / nostril interior are occluded)
import mathutils
from mathutils.bvhtree import BVHTree
front = y > 9.0; bvh = BVHTree.FromPolygons([tuple(p) for p in S], [tuple(int(i) for i in t) for t in T])
occl = np.zeros(NS, bool); dirv = mathutils.Vector((0, 1, 0))
for i in np.nonzero(front & (z > 153.0) & (z < 160.5) & (ax < 3.4))[0]:
    hit = bvh.ray_cast(mathutils.Vector((S[i, 0], S[i, 1]+0.01, S[i, 2])), dirv, 4.0)
    occl[i] = hit[0] is not None
ow = np.where(front & ~occl, 1.0, 0.0)
# vermilion on the outer skin: vertex-smoothed redness, flood-filled from midline seeds (isolated reddish skin spots are not lip)
mouth = (z > 154.2) & (z < 157.0) & (ax < 2.9) & (y > 11.0)
rs = red[:, None].copy()
for _ in range(2): rs = 0.5*rs+0.5*lap(rs)
rs = rs[:, 0]; skin = np.median(rs[(ow > 0.5) & (z > 156.9) & (z < 157.4) & (ax > 0.9) & (ax < 1.8)])
cand = mouth & (ow > 0.5) & (rs > skin+0.07); verm = cand & (ax < 0.3) & (((z > 155.8) & (z < 156.4)) | ((z > 154.8) & (z < 155.4)))
nb = [[] for _ in range(NS)]
for e0, e1 in E: nb[e0].append(e1); nb[e1].append(e0)
fr = list(np.nonzero(verm)[0])
while fr:
    nf = []
    for i in fr:
        for j in nb[i]:
            if cand[j] and not verm[j]: verm[j] = True; nf.append(j)
    fr = nf
# stomion line: local minimum of the front-most y(z) inside the vermilion, per |x| bin; corner = lateral-most outer vermilion
bins = np.arange(0, 2.61, 0.2); xb = 0.5*(bins[1:]+bins[:-1]); szb = np.full(len(xb), np.nan)
for i in range(len(xb)):
    m = verm & (ax >= bins[i]) & (ax < bins[i+1]) & (z > 155.0) & (z < 156.3)
    if m.sum() < 8: continue
    zg = np.arange(155.05, 156.26, 0.04); yg = np.array([y[m & (np.abs(z-zz) < 0.04)].max() if (m & (np.abs(z-zz) < 0.04)).any() else np.nan for zz in zg])
    ok = ~np.isnan(yg)
    if ok.sum() < 8: continue
    yg = np.interp(zg, zg[ok], yg[ok]); ysm = np.convolve(np.pad(yg, 2, mode='edge'), np.ones(5)/5, 'valid')
    j = np.argmin(ysm[2:-2])+2
    if ysm[j] < ysm[:j].max()-0.02 and ysm[j] < ysm[j+1:].max()-0.02: szb[i] = zg[j]   # genuine local minimum (both lips in front of it)
cm = verm & (np.abs(z-155.65) < 0.5); corner_ax = float(np.percentile(ax[cm], 98)); corner_z = float(np.median(z[cm & (ax > corner_ax-0.12)]))
okb = ~np.isnan(szb); xs = np.r_[xb[okb], corner_ax]; zs = np.r_[szb[okb], corner_z]; szf = np.interp(ax, xs, zs)
upv = verm & (z > szf+0.03)
bzb = np.full(len(xb), np.nan)
for i in range(len(xb)):
    m = upv & (ax >= bins[i]) & (ax < bins[i+1])
    if m.sum() > 4: bzb[i] = np.percentile(z[m], 95)
okz = ~np.isnan(bzb) & (xb < corner_ax); bxs = np.r_[xb[okz], corner_ax]; bzs = np.r_[bzb[okz], corner_z]; bzf = np.interp(ax, bxs, bzs); hgt = np.maximum(bzf-szf, 0.02)
DBG = np.full((480, 600, 4), 0.15); DBG[..., 3] = 1
for i in np.nonzero((z > 153.8) & (z < 158.6) & (ax < 3.0) & front)[0]:
    c_ = (0.25, 0.25, 0.25) if ow[i] < 0.5 else ((1, 0.2, 0.2) if upv[i] else ((1, 0.6, 0.2) if verm[i] else (0.6, 0.8, 0.6)))
    DBG[int((z[i]-153.8)*100), int((x[i]+3.0)*100), :3] = c_
for xi in range(600):
    axx = abs(xi/100-3.0); zz1 = np.interp(axx, xs, zs); zz2 = np.interp(axx, bxs, bzs)
    for zz, cc in ((zz1, (0.2, 0.6, 1)), (zz2, (1, 1, 0))):
        r_ = int((zz-153.8)*100)
        if 0 <= r_ < 480: DBG[r_, xi, :3] = cc
gi.save(OUT.replace('.npy', '_class.png'), DBG)
D = np.zeros_like(S)
# F1 border-ridge push-back
v = z-bzf
band = np.where(v < -0.008, ss((v+0.45)/0.37), np.where(v > 0.004, ss((0.40-v)/0.36), 1.0))*ss((z-szf)/0.15)
ampx = (1+LATB*ss((ax-0.6)/0.8))*ss((corner_ax+0.25-ax)/0.45)
w1 = np.where((ax < corner_ax+0.25) & (y > 11.0) & (z < bzf+0.45) & (z > szf), band*ampx*ow, 0.0); D[:, 1] -= BP*w1
# F2 lateral vertical taper
c = CT*ss((ax-0.5)/0.8)*ss((corner_ax+0.1-ax)/0.35)
dz2 = np.where(z <= bzf, -c*(z-szf), -c*hgt*ss((bzf+0.6-z)/0.6))
w2 = np.where((z > szf) & (z < bzf+0.6) & (ax < corner_ax+0.1) & (y > 11.0), ow, 0.0); D[:, 2] += dz2*w2
# F3 alar narrowing + dome narrowing
wz = ss((z-157.45)/0.35)*ss((159.35-z)/0.5); wy = ss((y-11.0)/0.6)
shift = ALAR*np.minimum(ax, 1.78)*ss((ax-0.45)/0.5)*np.where(ax > 1.78, ss((2.6-ax)/0.82), 1.0)
D[:, 0] -= sg*shift*wz*wy
wt = ss((z-158.4)/0.4)*ss((159.95-z)/0.4)*ss((1.15-ax)/0.35)*ss((y-13.8)/0.5); D[:, 0] -= TIPX*x*wt
# F4 lower-nose scale about the nose-base centre
P0 = np.array([MX, 12.9, 158.1]); wN = ss((z-157.35)/0.4)*ss((160.4-z)/0.8)*ss((2.4-ax)/0.6)*ss((y-12.0)/0.5)*(z < 160.4)
D -= NSC*(S-P0)*wN[:, None]
# F6 upper-lip skin concavity
snz = 157.70; tp = np.clip((z-(bzf+0.08))/np.maximum(snz-(bzf+0.08), 0.1), 0, 1)
w6 = np.where((z > bzf+0.08) & (z < snz) & (y > 11.0), np.sin(np.pi*tp)*ss((1.6-ax)/0.7)*ow, 0.0); D[:, 1] -= PH*w6
# F5 mouth-line raise (hinge-continuous across the stomion: both lips move together at the contact)
hu = np.maximum(hgt, 0.5); wu = np.where(z >= szf, 1-ss((z-szf)/hu), 1-ss((szf-z)/0.45))
w5 = wu*ss((y-12.25)/0.4)*ss((corner_ax+0.5-ax)/0.5)*(y > 11.5); D[:, 2] += MU*w5
for _ in range(K): D = 0.5*D+0.5*lap(D)
Y = X.copy(); Y[:NS] = S+D; np.save(OUT, Y); S2 = Y[:NS]
def lobule(Q, z0, z1):
    m = (Q[:, 2] > z0) & (Q[:, 2] < z1) & (Q[:, 1] > 13.3) & (np.abs(Q[:, 0]-MX) < 2.4)
    return float(np.percentile(Q[m, 0]-MX, 99.5)-np.percentile(Q[m, 0]-MX, 0.5))*10
def midline(Q):
    m = (ax < 0.12) & (ow > 0.8) & (z > 155.5) & (z < 158.0); o = np.argsort(-z[m]); return [(round(float(z[m][i]), 2), round(float(Q[m, 1][i]), 2)) for i in o]
d = np.linalg.norm(D, axis=1)*10
print('GD37E2 skin red %.3f thr %.3f | outer verm %d upper %d | corner ax %.2f z %.2f' % (skin, skin+0.07, verm.sum(), upv.sum(), corner_ax, corner_z))
print('GD37E2 stomion z by |x| bin:', ' '.join('%.1f:%s' % (xb[i], 'nan' if np.isnan(szb[i]) else '%.2f' % szb[i]) for i in range(len(xb))))
print('GD37E2 border  z by |x| bin:', ' '.join('%.1f:%s' % (xb[i], 'nan' if np.isnan(bzb[i]) else '%.2f' % bzb[i]) for i in range(len(xb))))
print('GD37E2 lobule width z158.0-158.6: %.2f -> %.2f mm | z157.6-158.0: %.2f -> %.2f mm' % (lobule(S, 158.0, 158.6), lobule(S2, 158.0, 158.6), lobule(S, 157.6, 158.0), lobule(S2, 157.6, 158.0)))
print('GD37E3 MU %.2f mm NSC %.3f PH %.2f mm' % (MU*10, NSC, PH*10)); print('GD37E2 moved>0.1mm %d max %.2f mm | max dy F1 %.2f mm | max dz F2 %.2f mm' % ((d > 0.1).sum(), d.max(), -D[:, 1].min()*10, -D[:, 2].min()*10))
mb, ma = midline(S), midline(S2); print('GD37E2 midline y(z) before:', ' '.join('%.2f:%.2f' % p for p in mb[::2])); print('GD37E2 midline y(z) after :', ' '.join('%.2f:%.2f' % p for p in ma[::2]))
json.dump({'PH_mm': PH*10, 'MU_mm': MU*10, 'NSC': NSC, 'BP_mm': BP*10, 'LATB': LATB, 'CT': CT, 'ALAR': ALAR, 'TIPX': TIPX, 'K': K, 'skin_red': float(skin), 'outer_verm': int(verm.sum()), 'upper_verm': int(upv.sum()), 'corner_ax': corner_ax, 'corner_z': corner_z,
           'stomion_bins': [None if np.isnan(t) else float(t) for t in szb], 'border_bins': [None if np.isnan(t) else float(t) for t in bzb], 'lobule_before_mm': lobule(S, 158.0, 158.6), 'lobule_after_mm': lobule(S2, 158.0, 158.6), 'max_mm': float(d.max())},
          open(OUT.replace('.npy', '_edit.json'), 'w'), indent=1)
