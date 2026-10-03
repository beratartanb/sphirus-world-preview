"""GUARDIAN-14: draw the clay silhouette outline (and its internal depth edges) over the reference photo, same review frame.
usage: blender -b -P blender_gd14_outline.py -- <out.png> <ref.png> <clay.png> [<clay2.png> ...]   (clay1 red, clay2 cyan, clay3 yellow)"""
import bpy, sys, os, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; out, ref = a[0], a[1]; clays = a[2:]
def load(p):
    im = bpy.data.images.load(os.path.abspath(p)); w, h = im.size; x = np.asarray(im.pixels[:], np.float32).reshape(h, w, im.channels)[::-1, :, :3].copy(); return x
R = load(ref); cols = [np.array([1, 0.1, 0.1]), np.array([0.1, 1, 1]), np.array([1, 1, 0.1])]
for i, cp in enumerate(clays):
    Cl = load(cp); bg = Cl[2, 2]; m = np.abs(Cl-bg).sum(2) > 0.04
    e = m ^ np.roll(m, 1, 0) | m ^ np.roll(m, 1, 1)
    e = e | np.roll(e, 1, 0) | np.roll(e, 1, 1)
    R[e] = cols[i % 3]
h, w = R.shape[:2]; rgba = np.ones((h, w, 4), np.float32); rgba[..., :3] = R; o = bpy.data.images.new('o', w, h); o.pixels.foreach_set(np.ascontiguousarray(rgba[::-1]).ravel()); o.filepath_raw = os.path.abspath(out); o.file_format = 'PNG'; o.save(); print('OUTLINE_OK')
