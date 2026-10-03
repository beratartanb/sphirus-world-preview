"""GUARDIAN-12C targeted form ops on a DNA-order head npy (UE cm, x lateral, y forward, z up, midline x = MX). Each op is anatomical and
local (never a blanket inflate/smooth): ops run in order on the skin + cartilage vertices only (eyes / teeth untouched).
  profile : {"knots": [[z, y_target]..], "sigma": s | [[z, s]..], "pow": 2|4, "front": 0.25}  midline profile y(z) -> target, applied in +y
            with lateral weight exp(-|(x-MX)/sigma|^pow); "front" = only front-facing surface (normal_y ramp 0..front) so inner lip /
            mouth-interior surfaces are not dragged into the teeth.
  normal  : {"c": [dx_from_mid, y, z], "r": [rx, ry, rz], "amt": cm, "sym": true}  move along the vertex normal, ellipsoid falloff (1-q^2)^2
  grab    : {"c": .., "r": .., "d": [dx, dy, dz], "sym": true}  move by a vector (dx mirrored on the other side)
  field   : {"axis": "x"|"y", "A": cm, "tz": [z0..z3], "ty": [y0..y3], "tx": [|x|0..|x|3]}  smooth plateau displacement band (no point
            centres -> no lumps): A * P(z) * P(y) * P(|x-MX|), +x outward on both sides (axis x) or +y forward (axis y)
  relax   : {"c": .., "r": .., "iters": n, "sym": true}  Taubin relax inside the ellipsoid falloff (cleans the transition of the ops above)
usage: blender -b -P blender_gd12c_ops.py -- <in.npy> <ops.json> <out.npy>"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from id_common import pkg, SEG
a = sys.argv[sys.argv.index('--')+1:]; X0 = np.load(a[0]); X = X0.copy(); C = json.load(open(a[1])); OUT = a[2]
MX = C.get('mx', -0.25); NH = 24049
P = pkg(); TRI = np.asarray(P['head']['triangles']); SOFT = np.r_[np.arange(*SEG['skin']), np.arange(*SEG['cartilage'])]; SOFT = SOFT[SOFT < NH]
E_ = np.r_[TRI[:, [0, 1]], TRI[:, [1, 2]], TRI[:, [2, 0]]]; E_ = np.r_[E_, E_[:, ::-1]]; DEG = np.bincount(E_[:, 0], minlength=len(X)).astype(float)
SM = np.zeros(len(X), bool); SM[SOFT] = True
def sstep(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
def normals(X):
    N = np.zeros_like(X); fn = -np.cross(X[TRI[:, 1]]-X[TRI[:, 0]], X[TRI[:, 2]]-X[TRI[:, 0]])
    for k in range(3): np.add.at(N, TRI[:, k], fn)
    return N/np.maximum(np.linalg.norm(N, axis=1), 1e-9)[:, None]
def profile(X, z):
    H = X[:NH]; m = (np.abs(H[:, 0]-MX) < 0.15) & (H[:, 1] > 11); out = []
    for zz in z:
        s = H[m & (np.abs(H[:, 2]-zz) < 0.11)]; out.append(s[:, 1].max() if len(s) else np.nan)
    return np.array(out)
def mono_cubic(xk, yk, x):
    xk = np.asarray(xk, float); yk = np.asarray(yk, float); h = np.diff(xk); dl = np.diff(yk)/h; m = np.r_[dl[0], (dl[:-1]+dl[1:])/2, dl[-1]]
    for i in range(len(dl)):
        if dl[i] == 0: m[i] = m[i+1] = 0
        else:
            al, be = m[i]/dl[i], m[i+1]/dl[i]; s = al*al+be*be
            if s > 9: t = 3/np.sqrt(s); m[i] = t*al*dl[i]; m[i+1] = t*be*dl[i]
    i = np.clip(np.searchsorted(xk, x)-1, 0, len(h)-1); t = (x-xk[i])/h[i]
    return (2*t**3-3*t**2+1)*yk[i]+(t**3-2*t**2+t)*h[i]*m[i]+(-2*t**3+3*t**2)*yk[i+1]+(t**3-t**2)*h[i]*m[i+1]
def plateau(v, q): return sstep((v-q[0])/max(q[1]-q[0], 1e-6))*(1-sstep((v-q[2])/max(q[3]-q[2], 1e-6)))
def ell(c, r, side):
    cc = np.array([MX+side*c[0], c[1], c[2]]); q = np.sqrt((((X[:NH]-cc)/np.asarray(r, float))**2).sum(1)); w = (1-np.clip(q, 0, 1)**2)**2
    out = np.zeros(len(X)); out[:NH] = w; out[~SM] = 0; return out
log = []
for op in C['ops']:
    t = op['type']; sides = (1, -1) if op.get('sym', True) and t != 'profile' else (1,)
    if t == 'profile':
        K = np.asarray(sorted(op['knots']), float); zk = K[:, 0]; dk = K[:, 1]-profile(X, zk)
        Q = X[SOFT]; z = Q[:, 2]; d = np.zeros(len(Q)); inr = (z >= zk[0]) & (z <= zk[-1]); d[inr] = mono_cubic(zk, dk, z[inr])
        sg = op['sigma']; sig = np.interp(z, np.asarray(sg)[:, 0], np.asarray(sg)[:, 1]) if isinstance(sg, list) else np.full(len(Q), sg)
        w = np.exp(-np.abs((Q[:, 0]-MX)/sig)**op.get('pow', 2))
        if op.get('front'): w *= sstep(normals(X)[SOFT, 1]/op['front'])
        if op.get('depth'):  # only the outer shell: full weight within d0 of the front surface at this (x, z), none beyond d0 + d1
            d0, d1 = op['depth']; bx = np.round((Q[:, 0]-MX)/0.12).astype(int); bz = np.round(z/0.12).astype(int); key = bx*100000+bz
            uk, inv = np.unique(key, return_inverse=True); ymax = np.full(len(uk), -1e9); np.maximum.at(ymax, inv, Q[:, 1])
            w *= 1-sstep((ymax[inv]-Q[:, 1]-d0)/d1)
        X[SOFT, 1] += d*w; log.append({op.get('name', 'profile'): {f'{q:.2f}': round(10*v, 2) for q, v in zip(zk, dk)}})
        continue
    if t == 'field':
        Q = X[SOFT]; f = op['A']*plateau(Q[:, 2], op['tz'])*plateau(Q[:, 1], op['ty'])*plateau(np.abs(Q[:, 0]-MX), op['tx'])
        if op['axis'] == 'x': X[SOFT, 0] += f*np.sign(Q[:, 0]-MX)
        else: X[SOFT, 1] += f
        log.append({op.get('name', t): round(10*float(np.abs(f).max()), 2)}); continue
    for sd in sides:
        w = ell(op['c'], op['r'], sd)
        if t == 'normal': X += (op['amt']*w)[:, None]*normals(X)
        elif t == 'grab': dv = np.array(op['d'], float); dv[0] *= sd; X += w[:, None]*dv
        elif t == 'relax':
            for k in range(op.get('iters', 3)):
                for lam in (0.5, -0.53):
                    acc = np.zeros_like(X); np.add.at(acc, E_[:, 0], X[E_[:, 1]]); L = acc/np.maximum(DEG, 1)[:, None]-X; X += lam*w[:, None]*L
    log.append({op.get('name', t): round(10*float(np.linalg.norm(X-X0, axis=1).max()), 2)})
np.save(OUT, X); print('G12C_OPS_OK', json.dumps(log))
