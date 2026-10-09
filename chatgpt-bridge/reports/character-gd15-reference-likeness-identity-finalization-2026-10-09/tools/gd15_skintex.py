"""GD15 face base-colour authoring (support tool; the eye judges the result in UE). From the exported x19 baked base colour:
 1. anatomical region weights are defined on the 3D head (DNA order, project frame cm) and carried into UV space with the per-corner UV0
    (vertex splat + gaussian fill): freckle density, lip (vermilion) mask, redness mask;
 2. freckles: clustered, varied size / shape / opacity, dense on nose + cheeks, lighter on forehead / chin / upper lip, none on lids / lips;
 3. lips: luminance-preserving recolour of the whole vermilion (the x19 lower lip is grey-violet) toward a natural dusky rose;
 4. restrained redness on nose tip / cheek apples.
Seeded (reproducible). usage: blender -b --python gd15_skintex.py -- <bc.png> <head.npy> <uvc.f32> <tri.i32 (UE source triangles)> <out.png> <params json>"""
import sys, os, json, math, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'GD13_Identity_20261009', 'tools')); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; A = gi.load(a[0]); X = np.load(a[1]); UVC = np.fromfile(a[2], np.float32).reshape(-1, 3, 2); TRI = np.fromfile(a[3], np.int32).reshape(-1, 3); OUT = a[4]; PR = json.loads(open(a[5]).read())
rng = np.random.default_rng(PR.get('seed', 15)); N = A.shape[0]; MX = -0.23; NS = 24049
T = TRI
assert len(T) == len(UVC), (len(T), len(UVC))
S = X[:NS]; x = S[:, 0]-MX; ax = np.abs(x); y = S[:, 1]; z = S[:, 2]
def bump(v, c, w): return np.exp(-0.5*((v-c)/w)**2)
front = np.clip((y-4.0)/4.0, 0, 1)
nose = bump(ax, 0.0, 0.9)*bump(z, 160.0, 1.6)*np.clip((y-11.5)/1.5, 0, 1)
cheek = bump(ax, 3.4, 1.3)*bump(z, 159.6, 1.3)*front
forehead = bump(ax, 0.0, 3.5)*bump(z, 166.8, 1.8)*front
chin = bump(ax, 0.0, 1.8)*bump(z, 152.5, 1.0)*front
ulip_skin = bump(ax, 0.0, 1.6)*bump(z, 157.0, 0.45)*front
lids = bump(ax, 3.0, 1.2)*bump(z, 162.4, 0.55)
lipzone = (ax < 2.6) & (z > 154.3) & (z < 156.35) & (y > 11.5)
dens = PR.get('w_nose', 1.0)*nose+PR.get('w_cheek', 0.85)*cheek+PR.get('w_forehead', 0.25)*forehead+PR.get('w_chin', 0.25)*chin+PR.get('w_ulip', 0.2)*ulip_skin
dens = dens*(1-np.clip(lids*1.5, 0, 1))*(~lipzone)
red = PR.get('red_nose', 1.0)*bump(ax, 0.0, 0.7)*bump(z, 158.9, 0.8)*np.clip((y-13)/1.5, 0, 1)+PR.get('red_cheek', 0.7)*bump(ax, 3.0, 1.0)*bump(z, 159.0, 1.0)*front
lipw = np.zeros(NS); lipw[lipzone] = 1.0
# --- vertex weights -> UV maps (splat at every corner UV + gaussian fill), working res R
R = 1024
def tomap(w):
    acc = np.zeros((R, R)); cnt = np.zeros((R, R))
    sk = (T < NS).all(1); tri = T[sk]; uvc = UVC[sk]
    vi = tri.reshape(-1); uv = uvc.reshape(-1, 2); px = np.clip((uv[:, 0]*R).astype(int), 0, R-1); py = np.clip((uv[:, 1]*R).astype(int), 0, R-1)
    np.add.at(acc, (py, px), w[vi]); np.add.at(cnt, (py, px), 1.0)
    def blur(m, s):
        k = np.exp(-0.5*(np.arange(-3*s, 3*s+1)/s)**2); k /= k.sum()
        m = np.apply_along_axis(lambda r: np.convolve(r, k, 'same'), 1, m); return np.apply_along_axis(lambda c: np.convolve(c, k, 'same'), 0, m)
    a_ = blur(acc, 3); c_ = blur(cnt, 3); return np.where(c_ > 1e-3, a_/np.maximum(c_, 1e-6), 0.0)
def up(m):   # nearest 4x + light smooth to N
    f = N//R; m = np.kron(m, np.ones((f, f))); return m
lidm = np.clip(bump(ax, 3.0, 1.15)*bump(z, 162.3, 0.45)*1.4, 0, 1)
D = up(tomap(dens)); RD = up(tomap(red)); LP = up(tomap(lipw)); LD = up(tomap(lidm))
# f5 masks (optional ops, default off): upper-lip skin (philtrum band between the nostril sill and the vermilion; x19 has greenish-brown
# 'stubble' blotches there, the reference upper-lip skin is clean) and a faint infraorbital shadow (the reference shows under-eye darkness)
ulm = np.clip(bump(ax, 0.0, 1.5)*bump(z, 156.95, 0.42)*front*1.6, 0, 1)*(~lipzone)*np.clip((y-11.0)/1.0, 0, 1)
uem = np.clip(bump(ax, 2.75, 0.85)*bump(z, 160.55, 0.30)*front*1.3, 0, 1)
UL = up(tomap(ulm)) if PR.get('ulip_clean', 0) else None; UE = up(tomap(uem)) if PR.get('undereye_amt', 0) else None
print('MAPS', D.max().round(3), RD.max().round(3), LP.max().round(3))
B = A[..., :3].copy()
# --- lid margins: x19 lids are pink; luminance-preserving desaturation toward the surrounding skin hue
la = np.clip(LD, 0, 1)*PR.get('lid_desat', 0.0); lumL = B @ np.array([0.30, 0.59, 0.11]); sk = np.array(PR.get('lid_skin_rgb', [0.74, 0.55, 0.47])); skl = sk @ np.array([0.30, 0.59, 0.11])
B = B*(1-la[..., None])+(sk[None, None, :]*(lumL[..., None]/skl))*la[..., None]
if UL is not None:   # upper-lip skin: luminance-preserving hue toward the surrounding cheek skin + slight lift
    ua = np.clip(UL, 0, 1)*PR['ulip_clean']; lumU = B @ np.array([0.30, 0.59, 0.11]); us = np.array(PR.get('ulip_skin_rgb', [0.78, 0.58, 0.48])); usl = us @ np.array([0.30, 0.59, 0.11])
    B = B*(1-ua[..., None])+np.clip(us[None, None, :]*(lumU[..., None]/usl)*PR.get('ulip_lift', 1.0), 0, 1)*ua[..., None]
if UE is not None:   # faint infraorbital shadow, slightly violet-brown
    ue = np.clip(UE, 0, 1)*PR['undereye_amt']; tint = np.array(PR.get('undereye_rgb', [0.86, 0.80, 0.82])); B = B*(1-ue[..., None])+B*tint[None, None, :]*ue[..., None]
# --- redness (low amplitude)
rk = np.clip(RD, 0, 1)*PR.get('red_amt', 0.10); B[..., 1] *= (1-rk*0.9); B[..., 2] *= (1-rk*0.7)
# --- lips: luminance-preserving recolour toward a dusky rose
lt = np.array(PR.get('lip_rgb', [0.66, 0.42, 0.40])); lum = B @ np.array([0.30, 0.59, 0.11])
# vermilion = texture cue (lip texels have B/G > ~0.95, skin ~0.89) inside the dilated 3D lip zone, feathered
bg = B[..., 2]/np.maximum(B[..., 1], 1e-4); L0 = A[..., :3] @ np.array([0.30, 0.59, 0.11])
# lip texels: darker than the surrounding skin (L skin ~0.59) and B/G above skin (~0.86): sampled 2026-10-09 from x19
cue = np.clip((np.clip((PR.get('skinL', 0.59)-L0)/0.10, 0, 2)+np.clip((bg-0.88)/0.06, 0, 2))/2.0, 0, 1)
zone = np.clip(LP*2.0, 0, 1); lm0 = cue*zone
k = np.exp(-0.5*(np.arange(-6, 7)/2.0)**2); k /= k.sum(); lm0 = np.apply_along_axis(lambda r: np.convolve(r, k, 'same'), 1, lm0); lm0 = np.apply_along_axis(lambda c: np.convolve(c, k, 'same'), 0, lm0)
lm = np.clip(lm0*1.3, 0, 1)*PR.get('lip_amt', 0.75)
lum_ref = (lt @ np.array([0.30, 0.59, 0.11])); tgt = lt[None, None, :]*(lum[..., None]/lum_ref)**0.85
B = B*(1-lm[..., None])+np.clip(tgt, 0, 1)*lm[..., None]
# --- freckles: cluster centres ~ density, members around them
nC = PR.get('clusters', 260); nF = PR.get('freckles', 1700)
flat = D.ravel(); p = flat/flat.sum(); cidx = rng.choice(len(flat), size=nC, p=p); cy, cx = np.divmod(cidx, N)
px_per_cm = PR.get('px_per_cm', 136.0); mem = rng.integers(0, nC, size=nF)
spread = rng.uniform(0.15, 0.55, size=nC)*px_per_cm   # cluster radius 1.5-5.5 mm
ang = rng.uniform(0, 2*np.pi, nF); rad = np.abs(rng.normal(0, 1, nF))*spread[mem]
fx = (cx[mem]+np.cos(ang)*rad).astype(int); fy = (cy[mem]+np.sin(ang)*rad).astype(int); ok = (fx > 20) & (fx < N-20) & (fy > 20) & (fy < N-20)
fx, fy = fx[ok], fy[ok]; dl = D[fy, fx]; keep = rng.uniform(0, 1, len(fx)) < np.clip(dl/max(D.max(), 1e-6)*1.3, 0, 1); fx, fy = fx[keep], fy[keep]
fcol = np.array(PR.get('freckle_rgb', [0.70, 0.52, 0.40]))
cnt = 0
for i in range(len(fx)):
    r = float(np.clip(rng.lognormal(math.log(PR.get('r_mean_px', 6.0)), 0.45), 1.6, 14.0)); e = rng.uniform(0.65, 1.0); th = rng.uniform(0, np.pi)
    op = float(np.clip(rng.normal(PR.get('op_mean', 0.42), 0.14), 0.12, 0.8)); s = int(r*1.8)+2
    yy, xx = np.mgrid[-s:s+1, -s:s+1]; u_ = xx*np.cos(th)+yy*np.sin(th); v_ = (-xx*np.sin(th)+yy*np.cos(th))/e
    dd = np.sqrt(u_**2+v_**2)/r; m = np.clip(1.15-dd, 0, 1)**1.6*op
    m *= (0.8+0.4*rng.uniform(0, 1, m.shape))   # irregular edge
    m = np.clip(m, 0, 1)[..., None]; y0, x0 = fy[i], fx[i]
    reg = B[y0-s:y0+s+1, x0-s:x0+s+1]
    if reg.shape[:2] != m.shape[:2]: continue
    B[y0-s:y0+s+1, x0-s:x0+s+1] = reg*(1-m)+reg*fcol[None, None, :]*m; cnt += 1
hz = np.clip(D/max(D.max(), 1e-6), 0, 1)*PR.get('haze', 0.0); hc = np.array(PR.get('haze_rgb', [1.0, 0.95, 0.91]))
B = B*(1-hz[..., None])+B*hc[None, None, :]*hz[..., None]
O = A.copy(); O[..., :3] = np.clip(B, 0, 1); gi.save(OUT, O); print('SKINTEX_OK', OUT, 'freckles', cnt)
