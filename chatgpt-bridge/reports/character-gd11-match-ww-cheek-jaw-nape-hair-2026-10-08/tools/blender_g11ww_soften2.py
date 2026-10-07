"""pass WW: CHEEKBONE SOFTEN v2 (band-pass; v1 blender_g11ww_soften.py shrank the whole convex cheek and left steps at the mask edge).
D = normal offset of each skin vertex to the Gaussian average of the surface around it (sigma cm). The large-scale part of D (the whole cheek is
convex -> uniform shrink) is removed by subtracting a heavily surface-diffused copy (D_low), so only LOCAL peaks (the pointed cheekbone) and
LOCAL hollows (under it) remain: peaks are lowered by `cut`, hollows raised by `fill`. The offset field is diffused again and faded by a wide
cheek mask (fades >= 1 cm), eyes / lids, nose and lips excluded -> no new forms, no edges. Symmetric in |x|.
usage: blender -b --python blender_g11ww_soften2.py -- <in.npy> <out.npy> <sigma_cm> <fill 0..1> <cut 0..1> [iterations]
env SOFT_LOW_IT (D_low diffusion iterations, default 120), SOFT_OFF_IT (offset diffusion, default 10)"""
import bpy, sys, os, numpy as np
from mathutils.kdtree import KDTree
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from id_common import SEG, pkg
a = sys.argv[sys.argv.index('--')+1:]; X0 = np.load(a[0]); X = X0.copy(); sig, fill, cut = float(a[2]), float(a[3]), float(a[4]); IT = int(a[5]) if len(a) > 5 else 1
LOW_IT, OFF_IT = int(os.environ.get('SOFT_LOW_IT', '120')), int(os.environ.get('SOFT_OFF_IT', '10'))
MX = -0.23; NH = 24049; SOFT = np.r_[np.arange(*SEG['skin']), np.arange(*SEG['cartilage'])]; SOFT = SOFT[SOFT < NH]
def ss(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
TRI = np.asarray(pkg()['head']['triangles']); T3 = TRI[(TRI < NH).all(1)]
E = np.r_[T3[:, [0, 1]], T3[:, [1, 2]], T3[:, [2, 0]]]; E = np.r_[E, E[:, ::-1]]; DEG = np.bincount(E[:, 0], minlength=NH).astype(float)
def diffuse(f, n, w=None):
    """surface diffusion; with weights w: normalized (values outside w>0 do not leak in as zeros)"""
    if w is None: w = np.ones(NH)
    fw, ww = f*w, w.copy()
    for _ in range(n):
        a1 = np.zeros(NH); np.add.at(a1, E[:, 0], fw[E[:, 1]]); a2 = np.zeros(NH); np.add.at(a2, E[:, 0], ww[E[:, 1]])
        fw = fw+0.5*(a1/np.maximum(DEG, 1)-fw); ww = ww+0.5*(a2/np.maximum(DEG, 1)-ww)
    return fw/np.maximum(ww, 1e-6)
for it in range(IT):
    H = X[:NH]; ax = np.abs(H[:, 0]-MX); z = H[:, 2]; y = H[:, 1]
    eye = np.zeros(NH)
    for sd in (1, -1):
        c = np.array([MX+sd*2.97, 10.5, 162.25]); d = np.sqrt((((H-c)/np.array([1.9, 2.2, 1.25]))**2).sum(1)); eye = np.maximum(eye, 1-ss((d-0.75)/0.7))
    nose = (1-ss((ax-2.0)/0.9))*ss((z-156.4)/0.6)*ss((y-10.0)/0.8)
    lips = (1-ss((ax-3.0)/1.0))*ss((z-152.8)/0.7)*(1-ss((z-157.0)/0.7))*ss((y-9.0)/0.9)
    region = ss((ax-2.4)/1.1)*(1-ss((ax-6.6)/1.2))*ss((z-151.2)/1.6)*(1-ss((z-160.3)/1.1))*ss((y-1.5)/1.6)
    M = region*(1-eye)*(1-nose)*(1-lips); M[np.setdiff1d(np.arange(NH), SOFT)] = 0
    N = np.zeros((NH, 3)); fn = -np.cross(H[T3[:, 1]]-H[T3[:, 0]], H[T3[:, 2]]-H[T3[:, 0]])
    for k in range(3): np.add.at(N, T3[:, k], fn)
    N /= np.maximum(np.linalg.norm(N, axis=1), 1e-9)[:, None]
    idx = SOFT[(H[SOFT, 1] > -1.0)]; kd = KDTree(len(idx))
    for j, i in enumerate(idx): kd.insert(H[i], j)
    kd.balance()
    big = ss((ax-1.0)/0.5)*(1-ss((ax-8.6)/0.5))*ss((z-149.0)/0.5)*(1-ss((z-163.5)/0.5))*ss((y+0.5)/0.5)   # D evaluated on a wider area
    big[np.setdiff1d(np.arange(NH), SOFT)] = 0; V = np.where(big > 1e-3)[0]; D = np.zeros(NH); valid = np.zeros(NH)
    for i in V:
        hits = kd.find_range(H[i], 3*sig)
        if len(hits) < 8: continue
        P = np.array([h[0] for h in hits]); w = np.exp(-0.5*(np.array([h[2] for h in hits])/sig)**2); avg = (P*w[:, None]).sum(0)/w.sum()
        D[i] = float((avg-H[i])@N[i]); valid[i] = 1.0
    Dlow = diffuse(D, LOW_IT, valid); Db = (D-Dlow)*valid                     # band-pass: local peak (<0) / hollow (>0) only
    off = np.where(Db > 0, fill*Db, cut*Db)*M
    off = diffuse(off, OFF_IT)*ss(M*2.5)
    X[:NH] += N*off[:, None]
    print('SOFTEN2 it%d D on %d verts, moved %d, fill max %.2f mm, cut max %.2f mm' % (it, len(V), int((np.abs(off) > 1e-4).sum()), off.max()*10, -off.min()*10))
np.save(a[1], X)
