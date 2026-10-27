"""cam232.py label [label ...] [--win=<s>]: V2.32 cinematic-camera audit on the logged camera WORLD pose (never on SHME variables).
Per frame (Evidence JSON): alpha = view azimuth on the body = yaw(camera -> capsule) - actor yaw (0 = straight behind the body, +-90 = side,
+ = the camera sees the body's left side); beta = camera yaw - control yaw (the visual offset on top of the player's look: production
counter yaw, V2.32 orbit); look = |d control yaw / dt| (player look input); chest screen x (1 = half width); camera jerk (cm/frame^2 on the
3rd difference of the camera path, per-frame metric: compare equal FPS only); boom length (collision shortening); travel direction relative
to the control yaw (the input frame: must be identical with / without the camera layer).
Windows: every key / segment change (stage change with a new angle) opens a window of --win s (default 2.0). Per window: |beta| peak and at
the end, alpha start -> extreme -> end, seconds with the body seen at three-quarter (25 <= |alpha| <= 65), chest x range, jerk95 / max,
min camera-capsule horizontal distance (cm, collision / closeness). CAM232 {...} = run summary."""
import json, sys, math, pathlib
P = pathlib.Path(__file__).resolve().parents[2]
E = P / 'Saved/Codex/SHME_V1_20260925/Evidence'
sys.path.insert(0, str(P / 'Tools/SHME_V229_20261025'))
from screen229 import proj, rot, f
def wrap(a):
    return (a + 180.0) % 360.0 - 180.0
def load(lab):
    R0 = sorted([r for r in json.load(open(E / (lab + '.json'))) if isinstance(r, dict) and r.get('t') is not None and isinstance(r.get('camera'), list)], key=lambda r: f(r['t']))
    R = []
    for r in R0:   # the LTP / evidence sometimes logs a frame twice (same t)
        if R and abs(f(r['t']) - f(R[-1]['t'])) < 0.004: R[-1] = r
        else: R.append(r)
    out = []
    for r in R:
        rr = rot(r)
        if rr is None or not isinstance(r.get('ax'), list): continue
        cam = r['camera']; ax = r['ax']
        ycc = math.degrees(math.atan2(ax[1] - cam[1], ax[0] - cam[0]))
        sp = math.hypot(f(r.get('avx')), f(r.get('avy')))
        vyaw = math.degrees(math.atan2(f(r.get('avy')), f(r.get('avx')))) if sp > 30.0 else None
        c = proj(cam, rr, f(r.get('fov'), 60), r['vb_chest']) if isinstance(r.get('vb_chest'), list) else None
        out.append({'t': f(r['t']), 'st': str(r.get('stage', '')), 'sp': sp, 'ay': f(r.get('ay')), 'cy': f(r.get('cy')), 'camy': rr[1],
                    'alpha': wrap(ycc - f(r.get('ay'))), 'beta': wrap(rr[1] - f(r.get('cy'))), 'cam': cam, 'cx': c[0] if c else None,
                    'arm': math.hypot(ax[0] - cam[0], ax[1] - cam[1]), 'vin': wrap(vyaw - f(r.get('cy'))) if vyaw is not None else None, 'orb': f(r.get('cv_CamOrbitYaw'), 0.0), 'pos': ax})
    for i in range(1, len(out)):
        dt = max(out[i]['t'] - out[i - 1]['t'], 1e-3); out[i]['look'] = abs(wrap(out[i]['cy'] - out[i - 1]['cy'])) / dt
    if out: out[0]['look'] = 0.0
    for i in range(3, len(out)):
        a, b, c_, d = (out[i - 3]['cam'], out[i - 2]['cam'], out[i - 1]['cam'], out[i]['cam'])
        out[i]['jerk'] = math.sqrt(sum((d[k] - 3 * c_[k] + 3 * b[k] - a[k]) ** 2 for k in range(3)))
    return out
def q(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(p * len(xs)))] if xs else 0.0
if __name__ == "__main__":
    WIN = 2.0
    for a in sys.argv[1:]:
        if a.startswith('--win='): WIN = float(a.split('=')[1])
    for lab in [a for a in sys.argv[1:] if not a.startswith('--')]:
        R = load(lab)
        if not R: print('CAM232 %s NO_DATA' % lab); continue
        # window starts: a new movement stage (mv_* angle / keys) or a new look step (yaw_*)
        starts = []; prev = None
        for r in R:
            mv = '+'.join(s for s in r['st'].split('+') if s.startswith('mv_'))
            yw = '+'.join(s for s in r['st'].split('+') if s.startswith('yaw_') and s not in ('yaw_pre', 'yaw_done'))
            key = (mv.rsplit('_', 1)[0] if mv.startswith('mv_kb') else mv) + ('|' + yw if yw else '')
            if key != prev and prev is not None: starts.append((r['t'], key))
            prev = key
        print('%-34s %5s %6s %6s %6s %18s %5s %6s %6s %6s %5s %5s' % ('window (start, stage)', 'spd', 'bPk', 'bEnd', 'look', 'alpha s>ext>end', '3/4s', 'cxRng', 'jk95', 'jkMx', 'dist', 'vin'))
        allj = []; summ = {'beta_peak': 0.0, 'q34_s': 0.0, 'cx_rng': 0.0, 'jerk95': 0.0, 'jerk_max': 0.0, 'arm_min': 1e9, 'look_beta_max': 0.0}
        for t0, key in starts:
            W = [r for r in R if t0 <= r['t'] < t0 + WIN]
            if len(W) < 3: continue
            bpk = max((r['beta'] for r in W), key=abs); ext = max((r['alpha'] for r in W), key=lambda x: abs(x - W[0]['alpha']))
            dt = (W[-1]['t'] - W[0]['t']) / max(len(W) - 1, 1)
            q34 = sum(dt for r in W if 25.0 <= abs(r['alpha']) <= 65.0 and r['sp'] > 30.0)
            cxs = [r['cx'] for r in W if r['cx'] is not None]; js = [r.get('jerk', 0.0) for r in W]; arms = [r['arm'] for r in W if r['arm'] > 1]
            vins = [r['vin'] for r in W if r['vin'] is not None]
            lk = max(r['look'] for r in W)
            print('%-34s %5.0f %6.1f %6.1f %6.0f %6.0f>%5.0f>%5.0f %5.2f %6.3f %6.2f %6.2f %5.0f %5s' % (('%.2f %s' % (t0, key))[-34:], sum(r['sp'] for r in W) / len(W), bpk, W[-1]['beta'], lk,
                  W[0]['alpha'], ext, W[-1]['alpha'], q34, (max(cxs) - min(cxs)) if cxs else 0.0, q(js, 0.95), max(js), min(arms) if arms else 0.0, ('%.0f' % vins[-1]) if vins else '-'))
            summ['beta_peak'] = max(summ['beta_peak'], abs(bpk)); summ['q34_s'] += q34; summ['cx_rng'] = max(summ['cx_rng'], (max(cxs) - min(cxs)) if cxs else 0.0)
            summ['jerk_max'] = max(summ['jerk_max'], max(js)); allj += js; summ['arm_min'] = min(summ['arm_min'], min(arms) if arms else 1e9)
            if lk > 30.0: summ['look_beta_max'] = max(summ['look_beta_max'], max(abs(r['beta']) for r in W if r['look'] > 30.0) if any(r['look'] > 30.0 for r in W) else 0.0)
        summ['jerk95'] = q(allj, 0.95); summ['beta_abs_max_run'] = max(abs(r['beta']) for r in R); summ['orbit_abs_max'] = max(abs(r['orb']) for r in R)
        print('CAM232 %s %s' % (lab, json.dumps({k: round(v, 3) for k, v in summ.items()})))
