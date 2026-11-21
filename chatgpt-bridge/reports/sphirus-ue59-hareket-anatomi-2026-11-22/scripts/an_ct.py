# an_ct.py <label>: contact log summary. Per event (impact counter change or state change): time, speed before, class, severity, level,
# state timeline; plus anticipation (speed vs distance to the surface), hand reach envelope, speed cap and arrival speed.
import json, sys, math
lab = sys.argv[1]; D = json.load(open('Saved/Codex/Grip_20261106/rec/' + lab + '.json')); R0 = D['rows'] if isinstance(D, dict) else D
R = [r for r in R0 if isinstance(r.get('hook'), dict) and r['hook'].get('ct')]
if not R:
    print(lab, 'no ct data', [(r.get('hook') or {}).get('cterr') for r in R0[5:6]]); sys.exit(0)
K = ('State', 'Class', 'DB', 'Prox', 'Graze', 'VnPrev', 'LastS', 'LastV', 'LastC', 'LastL', 'Count', 'LockT', 'ReachA', 'CapT')
def g(r, k): return r['hook']['ct'][K.index(k)]
def sp(r): return math.hypot(r['vx'], r['vy'])
print('%s scene %s frames %d' % (lab, R[0]['hook'].get('scene'), len(R)))
CL = {0: '-', 1: 'wall', 2: 'waist', 3: 'knee', 4: 'chest'}; LV = {0: 'impulse', 1: 'blocked', 2: 'stagger', 3: 'down'}
ST = {0: 'normal', 3: 'blocked', 4: 'stagger', 5: 'kneeling', 6: 'down', 7: 'standing up'}
pc = g(R[0], 'Count'); ps = g(R[0], 'State'); vmax = 0; first = None
for i, r in enumerate(R):
    vmax = max(vmax, sp(r))
    if g(r, 'DB') < 200 and first is None and sp(r) > 60: first = i
    if g(r, 'Count') != pc:
        pc = g(r, 'Count')
        print('  t %6.2f IMPACT v %3.0f cm/s class %s severity %.2f -> %s | fat %.2f | speed 0.1 s before %.0f, after %.0f' % (
            r['t'], g(r, 'LastV'), CL[int(g(r, 'LastC'))], g(r, 'LastS'), LV[int(g(r, 'LastL'))], r['hook']['ctm'][3], sp(R[max(i - 6, 0)]), sp(r)))
    if g(r, 'State') != ps:
        print('  t %6.2f state %s -> %s (lock %.2f s)' % (r['t'], ST.get(int(ps), ps), ST.get(int(g(r, 'State')), g(r, 'State')), g(r, 'LockT'))); ps = g(r, 'State')
if first is not None:
    print('  approach: ' + ' | '.join('d %3.0f v %3.0f cap %s reach %.2f' % (g(r, 'DB'), sp(r), ('%.0f' % r['hook']['ctm'][0]) if r['hook']['ctm'][0] < 9000 else '-', r['hook']['ctm'][1]) for r in R[first::8][:14]))
gz = [r for r in R if g(r, 'Graze') > 0.5]
if gz:
    print('  graze: %.2f s, speed %.0f -> %.0f, reach max %.2f, roll lean (PS_LR) %.1f..%.1f' % (len(gz) / 60.0, sp(gz[0]), sp(gz[-1]), max(r['hook']['ctm'][1] for r in gz), min(r['hook']['ps'][20] for r in gz), max(r['hook']['ps'][20] for r in gz)))
mz = min(r['hook']['pv']['pelvis'][2] for r in R)
print('  max speed %.0f, lowest pelvis (component z) %.1f, max trunk impulse lean PS_LP %.1f / PS_LR %.1f' % (vmax, mz, max(abs(r['hook']['ps'][19]) for r in R), max(abs(r['hook']['ps'][20]) for r in R)))
