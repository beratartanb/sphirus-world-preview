"""camab234.py <labelCamOn> <labelCamOff> [...pairs] : the automatic camera must not change the body. Same body version, same input, camera
recentre on vs off: per pair the max over time of |speed diff| (cm/s), |travel yaw diff| (deg, moving > 30), |actor yaw diff| (deg), |accel
diff| (cm/s2, 0.1 s window), gait-class mismatch frames (walk < 190 <= jog < 380 <= sprint), planar position diff (cm) and the camera's own
turn (control yaw change, deg) - a large camera turn with ~0 body difference = decoupled. Prints CAMAB234 per pair."""
import sys, os, math, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'SHME_V231_20261026'))
from ltp231 import load
def f(x, d=None):
    try: return float(x)
    except Exception: return d
def wrap(a): return ((a + 180.0) % 360.0) - 180.0
def rows(lab):
    R = load(lab); out = []
    for r in R:
        p = r.get('mh_root') or r.get('vb_pelvis')
        out.append({'t': f(r.get('t'), 0.0), 'sp': f(r.get('Speed2D'), 0.0), 'ay': f(r.get('ay'), 0.0), 'cy': f(r.get('cy'), 0.0), 'p': p})
    for i, r in enumerate(out):
        j = min(i + 3, len(out) - 1); k = max(i - 3, 0); a, b = out[k]['p'], out[j]['p']
        r['ty'] = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])) if a and b and math.hypot(b[0] - a[0], b[1] - a[1]) > 1.0 else None
        dt = max(out[j]['t'] - out[k]['t'], 1e-3); r['acc'] = (out[j]['sp'] - out[k]['sp']) / dt
    return out
def g(v): return 0 if v < 190 else (1 if v < 380 else 2)
args = sys.argv[1:]
for a_, b_ in zip(args[0::2], args[1::2]):
    A, B = rows(a_), rows(b_); m = {'dsp': 0.0, 'dty': 0.0, 'day': 0.0, 'dacc': 0.0, 'gait_mis': 0, 'dpos': 0.0}
    n = min(len(A), len(B))
    for i in range(n):
        x, y = A[i], B[i]
        m['dsp'] = max(m['dsp'], abs(x['sp'] - y['sp'])); m['day'] = max(m['day'], abs(wrap(x['ay'] - y['ay']))); m['dacc'] = max(m['dacc'], abs(x['acc'] - y['acc']))
        if x['ty'] is not None and y['ty'] is not None and x['sp'] > 30 and y['sp'] > 30: m['dty'] = max(m['dty'], abs(wrap(x['ty'] - y['ty'])))
        if g(x['sp']) != g(y['sp']): m['gait_mis'] += 1
        if x['p'] and y['p']: m['dpos'] = max(m['dpos'], math.hypot(x['p'][0] - y['p'][0], x['p'][1] - y['p'][1]))
    m['cam_turn_on'] = round(max(abs(wrap(r['cy'] - A[0]['cy'])) for r in A), 1); m['cam_turn_off'] = round(max(abs(wrap(r['cy'] - B[0]['cy'])) for r in B), 1)
    m['vmax_on'] = round(max(r['sp'] for r in A)); m['vmax_off'] = round(max(r['sp'] for r in B))
    print('CAMAB234 %s vs %s %s' % (a_, b_, json.dumps({k: (round(v, 1) if isinstance(v, float) else v) for k, v in m.items()})))
