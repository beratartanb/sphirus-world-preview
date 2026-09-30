"""Crop a rectangle (fractions, may exceed the image: padded grey) and resample to W x H; optional 50 % blend with a reference.
Jobs: src|dst|x0|y0|x1|y1|W|H[|ref_to_blend]   usage: blender -b -P id_crop_rect.py -- job ..."""
import bpy, sys
import numpy as np
for job in sys.argv[sys.argv.index('--')+1:]:
    f = job.split('|'); src, dst = f[0], f[1]; x0, y0, x1, y1 = map(float, f[2:6]); W, H = int(f[6]), int(f[7])
    im = bpy.data.images.load(src); w, h = im.size; a = np.asarray(im.pixels[:], np.float32).reshape(h, w, im.channels)[::-1, :, :3]
    xs = (x0+(np.arange(W)+0.5)/W*(x1-x0))*w; ys = (y0+(np.arange(H)+0.5)/H*(y1-y0))*h
    xi = np.clip(xs.astype(int), 0, w-1); yi = np.clip(ys.astype(int), 0, h-1); o = a[yi][:, xi].copy()
    out_ = (ys < 0) | (ys >= h); o[out_] = 0.45; o[:, (xs < 0) | (xs >= w)] = 0.45
    if len(f) > 8:
        r = bpy.data.images.load(f[8]); rw, rh = r.size; b = np.asarray(r.pixels[:], np.float32).reshape(rh, rw, r.channels)[::-1, :, :3]
        b = b[(np.arange(H)*rh/H).astype(int)][:, (np.arange(W)*rw/W).astype(int)]; o = 0.5*o+0.5*b
    out = bpy.data.images.new('c', W, H); rgba = np.ones((H, W, 4), np.float32); rgba[..., :3] = o[::-1]; out.pixels.foreach_set(rgba.ravel()); out.filepath_raw = dst; out.file_format = 'PNG'; out.save(); print('RECT', dst)
