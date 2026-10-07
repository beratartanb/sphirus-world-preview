# brow mapping iteration: per-|x| raise table update from measured response (same-method centreline measurements, both sides averaged)
import json, sys
d0 = json.load(open(sys.argv[1])); d1 = json.load(open(sys.argv[2])); tab = json.loads(sys.argv[3]); CX = 413.6; K = 0.0332; PZ = 0.0336
def interp(t, x):
    if x <= t[0][0]: return t[0][1]
    for (a, va), (b, vb) in zip(t, t[1:]):
        if x <= b: return va+(vb-va)*(x-a)/(b-a)
    return t[-1][1]
def rows(d, s): return {r[0]: r for r in d['sides'][s]['rows'] if r[1] is not None and r[3] is not None}
U = {}
for s, rng in (('imgL', range(278, 381)), ('imgR', range(440, 546))):
    r0, r1 = rows(d0, s), rows(d1, s)
    for x in rng:
        if x in r0 and x in r1:
            u = round(abs(x-CX)); want = r0[x][3]-r0[x][1]; got = (r0[x][3]-r0[x][1])-(r1[x][3]-r1[x][1]); U.setdefault(u//5*5, []).append((want, got))
out = []
for u in sorted(U):
    w = sum(a for a, b in U[u])/len(U[u]); g = sum(b for a, b in U[u])/len(U[u]); ax = round(u*K+2.5*K, 3); ap = interp(tab, ax)/PZ
    gain = g/ap if abs(ap) > 0.5 else 1.0; gain = min(max(gain, 0.6), 3.0); new = w/gain
    out.append([ax, round(new*PZ, 3), round(w, 1), round(g, 1), round(gain, 2)])
print('ITER |x| new_raise_cm want_px got_px gain'); [print('ITER', *o) for o in out]
sm = [[o[0], round((out[max(i-1, 0)][1]+2*o[1]+out[min(i+1, len(out)-1)][1])/4, 3)] for i, o in enumerate(out)]
print('TABLE', json.dumps(sm))
