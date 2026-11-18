# an_stop.py <label>...: every input release while moving (plan segment with no move key after a moving segment):
# entry speed and gait keys, stop clip chain, stopping distance / time (v < 5), visible pelvis drop below its pre-release mean
# (height above the traced ground under the capsule), recovery time back within 2 cm, ball slide while in contact during the stop.
import json, sys, math, statistics as st
for L in sys.argv[1:]:
    d = json.load(open('Saved/Codex/Grip_20261106/rec/%s.json' % L)); R = d['rows']; plan = d['plan']
    print('==', L)
    segs = sorted(set(r['s'] for r in R))
    for s in segs:
        if s == 0: continue
        keys = plan[s][0]; prev = plan[s - 1][0]
        if any(k in keys for k in ('W', 'S', 'A', 'D')) or not any(k in prev for k in ('W', 'S', 'A', 'D')): continue
        S = [r for r in R if r['s'] == s]; Pv = [r for r in R if r['s'] == s - 1][-30:]
        if len(S) < 5 or len(Pv) < 5: continue
        t0 = S[0]['t']; v0 = st.mean(math.hypot(r['vx'], r['vy']) for r in Pv)
        g = lambda r: r['ub']['pelvis'][2] - r['gnd']['cap'][1] if isinstance(r.get('gnd'), dict) and r['gnd']['cap'][1] is not None else None
        base = st.mean(x for x in (g(r) for r in Pv) if x is not None)
        ph = [(r['t'] - t0, g(r)) for r in S if g(r) is not None]
        drop = base - min(h for _, h in ph); tmin = min(ph, key=lambda x: x[1])[0]
        stop_t = next((r['t'] - t0 for r in S if math.hypot(r['vx'], r['vy']) < 5), float('nan'))
        dist = math.hypot(S[-1]['x'] - S[0]['x'], S[-1]['y'] - S[0]['y'])
        rec = next((t for t, h in ph if t > tmin and abs(h - ph[-1][1]) < 2.0), float('nan'))
        clips = []
        for r in S[:int(len(S) * 0.8)]:
            c = (r.get('gasp') or [None])[0]
            if c and (not clips or clips[-1] != c): clips.append(c)
        dt = S[1]['t'] - S[0]['t']; sl = 0.0
        for k, b in ((0, 'ball_l'), (1, 'ball_r')):
            for j in range(1, len(S)):
                g0 = S[j - 1]['gnd']['f'][k]; g1 = S[j]['gnd']['f'][k]
                if g0 and g1 and S[j - 1]['ub'][b][2] - g0[0] < 6 and S[j]['ub'][b][2] - g1[0] < 6 and S[j]['t'] - t0 < (stop_t if stop_t == stop_t else 2.0) + 0.3:
                    sl += math.hypot(S[j]['ub'][b][0] - S[j - 1]['ub'][b][0], S[j]['ub'][b][1] - S[j - 1]['ub'][b][1])
        print('  seg %2d after %-24s v0 %3.0f | stop %.2fs dist %4.0f cm | pelvis drop %4.1f cm at %.2fs, settle %.2fs | foot slide %4.1f cm | %s' % (
            s, '"%s" %.2fs' % (prev, plan[s - 1][1]), v0, stop_t, dist, drop, tmin, rec, sl, ' > '.join(c[:30] for c in clips[:3])))
