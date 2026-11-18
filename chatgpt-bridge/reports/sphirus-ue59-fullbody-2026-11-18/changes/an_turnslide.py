# an_turnslide.py <label>...: per flick (requested yaw): per-ball slide while within 6 cm of its traced ground for 2.5 s, clip chain,
# straight-walk baseline slide (2 s before the first flick)
import json, sys, math
def slide(S, dt):
    o = []
    for k, b in ((0, 'ball_l'), (1, 'ball_r')):
        d = 0; mx = 0
        for j in range(1, len(S)):
            g0 = S[j-1]['gnd']['f'][k]; g1 = S[j]['gnd']['f'][k]
            if g0 and g1 and S[j-1]['ub'][b][2]-g0[0] < 6 and S[j]['ub'][b][2]-g1[0] < 6:
                v = math.hypot(S[j]['ub'][b][0]-S[j-1]['ub'][b][0], S[j]['ub'][b][1]-S[j-1]['ub'][b][1]); d += v; mx = max(mx, v/dt)
        o.append((d, mx))
    return o
for L in sys.argv[1:]:
    R = json.load(open('Saved/Codex/Grip_20261106/rec/%s.json' % L))['rows']; dt = R[1]['t']-R[0]['t']
    ev = []; prev = R[0]['yreq']
    for i, r in enumerate(R):
        if abs(r['yreq']-prev) > 1 and (not ev or r['t']-ev[-1] > 1.0): ev.append(r['t'])
        prev = r['yreq']
    B = [r for r in R if ev[0]-2.0 <= r['t'] < ev[0]]; bs = slide(B, dt)
    line = ['%-14s base %4.1f/%4.1f' % (L, bs[0][0]/2, bs[1][0]/2)]
    tot = 0
    for t0 in ev:
        S = [r for r in R if t0-0.05 <= r['t'] < t0+2.5]; req = S[-1]['yreq']-S[0]['yreq']; sl = slide(S, dt); tot += sl[0][0]+sl[1][0]
        line.append('%+4.0f:%4.1f+%4.1f' % (req, sl[0][0], sl[1][0]))
    print(' | '.join(line), '| total %.0f cm' % tot)
