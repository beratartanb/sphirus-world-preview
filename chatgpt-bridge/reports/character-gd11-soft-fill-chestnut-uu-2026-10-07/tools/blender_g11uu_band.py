"""pass UU: smooth convex BAND from the cheekbone along the under-eye to the upper nasal bridge (the reference's continuous malar ->
nose-bridge rise). A polyline of (|x|, z, amplitude cm, half-width cm) points on the front of the face; every front skin vertex gets
amp(t) * exp(-(d / w(t))^2) along its normal, d = distance to the polyline in the (|x|, z) plane, t interpolated along it; eyelids /
eyeballs frozen (fit-tool eye ellipsoid); then a light surface diffusion. Both sides.
usage: blender -b --python blender_g11uu_band.py -- <in.npy> <out.npy> <points json> [gain]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from id_common import SEG, pkg
a = sys.argv[sys.argv.index('--')+1:]; X0 = np.load(a[0]); X = X0.copy(); PTS = np.array(json.loads(a[2]), float); G = float(a[3]) if len(a) > 3 else 1.0
MX = -0.23; NH = 24049; SOFT = np.r_[np.arange(*SEG['skin']), np.arange(*SEG['cartilage'])]; SOFT = SOFT[SOFT < NH]
def ss(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
H = X0[:NH]; eye = np.zeros(NH)
for sd in (1, -1):
    c = np.array([MX+sd*2.97, 10.5, 162.25]); d = np.sqrt((((H-c)/np.array([1.9, 2.2, 1.25]))**2).sum(1)); eye = np.maximum(eye, 1-ss((d-0.8)/0.35))
TRI = np.asarray(pkg()['head']['triangles']); N = np.zeros((NH, 3)); T3 = TRI[(TRI < NH).all(1)]
fn = -np.cross(H[T3[:, 1]]-H[T3[:, 0]], H[T3[:, 2]]-H[T3[:, 0]])
for k in range(3): np.add.at(N, T3[:, k], fn)
N /= np.maximum(np.linalg.norm(N, axis=1), 1e-9)[:, None]
Q = np.c_[np.abs(H[:, 0]-MX), H[:, 2]]; best_d = np.full(NH, 1e9); amp = np.zeros(NH); wid = np.ones(NH)
for (x0, z0, a0, w0), (x1, z1, a1, w1) in zip(PTS[:-1], PTS[1:]):
    p0 = np.array([x0, z0]); v = np.array([x1, z1])-p0; L2 = v@v; t = np.clip(((Q-p0)@v)/L2, 0, 1); d = np.linalg.norm(Q-(p0+t[:, None]*v), axis=1)
    m = d < best_d; best_d[m] = d[m]; amp[m] = (a0+(a1-a0)*t)[m]; wid[m] = (w0+(w1-w0)*t)[m]
front = ss((H[:, 1]-9.0)/0.8)*ss((N[:, 1]+0.2)/0.4)   # front-facing skin only (no nostril interior / lid underside)
MASK = np.zeros(NH); MASK[SOFT] = 1.0; MASK *= (1-eye)
f = G*amp*np.exp(-(best_d/np.maximum(wid, 1e-3))**2)*front*MASK
E = np.r_[T3[:, [0, 1]], T3[:, [1, 2]], T3[:, [2, 0]]]; E = np.r_[E, E[:, ::-1]]; DEG = np.bincount(E[:, 0], minlength=NH).astype(float)
for _ in range(int(os.environ.get('BAND_SMOOTH', '12'))):
    acc = np.zeros(NH); np.add.at(acc, E[:, 0], f[E[:, 1]]); f = (f+0.5*(acc/np.maximum(DEG, 1)-f))*MASK
X[:NH] += N*f[:, None]; np.save(a[1], X)
print('BAND moved %d verts, max %.2f mm' % (int((f > 1e-4).sum()), f.max()*10))
