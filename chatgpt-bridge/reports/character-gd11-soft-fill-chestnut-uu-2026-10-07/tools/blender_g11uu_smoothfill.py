"""pass UU: SMOOTH FILL of the midface (no new forms). Each skin vertex in a soft midface mask is compared with the Gaussian average of
the surface around it (sigma cm, kd-tree): concave points (below the local average, along the normal) are raised toward it by `fill`,
convex bumps are lowered by `cut` (small) -> hollows / the eye-nose valley close and the 'muscular' undulation softens, without the
ridges that local bumps make. Lids / eyeballs, nose (dorsum, tip, alae), lips are excluded.
usage: blender -b --python blender_g11uu_smoothfill.py -- <in.npy> <out.npy> <sigma_cm> <fill 0..1> <cut 0..1> [iterations]"""
import bpy, sys, os, numpy as np
from mathutils.kdtree import KDTree
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from id_common import SEG, pkg
a = sys.argv[sys.argv.index('--')+1:]; X0 = np.load(a[0]); X = X0.copy(); sig, fill, cut = float(a[2]), float(a[3]), float(a[4]); IT = int(a[5]) if len(a) > 5 else 1
MX = -0.23; NH = 24049; SOFT = np.r_[np.arange(*SEG['skin']), np.arange(*SEG['cartilage'])]; SOFT = SOFT[SOFT < NH]
def ss(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
TRI = np.asarray(pkg()['head']['triangles']); T3 = TRI[(TRI < NH).all(1)]
for it in range(IT):
    H = X[:NH]; ax = np.abs(H[:, 0]-MX); z = H[:, 2]; y = H[:, 1]
    eye = np.zeros(NH)
    for sd in (1, -1):
        c = np.array([MX+sd*2.97, 10.5, 162.25]); d = np.sqrt((((H-c)/np.array([1.9, 2.2, 1.25]))**2).sum(1)); eye = np.maximum(eye, 1-ss((d-0.8)/0.35))
    nose = (1-ss((ax-1.05)/0.3))*ss((z-157.6)/0.4)*ss((y-11.5)/0.6)                                   # dorsum / tip / columella
    alae = (1-ss((ax-2.15)/0.25))*(1-ss((z-158.9)/0.35))*ss((z-156.9)/0.3)*ss((y-11.0)/0.5)          # alar lobules + crease
    lips = (1-ss((ax-2.9)/0.4))*ss((z-153.6)/0.4)*(1-ss((z-157.0)/0.3))*ss((y-10.5)/0.5)
    region = ss((ax-0.85)/0.35)*(1-ss((ax-5.6)/0.6))*ss((z-154.2)/0.8)*(1-ss((z-161.6)/0.35))*ss((y-6.5)/1.0)
    M = region*(1-eye)*(1-nose)*(1-alae)*(1-lips); M[np.setdiff1d(np.arange(NH), SOFT)] = 0
    N = np.zeros((NH, 3)); fn = -np.cross(H[T3[:, 1]]-H[T3[:, 0]], H[T3[:, 2]]-H[T3[:, 0]])
    for k in range(3): np.add.at(N, T3[:, k], fn)
    N /= np.maximum(np.linalg.norm(N, axis=1), 1e-9)[:, None]
    idx = SOFT[(H[SOFT, 1] > 3.0)]; kd = KDTree(len(idx))
    for j, i in enumerate(idx): kd.insert(H[i], j)
    kd.balance(); off = np.zeros(NH)
    for i in np.where(M > 1e-3)[0]:
        hits = kd.find_range(H[i], 3*sig)
        if len(hits) < 6: continue
        P = np.array([h[0] for h in hits]); w = np.exp(-0.5*(np.array([h[2] for h in hits])/sig)**2); avg = (P*w[:, None]).sum(0)/w.sum()
        o = float((avg-H[i])@N[i]); off[i] = (fill*o if o > 0 else cut*o)*M[i]
    X[:NH] += N*off[:, None]
    print('SMOOTHFILL it%d moved %d verts, fill max %.2f mm, cut max %.2f mm' % (it, int((np.abs(off) > 1e-4).sum()), off.max()*10, -off.min()*10))
np.save(a[1], X)
