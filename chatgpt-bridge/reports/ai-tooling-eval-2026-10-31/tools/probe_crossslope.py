"""probe_crossslope.py (measure, read-only): fine cross-slope check of the authored trail around the segment end (s 15.0-17.5 m)
and at the other extremes (s 0.5 and 11.5 m). Landscape height only (foliage and other meshes ignored, iterative ignore).
For each s: cross slope over +-0.5 / +-0.75 / +-1.0 m, the left and right heights relative to the centre, and which polyline
segment s lies on (a vertex of TRAIL is at the segment end -> the tangent turns there).
Output: <PILOT>/crossslope_fine.json"""
import unreal as u, json, os, math

PILOT = r'C:\Users\berat\AppData\Local\Temp\claude\C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS\5f49a232-b001-47ad-8881-1eb04d9cb1c5\scratchpad\pilot'
TRAIL = [(1950, 2110), (2300, 1850), (2560, 1300), (2520, 750), (2580, 250), (2790, -250), (3010, -760), (2930, -1260),
         (3110, -1800), (3080, -2300), (2780, -2800), (2350, -3340)]
S0 = 4159.0
world = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
IFA = [a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors() if a.get_class().get_name() == 'InstancedFoliageActor']
seg = [0.0]
for a, b in zip(TRAIL, TRAIL[1:]):
    seg.append(seg[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))


def ground(x, y):
    ign = list(IFA)
    for _ in range(10):
        t = u.SystemLibrary.line_trace_single(world, u.Vector(x, y, 6000), u.Vector(x, y, -3000), u.TraceTypeQuery.TRACE_TYPE_QUERY1, True, ign,
                                              u.DrawDebugTrace.NONE, True).to_tuple()
        if not t[0] or t[9] is None:
            return None, None
        if t[9].get_class().get_name() == 'Landscape':
            return t[4].z, t[9].get_actor_label()
        ign.append(t[9])
    return None, None


def frame(s):
    s = S0 + s
    for i in range(len(TRAIL) - 1):
        if s <= seg[i + 1] or i == len(TRAIL) - 2:
            L = seg[i + 1] - seg[i]; t = (s - seg[i]) / L; a, b = TRAIL[i], TRAIL[i + 1]
            return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])), ((b[0] - a[0]) / L, (b[1] - a[1]) / L), i, round(seg[i + 1] - S0, 1)


rows = []
for s in [50.0, 1150.0] + [1500.0 + 25.0 * k for k in range(0, 11)]:
    (x, y), (tx, ty), si, vert = frame(s)
    nx, ny = -ty, tx   # right normal (lat > 0 = right of travel)
    zc, _ = ground(x, y)
    r = {'s_cm': s, 'xy': [round(x, 1), round(y, 1)], 'segment_index': si, 'next_vertex_at_s_cm': vert, 'z_centre': zc}
    for h in (50, 75, 100):
        zr, _ = ground(x + nx * h, y + ny * h); zl, _ = ground(x - nx * h, y - ny * h)
        if None not in (zr, zl, zc):
            r['cross_deg_%dcm' % h] = round(math.degrees(math.atan2(zr - zl, 2 * h)), 1)   # > 0: right (uphill) side higher
            r['right_minus_centre_%dcm' % h] = round(zr - zc, 1); r['left_minus_centre_%dcm' % h] = round(zl - zc, 1)
    rows.append(r)
json.dump({'note': 'cross_deg > 0 = right side (lat > 0) higher; env_probe used (left - right) with its own left/right naming', 'rows': rows},
          open(os.path.join(PILOT, 'crossslope_fine.json'), 'w'), indent=1)
for r in rows:
    print('s %6.0f seg %d vertex@%7.1f  cross50 %5s cross75 %5s cross100 %5s  R-C75 %6s L-C75 %6s' % (r['s_cm'], r['segment_index'], r['next_vertex_at_s_cm'],
          r.get('cross_deg_50cm'), r.get('cross_deg_75cm'), r.get('cross_deg_100cm'), r.get('right_minus_centre_75cm'), r.get('left_minus_centre_75cm')))
