# an_ct6.py <label> [lane]: contact v2 summary + BODY-vs-OBSTACLE penetration of the visible body.
#  events: impact / trip (time, speed, class, severity, level, support foot, rear room, flat-ahead), state timeline.
#  penetration: for the lane's obstacle boxes (world AABB from the course scripts) the depth of visible-body points INSIDE the box, per body
#  part (knee = calf origin, shin = 3 points knee->ankle, foot, ball, pelvis, hand, elbow, head), with a limb radius subtracted from the free
#  distance: depth = radius - signed distance to the box surface (> 0 = the limb's surface is inside). Reports the worst frame per part.
#  lane names: wall waist knee side sprintwall wall45 step log tight beam (default: guessed from the pawn's start y)
import json, sys, math
lab = sys.argv[1]; D = json.load(open('Saved/Codex/Grip_20261106/rec/' + lab + '.json')); R0 = D['rows'] if isinstance(D, dict) else D
R = [r for r in R0 if isinstance(r.get('hook'), dict) and r['hook'].get('ct')]
if not R:
    print(lab, 'no ct data', [(r.get('hook') or {}).get('cterr') for r in R0[5:6]]); sys.exit(0)
BOX = {'wall': [((-5085, -6000, 150), (30, 600, 300))], 'waist': [((-5060, -6500, 52.5), (80, 300, 105))], 'knee': [((-5070, -7000, 30), (60, 300, 60))],
       'side': [((-4900, -7449, 150), (1400, 30, 300))], 'sprintwall': [((-4485, -8000, 150), (30, 600, 300))], 'step': [((-5070, -9000, 15), (60, 300, 30))],
       'log': [((-5090, -4700, 12.5), (20, 300, 25))], 'tight': [((-5710, -5200, 30), (60, 300, 60)), ((-5855, -5200, 150), (30, 300, 300))], 'beam': [((-5085, -3200, 175), (30, 300, 50))]}
LY = {-6000: 'wall', -6500: 'waist', -7000: 'knee', -7500: 'side', -8000: 'sprintwall', -9000: 'step', -4700: 'log', -5200: 'tight', -3200: 'beam'}
lane = sys.argv[2] if len(sys.argv) > 2 else LY.get(int(round(R[0]['y'] / 100.0) * 100), None)
K = ('State', 'Class', 'DB', 'Prox', 'Graze', 'VnPrev', 'LastS', 'LastV', 'LastC', 'LastL', 'Count', 'LockT', 'ReachA', 'CapT'); K6 = ('Pend', 'Kind', 'Sup', 'Room', 'DBk', 'DSh', 'Flat', 'Sep', 'Since')
def g(r, k): return r['hook']['ct'][K.index(k)]
def g6(r, k): return r['hook']['ct6'][K6.index(k)]
def sp(r): return math.hypot(r['vx'], r['vy'])
CL = {0: '-', 1: 'wall', 2: 'waist', 3: 'knee', 4: 'chest', 5: 'low(trip)'}; LV = {0: 'impulse', 1: 'light', 2: 'stagger', 3: 'balance lost'}
ST = {0: 'normal', 3: 'blocked', 4: 'stagger', 5: 'kneeling down', 6: 'on one knee', 7: 'standing up', 8: 'falling forward', 9: 'lying', 10: 'getting up'}
print('%s lane %s frames %d fat %.2f seterr %s' % (lab, lane, len(R), R[len(R) // 2]['hook']['ctm'][3], R[5]['hook'].get('seterr')))
pc = g(R[0], 'Count'); ps = g(R[0], 'State'); vmax = 0; pp = g6(R[0], 'Pend')
for i, r in enumerate(R):
    vmax = max(vmax, sp(r))
    if g(r, 'Count') != pc:
        pc = g(r, 'Count')
        print('  t %6.2f %s v %3.0f cm/s class %s severity %.2f -> %s | support %s | rear room %.0f cm | object %s | speed 0.1 s before %.0f, after %.0f' % (
            r['t'], 'TRIP' if g6(r, 'Kind') == 2 else 'IMPACT', g(r, 'LastV'), CL[int(g(r, 'LastC'))], g(r, 'LastS'), LV[int(g(r, 'LastL'))], {0: 'none (airborne)', 1: 'left', 2: 'right'}[int(g6(r, 'Sup'))], g6(r, 'Room'), r['hook'].get('obj'), sp(R[max(i - 6, 0)]), sp(r)))
    if g(r, 'State') != ps or g6(r, 'Pend') != pp:
        print('  t %6.2f state %s -> %s%s (dist to surface %.0f)' % (r['t'], ST.get(int(ps), ps), ST.get(int(g(r, 'State')), g(r, 'State')), {1: ' [retreat step, kneel pending]', 2: ' [no room: standing brace]'}.get(int(g6(r, 'Pend')), ''), g(r, 'DB'))); ps = g(r, 'State'); pp = g6(r, 'Pend')
x0 = R[0]['x']; print('  capsule travel: start x %.0f, furthest %.0f, end %.0f | max speed %.0f | lowest pelvis (component z) %.1f | hand reach max %.2f' % (x0, max(r['x'] for r in R), R[-1]['x'], vmax, min(r['hook']['pv']['pelvis'][2] for r in R), max(r['hook']['ctm'][1] for r in R)))
if lane in BOX:
    RAD = {'knee': 6.0, 'shin': 5.0, 'foot': 4.0, 'ball': 3.5, 'pelvis': 11.0, 'hand': 3.5, 'elbow': 4.5, 'head': 9.0, 'thigh': 7.0}
    def pts(r):
        o = []; ub = r['ub']; u2 = r['ub2']
        for s in 'lr':
            kn = u2['calf_' + s]; ft = r['v_foot_' + s]; th = ub['thigh_' + s]
            o.append(('knee', kn)); o.append(('foot', ft)); o.append(('ball', ub['ball_' + s])); o.append(('hand', r['v_hand_' + s])); o.append(('elbow', u2['lowerarm_' + s]))
            for q in (0.25, 0.5, 0.75): o.append(('shin', [kn[k] + (ft[k] - kn[k]) * q for k in range(3)])); o.append(('thigh', [th[k] + (kn[k] - th[k]) * q for k in range(3)]))
        o.append(('pelvis', ub['pelvis'])); o.append(('head', r['v_head'])); return o
    worst = {}
    for r in R:
        for part, p in pts(r):
            for c, s in BOX[lane]:
                d = [abs(p[k] - c[k]) - s[k] / 2.0 for k in range(3)]
                sd = max(d) if max(d) < 0 else math.sqrt(sum(max(x, 0) ** 2 for x in d))
                dep = RAD[part] - sd
                if part in ('foot', 'ball') and p[2] - (c[2] + s[2] / 2.0) > -2.0 and abs(p[0] - c[0]) < s[0] / 2 + 6: continue      # standing ON the obstacle is not penetration
                if part == 'hand' and dep < RAD['hand'] + 1.5: continue                                                                # a hand resting on the surface is contact
                if dep > worst.get(part, (0, 0, 0))[0]: worst[part] = (dep, r['t'], g(r, 'State'))
    if worst: print('  PENETRATION (cm, limb surface inside the obstacle): ' + ' | '.join('%s %.1f at t %.2f (%s)' % (k_, v_[0], v_[1], ST.get(int(v_[2]), v_[2])) for k_, v_ in sorted(worst.items(), key=lambda x: -x[1][0])))
    else: print('  PENETRATION: none (no visible limb surface inside the obstacle)')
