"""cam229.py label [label ...]: walk / look framing audit (V2.29). Per stage (the harness stage label): chest screen x (1 = half width)
mean / range, peak screen speed |dx/dt| (half widths / s, 3-frame), rebound = number of direction reversals of the screen x motion with
amplitude > 0.01 inside the stage (spring-back), camera->capsule lateral and forward offset in the camera yaw frame (cm, range: how far
the follow lets the body drift from its shoulder place), capsule speed. CAM229 {...} = whole-run summary of the moving-walk stages."""
import json, sys, math, pathlib
E = pathlib.Path(__file__).resolve().parents[2] / 'Saved/Codex/SHME_V1_20260925/Evidence'
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from screen229 import proj, rot, f
for lab in [a for a in sys.argv[1:] if not a.startswith('--')]:
    R0 = sorted([r for r in json.load(open(E / (lab + '.json'))) if isinstance(r, dict) and r.get('t') is not None and isinstance(r.get('camera'), list) and isinstance(r.get('vb_chest'), list)], key=lambda r: f(r['t']))
    R = []
    for r in R0:
        if R and abs(f(r['t']) - f(R[-1]['t'])) < 0.004: R[-1] = r
        else: R.append(r)
    rows = []
    for r in R:
        rr = rot(r)
        if rr is None: continue
        c = proj(r['camera'], rr, f(r.get('fov'), 60), r['vb_chest'])
        if c is None: continue
        y = math.radians(rr[1]); fw = (math.cos(y), math.sin(y)); rt = (-math.sin(y), math.cos(y))
        d = (r['ax'][0] - r['camera'][0], r['ax'][1] - r['camera'][1])
        rows.append((f(r['t']), str(r.get('stage', '')), c[0], d[0] * rt[0] + d[1] * rt[1], d[0] * fw[0] + d[1] * fw[1], math.hypot(f(r.get('avx')), f(r.get('avy')))))
    st = {}
    for k in range(len(rows)):
        t, s, x, lat, fwd, sp = rows[k]
        o = st.setdefault(s, {'n': 0, 'x': [], 'v': [], 'lat': [], 'fwd': [], 'sp': [], 't': []})
        o['n'] += 1; o['x'].append(x); o['lat'].append(lat); o['fwd'].append(fwd); o['sp'].append(sp); o['t'].append(t)
        if 2 <= k < len(rows) - 2: o['v'].append(abs(rows[k + 2][2] - rows[k - 2][2]) / max(1e-3, rows[k + 2][0] - rows[k - 2][0]))
    print('%-28s %4s %7s %6s %6s %4s %6s %6s %5s' % ('stage', 'n', 'x_mean', 'x_rng', 'vmax', 'reb', 'lat_r', 'fwd_r', 'spd'))
    walk = {'x_rng': 0, 'vmax': 0, 'reb': 0, 'lat_r': 0}
    for s, o in st.items():
        xs = o['x']; reb = 0; last = 0; ext = xs[0]
        for i in range(1, len(xs)):
            dx = xs[i] - ext
            if abs(dx) > 0.01:
                sg = 1 if dx > 0 else -1
                if last and sg != last: reb += 1
                last = sg; ext = xs[i]
        line = (s[-28:], o['n'], sum(xs) / len(xs), max(xs) - min(xs), max(o['v']) if o['v'] else 0, reb, max(o['lat']) - min(o['lat']), max(o['fwd']) - min(o['fwd']), sum(o['sp']) / len(o['sp']))
        print('%-28s %4d %7.3f %6.3f %6.3f %4d %6.1f %6.1f %5.0f' % line)
        if 'mv_' in s and 'stop' not in s and line[8] > 40:
            walk['x_rng'] = max(walk['x_rng'], line[3]); walk['vmax'] = max(walk['vmax'], line[4]); walk['reb'] += reb; walk['lat_r'] = max(walk['lat_r'], line[6])
    print('CAM229 %s %s' % (lab, json.dumps({k: round(v, 3) for k, v in walk.items()})))
