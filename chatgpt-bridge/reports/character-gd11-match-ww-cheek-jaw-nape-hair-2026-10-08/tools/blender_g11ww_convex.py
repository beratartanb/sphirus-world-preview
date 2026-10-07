"""pass WW: local convexity of the skin (offset of each vertex above the Gaussian average of its surroundings along the normal, sigma cm) in
facial regions -> how 'pointed' the cheekbone reads. usage: blender -b --python blender_g11ww_convex.py -- <head.npy> [sigma] [label]"""
import bpy, sys, os, numpy as np
from mathutils.kdtree import KDTree
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from id_common import SEG, pkg
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0])[:24049]; sig = float(a[1]) if len(a) > 1 else 0.9; L = a[2] if len(a) > 2 else ''; MX = -0.23
SOFT = np.r_[np.arange(*SEG['skin']), np.arange(*SEG['cartilage'])]; SOFT = SOFT[SOFT < 24049]
TRI = np.asarray(pkg()['head']['triangles']); T3 = TRI[(TRI < 24049).all(1)]; N = np.zeros_like(X); fn = -np.cross(X[T3[:, 1]]-X[T3[:, 0]], X[T3[:, 2]]-X[T3[:, 0]])
for k in range(3): np.add.at(N, T3[:, k], fn)
N /= np.maximum(np.linalg.norm(N, axis=1), 1e-9)[:, None]
idx = SOFT[X[SOFT, 1] > 2.0]; kd = KDTree(len(idx))
for j, i in enumerate(idx): kd.insert(X[i], j)
kd.balance(); ax = np.abs(X[:, 0]-MX)
regs = {'zygoma (cheekbone)': (ax > 3.8) & (ax < 6.0) & (X[:, 2] > 158.6) & (X[:, 2] < 161.2) & (X[:, 1] > 6.5), 'malar front': (ax > 2.6) & (ax < 4.2) & (X[:, 2] > 158.0) & (X[:, 2] < 160.4) & (X[:, 1] > 10.5),
        'submalar': (ax > 3.8) & (ax < 5.6) & (X[:, 2] > 154.8) & (X[:, 2] < 157.8) & (X[:, 1] > 6.5), 'jaw angle': (ax > 4.2) & (X[:, 2] > 148.5) & (X[:, 2] < 152.5) & (X[:, 1] > 0) & (X[:, 1] < 6)}
for k, m in regs.items():
    vals = []
    for i in np.where(m)[0]:
        if i not in set(idx[:0]):
            hits = kd.find_range(X[i], 3*sig)
            if len(hits) < 8: continue
            P = np.array([h[0] for h in hits]); w = np.exp(-0.5*(np.array([h[2] for h in hits])/sig)**2); avg = (P*w[:, None]).sum(0)/w.sum(); vals.append(float((X[i]-avg)@N[i]))
    v = np.array(vals)*10; print('CONVEX %s %-20s n %4d max %.2f p90 %.2f mean %.2f mm' % (L, k, len(v), v.max(), np.percentile(v, 90), v.mean()))
