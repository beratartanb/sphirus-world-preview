"""player_stats.py <t1b_dir> : DESCRIPTIVE image statistics of the player-camera stills (not a quality score, not regression).
Per image: luma p5/p50/p95, value-group fractions (dark < 50, mid, light > 170 on 0-255 luma), mean saturation (HSV S),
mean local contrast (std of luma in 32x32 blocks), and the same with the character region excluded (fixed central-lower box
x 0.25-0.62 W, y 0.30-1.0 H, measured on these stills: the GraceRanger camera keeps the pawn there).
Output: <t1b_dir>/metrics/player_stats.json
"""
import sys, os, json, struct
import numpy as np

T = sys.argv[1]
PD = os.path.join(T, 'pie')


def load(n):
    with open(os.path.join(PD, n), 'rb') as f:
        w, h = struct.unpack('<ii', f.read(8))
        return np.frombuffer(f.read(), np.uint8).reshape(h, w, 3)[:, :, ::-1].astype(np.float32)


def stats(a, mask):
    L = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    mx, mn = a.max(-1), a.min(-1); S = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
    Lm = L[mask]
    h, w = L.shape; bh, bw = h // 32 * 32, w // 32 * 32
    blk = L[:bh, :bw].reshape(bh // 32, 32, bw // 32, 32).std((1, 3))
    mb = mask[:bh, :bw].reshape(bh // 32, 32, bw // 32, 32).all((1, 3))
    return {'luma_p5': round(float(np.percentile(Lm, 5)), 1), 'luma_p50': round(float(np.percentile(Lm, 50)), 1),
            'luma_p95': round(float(np.percentile(Lm, 95)), 1), 'dark_lt50': round(float((Lm < 50).mean()), 3),
            'mid': round(float(((Lm >= 50) & (Lm <= 170)).mean()), 3), 'light_gt170': round(float((Lm > 170).mean()), 3),
            'saturation_mean': round(float(S[mask].mean()), 3), 'local_contrast_32px': round(float(blk[mb].mean()), 2)}


res = {}
for f in sorted(os.listdir(PD)):
    if not f.endswith('.raw'):
        continue
    a = load(f); h, w, _ = a.shape
    full = np.ones((h, w), bool)
    env = full.copy(); env[int(0.30 * h):, int(0.25 * w):int(0.62 * w)] = False
    res[f[:-4]] = {'full_frame': stats(a, full), 'without_character_box': stats(a, env)}
json.dump(res, open(os.path.join(T, 'metrics', 'player_stats.json'), 'w'), indent=1)
for k, v in res.items():
    e = v['without_character_box']
    print('%-34s p5 %5.1f p50 %5.1f p95 %5.1f dark %.2f mid %.2f light %.2f sat %.2f lc %.1f' % (k, e['luma_p5'], e['luma_p50'], e['luma_p95'], e['dark_lt50'], e['mid'], e['light_gt170'], e['saturation_mean'], e['local_contrast_32px']))
