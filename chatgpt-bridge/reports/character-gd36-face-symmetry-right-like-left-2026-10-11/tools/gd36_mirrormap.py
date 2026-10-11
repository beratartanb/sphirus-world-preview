"""GD36 mirror map of the skin from the UV layout (the gd13 nearest-3D-vertex map is only 68.8 % mutual on this asymmetric head -> cracks when
used to mirror). The MetaHuman face UVs are left-right mirror symmetric (u -> 1-u). Per skin vertex: UV = mean of its corner UVs; candidates =
the K nearest vertices to (1-u, v) in UV; partner = the candidate whose 3-D position is nearest to the mirrored 3-D position (x -> 2 MX - x),
which resolves UV seams. Then mutual pairs are kept, non-mutual vertices take the partner of a mutual neighbour (fallback 3-D nearest). Reports
mutual %, UV and 3-D residuals. Writes data/mirror_map_uv.npy (skin only, NS entries).
usage: blender -b --factory-startup --python gd36_mirrormap.py -- <head.npy> <out.npy> [K=6]"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); from gd13_common import NS, MX, pkg
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0])[:NS].astype(float); OUT = a[1]; K = int(a[2]) if len(a) > 2 else 6
P = pkg()['head']; T = np.asarray(P['triangles']); UVc = np.asarray(P['uv'], float); U = np.zeros((NS, 2)); C = np.zeros(NS)
for k in range(3):
    m = T[:, k] < NS; np.add.at(U, T[m, k], UVc[m, k]); np.add.at(C, T[m, k], 1)
U = U/np.maximum(C, 1)[:, None]
Xm = X.copy(); Xm[:, 0] = 2*MX-Xm[:, 0]
MMu = np.zeros(NS, int); res3 = np.zeros(NS); resu = np.zeros(NS)
for s in range(0, NS, 500):
    q = np.c_[1-U[s:s+500, 0], U[s:s+500, 1]]; d = ((q[:, None, :]-U[None])**2).sum(-1); cand = np.argpartition(d, K, axis=1)[:, :K]
    d3 = np.linalg.norm(Xm[s:s+500, None, :]-X[cand], axis=2); j = np.argmin(d3, 1); MMu[s:s+500] = cand[np.arange(len(j)), j]
    res3[s:s+500] = d3[np.arange(len(j)), j]; resu[s:s+500] = np.sqrt(d[np.arange(len(j)), cand[np.arange(len(j)), j]])
mut = MMu[MMu] == np.arange(NS)
print('MIRRORMAP UV-based: mutual %.1f %% | uv residual median %.4f p99 %.4f | 3-D mirrored residual median %.2f mm p95 %.2f mm max %.1f mm' % (100*mut.mean(), np.median(resu), np.percentile(resu, 99), np.median(res3)*10, np.percentile(res3, 95)*10, res3.max()*10))
# repair non-mutual: if j = MMu[i] maps back to some i' != i, keep the pair with the smaller 3-D residual; the other takes the 3-D nearest mirrored vertex
bad = np.nonzero(~mut)[0]
for i in bad:
    j = MMu[i]
    if MMu[j] != i and res3[i] > 0.15:
        d = np.linalg.norm(X-Xm[i], axis=1); MMu[i] = int(np.argmin(d))
mut2 = MMu[MMu] == np.arange(NS); print('MIRRORMAP after repair: mutual %.1f %%, unique targets %d of %d' % (100*mut2.mean(), len(np.unique(MMu)), NS))
np.save(OUT, MMu)
