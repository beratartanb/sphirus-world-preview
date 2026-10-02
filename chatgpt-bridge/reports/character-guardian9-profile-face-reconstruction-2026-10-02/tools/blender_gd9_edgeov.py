"""GUARDIAN-9: edge overlay of clay renders on the reference (same camera frame): clay shading edges (gradient) drawn in colour over the
grey reference, several candidates in different colours (1st red, 2nd green, 3rd blue). usage: blender -b -P blender_gd9_edgeov.py -- <out.png> <ref.png> <clay1.png> [...]"""
import bpy, sys, os, numpy as np
a = sys.argv[sys.argv.index('--')+1:]
def L(p):
    im = bpy.data.images.load(os.path.abspath(p)); w, h = im.size; x = np.asarray(im.pixels[:], np.float32).reshape(h, w, im.channels)[::-1].copy(); return x
R = L(a[1]); g = R[..., :3].mean(-1, keepdims=True); out = np.repeat(g*0.85, 3, -1)
cols = [(1, 0.15, 0.1), (0.1, 0.9, 0.2), (0.2, 0.5, 1.0)]
for k, p in enumerate(a[2:]):
    C = L(p); A = C[..., 3] if C.shape[2] == 4 else np.ones(C.shape[:2]); l = C[..., :3].mean(-1)
    for _ in range(4): l = (l+np.roll(l, 1, 0)+np.roll(l, -1, 0)+np.roll(l, 1, 1)+np.roll(l, -1, 1))/5
    gy, gx = np.gradient(l); e = np.hypot(gx, gy); m = (e > np.percentile(e[A > 0.5], 97)) & (A > 0.5)
    sil = (A > 0.5) & ~((np.roll(A, 1, 0) > 0.5) & (np.roll(A, -1, 0) > 0.5) & (np.roll(A, 1, 1) > 0.5) & (np.roll(A, -1, 1) > 0.5))
    sil = sil | np.roll(sil, 1, 1); out[m | sil] = cols[k % 3]
h, w = out.shape[:2]; rgba = np.ones((h, w, 4), np.float32); rgba[..., :3] = out; im = bpy.data.images.new('o', w, h); im.pixels.foreach_set(np.ascontiguousarray(rgba[::-1]).ravel())
im.filepath_raw = os.path.abspath(a[0]); im.file_format = 'PNG'; im.save(); print('EDGEOV_OK')
