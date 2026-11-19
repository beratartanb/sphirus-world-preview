# an_turn2.py <label> [label ...] (2026-11-19): per requested flick (yreq jump), same contact definition as an_stop2:
#  contact = ball < 5 cm above traced ground AND |vz| < 20 cm/s (horizontal motion not used, a sliding planted foot still counts)
#  slide L/R = ball path while in contact during the 2.5 s after the flick; drift L/R = worst distance from contact start (cm)
#  pelvis drop = (pelvis height over ground smoothed by a centred 0.4 s moving average, so the gait bob does not count): mean of the
#               0.5 s before the flick minus the smoothed minimum in the 2.5 s after (cm)
#  rec = first time after that minimum from which the smoothed pelvis stays within 1.5 cm of the pre-flick reference for 0.3 s
#  clips = driver clip chain in the first 1.5 s
import json, sys, math, statistics as st
RD = 'Saved/Codex/Grip_20261106/rec/'
def gp(r):
    g = r.get('gnd'); return r['ub']['pelvis'][2] - g['cap'][1] if isinstance(g, dict) and g['cap'][1] is not None else None
def contact(S):
    sl = [0.0, 0.0]; dr = [0.0, 0.0]
    for k, b in ((0, 'ball_l'), (1, 'ball_r')):
        an = None
        for j in range(1, len(S)):
            a, c = S[j - 1], S[j]; ga, gc = a['gnd']['f'][k], c['gnd']['f'][k]
            if not (ga and gc): an = None; continue
            dt = max(1e-3, c['t'] - a['t']); vz = (c['ub'][b][2] - a['ub'][b][2]) / dt
            if a['ub'][b][2] - ga[0] < 5 and c['ub'][b][2] - gc[0] < 5 and abs(vz) < 20:
                if an is None: an = a['ub'][b][:2]
                sl[k] += math.hypot(c['ub'][b][0] - a['ub'][b][0], c['ub'][b][1] - a['ub'][b][1]); dr[k] = max(dr[k], math.hypot(c['ub'][b][0] - an[0], c['ub'][b][1] - an[1]))
            else: an = None
    return sl, dr
for L in sys.argv[1:]:
    R = json.load(open(RD + L + '.json'))['rows']; ev = []; prev = R[0]['yreq']
    for r in R:
        if abs(r['yreq'] - prev) > 1 and (not ev or r['t'] - ev[-1] > 1.0): ev.append(r['t'])
        prev = r['yreq']
    print('==', L)
    for t0 in ev:
        S = [r for r in R if t0 - 0.02 <= r['t'] < t0 + 2.5]; P = [r for r in R if t0 - 0.5 <= r['t'] < t0]
        req = S[-1]['yreq'] - S[0]['yreq']; sl, dr = contact(S)
        W = [(r['t'], gp(r)) for r in R if t0 - 0.8 <= r['t'] < t0 + 2.8 and gp(r) is not None]
        sm = lambda tc: st.mean(h for t, h in W if abs(t - tc) <= 0.2)
        ref = st.mean(sm(r['t']) for r in P if gp(r) is not None); ph = [(r['t'] - t0, sm(r['t'])) for r in S if gp(r) is not None]
        tmin, hmin = min(ph, key=lambda x: x[1]); rec = float('nan')
        for i, (t, h) in enumerate(ph):
            if t < tmin: continue
            w = [hh for tt, hh in ph[i:] if tt <= t + 0.3]
            if ph[-1][0] >= t + 0.3 and all(abs(hh - ref) < 1.5 for hh in w): rec = t; break
        spd = st.mean(math.hypot(r['vx'], r['vy']) for r in P); cl = []
        for r in S:
            if r['t'] - t0 > 1.5: break
            c = (r.get('gasp') or [None])[0]
            if c and (not cl or cl[-1] != c): cl.append(c)
        print('  %+5.0f v %3.0f | slide L %5.1f R %5.1f sum %5.1f | drift L %4.1f R %4.1f | pelvis drop %4.1f @%.2fs rec %.2fs | %s' % (req, spd, sl[0], sl[1], sl[0] + sl[1], dr[0], dr[1], ref - hmin, tmin, rec, ' > '.join(x[:30] for x in cl[:4])))
