"""GD42: front-surface height map of the chest by ray casting (robust to the sparse breast mesh), breast metrics.
usage: blender -b --python gd42_breastmap.py -- <libdir> <pkg> <lk> <extra|-> <label> <out_dir>"""
import sys, os, json, numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0, sys.argv[sys.argv.index('--')+1]); from gd42_lib import Body, MX
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+2:]; PKG, LKJ, EXTRA, LAB, OUT = a[:5]; os.makedirs(OUT, exist_ok=True)
B = Body(PKG, LKJ, extra=None if EXTRA == '-' else EXTRA); XR = B.XR; T = B.T
bvh = BVHTree.FromPolygons([Vector(p) for p in XR], [list(t) for t in T])
xs = np.arange(-20, 20.01, 0.25); zs = np.arange(104, 140.01, 0.25); Y = np.full((len(zs), len(xs)), np.nan)
for i, zz in enumerate(zs):
    for j, xx in enumerate(xs):
        hit = bvh.ray_cast(Vector((xx, 40.0, zz)), Vector((0, -1, 0)), 60.0)
        if hit[0] is not None: Y[i, j] = hit[0].y
np.save(os.path.join(OUT, f'chestmap_{LAB}.npy'), Y); json.dump({'xs': xs.tolist(), 'zs': zs.tolist()}, open(os.path.join(OUT, 'chestmap_axes.json'), 'w'))
# metrics (subject's left breast, x>0)
def col(xx): return Y[:, int(round((xx+20)/0.25))]
def row(zz): return Y[int(round((zz-104)/0.25)), :]
sub = Y[:, xs > 3.0]; sub = np.where(np.isnan(sub), -99, sub); sub[(zs < 118) | (zs > 136), :] = -99
i, j = np.unravel_index(np.argmax(sub), sub.shape); ax, az, ay = xs[xs > 3.0][j], zs[i], sub[i, j]
c = col(ax); zi = np.arange(len(zs))
below = (zs < az-1.5) & (zs > az-12); kf = np.nanargmin(np.where(below, c, np.inf)); imf_z, imf_y = zs[kf], c[kf]
wall_y = np.nanmean(c[(zs > imf_z-5) & (zs < imf_z-2)])
up3, up6 = c[int(round((az+3-104)/0.25))], c[int(round((az+6-104)/0.25))]
r = row(az); med = r[(xs > 0) & (xs < ax)]; valley_x = xs[(xs > 0) & (xs < ax)][np.nanargmin(med)]; valley_y = np.nanmin(med)
lat = r[(xs > ax) & (xs < 20)]; latx = xs[(xs > ax) & (xs < 20)]
# lateral wall: x where the surface has dropped to 50% / 90% of the projection toward the lateral wall
proj = ay-wall_y
def xat(frac):
    k = np.nonzero(lat < ay-frac*proj)[0]; return float(latx[k[0]]) if len(k) else None
print('BREAST', json.dumps({'label': LAB, 'apex': [round(float(ax), 2), round(float(ay), 2), round(float(az), 2)], 'imf_z': round(float(imf_z), 2), 'imf_y': round(float(imf_y), 2), 'wall_y': round(float(wall_y), 2),
    'projection_cm': round(float(proj), 2), 'apex_to_imf_cm': round(float(az-imf_z), 2), 'upper_pole_y_at+3': round(float(up3), 2), 'upper_pole_y_at+6': round(float(up6), 2),
    'valley_x': round(float(valley_x), 2), 'valley_y': round(float(valley_y), 2), 'valley_depth': round(float(ay-valley_y), 2), 'lat_x_50': xat(0.5), 'lat_x_90': xat(0.9)}))
print('SAGCOL', LAB, [(float(zz), round(float(v), 2)) for zz, v in zip(zs[::4], c[::4]) if not np.isnan(v)])
print('TRANSROW', LAB, [(float(xx), round(float(v), 2)) for xx, v in zip(xs[::4], r[::4]) if not np.isnan(v) and xx >= -2])
# image: height map normalised 0..16 cm, plus the apex-row and apex-column profiles as curves
img = np.clip((np.nan_to_num(Y, nan=0.0)-0.0)/16.0, 0, 1); img = np.repeat(img[::-1, :, None], 3, 2); gi.save(os.path.join(OUT, f'chestmap_{LAB}.png'), gi.resize(img, img.shape[1]*4, img.shape[0]*4)); print('MAP_OK')
