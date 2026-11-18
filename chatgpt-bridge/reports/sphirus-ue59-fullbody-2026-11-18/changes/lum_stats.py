# lum_stats.py (Blender background): blender -b --python lum_stats.py -- <out.txt> <x0,y0,x1,y1 fractions | full> <img>...
# Per image: mean display luminance (0-1, Rec.709 on the 8-bit values), p50/p95/p99, clipped share (all channels >= 0.985)
# and near-clipped share (max channel >= 0.985) in the full frame and in the given box (top-left origin fractions).
import bpy, sys, numpy as np
a = sys.argv[sys.argv.index('--') + 1:]; out = a[0]; box = a[1]; imgs = a[2:]
if len(imgs) == 1 and imgs[0].startswith('@'): imgs = [l.strip() for l in open(imgs[0][1:], encoding='utf8') if l.strip()]
rows = []
for p in imgs:
    im = bpy.data.images.load(p); w, h = im.size
    px = np.empty(w * h * 4, dtype=np.float32); im.pixels.foreach_get(px); px = px.reshape(h, w, 4)[::-1, :, :3]
    def st(z):
        lum = 0.2126 * z[..., 0] + 0.7152 * z[..., 1] + 0.0722 * z[..., 2]
        mx = z.max(axis=2); mn = z.min(axis=2)
        return (float(lum.mean()), float(np.percentile(lum, 50)), float(np.percentile(lum, 95)), float(np.percentile(lum, 99)), float((mn >= 0.985).mean()), float((mx >= 0.985).mean()))
    f = st(px)
    if box != 'full':
        x0, y0, x1, y1 = [float(v) for v in box.split(',')]; b = st(px[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)])
    else: b = f
    rows.append('%-40s full mean %.3f p50 %.3f p95 %.3f p99 %.3f clip %.4f near %.4f | box mean %.3f p95 %.3f p99 %.3f clip %.4f near %.4f' % ((p.replace('\\', '/').split('/')[-1],) + f + (b[0], b[2], b[3], b[4], b[5])))
    bpy.data.images.remove(im)
open(out, 'w').write('\n'.join(rows) + '\n')
