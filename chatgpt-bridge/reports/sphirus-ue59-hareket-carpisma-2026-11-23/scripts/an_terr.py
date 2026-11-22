# an_terr.py <label>: terrain / air summary. Capsule height profile (start, max), speed on the climb, trunk lean (pelvis->spine_05 vs
# vertical, visible body) on flat vs on the climb, air time segments (capsule vz != 0 with no ground under the feet is approximated by
# |vz| > 60), largest one-frame vertical step of the visible pelvis in world space (stair pop check), clips used.
import json, sys, math
lab = sys.argv[1]; D = json.load(open('Saved/Codex/Grip_20261106/rec/' + lab + '.json')); R = D['rows'] if isinstance(D, dict) else D
R = [r for r in R if isinstance(r.get('hook'), dict) and r['hook'].get('pv')]
def sp(r): return math.hypot(r['vx'], r['vy'])
def lean(r):
    a = r['ub']['pelvis']; b = r['ub']['spine_05']; v = sp(r)
    if v < 30: return None
    dx = (b[0] - a[0]) * r['vx'] / v + (b[1] - a[1]) * r['vy'] / v; return math.degrees(math.atan2(dx, b[2] - a[2]))
z0 = R[0]['z']; zmax = max(r['z'] for r in R); up = [r for r in R if r['vz'] > 25 and sp(r) > 60]; fl = [r for r in R if abs(r['vz']) < 5 and sp(r) > 60 and abs(r['z'] - z0) < 3]
def mean(x): x = [y for y in x if y is not None]; return sum(x) / len(x) if x else float('nan')
air = []; i = 0
while i < len(R):
    if abs(R[i]['vz']) > 60:
        j = i
        while j < len(R) and abs(R[j]['vz']) > 20: j += 1
        air.append((R[i]['t'], R[j - 1]['t'] - R[i]['t'], max(r['z'] for r in R[i:j]) - R[i]['z'])); i = j
    else: i += 1
pz = [R[k]['ub']['pelvis'][2] - R[k - 1]['ub']['pelvis'][2] for k in range(1, len(R))]
cl = []
for r in R:
    c = str((r.get('gasp') or ['?'])[0])
    if not cl or cl[-1] != c: cl.append(c)
print('  terrain: capsule z %.0f -> max %.0f | climbing speed %.0f (n %d) | trunk lean flat %.1f deg, climbing %.1f deg | largest pelvis step/frame %.1f cm | air segments %s' % (
    z0, zmax, mean([sp(r) for r in up]), len(up), mean([lean(r) for r in fl]), mean([lean(r) for r in up]), max(abs(x) for x in pz), [(round(a, 2), round(b, 2), round(c)) for a, b, c in air][:6]))
print('  clips: ' + ' > '.join(x[-26:] for x in cl[:14]))
