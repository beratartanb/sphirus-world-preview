"""pass S10: PROTECT mouth corners and lower eyelids from a soft-tissue pass. out = base + (cand - base) * (1 - P), P = smooth union of
ellipsoid masks around both mouth corners (commissure / lip-corner crease) and the lower lid band (lid margin -> lid-cheek junction), 0..1
with ~0.6 cm falloff, then surface-diffused so the blend has no edge. usage: blender -b --python blender_g11s10_protect.py -- <base.npy> <cand.npy> <out.npy>"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from id_common import pkg
a = sys.argv[sys.argv.index('--')+1:]; Bs = np.load(a[0]); C = np.load(a[1]); NH = 24049; MX = -0.23
def ss(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
H = Bs[:NH]; P = np.zeros(NH)
for sd in (1, -1):
    cm = np.array([MX+sd*2.45, 12.4, 154.7]); q = np.sqrt((((H-cm)/np.array([0.75, 1.1, 0.75]))**2).sum(1)); P = np.maximum(P, 1-ss((q-0.6)/0.8))     # mouth corner
    if 'lid' not in os.environ.get('PROT', 'mouth,lid'): continue
    ce = np.array([MX+sd*2.97, 10.5, 161.1]); q = np.sqrt((((H-ce)/np.array([2.4, 2.4, 0.9]))**2).sum(1)); P = np.maximum(P, 1-ss((q-0.6)/0.7))      # lower lid band
T = np.asarray(pkg()['head']['triangles']); T = T[(T < NH).all(1)]; E = np.r_[T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]]; E = np.r_[E, E[:, ::-1]]; DEG = np.bincount(E[:, 0], minlength=NH).astype(float)
for _ in range(6): acc = np.zeros(NH); np.add.at(acc, E[:, 0], P[E[:, 1]]); P = 0.5*P+0.5*acc/np.maximum(DEG, 1)
O = C.copy(); O[:NH] = Bs[:NH]+(C[:NH]-Bs[:NH])*(1-P)[:, None]
d0 = np.linalg.norm(C[:NH]-Bs[:NH], axis=1); d1 = np.linalg.norm(O[:NH]-Bs[:NH], axis=1)
print('PROTECT verts P>0.5: %d | max change in protected zone before %.2f after %.2f mm' % (int((P > 0.5).sum()), d0[P > 0.5].max()*10, d1[P > 0.5].max()*10))
np.save(a[2], O)
