# an_stop2.py <label> [label ...] (2026-11-19): stop / brake analysis with time-based windows and validated foot contact.
# Every release while moving (plan segment without move keys after a moving segment):
#  v_in      instantaneous horizontal speed at the release frame;  v_win = mean speed over the 0.5 s before release
#  stop      time / distance until speed < 5 cm/s
#  pelvis    reference = mean pelvis height above the ground under the capsule over the 0.5 s before release;
#            drop = reference - minimum during the stop (cm); t_min = time of that minimum
#  settle    first time after t_min from which the pelvis stays within 1.5 cm of its final value for at least 0.30 s
#            (a single-frame approach does not count)
#  contact   per foot (ball): height above the traced ground < 5 cm AND |vertical speed| < 20 cm/s; horizontal motion is NOT used,
#            so a sliding planted foot still counts as planted
#  slide_L / slide_R = summed horizontal path of that ball while in contact, from release until stop + 0.3 s (cm);
#  slide_sum = slide_L + slide_R (a path length over both feet, not a displacement and not cm/s)
#  drift_L / drift_R = largest distance of the ball from where its current contact began (worst single planted-foot drift, cm)
import json, sys, math, statistics as st
RD = 'Saved/Codex/Grip_20261106/rec/'
MOVE = ('W', 'S', 'A', 'D')
def gpel(r):
    g = r.get('gnd')
    return r['ub']['pelvis'][2] - g['cap'][1] if isinstance(g, dict) and g['cap'][1] is not None else None
def ana(L, out):
    d = json.load(open(RD + L + '.json')); R = d['rows']; plan = d['plan']
    out.append('== %s' % L)
    for s in sorted(set(r['s'] for r in R)):
        if s == 0: continue
        keys = plan[s][0]; prev = plan[s - 1][0]
        if any(k in keys.split() for k in MOVE) or not any(k in prev.split() for k in MOVE): continue
        S = [r for r in R if r['s'] == s]; Pall = [r for r in R if r['s'] == s - 1]
        if len(S) < 5 or len(Pall) < 5: continue
        t0 = S[0]['t']; Pv = [r for r in Pall if r['t'] >= t0 - 0.5]
        v_in = math.hypot(S[0]['vx'], S[0]['vy']); v_win = st.mean(math.hypot(r['vx'], r['vy']) for r in Pv)
        ref = st.mean(x for x in (gpel(r) for r in Pv) if x is not None)
        ph = [(r['t'] - t0, gpel(r)) for r in S if gpel(r) is not None]
        tmin, hmin = min(ph, key=lambda x: x[1]); drop = ref - hmin
        stop_t = next((r['t'] - t0 for r in S if math.hypot(r['vx'], r['vy']) < 5), float('nan'))
        dist = math.hypot(S[-1]['x'] - S[0]['x'], S[-1]['y'] - S[0]['y'])
        fin = ph[-1][1]; settle = float('nan')
        for i, (t, h) in enumerate(ph):
            if t < tmin: continue
            win = [hh for tt, hh in ph[i:] if tt <= t + 0.30]
            if ph[-1][0] >= t + 0.30 and all(abs(hh - fin) < 1.5 for hh in win): settle = t; break
        lim = (stop_t if stop_t == stop_t else 2.0) + 0.3
        sl = [0.0, 0.0]; dr = [0.0, 0.0]
        for k, b in ((0, 'ball_l'), (1, 'ball_r')):
            anchor = None
            for j in range(1, len(S)):
                a_, b_ = S[j - 1], S[j]
                if b_['t'] - t0 > lim: break
                ga, gb = a_['gnd']['f'][k], b_['gnd']['f'][k]
                if not (ga and gb): anchor = None; continue
                dt = max(1e-3, b_['t'] - a_['t']); za, zb = a_['ub'][b][2] - ga[0], b_['ub'][b][2] - gb[0]
                vz = (b_['ub'][b][2] - a_['ub'][b][2]) / dt
                if za < 5 and zb < 5 and abs(vz) < 20:
                    if anchor is None: anchor = a_['ub'][b][:2]
                    sl[k] += math.hypot(b_['ub'][b][0] - a_['ub'][b][0], b_['ub'][b][1] - a_['ub'][b][1])
                    dr[k] = max(dr[k], math.hypot(b_['ub'][b][0] - anchor[0], b_['ub'][b][1] - anchor[1]))
                else: anchor = None
        clips = []
        for r in S[:int(len(S) * 0.8)]:
            c = (r.get('gasp') or [None])[0]
            if c and (not clips or clips[-1] != c): clips.append(c)
        out.append('  seg %2d after %-26s v_in %3.0f v_win %3.0f | stop %.2fs %4.0f cm | pelvis ref %5.1f drop %4.1f @%.2fs settle %4.2fs | slide L %5.1f R %5.1f sum %5.1f | drift L %4.1f R %4.1f | %s' % (
            s, '"%s" %.2fs' % (prev, plan[s - 1][1]), v_in, v_win, stop_t, dist, ref, drop, tmin, settle, sl[0], sl[1], sl[0] + sl[1], dr[0], dr[1], ' > '.join(c[:32] for c in clips[:3])))
o = []
for L in sys.argv[1:]: ana(L, o)
print('\n'.join(o))
