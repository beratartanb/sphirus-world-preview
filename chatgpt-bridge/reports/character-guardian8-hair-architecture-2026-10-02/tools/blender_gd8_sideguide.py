"""GUARDIAN-8 side-hair-start guide: orthographic profile (y-z) of the LATERAL hair (|x|>XMIN, main+loose) over the head silhouette.
GD7 hair = red, GD8 hair = green, overlap = yellow; white line = the GD8 lateral-mass front boundary (5th pct of forward reach per height).
usage: blender -b -P blender_gd8_sideguide.py -- <head.npy> <gd7 strands.npz> <gd8 strands.npz> <out.png> [xmin]"""
import bpy, sys, os, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]); S = X[:24049]; XMIN = float(a[4]) if len(a) > 4 else 4.5; R = 9; W = 330; H = 340; y0, z0 = -18.0, 140.0
def pix(P): return ((P[:, 1]-y0)*R).astype(int), (H-1-(P[:, 2]-z0)*R).astype(int)
img = np.full((H, W, 3), 0.94, np.float32); u, v = pix(S); m = (u >= 0) & (u < W) & (v >= 0) & (v < H); img[v[m], u[m]] = 0.62
masks = []
for npz in a[1:3]:
    D = np.load(npz); Hh = np.concatenate([D['main'].reshape(-1, 3), D['loose'].reshape(-1, 3)]); Hh = Hh[np.abs(Hh[:, 0]) > XMIN]; mk = np.zeros((H, W), bool); u, v = pix(Hh); m = (u >= 0) & (u < W) & (v >= 0) & (v < H); mk[v[m], u[m]] = True
    mk = mk | np.roll(mk, 1, 0) | np.roll(mk, 1, 1); masks.append(mk)
a7, a8 = masks; img[a7 & ~a8] = (0.85, 0.25, 0.2); img[a8 & ~a7] = (0.2, 0.7, 0.3); img[a7 & a8] = (0.9, 0.8, 0.2)
for row in range(H):   # GD8 front boundary: right-most (forward, +y is right) occupied column with enough coverage
    cols = np.nonzero(a8[row])[0]
    if len(cols) > 6: img[row, max(int(np.percentile(cols, 97))-1, 0):int(np.percentile(cols, 97))+1] = (1, 1, 1)
rgba = np.ones((H, W, 4), np.float32); rgba[..., :3] = img; im = bpy.data.images.new('o', W, H); im.pixels.foreach_set(np.ascontiguousarray(rgba[::-1]).ravel())
im.filepath_raw = os.path.abspath(a[3]); im.file_format = 'PNG'; im.save(); im.scale(W*2, H*2); im.save(); print('SIDEGUIDE_OK')
