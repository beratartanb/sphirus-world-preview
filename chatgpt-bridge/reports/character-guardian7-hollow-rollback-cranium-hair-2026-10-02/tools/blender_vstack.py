"""Stack images vertically (each scaled to a common width) with a label bar per row. usage: blender -b -P blender_vstack.py -- <out.png> <width> <img>|<label> ..."""
import bpy, sys, os, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; OUT, W = a[0], int(a[1]); rows = []
for it in a[2:]:
    p, _, lab = it.partition('|'); im = bpy.data.images.load(os.path.abspath(p)); w, h = im.size; im.scale(W, max(1, int(h*W/w))); w, h = im.size
    x = np.asarray(im.pixels[:], np.float32).reshape(h, w, im.channels)[::-1, :, :3]; bar = np.full((14, W, 3), 0.1, np.float32); rows += [bar, x, np.full((6, W, 3), 0.2, np.float32)]
out = np.concatenate(rows, 0); h = out.shape[0]; rgba = np.ones((h, W, 4), np.float32); rgba[..., :3] = out
o = bpy.data.images.new('o', W, h); o.pixels.foreach_set(np.ascontiguousarray(rgba[::-1]).ravel()); o.filepath_raw = os.path.abspath(OUT); o.file_format = 'PNG'; o.save(); print('VSTACK_OK', OUT, W, h)
