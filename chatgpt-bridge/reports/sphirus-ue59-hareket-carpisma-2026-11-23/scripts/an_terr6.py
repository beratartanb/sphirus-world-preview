# an_terr6.py <label>: terrain / air summary, round 6 (fixes of an_terr.py: a walking capsule has vz = 0 on stairs and ramps, so "climbing"
# is now taken from the capsule height change over 0.2 s; air time comes from the real gap between the capsule bottom and the ground
# under it (> 6 cm) instead of |vz| pieces).
#  per phase (flat / climbing / descending): speed, trunk lean (pelvis->spine_05 against vertical along travel), visible pelvis height above
#  the LOWER foot and above the HIGHER foot (cm; standing = ~90), smallest knee angle (thigh-calf-foot, deg; standing ~170), largest
#  one-frame vertical pelvis step in world space.  air: list of (start, duration, horizontal distance, max rise).
import json, sys, math
lab = sys.argv[1]; D = json.load(open('Saved/Codex/Grip_20261106/rec/' + lab + '.json')); R = D['rows'] if isinstance(D, dict) else D
R = [r for r in R if isinstance(r.get('hook'), dict) and r['hook'].get('pv')]
def sp(r): return math.hypot(r['vx'], r['vy'])
def ang(a, b, c):
    u = [a[i] - b[i] for i in range(3)]; v = [c[i] - b[i] for i in range(3)]; d = sum(u[i] * v[i] for i in range(3)); n = math.sqrt(sum(x * x for x in u) * sum(x * x for x in v)) or 1
    return math.degrees(math.acos(max(-1, min(1, d / n))))
def lean(r):
    a = r['ub']['pelvis']; b = r['ub']['spine_05']; v = sp(r)
    if v < 30: return None
    return math.degrees(math.atan2((b[0] - a[0]) * r['vx'] / v + (b[1] - a[1]) * r['vy'] / v, b[2] - a[2]))
PH = {'flat': [], 'climbing': [], 'descending': []}
for i, r in enumerate(R):
    j = i
    while j < len(R) - 1 and R[j]['t'] - r['t'] < 0.2: j += 1
    dz = (R[j]['z'] - r['z']) / max(R[j]['t'] - r['t'], 1e-3)
    if sp(r) < 60: continue
    PH['climbing' if dz > 20 else ('descending' if dz < -20 else 'flat')].append(r)
print('%s frames %d capsule z %.0f -> max %.0f' % (lab, len(R), R[0]['z'], max(r['z'] for r in R)))
for k, W in PH.items():
    if len(W) < 10: print('  %-10s n %d' % (k, len(W))); continue
    L = [x for x in (lean(r) for r in W) if x is not None]; lo = []; hi = []; kn = []
    for r in W:
        pv = r['hook']['pv']; fz = (pv['foot_l'][2], pv['foot_r'][2]); lo.append(pv['pelvis'][2] - min(fz)); hi.append(pv['pelvis'][2] - max(fz))
        for s in 'lr': kn.append(ang(pv['thigh_' + s], pv['calf_' + s], pv['foot_' + s]))
    kn.sort(); lo.sort(); hi.sort()
    print('  %-10s n %4d | speed %3.0f | trunk lean %5.1f | pelvis above lower foot mean %5.1f min %5.1f, above higher foot mean %5.1f min %5.1f | knee angle min %5.1f p05 %5.1f' % (
        k, len(W), sum(sp(r) for r in W) / len(W), sum(L) / max(len(L), 1), sum(lo) / len(lo), lo[0], sum(hi) / len(hi), hi[0], kn[0], kn[int(0.05 * len(kn))]))
st = max(abs(R[i]['ub']['pelvis'][2] - R[i - 1]['ub']['pelvis'][2]) for i in range(1, len(R)))
air = []; i = 0
def gap(r):
    g = r['gnd'].get('mz'); return g[0] if g else 0.0
while i < len(R):
    if gap(R[i]) > 6:
        j = i
        while j < len(R) and gap(R[j]) > 6: j += 1
        if R[j - 1]['t'] - R[i]['t'] > 0.05: air.append((round(R[i]['t'], 2), round(R[j - 1]['t'] - R[i]['t'], 2), round(math.hypot(R[j - 1]['x'] - R[i]['x'], R[j - 1]['y'] - R[i]['y'])), round(max(gap(R[q]) for q in range(i, j)))))
        i = j
    else: i += 1
print('  largest pelvis step/frame %.1f cm | air (start s, duration s, distance cm, max gap cm): %s' % (st, air[:8]))
