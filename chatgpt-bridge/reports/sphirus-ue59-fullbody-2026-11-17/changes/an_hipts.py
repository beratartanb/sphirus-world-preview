# an_hipts.py <label> <eventIndex> [step]: time series around one turn event (driver skeleton): yaw of capsule, hip line, chest line vs final heading, lateral pelvis, roll.
import sys, math, os; sys.argv0 = sys.argv[0]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'an_hip.py')).read().split('for lb in sys.argv[1:]')[0]
exec(src)
lb, n = sys.argv[1], int(sys.argv[2]); st = int(sys.argv[3]) if len(sys.argv) > 3 else 2
j, R, bone, S = load(lb); T = [r[0] for r in R]; cy = unwrap([r[5] for r in R]); ay = unwrap([r[4] for r in R])
ev = []; i = 1
while i < len(R):
    dt = T[i] - T[i - 1]
    if dt > 0 and abs((cy[i] - cy[i - 1]) / dt) > 100:
        k = i
        while k + 1 < len(R) and abs((cy[k + 1] - cy[k]) / max(T[k + 1] - T[k], 1e-4)) > 100: k += 1
        ev.append((i - 1, k)); i = k + 20
    else: i += 1
i0, i1 = ev[n]; fin = cy[i1]; s = series(R, bone, 1)
print('t | ctrl-fin | capsule-fin | hip-fin | chest-fin | lat cm | roll | pz | speed | h_level turn_sev')
for k in range(i0 - 16, min(len(R), i0 + 80), st):
    print('%5.2f | %6.1f | %6.1f | %6.1f | %6.1f | %5.1f | %5.1f | %5.1f | %4.0f | %s %s' % (T[k] - T[i0], cy[k] - fin, ay[k] - fin, wrap(s[k]['hip'] - fin), wrap(s[k]['chest'] - fin), s[k]['lat'], s[k]['roll'], s[k]['pz'], math.hypot(R[k][6], R[k][7]), R[k][S['h_level']], R[k][S['turn_sev']]))
