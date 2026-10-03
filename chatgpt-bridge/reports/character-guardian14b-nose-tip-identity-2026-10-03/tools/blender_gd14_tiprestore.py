"""GUARDIAN-14 nose-TIP identity restore: keep K2's nose-base morphology (nostrils / alar rim / sill / columella base) and bring back the
LOW-FREQUENCY tip shape of an earlier sculpt (HS3).  new = K2 + alpha * W * LP_k(old - K2)
LP_k = umbrella low-pass over the skin mesh (k iterations) -> only broad tip volume / projection / width moves, no old crease detail.
W = tip / lobule / supratip mask: |x| fade (TX0 -> TX1), height plateau (ZL0, ZL1, ZH0, ZH1), front-of-nose only (y > tip - YD), and
fade on downward-facing surface (nostril / columella underside stays K2).
usage: blender -b -P blender_gd14_tiprestore.py -- <k2.npy> <old.npy> <out.npy> [alpha=1] [k=40]   env TX0 TX1 ZL0 ZL1 ZH0 ZH1 YD NZ"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import head_topology
a = sys.argv[sys.argv.index('--')+1:]; K2 = np.load(a[0]); OLD = np.load(a[1]); OUT = a[2]; AL = float(a[3]) if len(a) > 3 else 1.0; KK = int(a[4]) if len(a) > 4 else 40
E = lambda k, d: float(os.environ.get(k, d)); MX = -0.25; NH = 24049
T, MI = head_topology(); TT = T[(MI == 0) & (T.max(1) < NH)]
E_ = np.r_[TT[:, [0, 1]], TT[:, [1, 2]], TT[:, [2, 0]]]; E_ = np.unique(np.sort(E_, 1), axis=0); Ei = np.r_[E_, E_[:, ::-1]]; deg = np.bincount(Ei[:, 0], minlength=NH).astype(float)
def sstep(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
def normals(X):
    N = np.zeros((NH, 3)); fn = -np.cross(X[TT[:, 1]]-X[TT[:, 0]], X[TT[:, 2]]-X[TT[:, 0]])
    for k in range(3): np.add.at(N, TT[:, k], fn)
    return N/np.maximum(np.linalg.norm(N, axis=1), 1e-9)[:, None]
D = OLD[:NH]-K2[:NH]
for _ in range(KK):
    acc = np.zeros_like(D); np.add.at(acc, Ei[:, 0], D[Ei[:, 1]]); D = D+0.5*(acc/np.maximum(deg, 1)[:, None]-D)
S = K2[:NH]; ax = np.abs(S[:, 0]-MX); N = normals(K2)
tipy = S[(ax < 0.2) & (S[:, 1] > 11)][:, 1].max()
W = ((1-sstep((ax-E('TX0', 0.9))/(E('TX1', 1.7)-E('TX0', 0.9))))*sstep((S[:, 2]-E('ZL0', 157.9))/(E('ZL1', 158.5)-E('ZL0', 157.9)))
     *(1-sstep((S[:, 2]-E('ZH0', 160.0))/(E('ZH1', 161.0)-E('ZH0', 160.0))))*sstep((S[:, 1]-(tipy-E('YD', 1.6)))/0.4)*sstep((N[:, 2]+E('NZ', 0.45))/0.3))
X = K2.copy(); X[:NH] += AL*W[:, None]*D
d = np.linalg.norm(X-K2, axis=1)
print('TIPRESTORE_OK', json.dumps({'alpha': AL, 'k': KK, 'max_mm': round(10*float(d.max()), 2), 'n_moved': int((d > 0.01).sum())}))
np.save(OUT, X)
