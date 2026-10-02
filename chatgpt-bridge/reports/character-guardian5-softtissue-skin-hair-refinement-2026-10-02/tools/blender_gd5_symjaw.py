"""GUARDIAN-5: lock a visually BALANCED jaw / chin (user reference correction 2026-10-02: the Tier A front jaw is near-symmetric).
Skin + cartilage vertices of the jaw / chin region are blended toward the mirror-average of themselves and their mirror partner about the
facial midline plane x = MX (mirror partners mapped on the symmetric archetype topology). Weight = 1 below Z_TOP-FADE_UP (lower face),
fading to 0 at Z_TOP (above it: cheeks, mouth corners, lips keep their subtle natural asymmetry) and to 0 below the neck collar guard
(146.5 -> 148.5) so the head / body weld stays exact; only the region in front of the ear (y > Y_MIN) changes.
usage: blender -b -P blender_gd5_symjaw.py -- <in.npy> <out.npy>   env: MX (default: mean x of eye midpoint / pronasale), Z_TOP 155.0, FADE_UP 1.5, AMT 1.0"""
import sys, os, json, numpy as np
from mathutils import kdtree
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from id_common import SEG
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]).copy(); OUT = a[1]; E = lambda k, d: float(os.environ.get(k, d))
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from id_common import pkg
def sstep(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
SOFT = np.r_[np.arange(*SEG['skin']), np.arange(*SEG['cartilage'])]
P_ = pkg(); TRI = np.asarray(P_['head']['triangles']); MID = np.asarray(P_['head']['material_ids']); TRI = TRI[MID == 0]
eL = X[28955:29725].mean(0); eR = X[29725:30495].mean(0); pr = X[SOFT][np.argmax(X[SOFT][:, 1])]
MX = E('MX', float(np.mean([(eL[0]+eR[0])/2, pr[0]])))
bvh = BVHTree.FromPolygons([Vector(q) for q in X], [list(t) for t in TRI])
S = X[SOFT]; avg = S.copy(); merr = np.zeros(len(S))
for k, v in enumerate(S):
    q = Vector((2*MX-v[0], v[1], v[2])); loc, nrm, idx, dist = bvh.find_nearest(q)
    if loc is None: merr[k] = 9; continue
    c = np.array([2*MX-loc[0], loc[1], loc[2]]); avg[k] = 0.5*(v+c); merr[k] = dist
z = S[:, 2]; w = (1-sstep((z-(E('Z_TOP', 155.0)-E('FADE_UP', 1.5)))/E('FADE_UP', 1.5)))*sstep((z-146.5)/2.0)*sstep((S[:, 1]-E('Y_MIN', -1.0))/2.0)*(merr < 1.0)*E('AMT', 1.0)
X[SOFT] = S+(avg-S)*w[:, None]
d = np.linalg.norm((avg-S)*w[:, None], axis=1)
np.save(OUT, X); print('SYMJAW_OK', json.dumps({'MX': round(MX, 3), 'mirror_surface_max_dist_cm': round(float(merr.max()), 4), 'moved_verts': int((d > 0.005).sum()), 'max_disp_mm': round(float(d.max()*10), 2), 'mean_disp_mm_moved': round(float(d[d > 0.005].mean()*10), 2)}))
