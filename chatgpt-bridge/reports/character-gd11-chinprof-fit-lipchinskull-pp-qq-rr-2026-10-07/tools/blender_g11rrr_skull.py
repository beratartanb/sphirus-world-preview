"""GD11 pass RR: back-of-head SHAPE (not size) against the bald reference profile. Midline radius r(psi) from a vault centre in the y/z plane
(psi 0 = straight back, 90 = up) for the model and for the reference outline (tragus + lateral canthus alignment as in pass OO). The reference
is rescaled by the least-squares factor over the back arc so only the curvature difference is left (photo scale / alignment error cancels).
Prints per-angle residual (cm, + = reference rounder / further out) and writes an overlay png.
usage: blender -b --python blender_g11rrr_skull.py -- <head.npy> <out.png> [label]"""
import bpy, sys, os, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0])[:24049]; L = a[2] if len(a) > 2 else 'cand'; MX = -0.23
RT, RC = np.array([452.0, 505.0]), np.array([700.0, 425.0]); MT, MC = np.array([3.83, 159.97]), np.array([10.73, 162.27])
s = np.linalg.norm(RC-RT)/np.linalg.norm(MC-MT)
def topx(y, z): return RT[0]+(y-MT[0])*s, RT[1]-(z-MT[1])*s
im = bpy.data.images.load(os.path.abspath('Saved/Codex/GD11_MalarSkullOO_20261007/data/ref_bald_profile.png')); w, h = im.size; R = np.array(im.pixels[:], np.float32).reshape(h, w, 4)[::-1].copy()
bg = np.median(np.concatenate([R[:20, :, :3].reshape(-1, 3), R[:, -20:, :3].reshape(-1, 3)]), 0); rm = np.linalg.norm(R[..., :3]-bg, axis=-1) > 0.08
C = np.array([1.0, 163.6]); PS = np.arange(-10, 106, 5.0)
mid = (np.abs(X[:, 0]-MX) < 0.5) & (X[:, 2] > 156.0); Q = X[mid][:, 1:3]-C; psi_m = np.degrees(np.arctan2(Q[:, 1], -Q[:, 0])); rad_m = np.linalg.norm(Q, axis=1)
rmod, rref = [], []
for p in PS:
    sel = np.abs(psi_m-p) < 2.5; rmod.append(rad_m[sel].max() if sel.any() else np.nan)
    d = np.array([-np.cos(np.radians(p)), np.sin(np.radians(p))]); last = np.nan; inside = False
    for t in np.arange(2.0, 18.0, 0.02):
        y, z = C+t*d; px, py = topx(y, z); xi, yi = int(round(px)), int(round(py))
        if not (0 <= xi < w and 0 <= yi < h): break
        if rm[yi, xi]: inside = True; last = t
        elif inside and t-last > 0.3: break
    rref.append(last)
rmod, rref = np.array(rmod), np.array(rref); ok = np.isfinite(rmod) & np.isfinite(rref) & (PS >= 0)
k = float(np.sum(rref[ok]*rmod[ok])/np.sum(rref[ok]**2)); e = k*rref-rmod; e1 = rref-rmod
print('SKULL %s centre y%.1f z%.1f  ref scale-fit %.3f (1 = photo alignment exact)' % (L, C[0], C[1], k))
print('SKULL_ROW psi  r_model  r_ref(aligned)  diff_raw  diff_shape')
for p, m_, r_, d1, d2 in zip(PS, rmod, rref, e1, e): print('SKULL_ROW %4d  %6.2f  %6.2f  %+6.2f  %+6.2f' % (p, m_, r_, d1, d2))
O = R[..., :3].copy()
for p, m_, r_ in zip(PS, rmod, rref):
    d = np.array([-np.cos(np.radians(p)), np.sin(np.radians(p))])
    for rr, col in ((m_, (1, 0, 1)), (k*r_ if np.isfinite(r_) else np.nan, (0.1, 0.9, 1.0))):
        if not np.isfinite(rr): continue
        y, z = C+rr*d; px, py = topx(y, z); xi, yi = int(round(px)), int(round(py))
        if 0 <= xi < w and 0 <= yi < h: O[max(yi-4, 0):yi+5, max(xi-4, 0):xi+5] = col
O4 = np.concatenate([O, np.ones(O.shape[:2]+(1,), np.float32)], -1)[::-1]; o = bpy.data.images.new('s', w, h); o.pixels.foreach_set(np.ascontiguousarray(O4).ravel())
o.filepath_raw = os.path.abspath(a[1]); o.file_format = 'PNG'; o.save(); print('SKULL_OK', a[1])
