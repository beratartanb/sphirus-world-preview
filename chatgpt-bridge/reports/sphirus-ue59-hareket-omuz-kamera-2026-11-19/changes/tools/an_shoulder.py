# an_shoulder.py <label> [label ...] : shoulder girdle / upper-arm carriage over time (seconds-based windows), visible MetaHuman body
# (VIS) and the UEFN driver skeleton (DRV) separately. Actor frame: x forward, y right, z up (cm / deg).
#  elev   = mean upperarm joint height above the spine_05 joint (shoulder raise)
#  retr   = mean upperarm joint x relative to spine_05 (negative = shoulders held back)
#  width  = upperarm_r.y - upperarm_l.y (shoulder joint width)
#  abd    = upper-arm abduction: angle of the upperarm->elbow segment from straight down, in the frontal plane (+ = elbow out)
#  elbow  = elbow (lowerarm joint) lateral offset outside the shoulder joint (cm)
#  handx  = hand fore-aft swing range (max-min of mean-free hand x) per side
# Windows are fixed durations in seconds relative to the start of each plan segment, independent of the data step.
import sys, json, math, statistics as st
RD = 'Saved/Codex/Grip_20261106/rec/'
def loc(r, p):
    y = math.radians(r['yaw']); dx = p[0] - r['x']; dy = p[1] - r['y']
    return (dx * math.cos(y) + dy * math.sin(y), -dx * math.sin(y) + dy * math.cos(y), p[2] - r['z'])
def vis(r, b):
    if b in ('hand_l', 'hand_r'): return loc(r, r['v_' + b])
    if b in r['ub']: return loc(r, r['ub'][b][:3])
    return loc(r, r['ub2'][b])
def drv(r, b): return loc(r, r['sh']['d'][b])
def met(r, P):
    s5 = P(r, 'spine_05'); ua = [P(r, 'upperarm_l'), P(r, 'upperarm_r')]; la = [P(r, 'lowerarm_l'), P(r, 'lowerarm_r')]
    elev = st.mean(a[2] - s5[2] for a in ua); retr = st.mean(a[0] - s5[0] for a in ua); width = ua[1][1] - ua[0][1]
    abd = []; elb = []
    for k, sg in ((0, -1), (1, 1)):
        dy = (la[k][1] - ua[k][1]) * sg; dz = ua[k][2] - la[k][2]; abd.append(math.degrees(math.atan2(dy, dz))); elb.append(dy)
    return elev, retr, width, st.mean(abd), st.mean(elb)
def window(R, t0, t1): return [r for r in R if t0 <= r['t'] < t1 and isinstance(r.get('sh'), dict)]
def summ(rows, P):
    if not rows: return None
    m = [met(r, P) for r in rows]; return [st.mean(x[i] for x in m) for i in range(5)]
for L in sys.argv[1:]:
    d = json.load(open(RD + L + '.json')); R = d['rows']; plan = d['plan']
    starts = {}
    for r in R: starts.setdefault(r['s'], r['t'])
    print('==', L, 'segments', [(i, plan[i][0], plan[i][1]) for i in range(len(plan))])
    for i, sgm in enumerate(plan):
        if sgm[0] != 'W' or i not in starts: continue
        t0 = starts[i]; prev = plan[i - 1][0] if i else ''
        print('  W segment %d after "%s" (t0 %.2f)' % (i, prev, t0))
        print('     window        spd  RunA  EffA   Fat |  VIS elev  retr width   abd elbow |  DRV elev  retr width   abd elbow')
        wins = [(-1.0, 0.0)] + [(a / 2, a / 2 + 0.5) for a in range(0, 8)] + [(4.0, 6.0), (6.0, sgm[1])]
        for a, b in wins:
            rows = window(R, t0 + a, t0 + b)
            if not rows: continue
            v = summ(rows, vis); dv = summ(rows, drv); spd = st.mean(math.hypot(r['vx'], r['vy']) for r in rows)
            A = lambda k: st.mean(r['sh']['a'].get(k, float('nan')) for r in rows)
            print('    %5.1f..%-5.1f %4.0f  %.2f  %.2f  %.2f | %8.1f %5.1f %5.1f %5.1f %5.1f | %8.1f %5.1f %5.1f %5.1f %5.1f' % ((a, b, spd, A('RunA'), A('EffA'), A('mFat')) + tuple(v) + tuple(dv)))
