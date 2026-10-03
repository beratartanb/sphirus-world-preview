"""GUARDIAN-12C nose + upper-temple correction on a DNA-order head npy (UE cm, x lateral, y forward, z up; facial midline x = MX).
NOSE: the nose is rebuilt as ONE profile curve instead of brush dabs. The current midline profile y(z) is measured, a target profile is
given as knots (cfg 'nose_knots' [[z, y_target], ...], one continuous radix -> dorsum -> supratip -> tip line) and the per-height delta
d(z) = y_target(z) - y_cur(z) (pchip-like monotone cubic, 0 outside the knot range) is applied in +y with a lateral gaussian
exp(-((x-MX)/sigma(z))^2) so the whole cross-section moves as one form (bridge sidewalls follow the ridge, alar base stays). Below the
last knot (tip underside / columella) the tip delta fades with depth y and height z, so the columella base and subnasale stay put.
Optional 'alar' ({'dy','dz','r','x','y','z'}): soft grab of the alar lobule (both sides) to re-seat it against the tip.
Then Taubin smoothing of the moved nose vertices (removes facets, keeps volume).
TEMPLE: small inward x push of the upper temple / parietal side wall: A * f(z) * g(y) * (|x - MX| / r)^2 (lateral-facing only),
f = plateau 'tz' [z0, z1, z2, z3], g = plateau 'ty' [y0, y1, y2, y3]; the top arc above z3 and everything below z0 are untouched.
usage: blender -b -P blender_gd12c_nose_temple.py -- <in.npy> <cfg.json> <out.npy>"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from id_common import pkg, SEG
a = sys.argv[sys.argv.index('--')+1:]; X0 = np.load(a[0]); X = X0.copy(); C = json.load(open(a[1])); OUT = a[2]
MX = C.get('mx', -0.25); NH = 24049
P = pkg(); TRI = np.asarray(P['head']['triangles']); SOFT = np.r_[np.arange(*SEG['skin']), np.arange(*SEG['cartilage'])]
def sstep(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
def plateau(v, q): return sstep((v-q[0])/max(q[1]-q[0], 1e-6))*(1-sstep((v-q[2])/max(q[3]-q[2], 1e-6)))
def profile(X, z):
    H = X[:NH]; m = (np.abs(H[:, 0]-MX) < 0.15) & (H[:, 1] > 11); out = []
    for zz in z:
        s = H[m & (np.abs(H[:, 2]-zz) < 0.13)]; out.append(s[:, 1].max() if len(s) else np.nan)
    return np.array(out)
def mono_cubic(xk, yk, x):  # Fritsch-Carlson monotone cubic (no overshoot)
    xk = np.asarray(xk, float); yk = np.asarray(yk, float); h = np.diff(xk); dlt = np.diff(yk)/h; m = np.r_[dlt[0], (dlt[:-1]+dlt[1:])/2, dlt[-1]]
    for i in range(len(dlt)):
        if dlt[i] == 0: m[i] = m[i+1] = 0
        else:
            al, be = m[i]/dlt[i], m[i+1]/dlt[i]; s = al*al+be*be
            if s > 9: t = 3/np.sqrt(s); m[i] = t*al*dlt[i]; m[i+1] = t*be*dlt[i]
    i = np.clip(np.searchsorted(xk, x)-1, 0, len(h)-1); t = (x-xk[i])/h[i]
    h00 = 2*t**3-3*t**2+1; h10 = t**3-2*t**2+t; h01 = -2*t**3+3*t**2; h11 = t**3-t**2
    return h00*yk[i]+h10*h[i]*m[i]+h01*yk[i+1]+h11*h[i]*m[i+1]
log = {}
# ---------------- nose ----------------
if 'nose_knots' in C:
    K = np.asarray(sorted(C['nose_knots']), float); zk = K[:, 0]; cur_k = profile(X0, zk); dk = K[:, 1]-cur_k
    log['knot_delta_mm'] = {f'{z:.2f}': round(10*d, 2) for z, d in zip(zk, dk)}
    sig_k = np.asarray(C.get('sigma', [[zk[0], 0.75], [zk[-1], 0.85]]), float)
    S = SOFT[SOFT < NH]; Q = X[S]; z = Q[:, 2]
    inr = (z >= zk[0]) & (z <= zk[-1]); d = np.zeros(len(S))
    d[inr] = mono_cubic(zk, dk, z[inr])
    sig = np.interp(z, sig_k[:, 0], sig_k[:, 1])
    # tip underside / columella: below the lowest knot the lowest-knot delta fades with depth and height
    U = C.get('under', {'y0': 13.9, 'y1': 15.0, 'z0': 157.6, 'z1': 158.5}); low = z < zk[0]
    d[low] = dk[0]*sstep((Q[low, 1]-U['y0'])/(U['y1']-U['y0']))*sstep((z[low]-U['z0'])/(U['z1']-U['z0']))
    w = np.exp(-((Q[:, 0]-MX)/sig)**2)*(Q[:, 1] > C.get('y_floor', 11.5))
    X[S, 1] += d*w; moved = S[np.abs(d*w) > 0.005]
    if 'alar' in C:
        al = C['alar']
        for sx in (1, -1):
            c = np.array([MX+sx*al['x'], al['y'], al['z']]); r = np.linalg.norm(X[S]-c, axis=1); f = (1-np.clip(r/al['r'], 0, 1)**2)**2
            X[S, 1] += al.get('dy', 0)*f; X[S, 2] += al.get('dz', 0)*f; X[S, 0] += sx*al.get('dx', 0)*f
            moved = np.union1d(moved, S[f > 0.01])
    # Taubin smoothing restricted to the moved region (+1 ring), weights fade at the region edge
    it = C.get('smooth_iters', 4)
    if it:
        reg = np.zeros(len(X), bool); reg[moved] = True
        E_ = np.r_[TRI[:, [0, 1]], TRI[:, [1, 2]], TRI[:, [2, 0]]]; E_ = np.r_[E_, E_[:, ::-1]]
        ring = np.zeros(len(X), bool); ring[E_[reg[E_[:, 0]], 1]] = True; reg |= ring
        deg = np.bincount(E_[:, 0], minlength=len(X)).astype(float); soft = np.zeros(len(X), bool); soft[SOFT] = True; reg &= soft
        for k in range(it):
            for lam in (0.5, -0.53):
                acc = np.zeros_like(X); np.add.at(acc, E_[:, 0], X[E_[:, 1]]); L = acc/np.maximum(deg, 1)[:, None]-X
                X[reg] += lam*L[reg]
    if 'blend' in C:  # lobule <-> ala blend: soft-masked Taubin over the alar groove so tip + alae read as one form
        bl = C['blend']; Q = X[:NH]; ax = np.abs(Q[:, 0]-MX)
        wb = (sstep((ax-bl['x'][0])/0.2)*(1-sstep((ax-bl['x'][1])/0.3))*sstep((Q[:, 2]-bl['z'][0])/0.25)*(1-sstep((Q[:, 2]-bl['z'][1])/0.25))
              *sstep((Q[:, 1]-bl['y_min'])/0.3))
        wf = np.zeros(len(X)); wf[:NH] = wb; soft = np.zeros(len(X), bool); soft[SOFT] = True; wf[~soft] = 0
        E_ = np.r_[TRI[:, [0, 1]], TRI[:, [1, 2]], TRI[:, [2, 0]]]; E_ = np.r_[E_, E_[:, ::-1]]; deg = np.bincount(E_[:, 0], minlength=len(X)).astype(float)
        for k in range(bl['iters']):
            for lam in (0.5, -0.53):
                acc = np.zeros_like(X); np.add.at(acc, E_[:, 0], X[E_[:, 1]]); L = acc/np.maximum(deg, 1)[:, None]-X
                X += lam*wf[:, None]*L
        log['blend_verts'] = int((wf > 0.05).sum())
    zz = np.arange(164.25, 158.24, -0.25); log['profile_before'] = {f'{q:.2f}': round(v, 3) for q, v in zip(zz, profile(X0, zz))}
    log['profile_after'] = {f'{q:.2f}': round(v, 3) for q, v in zip(zz, profile(X, zz))}
# ---------------- temple ----------------
if 'temple' in C:
    T = C['temple']; S = SOFT[SOFT < NH]; Q = X[S]
    r = np.linalg.norm((Q-np.array([MX, T.get('yc', 1.0), T.get('zc', 165.0)]))*np.array([1, 1, 1]), axis=1)
    lat = (np.abs(Q[:, 0]-MX)/np.maximum(r, 1e-6))**2
    f = plateau(Q[:, 2], T['tz'])*plateau(Q[:, 1], T['ty'])*lat
    dx = -T['A']*f*np.sign(Q[:, 0]-MX); X[S, 0] += dx
    def hw(X, z, y0, y1):
        H = X[:NH]; s = H[(np.abs(H[:, 2]-z) < 0.3) & (H[:, 1] > y0) & (H[:, 1] < y1)]; return round(float(np.abs(s[:, 0]-MX).max()), 3)
    log['temple_halfwidth'] = {f'z{z}': [hw(X0, z, -4, 6), hw(X, z, -4, 6)] for z in (162, 164, 165, 166, 167, 168, 169, 170, 171, 172)}
    log['temple_max_mm'] = round(10*float(np.abs(dx).max()), 2)
np.save(OUT, X); print('G12C_OK', json.dumps(log))
