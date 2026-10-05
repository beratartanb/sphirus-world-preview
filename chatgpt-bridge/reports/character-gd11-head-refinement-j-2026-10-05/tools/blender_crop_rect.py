"""crop PNGs (top-left pixel coords). usage: blender -b --factory-startup --python blender_crop_rect.py -- x0 y0 x1 y1 <out1> <in1> [<out2> <in2> ...]"""
import bpy, sys, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; x0, y0, x1, y1 = map(int, a[:4]); pairs = a[4:]
for o_, i_ in zip(pairs[::2], pairs[1::2]):
    im = bpy.data.images.load(i_); w, h = im.size; A = np.array(im.pixels[:], np.float32).reshape(h, w, 4)[::-1]; A = A[y0:y1, x0:x1]
    o = bpy.data.images.new('c', A.shape[1], A.shape[0]); o.pixels.foreach_set(np.ascontiguousarray(A[::-1]).ravel()); o.filepath_raw = o_; o.file_format = 'PNG'; o.save(); print('CROP', o_)
