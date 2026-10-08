"""pass XX: soften6 = soften5 where lips / philtrum / alae are NO-SOURCE (their own relief is not flattened) but NOT pinned: the smooth
offset field diffuses over them, so nothing steps at their border (soften5 left creases at the commissure and alar base). Pinned (hard 0):
lids / eyes, nose dorsum + tip, mouth interior (lip surfaces facing back), ear.
soften5 doc: relief flattening of the PERIORAL RING (orbicularis 'muzzle' bulge + nasolabial / marionette grooves) and the
UNDER-EYE ridge / groove pair (+ nose-cheek junction), found with blender_g11xx_reliefmap.py. Band-pass relief Db (Gaussian sigma minus a
surface-diffused copy) -> offset (hollows raised by `fill`, ridges lowered by `cut`) -> diffused (smooth field) -> weighted by
  region box (wide fades) * frozen-distance ramp: the frozen set (lip vermilion, philtrum, nose core + alae, lids / eyes, ear) is turned into
  a smooth 0..1 ramp by heat diffusion, so the offset fades over ~RAMP_IT edges (~1 cm) instead of stopping at a mask edge (soften3/4 steps).
usage: blender -b --python blender_g11xx_soften5.py -- <in.npy> <out.npy> <sigma_cm> <fill> <cut> [iterations]
env SOFT_BOX = "ax0,ax1,z0,z1,ymin" (fades SOFT_FADE, default 0.7 cm), RAMP_IT (default 25), OFF_IT (default 8)"""
import bpy, sys, os, numpy as np
from mathutils.kdtree import KDTree
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from id_common import SEG, pkg
a = sys.argv[sys.argv.index('--')+1:]; X0 = np.load(a[0]); X = X0.copy(); sig, fill, cut = float(a[2]), float(a[3]), float(a[4]); IT = int(a[5]) if len(a) > 5 else 1
ev = lambda k, d: float(os.environ.get(k, d))
AX0, AX1, Z0, Z1, YMIN = [float(v) for v in os.environ.get('SOFT_BOX', '0.8,4.4,151.6,157.8,8.0').split(',')]; FD = ev('SOFT_FADE', 0.7)
RAMP_IT, OFF_IT, LOW_IT = int(ev('RAMP_IT', 25)), int(ev('OFF_IT', 16)), int(ev('LOW_IT', 120))
MX = -0.23; NH = 24049
def ss(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
TRI = np.asarray(pkg()['head']['triangles']); T3 = TRI[(TRI < NH).all(1)]
E = np.r_[T3[:, [0, 1]], T3[:, [1, 2]], T3[:, [2, 0]]]; E = np.r_[E, E[:, ::-1]]; DEG = np.bincount(E[:, 0], minlength=NH).astype(float)
def lap(f):
    acc = np.zeros(NH); np.add.at(acc, E[:, 0], f[E[:, 1]]); return acc/np.maximum(DEG, 1)
for it in range(IT):
    H = X[:NH]; ax = np.abs(H[:, 0]-MX); z = H[:, 2]; y = H[:, 1]
    eye = np.zeros(NH)
    for sd in (1, -1):
        c = np.array([MX+sd*2.97, 10.5, 162.25]); d = np.sqrt((((H-c)/np.array([1.9, 2.2, 1.25]))**2).sum(1)); eye = np.maximum(eye, (d < ev('EYE_R', 1.0)).astype(float))
    nose = ((ax < 1.15)&(z > 156.6)&(z <= 158.4)&(y > 10.5)) | ((ax < ev('NOSE_AX_UP', 1.15))&(z > 158.4)&(y > 10.5)) | (ax < 2.15)&(z > 156.7)&(z < 158.5)&(y > 10.6)                                   # dorsum / tip / columella + alae
    lips = (ax < ev('LIP_AX', 2.55))&(z > ev('LIP_Z0', 153.75))&(z < ev('LIP_Z1', 155.75))&(y > 11.6)                              # vermilion + commissure
    phil = (ax < 0.5)&(z > 155.6)&(z < 156.9)&(y > 12.0)
    ear = (ax > 7.0)&(y < 3.6)
    box = ss((ax-AX0)/FD+0.5)*(1-ss((ax-AX1)/FD+0.5))*ss((z-Z0)/FD+0.5)*(1-ss((z-Z1)/FD+0.5))*ss((y-YMIN)/FD+0.5)
    N = np.zeros((NH, 3)); fn = -np.cross(H[T3[:, 1]]-H[T3[:, 0]], H[T3[:, 2]]-H[T3[:, 0]])
    for k in range(3): np.add.at(N, T3[:, k], fn)
    N /= np.maximum(np.linalg.norm(N, axis=1), 1e-9)[:, None]
    idx = np.where(H[:, 1] > -1.0)[0]; kd = KDTree(len(idx))
    for j, i in enumerate(idx): kd.insert(H[i], j)
    kd.balance()
    V = np.where((box > 1e-3) | ((ax < AX1+2) & (z > Z0-2) & (z < Z1+2) & (y > YMIN-2)))[0]; D = np.zeros(NH); val = np.zeros(NH)
    for i in V:
        hits = kd.find_range(H[i], 3*sig)
        if len(hits) < 8: continue
        P = np.array([h[0] for h in hits]); w = np.exp(-0.5*(np.array([h[2] for h in hits])/sig)**2); avg = (P*w[:, None]).sum(0)/w.sum()
        D[i] = float((avg-H[i])@N[i]); val[i] = 1.0
    fw, ww = D*val, val.copy()
    for _ in range(LOW_IT): fw = fw+0.5*(lap(fw)-fw); ww = ww+0.5*(lap(ww)-ww)
    Db = (D-fw/np.maximum(ww, 1e-6))*val
    core = ((ax < 1.15)&(z > 156.6)&(z <= 158.4)&(y > 10.5)) | ((ax < ev('CORE_AX_UP', 1.15))&(z > 158.4)&(y > 10.5))                                                                     # nose dorsum / tip / columella
    mouth_in = (ax < 2.8)&(z > 153.5)&(z < 156.0)&(N[:, 1] < 0.25)                                                  # lip surfaces facing back (mouth interior)
    PIN = (eye > 0) | core | mouth_in | ear
    alae = (ax < 2.25)&(z > 156.6)&(z < 158.6)&(y > 10.4)
    NOSRC = nose | lips | phil | alae
    src = box.copy(); src[NOSRC] = 0
    hs = NOSRC.astype(float)
    for _ in range(6): hs = 0.5*hs+0.5*lap(hs)
    src *= (1-np.clip(hs*1.5, 0, 1))                                                                                # source fades out near the no-source features
    off = np.where(Db > 0, fill*Db, cut*Db)*val*src; off[PIN] = 0
    for _ in range(OFF_IT): off = 0.5*off+0.5*lap(off); off[PIN] = 0
    off *= ss(box*2.0+0.2) if os.environ.get('BOXCLIP', '1') == '1' else 1.0
    FR = PIN
    X[:NH] += N*off[:, None]
    print('SOFTEN6 it%d box n %d frozen %d moved %d fill max %.2f mm cut max %.2f mm' % (it, int((box > 0.5).sum()), int(FR.sum()), int((np.abs(off) > 1e-4).sum()), off.max()*10, -off.min()*10))
np.save(a[1], X)
