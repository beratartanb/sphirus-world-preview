"""t1b_metrics.py <t1b_dir> : 5-frame median vs single frame, real-change detection, and a noise-source decomposition (numpy only).

Inputs: <t1b_dir>/shots/*.raw (imgconv.ps1 png2raw), <t1b_dir>/t1b_log.json. Output: <t1b_dir>/metrics/t1b_metrics.json + heat maps (.raw).

Detection metrics (no knowledge of where the change is):
  tile16 = max |mean luma| difference over a 16x9 tile grid, tile48 = same on 48x27 (finer), ssim_d8 = SSIM after 8x box downsample.
ROI metrics (the hidden actor's projected screen box + 12 px; used only to judge whether a known change survives):
  roi_mae = mean |luma diff| inside the box; snr = roi_mae(change pair) / roi_mae(noise pair S2-vs-S5 in the same box).
Noise-source decomposition of within-set frame-to-frame differences (ESTIMATE; heuristic masks, no render settings were changed):
  exposure   = energy of the image-wide mean luma change (auto exposure / global light)
  shadow_lf  = low-frequency (Gaussian sigma 4 px) luma change on NON-vegetation pixels (sun flecks moving over ground/house)
  aa_hf      = high-frequency residual on NON-vegetation pixels (TSR jitter / temporal noise on static surfaces)
  foliage    = all change on vegetation pixels (wind motion, its shadows and its TSR history)
  vegetation mask: 2G-R-B > 12 and G > 40 on the frame (green-dominant pixels).
"""
import sys, os, json, struct
import numpy as np

T = sys.argv[1]
SH, MO = os.path.join(T, 'shots'), os.path.join(T, 'metrics')
os.makedirs(MO, exist_ok=True)
log = json.load(open(os.path.join(T, 't1b_log.json')))


def load(n):
    with open(os.path.join(SH, n.replace('.png', '.raw')), 'rb') as f:
        w, h = struct.unpack('<ii', f.read(8))
        return np.frombuffer(f.read(), np.uint8).reshape(h, w, 3)[:, :, ::-1].astype(np.float32)


def save_raw(name, rgb):
    h, w, _ = rgb.shape
    with open(os.path.join(MO, name + '.raw'), 'wb') as f:
        f.write(struct.pack('<ii', w, h)); f.write(np.ascontiguousarray(rgb[:, :, ::-1]).astype(np.uint8).tobytes())


def luma(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def gk(s):
    r = int(3 * s + 0.5); g = np.exp(-0.5 * (np.arange(-r, r + 1) / s) ** 2); return g / g.sum(), r


def blur(x, s):
    g, r = gk(s); H, W = x.shape
    p = np.pad(x, r, mode='reflect')
    yh = sum(g[k] * p[:, k:k + W] for k in range(2 * r + 1))
    return sum(g[k] * yh[k:k + H, :] for k in range(2 * r + 1))


def down(x, k):
    h, w = (x.shape[0] // k) * k, (x.shape[1] // k) * k
    return x[:h, :w].reshape(h // k, k, w // k, k).mean((1, 3))


def ssim(x, y):
    x, y = x / 255.0, y / 255.0; C1, C2 = 0.01 ** 2, 0.03 ** 2
    mx, my = blur(x, 1.5), blur(y, 1.5)
    sxx, syy, sxy = blur(x * x, 1.5) - mx * mx, blur(y * y, 1.5) - my * my, blur(x * y, 1.5) - mx * my
    m = ((2 * mx * my + C1) * (2 * sxy + C2)) / ((mx * mx + my * my + C1) * (sxx + syy + C2))
    return float(m[5:-5, 5:-5].mean())


def tiles(x, nx, ny):
    h, w = x.shape[0] // ny * ny, x.shape[1] // nx * nx
    return x[:h, :w].reshape(ny, h // ny, nx, w // nx).mean((1, 3))


def detect(La, Lb):
    return {'tile16': round(float(np.abs(tiles(La, 16, 9) - tiles(Lb, 16, 9)).max()), 3),
            'tile48': round(float(np.abs(tiles(La, 48, 27) - tiles(Lb, 48, 27)).max()), 3),
            'ssim_d8': round(ssim(down(La, 8), down(Lb, 8)), 5),
            'global': round(float(Lb.mean() - La.mean()), 3)}


def roi(La, Lb, box):
    if not box:
        return None
    x0, y0, x1, y1 = box
    x0, y0, x1, y1 = max(0, x0 - 12), max(0, y0 - 12), min(La.shape[1], x1 + 12), min(La.shape[0], y1 + 12)
    return round(float(np.abs(La[y0:y1, x0:x1] - Lb[y0:y1, x0:x1]).mean()), 3)


sets = {}
for s in log['shots']:
    sets.setdefault((s['view'], s['set']), []).append(s['file'])
res = {'views': {}, 'note': 'median = per-pixel median of the 5 frames of a set; single = frame k of set A vs frame k of set B (mean over k)'}
for view in log['views']:
    names = sorted({k[1] for k in sets if k[0] == view and k[1] != 'warm'})
    F = {n: [load(f) for f in sorted(sets[(view, n)])] for n in names}
    LF = {n: [luma(a) for a in F[n]] for n in names}
    MED = {n: luma(np.median(np.stack(F[n]), axis=0)) for n in names}
    picks = log['picks'].get(view, {})
    V = {'sets': {n: len(F[n]) for n in names}, 'picks': picks, 'pairs': {}}

    def pair(a, b, box=None):
        r = {'median': detect(MED[a], MED[b])}
        singles = [detect(LF[a][k], LF[b][k]) for k in range(min(len(LF[a]), len(LF[b])))]
        r['single_mean'] = {m: round(float(np.mean([s[m] for s in singles])), 4) for m in singles[0]}
        r['single_worst'] = {'tile16': max(s['tile16'] for s in singles), 'tile48': max(s['tile48'] for s in singles),
                             'ssim_d8': min(s['ssim_d8'] for s in singles)}
        if box:
            r['roi_mae_median'] = roi(MED[a], MED[b], box)
            r['roi_mae_single_mean'] = round(float(np.mean([roi(LF[a][k], LF[b][k], box) for k in range(min(len(LF[a]), len(LF[b])))])), 3)
        return r

    V['pairs']['revisit_S1_S2'] = pair('S1', 'S2')
    V['pairs']['static_S2_S5'] = pair('S2', 'S5')
    for size, sname in (('small', 'S3small'), ('medium', 'S4medium')):
        if sname in F:
            box = picks[size]['screen_box_1920x1080']
            ca, cb = pair('S2', sname, box), pair('S5', sname, box)
            noise_roi_med, noise_roi_single = roi(MED['S2'], MED['S5'], box), float(np.mean([roi(LF['S2'][k], LF['S5'][k], box) for k in range(5)]))
            for c in (ca, cb):
                c['roi_noise_median'] = noise_roi_med; c['roi_noise_single_mean'] = round(noise_roi_single, 3)
                c['snr_median'] = round(c['roi_mae_median'] / max(noise_roi_med, 1e-3), 2)
                c['snr_single'] = round(c['roi_mae_single_mean'] / max(noise_roi_single, 1e-3), 2)
            V['pairs']['change_%s_S2' % size] = ca
            V['pairs']['change_%s_S5' % size] = cb
            d = np.abs(MED['S5'] - MED[sname]); hm = np.clip(d * 8, 0, 255)
            save_raw('%s_change_%s_median_absdiff_x8' % (view, size), np.stack([hm, hm, hm], -1))
            d1 = np.abs(LF['S5'][0] - LF[sname][0]); hm1 = np.clip(d1 * 8, 0, 255)
            save_raw('%s_change_%s_single_absdiff_x8' % (view, size), np.stack([hm1, hm1, hm1], -1))
    d = np.abs(MED['S2'] - MED['S5']); hm = np.clip(d * 8, 0, 255)
    save_raw('%s_noise_static_median_absdiff_x8' % view, np.stack([hm, hm, hm], -1))
    d1 = np.abs(LF['S2'][0] - LF['S5'][0]); hm1 = np.clip(d1 * 8, 0, 255)
    save_raw('%s_noise_static_single_absdiff_x8' % view, np.stack([hm1, hm1, hm1], -1))

    # ---- noise-source decomposition on consecutive frames of the unchanged sets (S1, S2, S5)
    comp = {'exposure': 0.0, 'shadow_lf': 0.0, 'aa_hf': 0.0, 'foliage': 0.0}; tot = 0.0; npairs = 0
    for n in ('S1', 'S2', 'S5'):
        for k in range(len(LF[n]) - 1):
            a, b, rgb = LF[n][k], LF[n][k + 1], F[n][k]
            veg = ((2 * rgb[..., 1] - rgb[..., 0] - rgb[..., 2]) > 12) & (rgb[..., 1] > 40)
            dd = b - a; g = float(dd.mean()); r = dd - g
            lf = blur(r, 4.0); hf = r - lf
            nv = ~veg
            comp['exposure'] += g * g * dd.size
            comp['shadow_lf'] += float((lf[nv] ** 2).sum()); comp['aa_hf'] += float((hf[nv] ** 2).sum()); comp['foliage'] += float((r[veg] ** 2).sum())
            tot += float((dd ** 2).sum()); npairs += 1
    V['noise_sources_within_set'] = {'fraction_of_energy': {k: round(v / tot, 4) for k, v in comp.items()},
                                     'rms_luma_total': round(float(np.sqrt(tot / (npairs * LF['S1'][0].size))), 3),
                                     'vegetation_pixel_fraction': round(float((((2 * F['S1'][0][..., 1] - F['S1'][0][..., 0] - F['S1'][0][..., 2]) > 12) & (F['S1'][0][..., 1] > 40)).mean()), 3),
                                     'frame_pairs': npairs}
    # exposure drift inside a set and between sets (mean luma per frame)
    V['mean_luma_per_frame'] = {n: [round(float(x.mean()), 3) for x in LF[n]] for n in names}
    res['views'][view] = V
json.dump(res, open(os.path.join(MO, 't1b_metrics.json'), 'w'), indent=1)
print('T1B_METRICS_DONE')
