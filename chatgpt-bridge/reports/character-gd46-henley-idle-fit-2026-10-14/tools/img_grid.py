"""GD46: grid board from PNGs (Blender numpy; no PIL in the engine Python). Each cell is box-downsampled to a common height; rows are given as
groups of paths; optional crop box applied to every input (top-left coords of the source images).
usage: blender -b --python img_grid.py -- out.png cell_h "a.png,b.png,c.png" "d.png,e.png,f.png" [x0 y0 x1 y1]"""
import bpy, sys, numpy as np
a = sys.argv[sys.argv.index('--') + 1:]; out = a[0]; CH = int(a[1]); rows = [r.split(',') for r in a[2:] if ',' in r or r.endswith('.png')]
crop = None
if len(a) >= 7 and all(x.lstrip('-').isdigit() for x in a[-4:]): crop = [int(x) for x in a[-4:]]; rows = [r.split(',') for r in a[2:-4]]
def load(p):
    im = bpy.data.images.load(p); w, h = im.size; buf = np.empty(w * h * 4, dtype=np.float32); im.pixels.foreach_get(buf); arr = buf.reshape(h, w, 4)[::-1].copy(); arr[..., 3] = 1.0
    if crop: arr = arr[crop[1]:crop[3], crop[0]:crop[2]]
    return arr
def fit(arr, H):
    h, w = arr.shape[:2]; f = max(1, int(round(h / H)))
    if f > 1: h2, w2 = h // f * f, w // f * f; arr = arr[:h2, :w2].reshape(h2 // f, f, w2 // f, f, 4).mean(axis=(1, 3))
    return arr
gap = 16; cells = [[fit(load(p), CH) for p in r] for r in rows]
W = max(sum(c.shape[1] for c in r) + gap * (len(r) + 1) for r in cells); H = sum(max(c.shape[0] for c in r) for r in cells) + gap * (len(cells) + 1)
canvas = np.ones((H, W, 4), dtype=np.float32) * np.array([0.12, 0.12, 0.12, 1.0], dtype=np.float32); y = gap
for r in cells:
    x = gap; rh = max(c.shape[0] for c in r)
    for c in r: canvas[y:y + c.shape[0], x:x + c.shape[1]] = c; x += c.shape[1] + gap
    y += rh + gap
img = bpy.data.images.new('grid', W, H, alpha=True); img.pixels.foreach_set(canvas[::-1].reshape(-1)); img.filepath_raw = out; img.file_format = 'PNG'; img.save(); print('GRID', out, W, H)
