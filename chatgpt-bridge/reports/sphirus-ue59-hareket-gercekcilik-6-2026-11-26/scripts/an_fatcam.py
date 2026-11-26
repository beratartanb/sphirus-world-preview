# an_fatcam.py <label>...: long-run fatigue + gameplay-camera speed feel. Per 1 s window: speed, motion Fat / E (tele f M.Fat, M.E if present),
# visible chest lean (spine_05 vs pelvis, deg), gameplay FOV, camera distance to the pawn (3D) and its behind / side split, and the camera's
# vertical jitter (std of the high-passed camera z, cm) as the shake measure.
import json, sys, math
for n in sys.argv[1:]:
    R = json.load(open('C:/Users/berat/Documents/Unreal Projects/sphirus_UE59/Saved/Codex/Grip_20261106/rec/%s.json' % n))['rows']; W = {}
    for i, r in enumerate(R):
        k = int(r['t']); e = W.setdefault(k, {'v': [], 'fat': [], 'fov': [], 'd': [], 'b': [], 's': [], 'cz': [], 'lean': []})
        e['v'].append(math.hypot(r['vx'], r['vy'])); f = (r['hook'].get('tele') or {}).get('f', {}) if isinstance(r['hook'].get('tele'), dict) else {}
        eff = r['hook'].get('eff'); e['fat'].append(eff[2] if eff else f.get('M.Fat', 0.0)); e['fov'].append(r['fov'])
        cx, cy, cz = r['cam'][:3]; dx, dy = cx - r['x'], cy - r['y']; yw = math.radians(r['yaw']); fx, fy = math.cos(yw), math.sin(yw)
        e['d'].append(math.dist((cx, cy, cz), (r['x'], r['y'], r['z']))); e['b'].append(-(dx * fx + dy * fy)); e['s'].append(-dx * fy + dy * fx)
        if 2 <= i < len(R) - 2: e['cz'].append(cz - sum(R[j]['cam'][2] for j in range(i - 2, i + 3)) / 5.0)
        p = r['hook'].get('pv')
        if isinstance(p, dict):
            a, b = p['pelvis'], p['spine_05']; h = math.hypot(b[0] - a[0], b[1] - a[1]); e['lean'].append(math.degrees(math.atan2(h, b[2] - a[2])))
    print('==', n)
    for k in sorted(W):
        e = W[k]; m = lambda x: sum(x) / len(x) if x else float('nan'); sd = math.sqrt(m([x * x for x in e['cz']])) if e['cz'] else float('nan')
        print('  t%3d v %4.0f fat %.2f lean %4.1f fov %4.1f dist %4.0f behind %4.0f side %4.0f shake %.2f' % (k, m(e['v']), m(e['fat']), m(e['lean']), m(e['fov']), m(e['d']), m(e['b']), m(e['s']), sd))
