"""pass WW: map a DNA-order shape delta (new - base head npy) onto a face SKM's dynamic-mesh vertex order (nearest postrig vertex of the
rig the SKM was built from; seam duplicates share the value) -> [[index, dx, dy, dz], ...] for ue_g11uu_apply2.py. The ops are smooth, so
no low-pass is applied (localised forms such as the malar apple survive, unlike the low-passed rig residual).
usage: blender -b --python blender_g11ww_deltamap.py -- <base.npy> <new.npy> <postrig.npy> <dm.json> <out.json>"""
import sys, json, numpy as np, mathutils
a = sys.argv[sys.argv.index('--')+1:]; A = np.load(a[0])[:24049]; Bn = np.load(a[1])[:24049]; P = np.load(a[2])[:24049]; D = np.array(json.load(open(a[3])))
R = Bn-A; kd = mathutils.kdtree.KDTree(len(P))
for i, p in enumerate(P): kd.insert(p, i)
kd.balance(); out = []; mx = 0.0
for j, q in enumerate(D):
    co, i, dist = kd.find(q)
    if dist > 0.02: continue
    r = R[i]
    if np.linalg.norm(r) > 0.002: out.append([j, round(float(r[0]), 5), round(float(r[1]), 5), round(float(r[2]), 5)]); mx = max(mx, float(np.linalg.norm(r)))
json.dump(out, open(a[4], 'w')); print('DELTAMAP n %d max %.2f mm' % (len(out), mx*10))
