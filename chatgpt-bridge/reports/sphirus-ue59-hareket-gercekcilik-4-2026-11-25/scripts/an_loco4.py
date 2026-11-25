# an_loco4.py <label> <plan> : locomotion transitions as the body performs them (pass 4; replaces an_trans.py readings).
# Fixes vs an_trans: a start from rest is named "rest->X start" (0 -> 415 is a rest->run start, not walk->run); steps are STANCE PHASES
# (a foot counts once per support: planted for >= 3 samples after a swing of >= 0.10 s with >= 3 cm lift), not re-detections of the
# same planted foot; a stop that does not reach rest inside its segment is reported as NOT STOPPED with the end speed; idle-clip entry
# while the capsule still moves and foot travel after the capsule stopped are flagged; brake-assist reaction = new key -> CS_Clear off;
# real frame times (rdt) are summarised (a "60/30" label is not FPS evidence).
import json, sys, math
lab = sys.argv[1]; rows = json.load(open('Saved/Codex/Grip_20261106/rec/%s.json' % lab))['rows']; plan = eval(open(sys.argv[2]).read())
H = lambda r: r['hook'] if isinstance(r['hook'], dict) else {}
sp = lambda r: math.hypot(r['vx'], r['vy'])
zmin = {f: min(r[f][2] for r in rows) for f in ('v_foot_l', 'v_foot_r')}
def fspeed(i, f):
    if i == 0: return 0.0
    a, b = rows[i - 1], rows[i]; dt = max(b['t'] - a['t'], 1e-3); return math.hypot(b[f][0] - a[f][0], b[f][1] - a[f][1]) / dt
def stance_onsets(i0, i1, f):
    # a foot already in support when the segment starts is NOT a new step: counting starts after its first swing
    out = []; i0 = max(1, i0); pl0 = fspeed(i0, f) < 30 and rows[i0][f][2] - zmin[f] < 4
    run = 3 if pl0 else 0; swing_t = 0.0; swing_lift = 0.0
    for i in range(i0, i1 + 1):
        pl = fspeed(i, f) < 30 and rows[i][f][2] - zmin[f] < 4
        if pl:
            run += 1
            if run == 3 and swing_t >= 0.10 and swing_lift >= 3.0:
                out.append(rows[i - 2]['t'])
        else:
            if run >= 3: swing_t = 0.0; swing_lift = 0.0
            run = 0; swing_t += rows[i]['t'] - rows[i - 1]['t']; swing_lift = max(swing_lift, rows[i][f][2] - zmin[f])
    return out
def gait(keys, tempo):
    k = keys.split()
    if not any(x in k for x in ('W', 'A', 'S', 'D')): return 'rest'
    g = 'sprint' if 'LeftControl' in k else 'run' if 'LeftShift' in k else 'tempo' if tempo else 'walk'
    return ('back ' if k == ['S'] or (('S' in k) and 'W' not in k and 'A' not in k and 'D' not in k) else '') + g
segs = {}
for i, r in enumerate(rows): segs.setdefault(r['s'], []).append(i)
rdt = sorted(r.get('rdt') or 0 for r in rows if r.get('rdt')); gdt = sorted(r.get('gdt') or 0 for r in rows if r.get('gdt'))
pc = lambda a, q: a[min(len(a) - 1, int(q * len(a)))] if a else 0
print('%s | real frame time ms p50 %.1f p95 %.1f max %.1f | game dt ms p50 %.1f p95 %.1f | frames %d' % (lab, 1000 * pc(rdt, .5), 1000 * pc(rdt, .95), 1000 * (rdt[-1] if rdt else 0), 1000 * pc(gdt, .5), 1000 * pc(gdt, .95), len(rows)))
tempo = False
for s, ix in sorted(segs.items()):
    if s == 0 or s >= len(plan): continue
    i0, i1 = ix[0], ix[-1]; k = plan[s][0]; kp = plan[s - 1][0]; dur = plan[s][1]; t0 = rows[i0]['t']
    tempo = bool(H(rows[i0]).get('GR_TempoOn', tempo)); g1 = gait(k, tempo); g0 = gait(kp, bool(H(rows[i0 - 1]).get('GR_TempoOn', tempo)))
    v0 = sp(rows[i0 - 1]); ve = sp(rows[i1]); vmax = max(sp(rows[i]) for i in ix)
    if 'X' in k.split() and g1 == g0: continue
    if g1 == 'rest' and v0 < 20: continue
    if g1 != 'rest': kind = ('rest->%s start' % g1) if v0 < 20 else ('re-press %s during stop' % g1 if g0 == 'rest' else '%s->%s' % (g0, g1))
    elif k.strip(): kind = '%s key while moving (%s)' % (k.strip(), g0)
    else: kind = '%s stop' % g0
    if g1 != 'rest' and dur < 0.4: kind = 'tap %s %.2f s' % (g1, dur)
    st = sorted([(t - t0, 'L') for t in stance_onsets(i0, i1, 'v_foot_l')] + [(t - t0, 'R') for t in stance_onsets(i0, i1, 'v_foot_r')])
    line = '%-34s s%-2d [%-11s] v %3.0f -> %3.0f (max %3.0f)' % (kind, s, k.replace('LeftShift', 'Sh').replace('LeftControl', 'Ct') or '-', v0, ve, vmax)
    if (g1 == 'rest' and not k.strip()) or kind.startswith('tap'):
        # stop: rest = speed < 5 for >= 0.15 s
        ts = None
        for i in ix:
            if sp(rows[i]) < 5:
                j = i
                while j <= i1 and sp(rows[j]) < 5: j += 1
                if rows[min(j, i1)]['t'] - rows[i]['t'] >= 0.15 or j > i1: ts = i; break
        dist = sum(math.hypot(rows[i]['x'] - rows[i - 1]['x'], rows[i]['y'] - rows[i - 1]['y']) for i in range(i0, (ts or i1) + 1))
        early = [rows[i]['t'] - t0 for i in ix if 'Idle' in (rows[i]['gasp'][0] or '') and sp(rows[i]) > 30]
        after = ''
        if ts is not None:
            fm = max(math.hypot(rows[i][f][0] - rows[ts][f][0], rows[i][f][1] - rows[ts][f][1]) for f in ('v_foot_l', 'v_foot_r') for i in range(ts, i1 + 1))
            na = [x for x in st if x[0] > rows[ts]['t'] - t0 + 0.05]
            after = ' | feet after rest: max travel %.1f cm, %d new supports' % (fm, len(na))
        cs = [rows[i]['t'] - t0 for i in ix if H(rows[i]).get('exs', [None])[0] in (True, 1, 'True')] if False else []
        ex = [H(rows[i]).get('ex') for i in ix]; coast = [rows[i]['t'] - t0 for i, e in zip(ix, ex) if isinstance(e, list) and len(e) >= 5 and False]
        line += ' | %s%s | %d supports %s%s%s' % ('rest after %.2f s, %.0f cm' % (rows[ts]['t'] - t0, dist) if ts is not None else 'NOT STOPPED in segment (end %.0f cm/s after %.2f s, %.0f cm)' % (ve, rows[i1]['t'] - t0, dist), '',
                                              len(st), ' '.join('%s%.2f' % (f, t) for t, f in st[:8]), (' | IDLE CLIP WHILE MOVING from %.2f s' % early[0]) if early else '', after)
    else:
        tgt = ve if abs(ve - vmax) < 25 else vmax
        t90 = next((rows[i]['t'] - t0 for i in ix if (sp(rows[i]) >= v0 + 0.9 * (tgt - v0) if tgt > v0 else sp(rows[i]) <= v0 + 0.9 * (tgt - v0))), None)
        j90 = next((i for i in ix if rows[i]['t'] - t0 >= (t90 or 0)), i1)
        dist = sum(math.hypot(rows[i]['x'] - rows[i - 1]['x'], rows[i]['y'] - rows[i - 1]['y']) for i in range(i0, j90 + 1))
        ns = len([x for x in st if x[0] <= (t90 or 9e9) + 0.05])
        line += ' | 90%% of change after %s, %.0f cm, %d supports %s' % ('%.2f s' % t90 if t90 is not None else 'n/a', dist, ns, ' '.join('%s%.2f' % (f, t) for t, f in st[:ns][:8]))
    clips = []
    for i in ix:
        c = rows[i]['gasp'][0] or 'None'
        if not clips or clips[-1][0] != c: clips.append([c, rows[i]['t'] - t0])
    print(line); print('      clips: ' + '  '.join('%s@%.2f' % (c[-28:], t) for c, t in clips[:6]))
# brake-assist reaction: segments that start while the assist is active (CS_Clear true on the previous frame)
for s, ix in sorted(segs.items()):
    if s == 0 or s >= len(plan) or not plan[s][0].strip(): continue
    i0 = ix[0]; e = H(rows[i0 - 1]).get('exs')
    act = isinstance(e, list) and e and e[0] in (True, 1, 'True', 1.0)
    if not act: continue
    off = next((rows[i]['t'] - rows[i0]['t'] for i in ix if not (isinstance(H(rows[i]).get('exs'), list) and H(rows[i])['exs'][0] in (True, 1, 'True', 1.0))), None)
    print('REACTION s%d [%s] new key during brake assist -> assist off after %s' % (s, plan[s][0], '%.3f s' % off if off is not None else 'NEVER in segment'))
