"""GD11 head refinement — LOCAL face continuity fixes on the real GD11 E neutral (package topology, UE cm). Script-based (not freehand sculpt).
Each op only touches the high-frequency (HF) layer of the surface, never the low-frequency form, so the GD11 type / proportions stay:
  V = LP_k(V) + HF ;  LP_k = k umbrella iterations on the skin mesh.
  cheekR : HF of the right cheek band replaced (smooth weight) by the mirrored HF of the clean left cheek (removes the right-only crease)
  nose   : HF scaled by NOSE_W on the outer alar-lobule / alar-groove / alar-cheek junction surface; nostril openings and underside excluded
usage: blender -b --factory-startup --python gd11r_face_ops.py -- <in.npy> <out.npy> <mirror.npy>   env: OPS=cheekR,nose NOSE_W=0.5 CHEEK_W=1.0 K=25"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import head_topology
a = sys.argv[sys.argv.index('--')+1:]; IN, OUT, MIRP = a[0], a[1], a[2]
E = lambda k, d: os.environ.get(k, d); OPS = E('OPS', 'cheekR,nose').split(','); NH = 24049; MX = -0.23
X = np.load(IN); S = X[:NH].copy(); mir = np.load(MIRP)
T, MI = head_topology(); TT = T[(MI == 0) & (T.max(1) < NH)]
Ed = np.r_[TT[:, [0, 1]], TT[:, [1, 2]], TT[:, [2, 0]]]; Ed = np.unique(np.sort(Ed, 1), axis=0); Ei = np.r_[Ed, Ed[:, ::-1]]; deg = np.bincount(Ei[:, 0], minlength=NH)
def lp(P, k):
    L = P.copy()
    for _ in range(k): acc = np.zeros_like(L); np.add.at(acc, Ei[:, 0], L[Ei[:, 1]]); L = 0.5*L+0.5*acc/np.maximum(deg, 1)[:, None]
    return L
def smooth_w(w, k=6):
    for _ in range(k): acc = np.zeros(NH); np.add.at(acc, Ei[:, 0], w[Ei[:, 1]]); w = 0.5*w+0.5*acc/np.maximum(deg, 1)
    return w
def normals(P):
    N = np.zeros((NH, 3)); fn = -np.cross(P[TT[:, 1]]-P[TT[:, 0]], P[TT[:, 2]]-P[TT[:, 0]])
    for k in range(3): np.add.at(N, TT[:, k], fn)
    return N/np.maximum(np.linalg.norm(N, axis=1), 1e-9)[:, None]
def sstep(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
K = int(E('K', '25')); L = lp(S, K); HF = S-L; N = normals(S); x = S[:, 0]-MX; y, z = S[:, 1], S[:, 2]; rep = {}
new = S.copy()
if 'cheekR' in OPS:
    # band from under the outer eye down the cheek (right side, character right = -x); eyes / lids / nose / mouth excluded by ramps
    w = sstep((-x-2.9)/0.8)*(1-sstep((-x-7.0)/0.6))*sstep((z-150.0)/1.2)*(1-sstep((z-161.0)/0.8))*sstep((y-4.5)/1.2)
    w = smooth_w(w)*float(E('CHEEK_W', '1.0'))
    HFm = HF[mir]*np.array([-1.0, 1.0, 1.0])
    new = new+(w[:, None]*(HFm-HF))
    d = np.linalg.norm(new-S, axis=1)*10; rep['cheekR'] = {'n': int((w > 0.05).sum()), 'max_mm': round(float(d.max()), 2), 'mean_mm_in_zone': round(float(d[w > 0.5].mean()), 3)}
if 'nose' in OPS:
    tipz = S[np.argmax(np.where(np.abs(x) < 0.3, y, -1e9)), 2]
    outer = (N[:, 2] > -0.35)                                          # not the nostril floor / underside
    w = sstep((np.abs(x)-0.55)/0.4)*(1-sstep((np.abs(x)-2.9)/0.6))*sstep((z-(tipz-1.9))/0.5)*(1-sstep((z-(tipz+1.2))/0.6))*sstep((y-9.0)/0.8)*outer
    w = smooth_w(w.astype(float), 4)*(1-float(E('NOSE_W', '0.5')))
    new = new-w[:, None]*HF
    d = np.linalg.norm(new-S, axis=1)*10; rep['nose'] = {'tipz': round(float(tipz), 2), 'n': int((w > 0.05).sum()), 'max_mm_total': round(float(d.max()), 2)}
X2 = X.copy(); X2[:NH] = new; np.save(OUT, X2)
d = np.linalg.norm(X2[:NH]-S, axis=1)*10
print('FACEOPS_OK', json.dumps({'ops': OPS, 'report': rep, 'max_mm': round(float(d.max()), 2), 'moved_gt_0.1mm': int((d > 0.1).sum())}))
