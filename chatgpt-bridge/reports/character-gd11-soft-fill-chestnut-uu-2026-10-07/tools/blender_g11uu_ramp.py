"""pass UU: under-eye -> upper nasal-bridge RAMP. At each height z the current front surface y(x) between the nasal sidewall anchor x_a and
the under-eye anchor x_b is compared with the straight line joining y(x_a) and y(x_b); skin BELOW that line is raised toward it by `amt`
(fill only, never cut), so the step between the nose sidewall and the cheek becomes a flat, inclined ramp. Eyelids / eyeballs are frozen with
the same eye ellipsoid as the fit tools; smooth z / x fades. Applied symmetrically (both sides).
usage: blender -b --python blender_g11uu_ramp.py -- <in.npy> <out.npy> <x_a> <x_b> <z0> <z1> <amt> [ramp_fade_cm]"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from id_common import SEG, pkg
a = sys.argv[sys.argv.index('--')+1:]; X0 = np.load(a[0]); X = X0.copy(); xa, xb, z0, z1, amt = [float(v) for v in a[2:7]]; fd = float(a[7]) if len(a) > 7 else 0.3
MX = -0.23; NH = 24049; SOFT = np.r_[np.arange(*SEG['skin']), np.arange(*SEG['cartilage'])]; SOFT = SOFT[SOFT < NH]
def ss(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
H = X0[:NH]; eye = np.zeros(NH)
for sd in (1, -1):
    c = np.array([MX+sd*2.97, 10.5, 162.25]); d = np.sqrt((((H-c)/np.array([1.9, 2.2, 1.25]))**2).sum(1)); eye = np.maximum(eye, 1-ss((d-0.8)/0.35))
def front_y(x, z):
    s = (np.abs(np.abs(H[:, 0]-MX)-x) < 0.09) & (np.abs(H[:, 2]-z) < 0.09) & (H[:, 1] > 9)
    return H[s, 1].max() if s.any() else np.nan
zs = np.arange(z0-fd, z1+fd+0.001, 0.1); YA = np.array([front_y(xa, z) for z in zs]); YB = np.array([front_y(xb, z) for z in zs])
ok = np.isfinite(YA) & np.isfinite(YB); zs, YA, YB = zs[ok], YA[ok], YB[ok]
dy = np.zeros(NH)
for i in SOFT:
    p = H[i]; ax = abs(p[0]-MX)
    if not (xa < ax < xb) or p[1] < 9 or not (z0-fd < p[2] < z1+fd): continue
    ya = np.interp(p[2], zs, YA); yb = np.interp(p[2], zs, YB); line = ya+(yb-ya)*(ax-xa)/(xb-xa)
    if line <= p[1]: continue
    wz = ss((p[2]-(z0-fd))/fd)*(1-ss((p[2]-z1)/fd)); wx = ss((ax-xa)/0.45)*(1-ss((ax-(xb-0.45))/0.45))
    dy[i] = amt*(line-p[1])*wz*wx*(1-eye[i])
# outer-shell only: a vertex well behind the local front surface (inner nostril / lid underside) is not moved
TRI = np.asarray(pkg()['head']['triangles']); E = np.r_[TRI[:, [0, 1]], TRI[:, [1, 2]], TRI[:, [2, 0]]]; E = np.r_[E, E[:, ::-1]]; E = E[(E[:, 0] < NH) & (E[:, 1] < NH)]
DEG = np.bincount(E[:, 0], minlength=NH).astype(float); MASK = np.zeros(NH); MASK[SOFT] = 1.0; MASK *= (1-eye)
for _ in range(int(os.environ.get('RAMP_SMOOTH', '25'))):   # diffuse the displacement field over the surface (no patch edges); eyes stay frozen
    acc = np.zeros(NH); np.add.at(acc, E[:, 0], dy[E[:, 1]]); dy = (dy+0.5*(acc/np.maximum(DEG, 1)-dy))*MASK
X[:NH, 1] += dy; np.save(a[1], X)
print('RAMP moved %d verts, max %.2f mm, mean(moved) %.2f mm' % (int((dy > 1e-4).sum()), dy.max()*10, dy[dy > 1e-4].mean()*10 if (dy > 1e-4).any() else 0))
