"""GD34 brow path smoothing + tail taper (user: the temple tail must thin out and end naturally; the brow is wavy). The builder interpolates
the stations LINEARLY, so every station is a small corner, and the c7u3 tail (GD33, lifted from the user-marked region) joins the body with an
S (flat body, then a late, steep turn). Per side: the station centres are resampled every 0.5 mm along arc length, smoothed with a Gaussian of
SIGMA mm whose ends are padded by point reflection (end points and end tangents kept: medial head and the marked tail tip stay put), projected
back to the skin (2 passes). The half-height is smoothed the same way along arc length, then the tail zone (u > TU) is tapered smoothly to
TIPF x its value at TU (smoothstep). The up direction (top - bot) is smoothed and re-orthogonalised to the path. Output: M stations per side,
evenly spaced in arc length. Reports the wiggle before / after: RMS and max distance of the centre polyline from its own 6 mm-Gaussian
version (corner noise), and the count of sign changes of the vertical curvature along the lateral half.
usage: blender -b --factory-startup --python gd34_browsmooth.py -- <head.npy> <brow3d in> <brow3d out> [SIGMA=3.0] [TU=0.62] [TIPF=0.18] [M=28]"""
import sys, os, json, numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from gd_common import head_topology
a = sys.argv[sys.argv.index('--')+1:]; HEAD, IN, OUT = a[:3]
SIG = float(a[3]) if len(a) > 3 else 3.0; TU = float(a[4]) if len(a) > 4 else 0.62; TIPF = float(a[5]) if len(a) > 5 else 0.18; M = int(a[6]) if len(a) > 6 else 28
X = np.load(HEAD)[:24049]; T, MI = head_topology(); TT = T[(MI == 0) & (T.max(1) < 24049)]
bvh = BVHTree.FromPolygons([tuple(map(float, p)) for p in X], [tuple(int(i) for i in t) for t in TT])
def surf(p): loc, nrm, idx, d = bvh.find_nearest(Vector(tuple(float(v) for v in p))); return np.asarray(loc)
def resample(P, step):
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]; n = max(int(s[-1]/step), 2); t = np.linspace(0, s[-1], n+1)
    return np.stack([np.interp(t, s, P[:, k]) for k in range(P.shape[1])], 1), t
def gsmooth(P, sig_pts):
    """Gaussian along the polyline, ends padded by point reflection (keeps end point + end tangent)."""
    k = int(3*sig_pts)+1; g = np.exp(-0.5*(np.arange(-k, k+1)/sig_pts)**2); g /= g.sum()
    pre = 2*P[0]-P[1:k+1][::-1]; post = 2*P[-1]-P[-k-1:-1][::-1]; Q = np.r_[pre, P, post]
    return np.stack([np.convolve(Q[:, j], g, 'valid') for j in range(P.shape[1])], 1)
def wiggle(C):
    D, _ = resample(C, 0.05); S = gsmooth(D, 0.6/0.05); r = np.linalg.norm(D-S, axis=1)*10
    half = D[len(D)//2:]; z = half[:, 2]; dz2 = np.diff(z, 2); sg = np.sign(dz2[np.abs(dz2) > 1e-6]); return float(np.sqrt((r**2).mean())), float(r.max()), int((np.diff(sg) != 0).sum())
B = json.load(open(IN)); out = dict(B); rep = {}
for side in ('imgL', 'imgR'):
    st = B[side]; TOP = np.array([s['top'] for s in st]); BOT = np.array([s['bot'] for s in st]); C = 0.5*(TOP+BOT); H = 0.5*np.linalg.norm(TOP-BOT, axis=1); UPv = TOP-BOT
    before = wiggle(C)
    D, sarc = resample(np.c_[C, H, UPv], 0.05)   # 0.5 mm
    Cs, Hs, Us = D[:, :3], D[:, 3], D[:, 4:]
    sig_pts = (SIG/10)/0.05
    for _ in range(2): Cs = gsmooth(Cs, sig_pts); Cs = np.array([surf(p) for p in Cs])
    Hs = gsmooth(Hs[:, None], sig_pts)[:, 0]; Us = gsmooth(Us, sig_pts)
    s2 = np.r_[0, np.cumsum(np.linalg.norm(np.diff(Cs, axis=0), axis=1))]; u = s2/s2[-1]
    hTU = np.interp(TU, u, Hs); w = np.clip((u-TU)/(1-TU), 0, 1); w = w*w*(3-2*w)
    Hs = np.where(u > TU, hTU*(1-w)+hTU*TIPF*w, Hs)
    tg = np.gradient(Cs, axis=0); tg /= np.maximum(np.linalg.norm(tg, axis=1), 1e-9)[:, None]
    Us = Us-tg*(Us*tg).sum(1)[:, None]; Us /= np.maximum(np.linalg.norm(Us, axis=1), 1e-9)[:, None]
    idx = np.unique(np.round(np.linspace(0, len(Cs)-1, M)).astype(int)); new = []
    for i in idx:
        c = Cs[i]; h = Hs[i]; top = surf(c+Us[i]*h); bot = surf(c-Us[i]*h)
        new.append({'col': None, 'top': top.round(4).tolist(), 'cen': c.round(4).tolist(), 'bot': bot.round(4).tolist(), 'u': round(float(u[i]), 3), 'thick_mm': round(float(np.linalg.norm(top-bot))*10, 2)})
    out[side] = new; after = wiggle(np.array([n['cen'] for n in new]))
    rep[side] = {'wiggle_before_rms_max_signchanges': [round(before[0], 3), round(before[1], 3), before[2]], 'wiggle_after': [round(after[0], 3), round(after[1], 3), after[2]],
                 'tip_shift_mm': round(float(np.linalg.norm(np.array(new[-1]['cen'])-C[-1]))*10, 2), 'head_shift_mm': round(float(np.linalg.norm(np.array(new[0]['cen'])-C[0]))*10, 2),
                 'thick_mm_TU_tip': [round(2*hTU*10, 2), new[-1]['thick_mm']], 'arc_cm': round(float(s2[-1]), 3)}
out['smoothing'] = {'sigma_mm': SIG, 'TU': TU, 'TIPF': TIPF, 'M': M, 'source': os.path.basename(IN), 'report': rep}
json.dump(out, open(OUT, 'w'), indent=1); print('BROWSMOOTH', json.dumps(rep))
