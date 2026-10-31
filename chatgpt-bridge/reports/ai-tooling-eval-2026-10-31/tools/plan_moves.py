"""plan_moves.py <env_probe.json> <out_plan.json> : composition pilot P1 - candidate instance moves on the authored rear trail (offline, no editor).

lat > 0 = RIGHT of travel = uphill (east) bank (verified: the near-camera pine at s 10 m / lat +172 is on the right in the frames).
Zones: approach s 0-5 m (kept unchanged - strongest part), compression s 5-11 m, release s 11-16.5 m.
Groups (each move keeps mesh, scale and yaw unless stated; z is resolved later on the landscape with the original height offset):
  G1 near-field   tall soft instances (h >= 150, no camera collision) whose crown edge is < 0.9 m from the trail centre in the
                  eye band -> pushed outward along the trail normal so the crown edge sits 1.0-1.2 m from the centre
                  (still part of the edge mass; no corridor clearing)
  G2 compression  uphill bank (right) gets weight: 2 young spruces from the far band (8-14 m, right) moved to 3.0-4.5 m at s 6.5-9 m,
                  and 1 existing dead pine trunk (collision mesh) from the far band laid along the bank at lat 2.6 m, s 7.5 m,
                  yaw = trail tangent + 12 deg (lead line toward the release)
  G3 tread edge   release (s 11-16.5): 6 low edge plants (ferns / ground cover) taken from the release mid band are set at 0.9-1.4 m
                  on alternating sides with 1.5-3 m gaps (irregular) -> the tread reads as the band between edge plants
  G4 lookback     young conifers that sit within +-7 deg of the release-station -> house sight line, 1.5-12 m away, are moved
                  1.8 m sideways (perpendicular to the sight line, away from it) -> a narrow window, not a clearing; only if the
                  terrain line of sight is open (env_probe: terrain never blocks the house from the segment)
"""
import sys, json, math

env = json.load(open(sys.argv[1])); OUTP = sys.argv[2]
TRAIL = [(1950, 2110), (2300, 1850), (2560, 1300), (2520, 750), (2580, 250), (2790, -250), (3010, -760), (2930, -1260),
         (3110, -1800), (3080, -2300), (2780, -2800), (2350, -3340)]
S0 = env['s0_on_trail_cm']
seg = [0.0]
for a, b in zip(TRAIL, TRAIL[1:]):
    seg.append(seg[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))


def frame(s):  # point, unit tangent, unit right-normal (lat > 0) at segment-relative arc s
    s = S0 + s
    for i in range(len(TRAIL) - 1):
        if s <= seg[i + 1] or i == len(TRAIL) - 2:
            L = seg[i + 1] - seg[i]; t = (s - seg[i]) / L; a, b = TRAIL[i], TRAIL[i + 1]
            tx, ty = (b[0] - a[0]) / L, (b[1] - a[1]) / L
            # right normal in UE top view (X north, Y east): rotate tangent +90 deg -> (-ty, tx)
            return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])), (tx, ty), (-ty, tx)


def at(s, lat):
    p, t, n = frame(s); return p[0] + n[0] * lat, p[1] + n[1] * lat


# sanity: the right normal must reproduce the probe's lat sign
chk = env['instances'][0]; p, t, n = frame(chk['s'])
sign_ok = ((chk['x'] - p[0]) * n[0] + (chk['y'] - p[1]) * n[1]) * chk['lat_cm'] >= 0
I = env['instances']
key = lambda i: '%s|%d' % (i['comp'], i['idx'])
soft = lambda i: not i['collision'].get('camera', '').startswith('ECR_BLOCK')
moves, used = [], set()


def add(i, x, y, grp, why, yaw=None):
    used.add(key(i))
    moves.append({'key': key(i), 'comp': i['comp'], 'idx': i['idx'], 'mesh': i['mesh'], 'group': grp, 'why': why,
                  'from': [i['x'], i['y'], i['z'], i['yaw']], 'to_xy': [round(x, 1), round(y, 1)], 'to_yaw': i['yaw'] if yaw is None else round(yaw, 1),
                  'scale': i['scale'], 's': i['s'], 'lat': i['lat_cm'], 'height_cm': i['height_cm'], 'crown_r_cm': i['crown_r_cm']})


# G1 near-field (all zones except approach is protected? approach kept unless a camera grazer exists there too)
for i in I:
    if soft(i) and i['height_cm'] >= 150 and 0 <= i['s'] <= 1650 and i['dist_cm'] - i['crown_r_cm'] < 90:
        side = 1 if i['lat_cm'] >= 0 else -1
        newlat = side * (i['crown_r_cm'] + 110)
        x, y = at(i['s'], newlat); add(i, x, y, 'G1_nearfield', 'crown edge %.0f cm from trail centre -> 110 cm' % (i['dist_cm'] - i['crown_r_cm']))
# G2 compression weight on the uphill bank
far_spruce = sorted([i for i in I if soft(i) and 'Spruce' in i['mesh'] and i['lat_cm'] > 800 and 300 <= i['s'] <= 1300 and key(i) not in used],
                    key=lambda i: -i['dist_cm'])[:2]
for i, (s, lat) in zip(far_spruce, ((680, 320), (860, 430))):
    x, y = at(s, lat); add(i, x, y, 'G2_compression', 'uphill bank pressure at s %.1f m' % (s / 100))
tgt = at(750, 260)
trunk = sorted([i for i in I if 'DeadTrunk' in i['mesh'] and 0 <= i['s'] <= 1650 and i['dist_cm'] > 600 and key(i) not in used],
               key=lambda i: math.hypot(i['x'] - tgt[0], i['y'] - tgt[1]))[:1]   # nearest trunk inside the pilot area (not one from elsewhere)
for i in trunk:
    p, t, n = frame(750); x, y = at(750, 260)
    add(i, x, y, 'G2_compression', 'dead trunk laid along the uphill bank as a lead line', yaw=math.degrees(math.atan2(t[1], t[0])) + 12)
# G3 tread-edge plants in the release zone
lows = [i for i in I if not soft(i) is False and i['height_cm'] < 90 and i['height_cm'] >= 25 and 1100 <= i['s'] <= 1650 and 350 <= i['dist_cm'] <= 900
        and ('Fern' in i['mesh'] or 'GroundCover' in i['mesh']) and key(i) not in used]
lows = sorted(lows, key=lambda i: i['dist_cm'], reverse=True)[:6]
slots = [(1150, 105), (1290, -120), (1380, 95), (1500, -100), (1560, 135), (1630, -130)]
for i, (s, lat) in zip(lows, slots):
    x, y = at(s, lat); add(i, x, y, 'G3_tread_edge', 'edge plant at s %.1f m lat %+.1f m' % (s / 100, lat / 100))
# G4 lookback window from the release station (s 14 m) toward the house
hb = env['lookback']['house_bounds']; hx, hy = (hb[0][0] + hb[1][0]) / 2, (hb[0][1] + hb[1][1]) / 2
st = at(1400, 0); bear = math.atan2(hy - st[1], hx - st[0])
win = []
for i in I:
    if not soft(i) or i['height_cm'] < 150 or key(i) in used:
        continue
    dx, dy = i['x'] - st[0], i['y'] - st[1]; d = math.hypot(dx, dy)
    if 150 <= d <= 1200:
        da = (math.degrees(math.atan2(dy, dx) - bear) + 540) % 360 - 180
        if abs(da) <= 7:
            win.append((d, da, i))
for d, da, i in sorted(win)[:3]:
    sgn = 1 if da >= 0 else -1; nx, ny = -math.sin(bear) * sgn, math.cos(bear) * sgn
    add(i, i['x'] + nx * 180, i['y'] + ny * 180, 'G4_lookback_window', 'on the house sight line (%.1f deg, %.1f m) -> 1.8 m aside' % (da, d / 100))
plan = {'sign_check_ok': sign_ok, 'segment_s0_cm': S0, 'release_station_xy': [round(st[0], 1), round(st[1], 1)], 'house_centre': [hx, hy],
        'house_bearing_deg': round(math.degrees(bear), 1), 'moves': moves,
        'counts': {g: sum(1 for m in moves if m['group'] == g) for g in ('G1_nearfield', 'G2_compression', 'G3_tread_edge', 'G4_lookback_window')}}
json.dump(plan, open(OUTP, 'w'), indent=1)
print('PLAN sign_ok', sign_ok, plan['counts'])
for m in moves:
    print('  %-18s %-26s s %5.0f lat %6.0f  (%7.1f,%8.1f) -> (%7.1f,%8.1f)  %s' % (m['group'], m['mesh'], m['s'], m['lat'], m['from'][0], m['from'][1], m['to_xy'][0], m['to_xy'][1], m['why']))
