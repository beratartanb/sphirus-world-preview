"""GD41 body mesh checks of a morph delta against the current neutral: flipped triangles (normal reversed), triangle area ratio min / max,
edge length ratio min / max, head/body seam pairs delta, per-region displacement summary (bands by z). Reports the worst locations.
usage: blender -b --factory-startup --python gd41_bodycheck.py -- <pkg.json.gz> <lk_lod0.json> <morph_lod0.json> [out.json]"""
import sys, json, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from gd41_lib import Body, MX
a = sys.argv[sys.argv.index('--')+1:]; PKG, LKJ, MJ = a[:3]; OUTJ = a[3] if len(a) > 3 else None
B = Body(PKG, LKJ); X0 = B.XR; T = B.T; NB = B.NB; D = np.zeros_like(X0)
for k, v in json.load(open(MJ))['Body']['GD41_Body'].items(): D[int(k)] = v
X1 = X0+D
def tri_n(X): n = np.cross(X[T[:, 1]]-X[T[:, 0]], X[T[:, 2]]-X[T[:, 0]]); return n
n0, n1 = tri_n(X0), tri_n(X1); a0, a1 = np.linalg.norm(n0, axis=1), np.linalg.norm(n1, axis=1); dot = (n0*n1).sum(1)
flip = (dot < 0) & (a0 > 1e-8); ratio = a1/np.maximum(a0, 1e-9)
el0 = np.linalg.norm(X0[B.E[:, 0]]-X0[B.E[:, 1]], axis=1); el1 = np.linalg.norm(X1[B.E[:, 0]]-X1[B.E[:, 1]], axis=1); er = el1/np.maximum(el0, 1e-9)
mag = np.linalg.norm(D, axis=1)*10; out = {'flipped': int(flip.sum()), 'area_ratio_min': float(ratio[a0 > 1e-6].min()), 'area_ratio_max': float(ratio[a0 > 1e-6].max()), 'edge_ratio_min': float(er[el0 > 1e-4].min()), 'edge_ratio_max': float(er[el0 > 1e-4].max()),
       'seam_pairs_max_mm': float(mag[B.weld].max()), 'max_mm': float(mag.max()), 'moved_gt_1mm': int((mag > 1).sum()), 'moved_gt_5mm': int((mag > 5).sum())}
worst = np.argsort(ratio)[:3]; out['worst_area'] = [{'ratio': round(float(ratio[t]), 3), 'at': [round(float(v), 1) for v in X0[T[t]].mean(0)]} for t in worst]
worst = np.argsort(-ratio)[:3]; out['worst_area_max'] = [{'ratio': round(float(ratio[t]), 3), 'at': [round(float(v), 1) for v in X0[T[t]].mean(0)]} for t in worst]
if flip.any(): out['flip_locations'] = [[round(float(v), 1) for v in X0[T[t]].mean(0)] for t in np.nonzero(flip)[0][:8]]
bands = {'chest 120-138': (120, 138), 'waist 104-120': (104, 120), 'pelvis 88-104': (88, 104), 'hip/crotch 74-88': (74, 88), 'thigh 50-74': (50, 74), 'knee 40-50': (40, 50), 'calf 12-40': (12, 40)}
out['bands_mm'] = {k: {'max': round(float(mag[(X0[:, 2] >= z0) & (X0[:, 2] < z1)].max()), 2), 'mean': round(float(mag[(X0[:, 2] >= z0) & (X0[:, 2] < z1)].mean()), 2)} for k, (z0, z1) in bands.items()}
if OUTJ: json.dump(out, open(OUTJ, 'w'), indent=1)
print('BODYCHECK', json.dumps(out))
