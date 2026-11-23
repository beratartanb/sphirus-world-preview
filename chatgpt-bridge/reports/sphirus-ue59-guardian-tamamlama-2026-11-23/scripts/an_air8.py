# an_air8.py <label> ...: airtime from the CAPSULE and the floor under it (round 8; an_terr6 used a ground probe that missed stair blocks).
#  gap = capsule bottom (actor z - half height from the capsule floor sweep) above the floor hit under the capsule (row.gnd.cap); a frame is
#  airborne when the sweep has no walkable floor or the gap > 4 cm. Phases shorter than 0.05 s are dropped. Mesh world z is not used.
import json, sys, math
for lab in sys.argv[1:]:
    R = json.load(open('Saved/Codex/Grip_20261106/rec/' + lab + '.json'))['rows']; ph = []; cur = None; bad = 0
    for r in R:
        g = (r.get('gnd') or {}).get('cap')
        if not g: bad += 1; continue
        # a walking capsule on stairs rides the step edge while the centre probe still sees the lower step (gap up to one riser) and has
        # vz = 0 (walking mode); a falling / jumping capsule has vz != 0 except for the apex frame (bridged below)
        air = ((g[2] < 0.5) or (r['z'] - g[0] - g[1] > 4.0)) and abs(r.get('vz', 0.0)) > 15.0 if len(g) > 2 else False
        if air:
            if cur is None: cur = [r['t'], r['t'], r['x'], r['y'], 0.0]
            cur[1] = r['t']; cur[4] = max(cur[4], r['z'] - g[0] - g[1])
            cur_end = (r['x'], r['y'])
        elif cur: ph.append((cur, cur_end)); cur = None
    if cur: ph.append((cur, cur_end))
    mg = []
    for c, e in ph:
        if mg and c[0] - mg[-1][0][1] < 0.07: mg[-1][0][1] = c[1]; mg[-1][0][4] = max(mg[-1][0][4], c[4]); mg[-1] = (mg[-1][0], e)
        else: mg.append((c, e))
    ph = [(c, e) for c, e in mg if c[1] - c[0] >= 0.05]
    print('%s airborne phases %d (rows without floor data %d): %s' % (lab, len(ph), bad, [(round(c[0], 2), 'dur %.2f s' % (c[1] - c[0]), 'dist %.0f cm' % math.hypot(e[0] - c[2], e[1] - c[3]), 'max gap %.0f cm' % c[4]) for c, e in ph]))
