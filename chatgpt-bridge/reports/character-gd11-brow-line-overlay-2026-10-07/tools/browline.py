"""brow centreline + band (top/bottom) per column relative to the pupil, same method for photo and render: luminance blurred to a common
softness, darkest band in the window above the eye; output per u = (x - pupil_x)/half_IPD (u<0 medial), averaged over both sides."""
import bpy, sys, os, json, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; L = a[1]; ey, xl, xr = float(a[2]), float(a[3]), float(a[4]); out = a[5]
im = bpy.data.images.load(os.path.abspath(a[0])); w, h = im.size; A = np.array(im.pixels[:], np.float32).reshape(h, w, 4)[::-1][..., :3]
Y = np.nan_to_num(A @ np.array([0.3, 0.59, 0.11]))
def blur(Z, s):
    k = np.exp(-0.5*(np.arange(-3*s, 3*s+1)/s)**2); k /= k.sum()
    Z = np.apply_along_axis(lambda r: np.convolve(r, k, 'same'), 1, Z); return np.apply_along_axis(lambda c: np.convolve(c, k, 'same'), 0, Z)
Yb = blur(Y, 2.5); hi = abs(xr-xl)/2; res = {}
for sd, px in ((-1, xl), (1, xr)):   # sd -1 = image-left eye; medial direction is towards the other eye
    med = 1 if px < (xl+xr)/2 else -1
    for u in np.arange(-0.9, 1.31, 0.1):
        x = int(round(px - med*u*hi)); y0, y1 = int(ey-0.95*hi), int(ey-0.28*hi)
        col = Yb[y0:y1, max(x-1, 0):x+2].mean(1); base = np.percentile(col, 90)
        i = int(np.argmin(col)); depth = base-col[i]; thr = col[i]+0.5*depth; band = np.where(col <= thr)[0]
        res.setdefault(round(u, 1), []).append(((ey-(y0+i))/hi, (ey-(y0+band.min()))/hi, (ey-(y0+band.max()))/hi, depth))
rows = {u: np.mean(np.array(v), 0).round(3).tolist() for u, v in res.items()}
json.dump({'label': L, 'half_ipd_px': hi, 'rows': rows}, open(out, 'w')); print('BROW', L, 'done', len(rows))
