# an_post6.py <label>: carriage of the visible body per plan segment with the TRANSITION (first 1.2 s of the segment) and the STEADY part
# reported separately (round-5 analysis skipped the first 1.2 s). Same thorax-frame definitions as an_carry5.py (imported, unchanged).
# Per part: mean [min..max] of trunk lean, neck angle, head pitch, head forward (cm), upper-arm abduction L/R, smallest wrist distance from
# the pelvis line (cm, < 0 = across the midline), and the largest change within 0.1 s of lean / head pitch / abduction (deg) = jerkiness.
import json, sys, math, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'UE59_20261122')); from an_carry5 import met
def st(v): return (sum(v)/len(v), min(v), max(v)) if v else (0, 0, 0)
def rate(W, M, k):
    b = 0.0
    for i in range(len(W)):
        j = i
        while j < len(W) and W[j]['t'] - W[i]['t'] < 0.1: j += 1
        if j < len(W) and k in M[i] and k in M[j]: b = max(b, abs(M[j][k] - M[i][k]))
    return b
SRC = sys.argv[2] if len(sys.argv) > 2 else 'pv'; lab = sys.argv[1]; D = json.load(open('Saved/Codex/Grip_20261106/rec/' + lab + '.json')); plan = D.get('plan') or []; R = D['rows']; segs = {}
for r in R:
    if isinstance(r.get('hook'), dict) and SRC in r['hook']: segs.setdefault(r['s'], []).append(r)
print('#### %s  (part: T = first 1.2 s, S = steady)' % lab)
for s, rr in sorted(segs.items()):
    for tag, W in (('T', [r for r in rr if r['t'] - rr[0]['t'] <= 1.2]), ('S', [r for r in rr if r['t'] - rr[0]['t'] > 1.2])):
        if len(W) < 20: continue
        M = [met(r['hook'][SRC], r['hook'].get('pq', {}).get('head') if SRC == 'pv' else None) for r in W]; g = lambda k: st([m[k] for m in M if k in m]); sp = st([math.hypot(r['vx'], r['vy']) for r in W])
        print('s%-2d %-11s %s v %3.0f..%3.0f | lean %5.1f [%5.1f..%5.1f] | neck %5.1f [%5.1f..%5.1f] | head pitch %5.1f [%5.1f..%5.1f] fwd %4.1f | abd L %4.1f [%4.1f..%4.1f] R %4.1f [%4.1f..%4.1f] | wrist min %5.1f/%5.1f | max change in 0.1 s: lean %4.1f pitch %4.1f abd %4.1f' % (
            s, (plan[s][0] if s < len(plan) else '?').replace('LeftShift', 'Sh').replace('LeftControl', 'Ct')[:11] or '-', tag, sp[1], sp[2], g('lean')[0], g('lean')[1], g('lean')[2], g('neck')[0], g('neck')[1], g('neck')[2],
            g('hpitch')[0], g('hpitch')[1], g('hpitch')[2], g('headfwd')[0], g('abd_l')[0], g('abd_l')[1], g('abd_l')[2], g('abd_r')[0], g('abd_r')[1], g('abd_r')[2], g('wlat_l')[1], g('wlat_r')[1],
            rate(W, M, 'lean'), rate(W, M, 'hpitch'), max(rate(W, M, 'abd_l'), rate(W, M, 'abd_r'))))
