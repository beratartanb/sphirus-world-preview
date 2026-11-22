# an_bob7.py <label> [tmin=1.5]: vertical bounce and lateral sway per steady plan segment, layer by layer.
#  capsule   : actor z (world)                                  -> must be flat on flat ground
#  driver    : driver mesh pelvis / head, COMPONENT space z      -> clip + GASP graph incl. FootPlacement pelvis offset
#  visible   : visible body pelvis / head, COMPONENT space z     -> + retarget + posture layer (Manny)
#  world     : visible pelvis / head WORLD z                     -> what a fixed diagnostic camera sees
#  camera    : camera location z and roll-free lateral           -> what the shoulder camera adds
# Per quantity: peak-to-peak (cm) and RMS around the segment mean; lateral = perpendicular to travel (cm); trunk roll p2p (deg, pelvis->neck
# against vertical in the frontal plane). Pelvis is only an approximate centre-of-mass indicator.
import json, sys, math
lab = sys.argv[1]; tmin = float(sys.argv[2]) if len(sys.argv) > 2 else 1.5
D = json.load(open('Saved/Codex/Grip_20261106/rec/' + lab + '.json')); plan = D.get('plan') or []; R = [r for r in D['rows'] if isinstance(r.get('hook'), dict) and r['hook'].get('pv')]
def pp(v): return max(v) - min(v) if v else 0
def rms(v):
    if not v: return 0
    m = sum(v) / len(v); return math.sqrt(sum((x - m) ** 2 for x in v) / len(v))
segs = {}
for r in R: segs.setdefault(r['s'], []).append(r)
print('#### %s (steady part, after %.1f s)  values: p2p / rms cm' % (lab, tmin))
print('seg  keys          v   | capsule z | driver pelvis z | visible pelvis z | world pelvis z | world head z | head-pelvis z | pelvis lat | head lat | trunk roll p2p | cam z  | cam lat')
for s, rr in sorted(segs.items()):
    W = [r for r in rr if r['t'] - rr[0]['t'] > tmin]
    if len(W) < 30: continue
    sp = sum(math.hypot(r['vx'], r['vy']) for r in W) / len(W)
    if sp < 20: continue
    lat = lambda r, p: ((p[0] - r['x']) * (-r['vy']) + (p[1] - r['y']) * r['vx']) / max(math.hypot(r['vx'], r['vy']), 1)
    q = {'cap': [r['z'] for r in W], 'dp': [r['hook']['pd']['pelvis'][2] for r in W], 'vp': [r['hook']['pv']['pelvis'][2] for r in W],
         'wp': [r['ub']['pelvis'][2] for r in W], 'wh': [r['v_head'][2] for r in W], 'hp': [r['v_head'][2] - r['ub']['pelvis'][2] for r in W],
         'pl': [lat(r, r['ub']['pelvis']) for r in W], 'hl': [lat(r, r['v_head']) for r in W], 'cz': [r['cam'][2] for r in W], 'cl': [lat(r, r['cam'][:3]) for r in W]}
    roll = []
    for r in W:
        p = r['ub']['pelvis']; n = r['ub']['neck_01']; v = max(math.hypot(r['vx'], r['vy']), 1); side = ((n[0] - p[0]) * (-r['vy']) + (n[1] - p[1]) * r['vx']) / v
        roll.append(math.degrees(math.atan2(side, n[2] - p[2])))
    f = lambda k: '%5.1f/%4.1f' % (pp(q[k]), rms(q[k]))
    print('s%-3d %-12s %4.0f | %s | %s     | %s      | %s    | %s  | %s   | %s | %s | %5.1f        | %s | %s' % (
        s, (plan[s][0] if s < len(plan) else '?').replace('LeftShift', 'Sh').replace('LeftControl', 'Ct')[:12], sp, f('cap'), f('dp'), f('vp'), f('wp'), f('wh'), f('hp'), f('pl'), f('hl'), pp(roll), f('cz'), f('cl')))
