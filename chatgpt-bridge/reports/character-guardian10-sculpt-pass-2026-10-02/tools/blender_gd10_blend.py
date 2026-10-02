"""50% blend of a clay render (alpha) over a reference image of the same frame. usage: blender -b -P blender_gd10_blend.py -- <out> <ref> <clay> [alpha]"""
import bpy, sys, os, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; al = float(a[3]) if len(a) > 3 else 0.5
def L(p):
    im = bpy.data.images.load(os.path.abspath(p)); w, h = im.size; x = np.asarray(im.pixels[:], np.float32).reshape(h, w, im.channels).copy(); return x, w, h
R, w, h = L(a[1]); C, _, _ = L(a[2]); m = C[..., 3:4]*al; out = R.copy(); out[..., :3] = R[..., :3]*(1-m)+C[..., :3]*m
im = bpy.data.images.new('o', w, h, alpha=True); im.pixels.foreach_set(np.ascontiguousarray(out).ravel()); im.filepath_raw = os.path.abspath(a[0]); im.file_format = 'PNG'; im.save(); print('BLEND_OK')
