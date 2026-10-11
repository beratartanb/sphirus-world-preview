"""GD38 continuous mirror correspondence through the (left-right symmetric) UV layout: for every skin vertex, the point of the skin surface at
UV (1-u, v) is found by barycentric interpolation inside the triangle that contains it (per-corner UVs, so UV seams are exact), then mirrored
(x -> 2 MX - x) and rigidly aligned to the head (Kabsch over the face). No vertex pairing is needed (the nearest-vertex maps were only ~70 %
mutual on this asymmetric head and cracked the surface). Writes the aligned mirror positions M (NS x 3) and the uv-hit residual.
usage: blender -b --factory-startup --python gd38_uvmirror.py -- <head.npy> <out_M.npy> [GRID=384]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); from gd13_common import NS, MX, pkg
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0])[:NS].astype(float); OUT = a[1]; G = int(a[2]) if len(a) > 2 else 384
P = pkg()['head']; T = np.asarray(P['triangles']); UVc = np.asarray(P['uv'], float); sk = (T < NS).all(1); T = T[sk]; UVc = UVc[sk]
U = np.zeros((NS, 2)); C = np.zeros(NS)
for k in range(3): np.add.at(U, T[:, k], UVc[:, k]); np.add.at(C, T[:, k], 1)
U = U/np.maximum(C, 1)[:, None]
# grid acceleration over triangle UV bounding boxes
lo = np.floor(UVc.min(1)*G).astype(int).clip(0, G-1); hi = np.floor(UVc.max(1)*G).astype(int).clip(0, G-1); cells = {}
for t in range(len(T)):
    for gx in range(lo[t, 0], hi[t, 0]+1):
        for gy in range(lo[t, 1], hi[t, 1]+1): cells.setdefault(gx*G+gy, []).append(t)
Q = np.c_[1-U[:, 0], U[:, 1]]; M = np.full((NS, 3), np.nan); miss = 0; hitd = np.zeros(NS)
for i in range(NS):
    q = Q[i]; key = int(min(q[0]*G, G-1))*G+int(min(q[1]*G, G-1)); best = None
    for t in cells.get(key, []):
        A, B_, C_ = UVc[t]; v0, v1, v2 = B_-A, C_-A, q-A; den = v0[0]*v1[1]-v1[0]*v0[1]
        if abs(den) < 1e-14: continue
        b1 = (v2[0]*v1[1]-v1[0]*v2[1])/den; b2 = (v0[0]*v2[1]-v2[0]*v0[1])/den; b0 = 1-b1-b2; mn = min(b0, b1, b2)
        if best is None or mn > best[0]: best = (mn, t, b0, b1, b2)
        if mn >= -1e-6: break
    if best is None: miss += 1; continue
    mn, t, b0, b1, b2 = best; w = np.clip(np.array([b0, b1, b2]), 0, None); w /= w.sum(); M[i] = w@X[T[t]]; hitd[i] = -min(mn, 0)
ok = ~np.isnan(M[:, 0]); M[~ok] = X[~ok]
Mr = M.copy(); Mr[:, 0] = 2*MX-Mr[:, 0]
ax = np.abs(X[:, 0]-MX); y, z = X[:, 1], X[:, 2]; ear = (ax > 6.2) & (y < 4.6) & (z > 154) & (z < 168); face = ok & ~ear & (y > 3) & (z > 148.5) & (z < 168)
use = face.copy()   # robust Kabsch: drop wrong-island hits (UV islands of the mouth / eye interior overlap the face mirror) and refit
for it in range(4):
    p, q_ = Mr[use], X[use]; pc, qc = p.mean(0), q_.mean(0); U_, s_, Vt = np.linalg.svd((p-pc).T@(q_-qc)); dd = np.sign(np.linalg.det(Vt.T@U_.T)); R = Vt.T@np.diag([1, 1, dd])@U_.T
    Ma = (Mr-pc)@R.T+qc; r = np.linalg.norm(X-Ma, axis=1); use = face & (r < max(0.25, np.percentile(r[face], 90)*1.5))
bad = r > 1.2   # residual > 12 mm = wrong island hit -> no mirror target (keep own position)
known = ok & ~bad; Dm = np.where(known[:, None], Ma-X, 0.0)   # harmonic fill of the mirror displacement where there is no valid hit (no steps)
E = np.unique(np.sort(np.r_[T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]], 1), axis=0); I0 = np.r_[E[:, 0], E[:, 1]]; I1 = np.r_[E[:, 1], E[:, 0]]; DEG = np.bincount(I0, minlength=NS).astype(float)
for it in range(400):
    acc = np.zeros_like(Dm); np.add.at(acc, I0, Dm[I1]); avg = acc/np.maximum(DEG, 1)[:, None]; Dm = np.where(known[:, None], Dm, avg)
Ma = X+Dm; np.save(OUT, Ma); print('UVMIRROR wrong-island hits filled harmonically:', int((bad & ok).sum()), 'of which face:', int((bad & face).sum()), '| misses filled:', int((~ok).sum()))
d = np.linalg.norm(X-Ma, axis=1)*10
print('UVMIRROR hits %d / %d (miss %d), outside-triangle hits %d | yaw %.3f deg | face |X - aligned mirror| mean %.2f mm p95 %.2f mm max %.1f mm' % (ok.sum(), NS, miss, int((hitd > 1e-4).sum()), np.degrees(np.arctan2(R[1, 0], R[0, 0])), d[face].mean(), np.percentile(d[face], 95), d[face].max()))
