# an_rev.py <rec> <seg> [...]: reversal / turn anatomy - per 0.1 s: capsule speed, velocity heading vs facing, visible
# pelvis speed and lateral offset from the capsule path, GASP selected anim. Shows arc ("car") vs plant-and-push.
import json, sys, math
d = json.load(open(sys.argv[1])); R = d['rows']
for s in map(int, sys.argv[2:]):
    rows = [r for r in R if r['s'] == s]; print('== seg', s, d['plan'][s][0], len(rows))
    t = 0; nxt = 0; prev = None
    for r in rows:
        if t >= nxt - 1e-6:
            sp = math.hypot(r['vx'], r['vy']); vh = math.degrees(math.atan2(r['vy'], r['vx'])) if sp > 5 else float('nan')
            pv = r.get('ub', {}).get('pelvis'); ps = ''
            if pv and prev: ps = '%4.0f' % (math.hypot(pv[0] - prev[0], pv[1] - prev[1]) / 0.1)
            off = (pv[0] - r['x'], pv[1] - r['y']) if pv else (0, 0)
            g = r.get('gasp'); a = (g[0] or '')[:30] if g else ''
            print('  t%.1f cap %3.0f velHdg %6.1f face %6.1f | pelvisSpd %s off %4.0f,%4.0f | %s' % (t, sp, vh, r['yaw'], ps, off[0], off[1], a))
            prev = pv; nxt += 0.1
        t += r['gdt']
