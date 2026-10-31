"""t1b_detect.py <t1b_dir> : small-loop change detector evaluated on T1b sets (numpy only).

Detector (deliberately simple):
  1. exposure normalisation: every frame's luma is scaled to the same image mean (removes the ~3.5 % global step seen in T1b);
  2. per-set reduction: 'median' = per-pixel median of the 5 frames, 'single' = frame 2 only;
  3. tile map 48x27 (40x40 px tiles) of mean normalised luma; change = |tile(A) - tile(B)|;
  4. per-tile noise model from INDEPENDENT no-change data, floor 0.5: 'pair' = S1 vs S2 (camera moved away and back);
     'rich' = max(pair, within-set frame-to-frame tile spread of S1 and S2). argv[2] selects the model (default pair);
  5. z = change / noise; detection if max z > Z_T. Localisation: the max-z tile must overlap the changed region.
Evaluated on: false alarm   S2 vs S5 (no change, after the hide/unhide cycle)
              real change   S5 vs S3small / S4medium (actor temporarily hidden in the editor; screen box from t1b_log.json)
              injected      S5 frames with a patch replaced by the same-size patch from 300 px to the left, applied to all 5 frames
                            (persistent change; median must keep it), sizes 24/48/96 px, in a quiet and in a busy (high-noise) tile.
Z_T is reported for 3 and 5. Output: <t1b_dir>/metrics/t1b_detect.json
"""
import sys, os, json, struct
import numpy as np

T = sys.argv[1]
SH, MO = os.path.join(T, 'shots'), os.path.join(T, 'metrics')
log = json.load(open(os.path.join(T, 't1b_log.json')))
NX, NY, TW, TH = 48, 27, 40, 40


def load(n):
    with open(os.path.join(SH, n.replace('.png', '.raw')), 'rb') as f:
        w, h = struct.unpack('<ii', f.read(8))
        a = np.frombuffer(f.read(), np.uint8).reshape(h, w, 3)[:, :, ::-1].astype(np.float32)
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def norm(L, m=86.0):
    return L * (m / L.mean())


def tiles(L):
    return L[:NY * TH, :NX * TW].reshape(NY, TH, NX, TW).mean((1, 3))


def reduce(frames, mode):
    return np.median(np.stack(frames), axis=0) if mode == 'median' else frames[2]


def box_tiles(box):
    x0, y0, x1, y1 = box
    return {(ty, tx) for ty in range(int(y0) // TH, min(NY, int(np.ceil(y1 / TH)))) for tx in range(int(x0) // TW, min(NX, int(np.ceil(x1 / TW))))}


def evaluate(A, B, noise, box=None):
    z = np.abs(tiles(A) - tiles(B)) / noise
    iy, ix = np.unravel_index(np.argmax(z), z.shape)
    r = {'max_z': round(float(z.max()), 2), 'max_tile': [int(ix), int(iy)]}
    if box:
        bt = box_tiles(box)
        r['z_in_change_tiles'] = round(max(float(z[t]) for t in bt), 2)
        r['localised'] = (int(iy), int(ix)) in bt
    for zt in (3, 5):
        r['detect_z%d' % zt] = bool(z.max() > zt) and (r.get('localised', True))
        r['false_tiles_z%d' % zt] = int((z > zt).sum() - (sum(1 for t in box_tiles(box) if z[t] > zt) if box else 0))
    return r


sets = {}
for s in log['shots']:
    sets.setdefault((s['view'], s['set']), []).append(s['file'])
NOISE_MODEL = sys.argv[2] if len(sys.argv) > 2 else 'pair'
res = {}
for view in log['views']:
    names = sorted({k[1] for k in sets if k[0] == view and k[1] != 'warm'})
    F = {n: [norm(load(f)) for f in sorted(sets[(view, n)])] for n in names}
    picks = log['picks'].get(view, {})
    V = {}
    for mode in ('median', 'single'):
        R = {n: reduce(F[n], mode) for n in names}
        noise_pair = np.maximum(np.abs(tiles(R['S1']) - tiles(R['S2'])), 0.5)
        # 'rich' model: also the within-set frame-to-frame tile spread of S1 and S2 (fast noise: TSR, flecks, wind)
        TF = {n: [tiles(f) for f in F[n]] for n in ('S1', 'S2')}
        spread = np.max([np.abs(TF[n][k + 1] - TF[n][k]) for n in TF for k in range(len(TF[n]) - 1)], axis=0)
        noise = np.maximum(noise_pair, spread) if NOISE_MODEL == 'rich' else noise_pair
        M = {'noise_model': NOISE_MODEL, 'noise_tile_p50': round(float(np.median(noise)), 2), 'noise_tile_p95': round(float(np.percentile(noise, 95)), 2),
             'false_alarm_S2_S5': evaluate(R['S2'], R['S5'], noise)}
        for size, sname in (('small', 'S3small'), ('medium', 'S4medium')):
            if sname in R:
                M['real_%s_S5' % size] = evaluate(R['S5'], R[sname], noise, picks[size]['screen_box_1920x1080'])
                M['real_%s_S2' % size] = evaluate(R['S2'], R[sname], noise, picks[size]['screen_box_1920x1080'])
        # injected persistent changes into every S5 frame
        quiet = np.unravel_index(np.argmin(noise[3:-3, 8:-3]), noise[3:-3, 8:-3].shape); quiet = (quiet[0] + 3, quiet[1] + 8)
        busy = np.unravel_index(np.argmax(noise[3:-3, 8:-3]), noise[3:-3, 8:-3].shape); busy = (busy[0] + 3, busy[1] + 8)
        inj = {}
        for where, (ty, tx) in (('quiet_tile', quiet), ('busy_tile', busy)):
            for sz in (24, 48, 96):
                cy, cx = ty * TH + TH // 2, tx * TW + TW // 2
                y0, x0 = cy - sz // 2, cx - sz // 2
                sx = x0 - 300 if x0 - 300 >= 0 else x0 + 300   # source patch 300 px to the left (right near the left edge)
                fr = []
                for f in F['S5']:
                    g = f.copy(); g[y0:y0 + sz, x0:x0 + sz] = f[y0:y0 + sz, sx:sx + sz]; fr.append(g)
                Bm = reduce(fr, mode)
                inj['%s_%dpx' % (where, sz)] = dict(evaluate(R['S5'], Bm, noise, [x0, y0, x0 + sz, y0 + sz]), tile=[int(tx), int(ty)],
                                                    tile_noise=round(float(noise[ty, tx]), 2))
        M['injected_patch_swap'] = inj
        V[mode] = M
    res[view] = V
json.dump(res, open(os.path.join(MO, 't1b_detect_%s.json' % NOISE_MODEL), 'w'), indent=1)
for view, V in res.items():
    for mode, M in V.items():
        print(view, mode, 'noise p50/p95', M['noise_tile_p50'], M['noise_tile_p95'], '| FA S2-S5 maxz', M['false_alarm_S2_S5']['max_z'],
              'z3 tiles', M['false_alarm_S2_S5']['false_tiles_z3'], 'z5 tiles', M['false_alarm_S2_S5']['false_tiles_z5'])
        for k in [k for k in M if k.startswith('real_')]:
            r = M[k]; print('   ', k, 'maxz', r['max_z'], 'z_in_change', r['z_in_change_tiles'], 'localised', r['localised'], 'det z3/z5', r['detect_z3'], r['detect_z5'])
        for k, r in M['injected_patch_swap'].items():
            print('    inj', k, 'tile_noise', r['tile_noise'], 'z_in_change', r['z_in_change_tiles'], 'max_z', r['max_z'], 'localised', r['localised'], 'det z3/z5', r['detect_z3'], r['detect_z5'])
