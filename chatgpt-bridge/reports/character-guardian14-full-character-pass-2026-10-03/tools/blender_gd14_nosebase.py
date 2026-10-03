"""GUARDIAN-14 Phase A: nose-base morphology transplant into the sculpt (method change after GUARDIAN-13c).
Finding: the inward-rolled alar rim / curled wings are NOT in the MetaHuman face model - the model-only reconstruction of our own
coefficients (no fit high-frequency delta) has a natural nose base. The defect is accumulated sculpt detail. So the nose base is rebuilt
from MetaHuman model morphology instead of being corrected on the surface.
Frequency-separated transfer inside a soft nose-base mask:  new = LF(base) + HF(cand)  where LF = umbrella low-pass (k iterations) on the
skin mesh and HF = X - LF. Our low-frequency nose (tip position / projection, width, dorsum) stays; the candidate's rim / ala / nostril /
columella / sill form replaces ours. mode 'full' instead takes the candidate geometry as is inside the mask.
Mask: nose base below the supratip (full weight z < z_full, fading to 0 at z_top), lateral fade into the cheek (|x| ax_full -> ax_out),
down into the upper lip (fade z_low0 -> z_low1), only y > y_floor.
usage: blender -b -P blender_gd14_nosebase.py -- <base.npy> <cand.npy> <out.npy> [mode=hf] [k=20] [alpha=1.0]"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import head_topology
a = sys.argv[sys.argv.index('--')+1:]; B = np.load(a[0]); Cn = np.load(a[1]); OUT = a[2]
MODE = a[3] if len(a) > 3 else 'hf'; K = int(a[4]) if len(a) > 4 else 20; AL = float(a[5]) if len(a) > 5 else 1.0
MX = -0.25; NH = 24049; T, MI = head_topology(); TT = T[(MI == 0) & (T.max(1) < NH)]
E_ = np.r_[TT[:, [0, 1]], TT[:, [1, 2]], TT[:, [2, 0]]]; E_ = np.unique(np.sort(E_, 1), axis=0); Ei = np.r_[E_, E_[:, ::-1]]; deg = np.bincount(Ei[:, 0], minlength=NH).astype(float)
def lowpass(X, k):
    Y = X[:NH].copy()
    for _ in range(k):
        acc = np.zeros_like(Y); np.add.at(acc, Ei[:, 0], Y[Ei[:, 1]]); Y = Y+0.5*(acc/np.maximum(deg, 1)[:, None]-Y)
    return Y
def sstep(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
S = B[:NH]; ax = np.abs(S[:, 0]-MX)
P = dict(z_full=float(os.environ.get('NB_ZFULL', 159.5)), z_top=float(os.environ.get('NB_ZTOP', 160.4)), ax_full=float(os.environ.get('NB_AXF', 2.2)),
         ax_out=float(os.environ.get('NB_AXO', 3.0)), z_low0=float(os.environ.get('NB_ZL0', 156.9)), z_low1=float(os.environ.get('NB_ZL1', 157.5)), y_floor=11.6)
W = ((1-sstep((S[:, 2]-P['z_full'])/(P['z_top']-P['z_full'])))*(1-sstep((ax-P['ax_full'])/(P['ax_out']-P['ax_full'])))
     *sstep((S[:, 2]-P['z_low0'])/(P['z_low1']-P['z_low0']))*sstep((S[:, 1]-P['y_floor'])/0.6))*AL
X = B.copy()
if MODE == 'hf':
    LB = lowpass(B, K); LC = lowpass(Cn, K); X[:NH] = B[:NH]+W[:, None]*((Cn[:NH]-LC)-(B[:NH]-LB))
else:
    X[:NH] = B[:NH]+W[:, None]*(Cn[:NH]-B[:NH])
d = np.linalg.norm(X-B, axis=1)
print('NOSEBASE_OK', MODE, K, AL, 'max mm %.2f' % (10*d.max()), 'moved>0.1mm', int((d > 0.01).sum()), 'mask>0.5', int((W > 0.5).sum()))
np.save(OUT, X)
