"""camcmp232.py <tag> <scenario> <varA> <varB> [...more variants] : same-input comparison of camera variants (V2.32 body x camera matrix).
Body independence: capsule path difference |ax_A - ax_B| (cm, max), control yaw difference (deg, max), travel direction relative to the
control yaw (deg, max diff) - a camera layer that feeds back into the body or the input frame shows up here (fixed step = same input).
Camera: per variant the max |camera yaw - control yaw| (the realised visual offset), the seconds the body is seen at three-quarter
(25 <= |alpha| <= 65 while moving), alpha extreme per key window, jerk95 / max, min camera-capsule distance, chest screen x range.
Prints CAMCMP232 lines."""
import sys, os, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cam232 import load, wrap, q
tag, scn = sys.argv[1], sys.argv[2]; vs = sys.argv[3:]
D = {v: load('v232%s_%s_%s_r1' % (tag, scn, v)) for v in vs}
base = vs[0]; A = D[base]
def at(R, t):
    return min(R, key=lambda r: abs(r['t'] - t))
for v in vs:
    R = D[v]
    if not R: print('CAMCMP232 %s %s %s NO_DATA' % (tag, scn, v)); continue
    dp = 0.0; dcy = 0.0; dvin = 0.0
    for r in R:
        a = at(A, r['t'])
        if abs(a['t'] - r['t']) > 0.02: continue
        dcy = max(dcy, abs(wrap(r['cy'] - a['cy']))); dp = max(dp, math.hypot(r['pos'][0] - a['pos'][0], r['pos'][1] - a['pos'][1]))
        if r['vin'] is not None and a['vin'] is not None: dvin = max(dvin, abs(wrap(r['vin'] - a['vin'])))
    P = {}
    for r in R: P[round(r['t'], 3)] = r
    js = [r.get('jerk', 0.0) for r in R]
    q34 = 0.0
    for i in range(1, len(R)):
        if 25.0 <= abs(R[i]['alpha']) <= 65.0 and R[i]['sp'] > 30.0: q34 += R[i]['t'] - R[i - 1]['t']
    cx = [r['cx'] for r in R if r['cx'] is not None]
    print('CAMCMP232 %-6s %-16s %-6s beta|max %5.1f  3/4 %4.2fs  jerk95 %5.2f max %6.2f  dist_min %5.0f  cx %5.2f..%5.2f  | vs %s: d_pos %.1f cm d_ctl %.2f deg d_vin %.1f deg' % (
        tag, scn, v, max(abs(r['beta']) for r in R), q34, q(js, 0.95), max(js), min(r['arm'] for r in R), min(cx) if cx else 0, max(cx) if cx else 0, base, dp, dcy, dvin))
