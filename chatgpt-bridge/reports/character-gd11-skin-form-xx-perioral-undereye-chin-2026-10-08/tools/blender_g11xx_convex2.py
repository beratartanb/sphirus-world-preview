"""pass XX: local relief of the skin per facial region (offset of each vertex from the Gaussian average of its surroundings along the normal,
sigma cm): + = bump / ridge, - = hollow / groove. Prints p90 (bumps), p10 (hollows) and rms (overall 'hardness') per region, mm.
usage: blender -b --python blender_g11xx_convex2.py -- <head.npy> [sigma] [label]"""
import bpy, sys, os, numpy as np
from mathutils.kdtree import KDTree
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from id_common import SEG, pkg
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0])[:24049]; sig = float(a[1]) if len(a) > 1 else 0.9; L = a[2] if len(a) > 2 else ''; MX = -0.23
SOFT = np.r_[np.arange(*SEG['skin']), np.arange(*SEG['cartilage'])]; SOFT = SOFT[SOFT < 24049]
TRI = np.asarray(pkg()['head']['triangles']); T3 = TRI[(TRI < 24049).all(1)]; N = np.zeros_like(X); fn = -np.cross(X[T3[:, 1]]-X[T3[:, 0]], X[T3[:, 2]]-X[T3[:, 0]])
for k in range(3): np.add.at(N, T3[:, k], fn)
N /= np.maximum(np.linalg.norm(N, axis=1), 1e-9)[:, None]
idx = SOFT[X[SOFT, 1] > -2.0]; kd = KDTree(len(idx))
for j, i in enumerate(idx): kd.insert(X[i], j)
kd.balance(); ax = np.abs(X[:, 0]-MX); y = X[:, 1]; z = X[:, 2]
regs = {'infraorbital': (ax > 1.6) & (ax < 4.2) & (z > 159.6) & (z < 161.0) & (y > 9.5), 'nasojugal (eye->nose)': (ax > 1.4) & (ax < 2.7) & (z > 158.4) & (z < 160.6) & (y > 10.0),
        'zygoma': (ax > 3.8) & (ax < 6.0) & (z > 158.6) & (z < 161.2) & (y > 6.5), 'lat cheek -> ear': (ax > 5.6) & (ax < 7.3) & (z > 156.0) & (z < 160.5) & (y > 1.0) & (y < 7.0),
        'cheek -> jaw band': (ax > 3.2) & (ax < 5.9) & (z > 151.5) & (z < 156.0) & (y > 4.0) & (y < 10.5), 'perioral skin': (ax > 1.8) & (ax < 3.6) & (z > 152.4) & (z < 157.2) & (y > 9.0),
        'chin': (ax < 2.3) & (z > 150.8) & (z < 153.4) & (y > 9.0)}
for k, m in regs.items():
    vals = []
    for i in np.where(m)[0]:
        hits = kd.find_range(X[i], 3*sig)
        if len(hits) < 8: continue
        P = np.array([h[0] for h in hits]); w = np.exp(-0.5*(np.array([h[2] for h in hits])/sig)**2); avg = (P*w[:, None]).sum(0)/w.sum(); vals.append(float((X[i]-avg)@N[i]))
    v = np.array(vals)*10; v = v-np.median(v)   # median removed (overall curvature of the region)
    print('RELIEF %-6s %-22s n %4d p90 %+.2f p10 %+.2f rms %.2f mm' % (L, k, len(v), np.percentile(v, 90), np.percentile(v, 10), np.sqrt((v**2).mean())))
