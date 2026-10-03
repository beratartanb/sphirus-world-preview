"""GUARDIAN-14 Phase D/E structural edits that stay anatomically consistent:
LIPS  - vermilion proportion remap in z between the semantic border curves (upper border zU, stomion zM, lower border zL as functions of |x|):
        each lip vertex keeps its fractional position inside its band, the bands are re-proportioned (stomion down dM, upper border up dU with
        cupid-peak extra, lower border up dL). Borders / stomion move as curves, so the lip seam stays closed and the vermilion colour (UV-bound)
        follows the new border. Lateral fade keeps the corners (mouth width unchanged); y-fade excludes the deep mouth interior.
LIDS  - upper lid rotated DOWN / lower lid UP about each eyeball centre (horizontal axis) inside the lid band: skin stays on the globe, so the
        lid / eyeball contact is preserved (no poke-through) while the palpebral fissure becomes less open.
usage: blender -b -P blender_gd14_lips_lids.py -- <in.npy> <out.npy>   env: L_DM L_DU L_DPEAK L_DL  E_UP_DEG E_LO_DEG"""
import sys, os, json, math, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; X0 = np.load(a[0]); X = X0.copy(); OUT = a[1]; MX = -0.25; NH = 24049
E = lambda k, d: float(os.environ.get(k, d))
def sstep(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
SEM = json.load(open('Saved/Codex/CharacterGuardian_20261001/semantic_j.json'))['front']
def crv(k): return np.array([(X0[np.array(t)]*np.array(w)[:, None]).sum(0) for t, w in SEM[k]])
def fx(k):   # curve as z(|x|) averaged over both sides
    P = np.vstack([crv(k+'_l'), crv(k+'_r')]); ax = np.abs(P[:, 0]-MX); o = np.argsort(ax); return ax[o], P[o, 2]
S = X0[:NH]; ax = np.abs(S[:, 0]-MX)
xu, zu = fx('crv_lip_upper_outer'); xp, zp = fx('crv_lip_philtrum'); xu = np.r_[xp, xu]; zu = np.r_[zp, zu]; o = np.argsort(xu); xu, zu = xu[o], zu[o]
xi, zi = fx('crv_lip_upper_inner'); xj, zj = fx('crv_lip_lower_inner'); xl, zl = fx('crv_lip_lower_outer')
ZU = np.interp(ax, xu, zu); ZM = 0.5*(np.interp(ax, xi, zi)+np.interp(ax, xj, zj)); ZL = np.interp(ax, xl, zl)
lat = 1-sstep((ax-E('L_X0', 1.9))/0.6); dep = sstep((S[:, 1]-11.8)/0.8)
dU = E('L_DU', 0.06)*lat+E('L_DPEAK', 0.03)*np.exp(-((ax-0.55)/0.25)**2); dM = E('L_DM', -0.12)*(lat*0.75+0.25*(1-sstep((ax-2.5)/0.2))); dL = E('L_DL', 0.09)*(1-sstep((ax-1.5)/0.5))
z = S[:, 2]; nz = z.copy()
up = (z >= ZM) & (z <= ZU); t = (z-ZM)/np.maximum(ZU-ZM, 1e-4); nz[up] = (ZM+dM+t*(ZU+dU-ZM-dM))[up]
lo = (z >= ZL) & (z < ZM); t = (z-ZL)/np.maximum(ZM-ZL, 1e-4); nz[lo] = (ZL+dL+t*(ZM+dM-ZL-dL))[lo]
ab = (z > ZU) & (z < ZU+0.6); nz[ab] = (z+dU*(1-sstep((z-ZU)/0.6)))[ab]
be = (z < ZL) & (z > ZL-0.6); nz[be] = (z+dL*(1-sstep((ZL-z)/0.6)))[be]
band = (ax < 2.9) & (z > 153.6) & (z < 157.2)
X[:NH, 2] = np.where(band, S[:, 2]+(nz-S[:, 2])*dep, S[:, 2])
log = {'lip_center_before_mm': [round(10*(np.interp(0, xu, zu)-0.5*(zi[0]+zj[0])), 2), round(10*(0.5*(zi[0]+zj[0])-zl[0]), 2)]}
# ---- lids
for nm, (s0, s1) in (('A', (28955, 29725)), ('B', (29725, 30495))):
    Eb = X0[s0:s1]; c = Eb.mean(0); r = np.linalg.norm(Eb-c, axis=1).max()
    P = X[:NH]-c; dist = np.linalg.norm(P, axis=1)-r; rx = (S[:, 0]-c[0])*np.sign(c[0]-MX)
    shell = (dist > -0.15) & (dist < 0.45) & (P[:, 1] > 0.1) & (rx > -1.55) & (rx < 1.65)
    latw = sstep((rx+1.55)/0.5)*(1-sstep((rx-1.15)/0.5))
    zrel = P[:, 2]
    # upper lid: margin height above centre ~0.45 cm; full weight up to margin+0.12, fade to 0 at +0.7
    wu = shell*(zrel > 0.05)*latw*(1-sstep((zrel-0.55)/0.6)); wl = shell*(zrel < -0.05)*latw*(1-sstep((-zrel-0.5)/0.45))
    for w, deg in ((wu, -E('E_UP_DEG', 3.5)), (wl, E('E_LO_DEG', 1.5))):
        ph = np.radians(deg)*w; cy, cz = P[:, 1], P[:, 2]
        ny = cy*np.cos(ph)-cz*np.sin(ph); nz2 = cy*np.sin(ph)+cz*np.cos(ph)
        P = np.stack([P[:, 0], ny, nz2], 1)
    X[:NH] = np.where(((wu > 0) | (wl > 0))[:, None], P+c, X[:NH])
d = np.linalg.norm(X-X0, axis=1)
print('LIPSLIDS_OK', json.dumps(log), 'max mm %.2f' % (10*d.max()))
np.save(OUT, X)
