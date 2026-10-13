"""GD46: crop + nearest upscale of a region of a PNG (Blender numpy; the engine Python has no PIL).
usage: blender -b --python img_crop.py -- in.png out.png x0 y0 x1 y1 [scale]   (top-left image coordinates)"""
import bpy, sys, numpy as np
a = sys.argv[sys.argv.index('--') + 1:]; src, out = a[0], a[1]; x0, y0, x1, y1 = (int(v) for v in a[2:6]); s = int(a[6]) if len(a) > 6 else 2
im = bpy.data.images.load(src); w, h = im.size; buf = np.empty(w * h * 4, dtype=np.float32); im.pixels.foreach_get(buf)
arr = buf.reshape(h, w, 4)[::-1]; crop = np.repeat(np.repeat(arr[y0:y1, x0:x1], s, axis=0), s, axis=1).copy(); crop[..., 3] = 1.0
o = bpy.data.images.new('crop', crop.shape[1], crop.shape[0], alpha=True); o.pixels.foreach_set(crop[::-1].reshape(-1)); o.filepath_raw = out; o.file_format = 'PNG'; o.save()
print('CROP', out, crop.shape[1], crop.shape[0])
