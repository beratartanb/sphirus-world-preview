# an_stop3.py <label> [label ...] (2026-11-19 evening): stop / brake analysis on SIMULATED time.
# Time: rows recorded after recorder patch #8 carry t = simulated game time. Older rows carry t = frame/FPS, which was wrong in
#   data-only 30 Hz runs (game ran ~1/60 per frame); for those the simulated time is rebuilt as the running sum of gdt.
#   'tsrc' in the header says which was used.
# Per release while moving (plan segment without move keys after a moving one):
#  v_in  instantaneous horizontal speed at the release row;  v_win = mean speed over the 0.5 s (sim) before release
#  stop  t_stop = first sim time with speed < 5 cm/s; d_stop = capsule PATH length from release to t_stop (cm)
#  held  t_held = first time from which speed stays < 5 cm/s for 0.30 s (recovery = held state, not one frame)
#  pelvis drop = ref (mean pelvis-above-ground 0.5 s before release) - min during the stop; settle = pelvis within 1.5 cm of
#        its final value for >= 0.30 s
#  contact per foot (ball bone): height above traced ground < 5 cm AND |vertical ball speed| < 20 cm/s (sim time), lasting at
#        least 0.10 s. Ball horizontal motion is not part of the test, so a sliding planted ball still counts as planted.
#        Heel-toe roll moves the ANKLE while the ball stays: only ball motion counts as slide.
#  slide_L/R = horizontal ball path while in contact, release .. t_held+0.3 (cm); sum = L+R (path, not displacement)
#  drift_L/R = largest ball distance from where its contact began (worst single contact, cm); nC = contacts per foot
import json, sys, math, statistics as st
RD = 'Saved/Codex/Grip_20261106/rec/'
MOVE = ('W', 'S', 'A', 'D')
def simtime(R):
    if 'tw' in R[0]: return [r['t'] for r in R], 'sim(t)'
    T = [0.0]
    for r in R[1:]: T.append(T[-1] + r['gdt'])
    return T, 'sim(sum gdt)'
def gpel(r):
    g = r.get('gnd')
    return r['ub']['pelvis'][2] - g['cap'][1] if isinstance(g, dict) and g['cap'][1] is not None else None
def contacts(S, T, k, b, lim):
    # returns list of (start_idx, end_idx) of validated contacts within the window
    flag = []
    for j in range(len(S)):
        if T[j] > lim or j == 0: flag.append(False); continue
        a_, b_ = S[j - 1], S[j]; ga, gb = a_['gnd']['f'][k], b_['gnd']['f'][k]
        if not (ga and gb): flag.append(False); continue
        dt = max(1e-3, T[j] - T[j - 1]); zb = b_['ub'][b][2] - gb[0]; za = a_['ub'][b][2] - ga[0]
        vz = (b_['ub'][b][2] - a_['ub'][b][2]) / dt
        flag.append(za < 5 and zb < 5 and abs(vz) < 20)
    out = []; j = 0
    while j < len(flag):
        if flag[j]:
            i = j
            while j < len(flag) and flag[j]: j += 1
            if T[j - 1] - T[i - 1] >= 0.10: out.append((i - 1, j - 1))
        else: j += 1
    return out
def ana(L, out):
    d = json.load(open(RD + L + '.json')); R = d['rows']; plan = d['plan']; TT, src = simtime(R)
    out.append('== %s  (%s, rows %d, sim %.2f s, label t %.2f s)' % (L, src, len(R), TT[-1], R[-1].get('tf', R[-1]['t'])))
    for s in sorted(set(r['s'] for r in R)):
        if s == 0: continue
        keys = plan[s][0]; prev = plan[s - 1][0]
        if any(k in keys.split() for k in MOVE) or not any(k in prev.split() for k in MOVE): continue
        idx = [i for i, r in enumerate(R) if r['s'] == s]; pidx = [i for i, r in enumerate(R) if r['s'] == s - 1]
        if len(idx) < 5 or len(pidx) < 5: continue
        S = [R[i] for i in idx]; T = [TT[i] - TT[idx[0]] for i in idx]
        Pv = [R[i] for i in pidx if TT[i] >= TT[idx[0]] - 0.5]
        sp = [math.hypot(r['vx'], r['vy']) for r in S]
        v_in = sp[0]; v_win = st.mean(math.hypot(r['vx'], r['vy']) for r in Pv)
        js = next((j for j in range(len(S)) if sp[j] < 5), None)
        t_stop = T[js] if js is not None else float('nan')
        d_stop = sum(math.hypot(S[j]['x'] - S[j - 1]['x'], S[j]['y'] - S[j - 1]['y']) for j in range(1, (js if js is not None else len(S) - 1) + 1))
        t_held = float('nan')
        for j in range(len(S)):
            if sp[j] < 5 and T[-1] >= T[j] + 0.30 and all(sp[i] < 5 for i in range(j, len(S)) if T[i] <= T[j] + 0.30): t_held = T[j]; break
        pv = [x for x in (gpel(r) for r in Pv) if x is not None]; ref = st.mean(pv) if pv else float('nan')
        ph = [(T[j], gpel(S[j])) for j in range(len(S)) if gpel(S[j]) is not None]
        tmin, hmin = min(ph, key=lambda x: x[1]); drop = ref - hmin; fin = ph[-1][1]; settle = float('nan')
        for i, (t, h) in enumerate(ph):
            if t < tmin: continue
            win = [hh for tt, hh in ph[i:] if tt <= t + 0.30]
            if ph[-1][0] >= t + 0.30 and all(abs(hh - fin) < 1.5 for hh in win): settle = t; break
        lim = (t_held if t_held == t_held else 2.0) + 0.3
        sl = [0.0, 0.0]; dr = [0.0, 0.0]; nc = [0, 0]; worst = [None, None]
        for k, b in ((0, 'ball_l'), (1, 'ball_r')):
            for (i0, i1) in contacts(S, T, k, b, lim):
                nc[k] += 1; a0 = S[i0]['ub'][b][:2]; m = 0.0
                for j in range(i0 + 1, i1 + 1):
                    sl[k] += math.hypot(S[j]['ub'][b][0] - S[j - 1]['ub'][b][0], S[j]['ub'][b][1] - S[j - 1]['ub'][b][1])
                    m = max(m, math.hypot(S[j]['ub'][b][0] - a0[0], S[j]['ub'][b][1] - a0[1]))
                if m > dr[k]: dr[k] = m; worst[k] = (round(T[i0], 2), round(T[i1], 2))
        clips = []
        for r in S[:int(len(S) * 0.8)]:
            c = (r.get('gasp') or [None])[0]
            if c and (not clips or clips[-1] != c): clips.append(c)
        out.append('  seg %2d after %-30s v_in %3.0f v_win %3.0f | stop %.2fs path %4.0f cm held %.2fs | pelvis drop %4.1f @%.2f settle %4.2f | slide L %5.1f R %5.1f sum %5.1f | drift L %4.1f%s R %4.1f%s nC %d/%d | %s' % (
            s, '"%s" %.2fs' % (prev, plan[s - 1][1]), v_in, v_win, t_stop, d_stop, t_held, drop, tmin, settle, sl[0], sl[1], sl[0] + sl[1],
            dr[0], str(worst[0] or ''), dr[1], str(worst[1] or ''), nc[0], nc[1], ' > '.join(c[:34] for c in clips[:3])))
o = []
for L in sys.argv[1:]:
    try: ana(L, o)
    except Exception as e: o.append('== %s ERROR %r' % (L, e))
print('\n'.join(o))
