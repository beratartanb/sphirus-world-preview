"""GD12 eyelid aperture: lowers the upper-lid margin (covers the top of the iris, calmer / deeper eye) and raises the lower lid slightly.
Weights fall from the margin toward the crease / cheek; lashes / eye shell segments follow the nearest skin vertex.
usage: blender -b --python blender_gd12_lids.py -- <in.npy> <out.npy> <upper_down_cm> <lower_up_cm>"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from id_common import SEG
a = sys.argv[sys.argv.index('--')+1:]; X0 = np.load(a[0]); X = X0.copy(); UD, LU = float(a[2]), float(a[3]); MX = -0.23; NH = 24049
def ss(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
H = X0[:NH]; D = np.zeros((NH, 3))
for sd in (1, -1):
    ex = MX+sd*2.97; dx = np.abs(H[:, 0]-ex); xf = 1-ss((dx-1.05)/0.45); front = ss((H[:, 1]-10.3)/0.4)
    up = ss((163.6-H[:, 2])/0.55)*ss((H[:, 2]-162.45)/0.12)*xf*front
    lo = ss((H[:, 2]-161.25)/0.45)*ss((162.05-H[:, 2])/0.12)*xf*front
    D[:, 2] += -UD*up+LU*lo; D[:, 1] += 0.15*UD*up
X[:NH] += D
for seg in ('lashes', 'eyeshell', 'eyeEdge'):
    idx = np.arange(*SEG[seg]); P = X0[idx]
    for j, i in enumerate(idx):
        k = np.argmin(((H-P[j])**2).sum(1)); X[i] += D[k]
print('LIDS_OK upper %.2f lower %.2f max %.2f mm' % (UD, LU, np.linalg.norm(D, axis=1).max()*10)); np.save(a[1], X)
