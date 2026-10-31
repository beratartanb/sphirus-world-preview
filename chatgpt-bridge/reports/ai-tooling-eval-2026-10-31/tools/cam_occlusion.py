"""cam_occlusion.py <env_probe.json> <trailwalk_log.json> <out.json> [moves.json] : per-frame camera / body vs foliage proxy (numpy-free).

For every pass-A frame: the camera position (from the PIE log) is tested against every NO-collision instance taller than 80 cm:
  inside  = horizontal distance < 0.85 x crown radius and camera z between instance base and base + height   (lens inside the crown)
  graze   = horizontal distance < crown radius + 35 cm (foliage fills the near field)
The pawn path is tested the same way for the body ('body_inside' = pawn within 0.6 x crown radius of a tall instance).
Crown radius / height come from mesh bounds x instance scale (an over-estimate for sparse young pines; treated as a proxy).
Optional moves.json = {"comp|idx": [x, y, z, yaw, sx, sy, sz]} replaces instance transforms -> the same camera track re-evaluated
(prediction only: in-game the camera track itself would also change slightly).
"""
import sys, json, math

env = json.load(open(sys.argv[1])); log = json.load(open(sys.argv[2])); OUTP = sys.argv[3]
moves = json.load(open(sys.argv[4])) if len(sys.argv) > 4 else {}
inst = []
for i in env['instances']:
    if i['collision'].get('camera', '').startswith('ECR_BLOCK') or i['height_cm'] < 80:
        continue
    k = '%s|%d' % (i['comp'], i['idx'])
    j = dict(i)
    if k in moves:
        m = moves[k]; j['x'], j['y'], j['z'] = m[0], m[1], m[2]
    inst.append((k, j))
ticks = log['passA']['ticks']
frames, culprits = [], {}
for t in ticks:
    cx, cy, cz = t['cam']; px, py, pz = t['pawn']
    ins, gr, body = [], [], []
    for k, j in inst:
        d = math.hypot(cx - j['x'], cy - j['y'])
        if d < 0.85 * j['crown_r_cm'] and j['z'] - 20 <= cz <= j['z'] + j['height_cm']:
            ins.append(k)
        elif d < j['crown_r_cm'] + 35 and j['z'] - 20 <= cz <= j['z'] + j['height_cm'] + 30:
            gr.append(k)
        if math.hypot(px - j['x'], py - j['y']) < 0.6 * j['crown_r_cm'] and j['height_cm'] > 120:
            body.append(k)
    for k in ins + gr:
        culprits[k] = culprits.get(k, 0) + 1
    frames.append({'game': t['game'], 's_cm': t['s_cm'], 'inside': ins, 'graze': gr, 'body_inside': body})
byk = {k: j for k, j in inst}
res = {'frames_total': len(frames), 'frames_inside': sum(1 for f in frames if f['inside']), 'frames_graze_only': sum(1 for f in frames if f['graze'] and not f['inside']),
       'frames_body_inside': sum(1 for f in frames if f['body_inside']),
       'inside_windows_s': [], 'culprits': sorted([{'key': k, 'frames': n, 'mesh': byk[k]['mesh'], 's': byk[k]['s'], 'lat_cm': byk[k]['lat_cm'],
                                                    'height_cm': byk[k]['height_cm'], 'crown_r_cm': byk[k]['crown_r_cm'], 'x': byk[k]['x'], 'y': byk[k]['y']}
                                                   for k, n in culprits.items()], key=lambda r: -r['frames']), 'frames': frames, 'moves_applied': len(moves)}
w = None
for f in frames:
    if f['inside'] and w is None:
        w = [f['game'], f['game']]
    elif f['inside']:
        w[1] = f['game']
    elif w:
        res['inside_windows_s'].append([round(w[0], 2), round(w[1], 2)]); w = None
if w:
    res['inside_windows_s'].append([round(w[0], 2), round(w[1], 2)])
json.dump(res, open(OUTP, 'w'), indent=1)
print('CAM_OCC frames %d inside %d graze-only %d body-inside %d windows %s' % (res['frames_total'], res['frames_inside'], res['frames_graze_only'], res['frames_body_inside'], res['inside_windows_s']))
for c in res['culprits'][:12]:
    print('  %4d fr  %-26s s %6.0f lat %6.0f h %5.0f r %5.0f' % (c['frames'], c['mesh'], c['s'], c['lat_cm'], c['height_cm'], c['crown_r_cm']))
