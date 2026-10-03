"""GUARDIAN-14 Phase C/E method change: separate the accumulated sculpt detail from the MetaHuman model anatomy.
D = sculpt - model (model = our own face-model coefficients reconstructed without the fit's high-frequency delta, aligned).
D = LP_k(D) + HF.  LP keeps every deliberate broad sculpt change (zygoma band, cheek / maxilla support, brow shelter, lid hood mass, mouth width,
nose-bridge width, lower-face rhythm); HF holds the accumulated creases / grooves / ridges (tear trough, nasojugal, nasolabial trench, perioral
ridges, crumpled detail) that make the clay read gaunt and over-aged.
new = model + LP(D) + w(x)*HF with w = 1 where exact detail is functional (eyelid margins + 1.0 cm around each eyeball: lid / eyeball fit; lip seam
band: closed-mouth fit), w = hf elsewhere on the face, 1 outside the face (cranium / ears / neck unchanged).
usage: blender -b -P blender_gd14_detailsep.py -- <sculpt.npy> <model.npy> <out.npy> [k=30] [hf=0.3]"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import head_topology
a = sys.argv[sys.argv.index('--')+1:]; A = np.load(a[0]); M = np.load(a[1]); OUT = a[2]; K = int(a[3]) if len(a) > 3 else 30; HFW = float(a[4]) if len(a) > 4 else 0.3
MX = -0.25; NH = 24049; T, MI = head_topology(); TT = T[(MI == 0) & (T.max(1) < NH)]
E_ = np.r_[TT[:, [0, 1]], TT[:, [1, 2]], TT[:, [2, 0]]]; E_ = np.unique(np.sort(E_, 1), axis=0); Ei = np.r_[E_, E_[:, ::-1]]; deg = np.bincount(Ei[:, 0], minlength=NH).astype(float)
def sstep(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
D = A[:NH]-M[:NH]; L = D.copy()
for _ in range(K):
    acc = np.zeros_like(L); np.add.at(acc, Ei[:, 0], L[Ei[:, 1]]); L = L+0.5*(acc/np.maximum(deg, 1)[:, None]-L)
HF = D-L; S = A[:NH]; ax = np.abs(S[:, 0]-MX)
face = sstep((S[:, 1]-6.0)/2.0)*sstep((S[:, 2]-149.0)/1.5)*(1-sstep((S[:, 2]-166.0)/1.0))*(1-sstep((ax-6.8)/0.8))
eye = np.zeros(NH)
for s0, s1 in ((28955, 29725), (29725, 30495)):
    c = A[s0:s1].mean(0); r = np.linalg.norm(A[s0:s1]-c, axis=1).max(); eye = np.maximum(eye, 1-sstep((np.linalg.norm(S-c, axis=1)-r-0.45)/0.6))
seam = (1-sstep((np.abs(S[:, 2]-155.65)-0.35)/0.3))*(1-sstep((ax-2.6)/0.4))*sstep((S[:, 1]-11.0)/0.5)
keep = np.maximum(eye, seam)
w = 1-face*(1-np.maximum(keep, HFW))
X = A.copy(); X[:NH] = M[:NH]+L+w[:, None]*HF
d = np.linalg.norm(X-A, axis=1)
print('DETAILSEP_OK k', K, 'hf', HFW, 'removed HF max mm %.2f mean(face) mm %.3f' % (10*d.max(), 10*d[:NH][face > 0.5].mean()))
np.save(OUT, X)
