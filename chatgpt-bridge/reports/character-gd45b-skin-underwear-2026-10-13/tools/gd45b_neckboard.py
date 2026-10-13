"""GD45b: before/after board for the underwear removal. Top row = full PIE frames (0.5x), bottom row = Henley neckline crop (3x nearest).
Left = before (run 5, body default material MI_RV_Body_Skin with the baked MetaHuman underwear), right = after (run 6, MI_GD15_Body_s1 override).
usage: blender -b --python gd45b_neckboard.py -- before.png after.png out.png [x0 y0 x1 y1]   (crop box in top-left image coordinates)"""
import bpy, sys, numpy as np
a = sys.argv[sys.argv.index('--') + 1:]; before, after, out = a[0], a[1], a[2]
x0, y0, x1, y1 = (int(v) for v in a[3:7]) if len(a) >= 7 else (560, 520, 900, 700)
def load(p):
    im = bpy.data.images.load(p); w, h = im.size; buf = np.empty(w * h * 4, dtype=np.float32); im.pixels.foreach_get(buf)
    arr = buf.reshape(h, w, 4)[::-1].copy(); arr[..., 3] = 1.0; return arr   # top-down rows
def half(arr): h, w = arr.shape[0] // 2 * 2, arr.shape[1] // 2 * 2; return arr[:h, :w].reshape(h // 2, 2, w // 2, 2, 4).mean(axis=(1, 3))
def crop3(arr): return np.repeat(np.repeat(arr[y0:y1, x0:x1], 3, axis=0), 3, axis=1)
B, A = load(before), load(after); gap = 20
r1 = [half(B), half(A)]; r2 = [crop3(B), crop3(A)]
W = max(sum(x.shape[1] for x in r) + gap for r in (r1, r2)); H = r1[0].shape[0] + gap + r2[0].shape[0] + 3 * gap
canvas = np.ones((H, W, 4), dtype=np.float32) * np.array([0.12, 0.12, 0.12, 1.0], dtype=np.float32)
def put(row, y):
    x = (W - (sum(t.shape[1] for t in row) + gap)) // 2
    for t in row: canvas[y:y + t.shape[0], x:x + t.shape[1]] = t; x += t.shape[1] + gap
put(r1, gap); put(r2, gap + r1[0].shape[0] + gap)
# marker bars: red (before) / green (after) strips under each column of the crop row
yb = gap + r1[0].shape[0] + gap + r2[0].shape[0] + 4; x = (W - (sum(t.shape[1] for t in r2) + gap)) // 2
for t, col in zip(r2, ([0.8, 0.15, 0.15, 1.0], [0.15, 0.7, 0.2, 1.0])): canvas[yb:yb + 10, x:x + t.shape[1]] = col; x += t.shape[1] + gap
img = bpy.data.images.new('board', W, H, alpha=True); img.pixels.foreach_set(canvas[::-1].reshape(-1)); img.filepath_raw = out; img.file_format = 'PNG'; img.save()
print('BOARD', out, W, H, 'crop', (x0, y0, x1, y1))
