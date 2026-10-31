"""metrics_t1.py <shots_dir> <out_dir> : T1 repeatability metrics (numpy only; run with Blender's bundled Python, nothing installed).

Per image pair:
  ssim_g    standard SSIM (Wang et al. 2004): Gaussian window sigma 1.5 (11 taps), K1 0.01, K2 0.03, on Rec.709 luma of the
            8-bit sRGB-coded values. SIMILARITY index: 1 = identical, lower = less similar (can go below 0).
  ssim_ue8  Unreal FImageComparer::CompareStructuralSimilarity re-implemented (8x8 non-overlapping windows, luminance*contrast
            terms only). Present in the engine but commented out in ScreenShotManager (not used for pass/fail).
  ue_low    Unreal automation screenshot comparison re-implemented (ImageComparer.cpp, 5.8): EComparisonTolerance::Low
            = R/G/B/A 16, MinBrightness 16, MaxBrightness 240, bIgnoreAntiAliasing true (FAutomationScreenshotOptions default),
            MaximumLocalError 0.10 (worst of 10x10 blocks), MaximumGlobalError 0.02. Reports global/local mismatch fractions and
            PASS/FAIL. ue_low_noaa = same without the anti-aliasing exemption.
  psnr, mae (0-255), p99 / max abs channel difference, frac of pixels with luma diff > 2/255 and > 8/255.
FLIP is NOT computed here (needs the official NVlabs implementation; not installed).
Heat maps (luma |diff| x8, and 1-SSIM) are written as .raw for imgconv.ps1 raw2png.
"""
import sys, os, json, struct
import numpy as np

SH, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)


def load(name):
    with open(os.path.join(SH, name.replace('.png', '.raw')), 'rb') as f:
        w, h = struct.unpack('<ii', f.read(8))
        a = np.frombuffer(f.read(), np.uint8).reshape(h, w, 3)[:, :, ::-1]  # BGR -> RGB
    return a


def save_raw(name, rgb):
    h, w, _ = rgb.shape
    with open(os.path.join(OUT, name + '.raw'), 'wb') as f:
        f.write(struct.pack('<ii', w, h)); f.write(np.ascontiguousarray(rgb[:, :, ::-1]).tobytes())


def luma(a):  # Rec.709 weights on the stored 8-bit values (same weights as Unreal's GetLuminance)
    a = a.astype(np.float64)
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


G = np.exp(-0.5 * (np.arange(-5, 6) / 1.5) ** 2); G /= G.sum()


def blur(x):  # separable 11-tap Gaussian, reflect padding
    H, W = x.shape
    p = np.pad(x, 5, mode='reflect')
    yh = sum(G[k] * p[:, k:k + W] for k in range(11))   # (H+10, W)
    return sum(G[k] * yh[k:k + H, :] for k in range(11))  # (H, W)


def ssim_g(a, b):
    x, y = luma(a) / 255.0, luma(b) / 255.0
    C1, C2 = 0.01 ** 2, 0.03 ** 2
    mx, my = blur(x), blur(y)
    sxx, syy, sxy = blur(x * x) - mx * mx, blur(y * y) - my * my, blur(x * y) - mx * my
    m = ((2 * mx * my + C1) * (2 * sxy + C2)) / ((mx * mx + my * my + C1) * (sxx + syy + C2))
    return float(m[5:-5, 5:-5].mean()), m


def ssim_ue8(a, b):
    x, y = luma(a), luma(b)
    h, w = (x.shape[0] // 8) * 8, (x.shape[1] // 8) * 8
    X = x[:h, :w].reshape(h // 8, 8, w // 8, 8); Y = y[:h, :w].reshape(h // 8, 8, w // 8, 8)
    mx, my = X.mean((1, 3)), Y.mean((1, 3))
    vx, vy = X.var((1, 3)), Y.var((1, 3))
    cxy = ((X - mx[:, None, :, None]) * (Y - my[:, None, :, None])).mean((1, 3))
    C1, C2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    s = (2 * mx * my + C1) / (mx ** 2 + my ** 2 + C1) * (2 * cxy + C2) / (vx + vy + C2)
    return float(s.mean())


def hue(a):
    f = a.astype(np.float32) / 255.0
    R, Gc, B = f[..., 0], f[..., 1], f[..., 2]
    mx, mn = f.max(-1), f.min(-1); d = mx - mn
    h = np.zeros_like(mx); nz = d > 0; dd = np.where(nz, d, 1)
    hr = (Gc - B) / dd + np.where(Gc < B, 6, 0); hg = (B - R) / dd + 2; hb = (R - Gc) / dd + 4
    h = np.where(mx == R, hr, np.where(mx == Gc, hg, hb))
    return np.where(nz, h / 6.0, 0.0)


def antialiased(a):
    """FPixelOperations::IsAntialiased for every pixel (3x3 neighbourhood, out-of-image neighbours skipped)."""
    H, W, _ = a.shape
    L = luma(a); Hh = hue(a); ai = a.astype(np.int16)
    hc = np.zeros((H, W), np.int16); same = np.zeros((H, W), np.int16); dh = np.zeros((H, W), np.int16)
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            if di == 0 and dj == 0:
                continue
            ys, ye = max(0, -di), H - max(0, di); xs, xe = max(0, -dj), W - max(0, dj)
            src = (slice(ys, ye), slice(xs, xe)); nb = (slice(ys + di, ye + di), slice(xs + dj, xe + dj))
            hc[src] += (np.abs(L[src] - L[nb]) > 240)
            same[src] += np.all(ai[src] == ai[nb], axis=-1)
            dh[src] += (np.abs(Hh[src] - Hh[nb]) > 0.3)
    return (dh > 1) | (hc > 1) | (same < 2)


def ue_compare(a, b, tol=16, minb=16, ignore_aa=True, aa_a=None, aa_b=None):
    ai, bi = a.astype(np.int16), b.astype(np.int16)
    rgb_ok = np.all(np.abs(ai - bi) <= tol, axis=-1)
    bright_ok = np.abs(luma(a) - luma(b)) <= minb
    if ignore_aa:
        aa = aa_a | aa_b
        mismatch = ~rgb_ok & ~(aa & bright_ok)
    else:
        mismatch = ~rgb_ok
    H, W = mismatch.shape
    bx, by = int(round(W / 10.0)), int(round(H / 10.0))
    yy, xx = np.mgrid[0:H, 0:W]
    hsh = (yy // by) * 10 + (xx // bx)
    local = np.bincount(hsh[mismatch], minlength=110)[:100]
    g, l = mismatch.mean(), local.max() / float(bx * by)
    return {'global': round(float(g), 5), 'max_local': round(float(l), 5),
            'pass': bool(g <= 0.02 and l <= 0.10), 'frac_aa_exempt_pixels': round(float((aa_a | aa_b).mean()), 4) if ignore_aa else None}


def pair(na, nb, heat=None):
    a, b = load(na), load(nb)
    d = np.abs(a.astype(np.int16) - b.astype(np.int16))
    mse = float(((a.astype(np.float64) - b) ** 2).mean())
    ld = np.abs(luma(a) - luma(b))
    s, smap = ssim_g(a, b)
    aa_a, aa_b = antialiased(a), antialiased(b)
    r = {'a': na, 'b': nb, 'ssim_g': round(s, 5), 'ssim_ue8': round(ssim_ue8(a, b), 5),
         'psnr_db': round(10 * np.log10(255 ** 2 / mse), 2) if mse > 0 else 'inf',
         'mae': round(float(d.mean()), 3), 'p99_absdiff': int(np.percentile(d.max(-1), 99)), 'max_absdiff': int(d.max()),
         'frac_luma_gt2': round(float((ld > 2).mean()), 4), 'frac_luma_gt8': round(float((ld > 8).mean()), 4),
         'ue_low': ue_compare(a, b, aa_a=aa_a, aa_b=aa_b), 'ue_low_noaa': ue_compare(a, b, ignore_aa=False)}
    if heat:
        hm = np.clip(ld * 8, 0, 255).astype(np.uint8)
        save_raw(heat + '__absdiff_x8', np.stack([hm, hm, hm], -1))
        sm = np.clip((1 - smap) * 255 * 2, 0, 255).astype(np.uint8)  # 1-SSIM, x2 for visibility
        save_raw(heat + '__one_minus_ssim_x2', np.stack([sm, sm // 3, sm // 3], -1))
    return r


views = ['house_front', 'pond', 'forest']
res = {'self_check': {}, 'static': [], 'revisit': [], 'settle_vs_last': []}
# self-check: identical image must give SSIM 1, PSNR inf, UE PASS with 0 mismatches
res['self_check'] = pair('pond__A_t14.0.png', 'pond__A_t14.0.png')
for v in views:
    A = lambda t: '%s__A_t%04.1f.png' % (v, t)
    res['static'] += [pair(A(10), A(12)), pair(A(12), A(14)), pair(A(10), A(14), heat='%s_static_t10_vs_t14' % v)]
    res['revisit'] += [pair(A(14), '%s__B_round2.png' % v), pair('%s__B_round2.png' % v, '%s__B_round3.png' % v, heat='%s_revisit_r2_vs_r3' % v),
                       pair(A(14), '%s__B_round3.png' % v)]
    for t in (0.5, 2.5, 6.0, 10.0, 12.0):
        res['settle_vs_last'].append(pair(A(t), A(14)))
with open(os.path.join(OUT, 'metrics_t1.json'), 'w') as f:
    json.dump(res, f, indent=1)
print('METRICS_DONE', os.path.join(OUT, 'metrics_t1.json'))
