import bpy, sys, numpy as np
a = sys.argv[sys.argv.index('--') + 1:]
src, dst, k, cap = a[0], a[1], float(a[2]), float(a[3])
im = bpy.data.images.load(src); W, H = im.size
p = np.empty(W * H * 4, np.float32); im.pixels.foreach_get(p); p = p.reshape(H, W, 4)
rgb = p[..., :3].astype(np.float64)
red = rgb[..., 0] - 0.5 * (rgb[..., 1] + rgb[..., 2])
B = 32
lo = red[:H // B * B, :W // B * B].reshape(H // B, B, W // B, B).mean((1, 3))
# bilinear upsample of the block means
ys = (np.arange(H) + 0.5) / B - 0.5; xs = (np.arange(W) + 0.5) / B - 0.5
y0 = np.clip(np.floor(ys).astype(int), 0, lo.shape[0] - 2); x0 = np.clip(np.floor(xs).astype(int), 0, lo.shape[1] - 2)
fy = np.clip(ys - y0, 0, 1)[:, None]; fx = np.clip(xs - x0, 0, 1)[None, :]
L = (lo[y0][:, x0] * (1 - fy) * (1 - fx) + lo[y0 + 1][:, x0] * fy * (1 - fx)
     + lo[y0][:, x0 + 1] * (1 - fy) * fx + lo[y0 + 1][:, x0 + 1] * fy * fx)
m = np.median(lo)
ex = np.clip(L - m, 0, cap)  # capped so lips keep most of their colour
rgb[..., 0] -= k * ex; rgb[..., 1] -= 0.15 * k * ex
p[..., :3] = np.clip(rgb, 0, 1)
print('REDNESS median %.4f excess mean %.4f max %.4f' % (m, ex.mean(), ex.max()))
im.pixels.foreach_set(p.ravel()); im.filepath_raw = dst; im.file_format = 'PNG'; im.save()
