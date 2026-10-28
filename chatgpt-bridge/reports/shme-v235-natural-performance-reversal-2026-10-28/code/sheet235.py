"""sheet235.py <capture label> <t0> <t1> <step frames> <out.png> [--start 3.0] [--cols 8] [--crop x0,y0,x1,y1] [--scale 0.5]
Time-stamped frame strip from an unedited 30 fps capture (Saved/Codex/SHME_V138_20260927/Video/<label>/fNNNNN.jpg, frame 1 = capture start).
Every tile carries its game time; nothing is interpolated or re-timed."""
import sys, os
from PIL import Image, ImageDraw
a = sys.argv[1:]; lab, t0, t1, st, out = a[0], float(a[1]), float(a[2]), int(a[3]), a[4]
def opt(k, d): return a[a.index(k) + 1] if k in a else d
start = float(opt('--start', '3.0')); cols = int(opt('--cols', '8')); sc = float(opt('--scale', '0.5'))
crop = [int(x) for x in opt('--crop', '0,0,0,0').split(',')]
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Saved', 'Codex', 'SHME_V138_20260927', 'Video', lab)
tiles = []
k = int(round((t0 - start) * 30)) + 1
while start + (k - 1) / 30.0 <= t1 + 1e-6:
    p = os.path.join(V, 'f%05d.jpg' % k)
    if os.path.exists(p):
        im = Image.open(p).convert('RGB')
        if crop[2] > crop[0]: im = im.crop(crop)
        im = im.resize((int(im.width * sc), int(im.height * sc)))
        d = ImageDraw.Draw(im); d.rectangle([0, 0, 64, 16], fill=(0, 0, 0)); d.text((3, 2), '%.2f s' % (start + (k - 1) / 30.0), fill=(255, 255, 0))
        tiles.append(im)
    k += st
if not tiles: sys.exit('no frames')
w, h = tiles[0].size; rows = (len(tiles) + cols - 1) // cols
S = Image.new('RGB', (w * cols, h * rows), (20, 20, 20))
for i, t in enumerate(tiles): S.paste(t, ((i % cols) * w, (i // cols) * h))
S.save(out); print('SHEET', out, len(tiles), S.size)
