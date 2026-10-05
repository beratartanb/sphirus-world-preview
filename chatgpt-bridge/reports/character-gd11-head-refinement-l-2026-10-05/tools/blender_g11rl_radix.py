"""GD11 refinement L: glabella-radix-upper-dorsum diagnosis on DNA-order head npys. Outer midline profile y(z) (front-most vertex per 0.1 cm bin,
|x-MX| < 0.25, y > 5; missing bins interpolated), printed for z 158-170; radix metrics: local minimum of y between z 162.2 and 164.8 (sellion),
glabella = max y between 164.0 and 166.5, dorsum reference = y at z 162.0; dip depth below the glabella->dorsum chord at the sellion (mm) and the
depth below the glabella alone (mm). Writes a profile plot (<out>.png): y(z) curves of all heads, mm scale, same axes.
usage: blender -b --factory-startup --python blender_g11rl_radix.py -- <out.png> <head1.npy> [<head2.npy> ...]"""
import bpy, sys, os, json, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; OUT = a[0]; HEADS = a[1:]; MX = -0.23
def profile(S):
    mid = (np.abs(S[:, 0]-MX) < 0.25) & (S[:, 1] > 5); zb = np.round(S[mid, 2]*10).astype(int); idx = np.flatnonzero(mid); P = {}
    for b in np.unique(zb):
        sel = idx[zb == b]; P[b] = float(S[sel, 1].max())
    ks = np.array(sorted(P)); vs = np.array([P[k] for k in ks]); return lambda z: float(np.interp(z*10, ks, vs))
curves = {}; W, H = 1400, 900; img = np.full((H, W, 3), 0.12, np.float32)
cols = [(0.9, 0.9, 0.9), (1.0, 0.45, 0.1), (0.3, 0.8, 1.0), (0.6, 1.0, 0.4), (1.0, 0.3, 0.8)]
zs = np.arange(158.0, 170.01, 0.1)
for i, hp in enumerate(HEADS):
    S = np.load(hp)[:24049]; Y = profile(S); ys = np.array([Y(z) for z in zs]); name = os.path.basename(hp).replace('.npy', ''); curves[name] = ys
    zz = np.arange(162.2, 164.81, 0.05); yy = np.array([Y(z) for z in zz]); si = int(np.argmin(yy)); sz, sy = float(zz[si]), float(yy[si])
    gz_ = np.arange(164.0, 166.51, 0.05); gy = np.array([Y(z) for z in gz_]); gi = int(np.argmax(gy)); gz, gyv = float(gz_[gi]), float(gy[gi])
    dz, dy = 162.0, Y(162.0); t = np.array([dy-gyv, dz-gz]); t /= np.linalg.norm(t); v = np.array([sy-gyv, sz-gz]); chord_dip = abs(v[0]*t[1]-v[1]*t[0])*10
    print('RADIX %s sellion y=%.2f z=%.1f | glabella y=%.2f z=%.1f | dorsum(162.0) y=%.2f | dip below chord %.2f mm | below glabella %.2f mm | slope 162->163 %.2f mm/cm' % (name, sy, sz, gyv, gz, dy, chord_dip, (gyv-sy)*10, (Y(162.0)-Y(163.0))*10))
    print('PROFILE %s ' % name+' '.join('%.1f:%.2f' % (z, Y(z)) for z in np.arange(158.0, 170.01, 0.5)))
    # plot: x = y (cm, 11..16.5), y = z (158..170)
    c = cols[i % len(cols)]
    for z, y in zip(zs, ys):
        px = int((y-11.0)/5.5*(W-80))+40; py = int(H-40-(z-158.0)/12.0*(H-80))
        if 0 <= px < W and 0 <= py < H: img[max(0, py-2):py+3, max(0, px-2):px+3] = c
for k in range(0, 13): py = int(H-40-k/12.0*(H-80)); img[py, 40:W-40] = np.maximum(img[py, 40:W-40], 0.22)
for k in range(0, 12): px = int(k*0.5/5.5*(W-80))+40; img[40:H-40, px] = np.maximum(img[40:H-40, px], 0.22)
o = bpy.data.images.new('p', W, H); rgba = np.ones((H, W, 4), np.float32); rgba[..., :3] = img; o.pixels.foreach_set(np.ascontiguousarray(rgba[::-1]).ravel()); o.filepath_raw = os.path.abspath(OUT); o.file_format = 'PNG'; o.save()
print('RADIX_PLOT', OUT, 'colours:', {os.path.basename(h).replace('.npy', ''): cols[i % len(cols)] for i, h in enumerate(HEADS)}, 'axes: x = y forward 11..16.5 cm (0.5 cm grid), y = z 158..170 cm (1 cm grid)')
