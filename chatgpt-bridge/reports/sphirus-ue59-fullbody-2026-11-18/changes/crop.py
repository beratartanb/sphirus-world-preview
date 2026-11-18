# crop.py (Blender background): -- <out.jpg> <x0,y0,x1,y1 fractions top-left> <cols> <img>... : crop each image to the box and tile them
import bpy, sys, numpy as np
a = sys.argv[sys.argv.index('--') + 1:]; out, box, cols, fs = a[0], [float(v) for v in a[1].split(',')], int(a[2]), a[3:]
if len(fs) == 1 and fs[0].startswith('@'): fs = [l.strip() for l in open(fs[0][1:], encoding='utf8') if l.strip()]
tiles = []
for f in fs:
    im = bpy.data.images.load(f); w, h = im.size; px = np.empty(w * h * 4, dtype=np.float32); im.pixels.foreach_get(px); px = px.reshape(h, w, 4)
    y0, y1 = int((1 - box[3]) * h), int((1 - box[1]) * h); x0, x1 = int(box[0] * w), int(box[2] * w); tiles.append(px[y0:y1, x0:x1].copy()); bpy.data.images.remove(im)
th, tw = tiles[0].shape[0], tiles[0].shape[1]; rows = (len(tiles) + cols - 1) // cols
canvas = np.ones((rows * th, cols * tw, 4), dtype=np.float32)
for i, t in enumerate(tiles):
    r = rows - 1 - i // cols; c = i % cols; canvas[r * th:(r + 1) * th, c * tw:(c + 1) * tw] = t
o = bpy.data.images.new('o', cols * tw, rows * th); o.pixels.foreach_set(canvas.ravel()); o.filepath_raw = out; o.file_format = 'JPEG'; o.save()
