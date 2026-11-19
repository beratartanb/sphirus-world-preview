# an_stride.py <label> [label...]: step length / cadence / swing-foot clearance by terrain grade (contact = an_stop2 definition).
# step = horizontal distance between consecutive opposite-foot touchdowns; cadence = touchdowns per minute; swing clear = max
# height of the swinging ball above ITS OWN traced ground between touchdowns; knee = min knee angle of the landing leg.
import json, sys, math, statistics as st
RD = 'Saved/Codex/Grip_20261106/rec/'
def grade(r):
    g = r['gnd']; nz = g['cap'][2] if g['cap'][2] else 1.0; a = math.degrees(math.acos(max(-1, min(1, nz)))); return a
for L in sys.argv[1:]:
    R = [r for r in json.load(open(RD + L + '.json'))['rows'] if isinstance(r.get('gnd'), dict) and r['gnd']['f'][0] and r['gnd']['f'][1]]
    tds = []
    for k, b in ((0, 'ball_l'), (1, 'ball_r')):
        on = False
        for i in range(1, len(R)):
            a, c = R[i - 1], R[i]; h = c['ub'][b][2] - c['gnd']['f'][k][0]; vz = (c['ub'][b][2] - a['ub'][b][2]) / max(1e-3, c['t'] - a['t'])
            now = h < 5 and abs(vz) < 20
            if now and not on: tds.append((c['t'], k, c['ub'][b][:2], i))
            on = now
    tds.sort(); rows = {}
    for j in range(1, len(tds)):
        (t0, k0, p0, i0), (t1, k1, p1, i1) = tds[j - 1], tds[j]
        if k0 == k1 or t1 - t0 > 1.2: continue
        r = R[i1]; spd = math.hypot(r['vx'], r['vy'])
        if spd < 60: continue
        gr = grade(r); bn = 'flat <4' if gr < 4 else ('6-15' if gr < 15 else '15-40')
        dz = (R[i1]['z'] - R[i0]['z']); bn = ('up ' if dz > 1 else ('down ' if dz < -1 else '')) + bn
        sw = 'ball_l' if k1 == 0 else 'ball_r'; clr = max(R[i]['ub'][sw][2] - R[i]['gnd']['f'][k1][0] for i in range(i0, i1 + 1))
        rows.setdefault(bn, []).append((math.hypot(p1[0] - p0[0], p1[1] - p0[1]), 60.0 / (t1 - t0), spd, clr))
    print('==', L)
    for bn, v in sorted(rows.items()):
        print('  %-12s n %3d step %5.1f cm  cadence %5.1f/min  speed %4.0f  swing clearance max %4.1f cm' % (bn, len(v), st.mean(x[0] for x in v), st.mean(x[1] for x in v), st.mean(x[2] for x in v), st.mean(x[3] for x in v)))
