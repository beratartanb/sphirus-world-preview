"""GUARDIAN-7: hair silhouette metrics (main + loose strands.npz vs the head npy): profile outline (mid-sagittal band |x|<1.5) stand-off of the
outermost hair point above the skull along rays from the head centre at angles 0 (front, +y) .. 180 (back) in the y-z plane, and front-view
half-width of hair at heights above the eyes. usage: blender -b -P blender_gd7_hairsil.py -- <head.npy> <strands.npz> [...]"""
import sys, os, json, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]); S = X[:24049]; HC = np.array([0.0, 1.0, 160.5]); ez = (X[28955:29725, 2].mean()+X[29725:30495, 2].mean())/2
def prof(P, band=1.5):
    P = P[np.abs(P[:, 0]) < band]; d = P-HC; ang = np.degrees(np.arctan2(d[:, 2], d[:, 1])); r = np.hypot(d[:, 1], d[:, 2]); out = {}
    for t in range(20, 200, 15):
        m = np.abs(ang-t) < 4
        if m.sum(): out[t] = float(r[m].max())
    return out
sk = prof(S)
for npz in a[1:]:
    D = np.load(npz); H = np.concatenate([D['main'].reshape(-1, 3), D['loose'].reshape(-1, 3)]); hp = prof(H, 1.5)
    so = {t: round(hp[t]-sk[t], 2) for t in hp if t in sk}
    hw = {}
    for dz in (6, 8, 10):
        m = np.abs(H[:, 2]-(ez+dz)) < 0.3; ms = np.abs(S[:, 2]-(ez+dz)) < 0.3
        if m.sum() and ms.sum(): hw[f'+{dz}'] = (round(float(H[m, 0].max()-H[m, 0].min()), 2), round(float(S[ms, 0].max()-S[ms, 0].min()), 2))
    print('HAIRSIL', os.path.basename(os.path.dirname(npz)), 'profile standoff cm by angle (90=top, 180=back):', so, 'front width hair/skull:', hw)
