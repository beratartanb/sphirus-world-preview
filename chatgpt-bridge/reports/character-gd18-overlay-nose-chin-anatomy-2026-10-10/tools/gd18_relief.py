"""GD18 surface-relief diagnosis: per-vertex relief = (vertex - mean of its one-ring) . outward normal (mm; mean-curvature proxy, + = convex bump,
- = crease). Reports, per anatomical zone, the relief noise (std of relief minus its 2-ring smoothed version = high-frequency unevenness) for
several heads, and lists the vertices where a candidate's relief differs most from a base (new dents / ridges made by sculpting).
usage: blender -b --python gd18_relief.py -- <topo.npz> <base label=npy> <label=npy> [...]"""
import sys, json, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; TP = np.load(a[0]); H = [x.split('=', 1) for x in a[1:]]; NS = 24049; MX = -0.23
T = TP['loops'].reshape(-1, 3); T = T[(T < NS).all(1)]; E = np.unique(np.sort(np.r_[T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]], 1), axis=0)
I0 = np.r_[E[:, 0], E[:, 1]]; I1 = np.r_[E[:, 1], E[:, 0]]; DEG = np.bincount(I0, minlength=NS).astype(float)
def lap(F): acc = np.zeros_like(F); np.add.at(acc, I0, F[I1]); return acc/np.maximum(DEG, 1)[:, None]
def normals(S):
    fn = np.cross(S[T[:, 1]]-S[T[:, 0]], S[T[:, 2]]-S[T[:, 0]]); N = np.zeros((NS, 3))
    for k in range(3): np.add.at(N, T[:, k], fn)
    return N/np.maximum(np.linalg.norm(N, axis=1), 1e-12)[:, None]
def relief(S):
    r = ((S-lap(S))*normals(S)).sum(1)*10; rs = lap(lap(r[:, None]))[:, 0]; return r, r-rs
S0 = np.load(H[0][1])[:NS]; ax = np.abs(S0[:, 0]-MX); x, y, z = S0[:, 0], S0[:, 1], S0[:, 2]
Z = {'dorsum/radix': (ax < 0.7) & (z > 159.6) & (z < 163.6) & (y > 12),
     'sidewalls': (ax > 0.5) & (ax < 1.6) & (z > 159.2) & (z < 162.5) & (y > 11.5),
     'tip lobule': (ax < 0.9) & (z > 158.1) & (z < 159.6) & (y > 13.8),
     'alar wings + alar crease': (ax > 0.9) & (ax < 2.2) & (z > 157.7) & (z < 159.4) & (y > 11.6),
     'nostril sill / columella': (ax < 1.4) & (z > 157.4) & (z < 158.3) & (y > 12.3),
     'chin pad': (ax < 1.6) & (z > 151.3) & (z < 153.6) & (y > 10.5),
     'upper lip corners': (ax > 1.4) & (ax < 2.7) & (z > 155.0) & (z < 156.3) & (y > 11)}
R = {}
for lab, p in H:
    S = np.load(p)[:NS]; r, hf = relief(S); R[lab] = (r, hf)
    print('RELIEF %-6s ' % lab + ' | '.join('%s hf %.3f max|r| %.2f' % (k, hf[m].std(), np.abs(r[m]).max()) for k, m in Z.items()))
b = H[0][0]
for lab, _ in H[1:]:
    d = R[lab][1]-R[b][1]; m = Z['tip lobule'] | Z['alar wings + alar crease'] | Z['nostril sill / columella'] | Z['sidewalls'] | Z['dorsum/radix']
    idx = np.nonzero(m)[0][np.argsort(-np.abs(d[m]))[:8]]
    print('NEWRELIEF', lab, 'vs', b, ' '.join('%+.2f@(%.2f,%.2f,%.2f)' % (d[i], S0[i, 0], S0[i, 1], S0[i, 2]) for i in idx))
