# an_bob8.py <label> [<label2> ...]: vertical / lateral body motion on TRUE steady gait only (round 8; replaces the time-window rule of an_bob7).
#  A sample belongs to a steady gait when the selected clip is a LOOP clip (name contains 'Loop', not Idle) and the capsule speed is within
#  4 % of the segment's own median. The run of such frames is cut into whole step cycles at left-foot contact onsets (game contact curve
#  crossing 50 downwards); only complete cycles count; at least 2 cycles are required, otherwise the segment is reported as 'no steady gait'
#  (start / transition clips are never measured as a gait). Pelvis values are a body marker, not the centre of mass.
#  per gait: clip, speed, cycles, cycle time, visible pelvis z p2p (mean over cycles) and worst cycle, head z p2p, head lateral p2p, camera z p2p.
import json, sys, math, ast
def D(x): return x if isinstance(x, dict) else ast.literal_eval(x)
for lab in sys.argv[1:]:
    R = [r for r in json.load(open('Saved/Codex/Grip_20261106/rec/' + lab + '.json'))['rows'] if isinstance(r.get('hook'), (dict, str)) and D(r['hook']).get('cv')]
    print('#### %s (steady = loop clip, whole step cycles)' % lab); seg = {}
    for r in R: seg.setdefault(r['s'], []).append(r)
    for s in sorted(seg):
        S = [r for r in seg[s] if 'Loop' in str(r['gasp'][0]) and 'Idle' not in str(r['gasp'][0])]
        if len(S) < 20:
            c = {}
            for r in seg[s]: c[str(r['gasp'][0])[-26:]] = c.get(str(r['gasp'][0])[-26:], 0) + 1
            if max(math.hypot(r['vx'], r['vy']) for r in seg[s]) > 60: print('s%-2d no steady gait (loop frames %d of %d; clips %s)' % (s, len(S), len(seg[s]), sorted(c.items(), key=lambda x: -x[1])[:2]))
            continue
        sp = sorted(math.hypot(r['vx'], r['vy']) for r in S); med = sp[len(sp) // 2]
        S = [r for r in S if abs(math.hypot(r['vx'], r['vy']) - med) <= 0.04 * med]
        on = [i for i in range(1, len(S)) if D(S[i - 1]['hook'])['cv'][0] > 50 >= D(S[i]['hook'])['cv'][0] and S[i]['f'] - S[i - 1]['f'] <= 2]
        cyc = [(a, b) for a, b in zip(on, on[1:]) if S[b]['f'] - S[a]['f'] == b - a or S[b]['t'] - S[a]['t'] < 1.6]
        cyc = [(a, b) for a, b in cyc if all(S[k + 1]['f'] - S[k]['f'] <= 2 for k in range(a, b))]
        if len(cyc) < 2: print('s%-2d no steady gait (complete cycles %d, loop frames %d)' % (s, len(cyc), len(S))); continue
        pz = []; hz = []; hl = []; cz = []; ct = []
        for a, b in cyc:
            W = S[a:b + 1]; yaw = math.radians(W[0]['yaw']); rx, ry = -math.sin(yaw), math.cos(yaw)
            p = [r['v_pelvis'][2] for r in W]; h = [r['v_head'][2] for r in W]; l = [(r['v_head'][0] - r['x']) * rx + (r['v_head'][1] - r['y']) * ry for r in W]; c = [r['cam'][2] for r in W]
            pz.append(max(p) - min(p)); hz.append(max(h) - min(h)); hl.append(max(l) - min(l)); cz.append(max(c) - min(c)); ct.append(W[-1]['t'] - W[0]['t'])
        m = lambda x: sum(x) / len(x)
        print('s%-2d %-22s v %3.0f | cycles %d x %.2f s | pelvis z p2p mean %4.1f worst %4.1f | head z %4.1f | head lateral %4.1f | camera z %4.1f' % (s, str(S[0]['gasp'][0])[-22:], med, len(cyc), m(ct), m(pz), max(pz), m(hz), m(hl), m(cz)))
