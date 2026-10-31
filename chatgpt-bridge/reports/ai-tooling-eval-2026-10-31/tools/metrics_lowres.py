"""metrics_lowres.py <shots_dir> <out_json> : noise floor of scale-reduced metrics + synthetic-change sensitivity (numpy only).

Full-resolution pixel metrics fail on the editor renders because foliage wind, TSR jitter and Lumen noise change most pixels
between two shots of an unchanged scene. This script measures the same pairs after box-downsampling by 8 and 16 and on a
16x9 tile grid (tile mean luma and mean RGB), which keeps object/lighting/layout-scale changes and averages away sub-pixel noise.

Sensitivity (SYNTHETIC, image-space only; nothing in the scene is changed): copies of the last converged shot with
  dark20   a 160x160 px area darkened by 20 % (e.g. a lost light / shadow change)
  patch    a 200x200 px area replaced by another part of the same image (e.g. a missing / moved object)
  shift3   the whole image shifted 3 px (camera pose error)
  gain5    global brightness +5 % (exposure drift)
are compared with the converged shot exactly like a real pair.
"""
import sys, os, json, struct
import numpy as np

SH, OUTJ = sys.argv[1], sys.argv[2]


def load(n):
    with open(os.path.join(SH, n.replace('.png', '.raw')), 'rb') as f:
        w, h = struct.unpack('<ii', f.read(8))
        return np.frombuffer(f.read(), np.uint8).reshape(h, w, 3)[:, :, ::-1].astype(np.float64)


def luma(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def down(a, k):
    h, w = (a.shape[0] // k) * k, (a.shape[1] // k) * k
    return a[:h, :w].reshape(h // k, k, w // k, k, -1).mean((1, 3))


G = np.exp(-0.5 * (np.arange(-5, 6) / 1.5) ** 2); G /= G.sum()


def blur(x):
    H, W = x.shape
    p = np.pad(x, 5, mode='reflect')
    yh = sum(G[k] * p[:, k:k + W] for k in range(11))
    return sum(G[k] * yh[k:k + H, :] for k in range(11))


def ssim(x, y):
    x, y = x / 255.0, y / 255.0
    C1, C2 = 0.01 ** 2, 0.03 ** 2
    mx, my = blur(x), blur(y)
    sxx, syy, sxy = blur(x * x) - mx * mx, blur(y * y) - my * my, blur(x * y) - mx * my
    m = ((2 * mx * my + C1) * (2 * sxy + C2)) / ((mx * mx + my * my + C1) * (sxx + syy + C2))
    return float(m[5:-5, 5:-5].mean())


def tiles(a):
    h, w = a.shape[0] // 9 * 9, a.shape[1] // 16 * 16
    return a[:h, :w].reshape(9, h // 9, 16, w // 16, -1).mean((1, 3))


def metrics(a, b):
    r = {}
    for k in (8, 16):
        da, db = down(a, k), down(b, k)
        la, lb = luma(da), luma(db)
        r['ssim_d%d' % k] = round(ssim(la, lb), 5)
        r['mae_luma_d%d' % k] = round(float(np.abs(la - lb).mean()), 3)
        r['p99_luma_d%d' % k] = round(float(np.percentile(np.abs(la - lb), 99)), 2)
    ta, tb = tiles(a), tiles(b)
    dl = np.abs(luma(ta) - luma(tb))
    r['tile_luma_max'] = round(float(dl.max()), 3)
    r['tile_luma_mean'] = round(float(dl.mean()), 3)
    r['tile_rgb_max'] = round(float(np.abs(ta - tb).max()), 3)
    r['global_luma_diff'] = round(float(luma(b).mean() - luma(a).mean()), 3)
    return r


views = ['house_front', 'pond', 'forest']
res = {'pairs': [], 'synthetic': []}
for v in views:
    A = lambda t: '%s__A_t%04.1f.png' % (v, t)
    pairs = [(A(12), A(14), 'static_converged'), (A(14), '%s__B_round2.png' % v, 'revisit'),
             ('%s__B_round2.png' % v, '%s__B_round3.png' % v, 'revisit'), (A(14), '%s__B_round3.png' % v, 'revisit')]
    if v != 'house_front':
        pairs.append((A(10), A(12), 'static_converged'))
    for na, nb, kind in pairs:
        r = metrics(load(na), load(nb)); r.update({'view': v, 'a': na, 'b': nb, 'kind': kind}); res['pairs'].append(r)
    base = load('%s__B_round3.png' % v)
    H, W, _ = base.shape
    s = {}
    m = base.copy(); m[H // 2 - 80:H // 2 + 80, W // 2 - 80:W // 2 + 80] *= 0.8; s['dark20_160px'] = m
    m = base.copy(); m[H // 2 - 100:H // 2 + 100, W // 2 - 100:W // 2 + 100] = base[100:300, 100:300]; s['patch_200px'] = m
    m = base.copy(); m[:, 3:] = base[:, :-3]; s['shift3px'] = m
    s['gain5pct'] = np.clip(base * 1.05, 0, 255)
    for name, img in s.items():
        r = metrics(base, img); r.update({'view': v, 'change': name}); res['synthetic'].append(r)
with open(OUTJ, 'w') as f:
    json.dump(res, f, indent=1)
print('LOWRES_DONE')
