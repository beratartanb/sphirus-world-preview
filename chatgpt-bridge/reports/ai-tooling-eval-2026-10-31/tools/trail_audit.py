"""trail_audit.py (measure job, read-only): what occupies the walk line of the rear-trail pilot segment.
Samples the pass-A pawn track of walk2 every ~1 m and, in the EDITOR world, counts instanced (foliage / HISM / ISM) instances whose
origin is within 0.8 m / 1.5 m / 3.0 m (2D) of the track, grouped by component mesh and owner; lists static-mesh actors within 3 m;
and samples the landscape height along the track (walkable slope). Also counts instances in a 3-12 m band either side (mid-ground).
Nothing is selected, edited or saved. Output: <OUT>/trail_audit.json
"""
import unreal as u, json, os, math

W2 = r'C:\Users\berat\AppData\Local\Temp\claude\C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS\5f49a232-b001-47ad-8881-1eb04d9cb1c5\scratchpad\walk2'
log = json.load(open(os.path.join(W2, 'walk_log.json')))
track = [t['pawn'] for t in log['passA']['ticks']]
pts = [track[0]]
for p in track[1:]:
    if math.hypot(p[0] - pts[-1][0], p[1] - pts[-1][1]) >= 100:
        pts.append(p)
A = u.get_editor_subsystem(u.EditorActorSubsystem)
world = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
xs, ys = [p[0] for p in pts], [p[1] for p in pts]
bb = (min(xs) - 1300, max(xs) + 1300, min(ys) - 1300, max(ys) + 1300)


def dist2(x, y):
    best = 1e18
    for i in range(len(pts) - 1):
        ax, ay, bx, by = pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1]
        dx, dy = bx - ax, by - ay; L = dx * dx + dy * dy
        t = max(0.0, min(1.0, ((x - ax) * dx + (y - ay) * dy) / L)) if L > 0 else 0.0
        best = min(best, (ax + t * dx - x) ** 2 + (ay + t * dy - y) ** 2)
    return math.sqrt(best)


bands = {'0.8m': 80, '1.5m': 150, '3m': 300}
inst, mid, actors = {}, {}, []
for a in A.get_all_level_actors():
    for c in a.get_components_by_class(u.InstancedStaticMeshComponent):
        m = c.get_editor_property('static_mesh')
        key = '%s | %s' % (m.get_name() if m else None, a.get_actor_label())
        n = c.get_instance_count()
        if n == 0:
            continue
        for i in range(n):
            t = c.get_instance_transform(i, True)
            x, y = t.translation.x, t.translation.y
            if not (bb[0] < x < bb[1] and bb[2] < y < bb[3]):
                continue
            d = dist2(x, y)
            s = max(t.scale3d.x, t.scale3d.y, t.scale3d.z)
            for bn, r in bands.items():
                if d <= r:
                    inst.setdefault(key, {b: 0 for b in bands}); inst[key][bn] += 1
            if 300 < d <= 1200:
                mid[key] = mid.get(key, 0) + 1
    if a.get_components_by_class(u.StaticMeshComponent) and not a.get_components_by_class(u.InstancedStaticMeshComponent):
        o = a.get_actor_location()
        if bb[0] < o.x < bb[1] and bb[2] < o.y < bb[3]:
            d = dist2(o.x, o.y)
            if d <= 300:
                smc = a.get_components_by_class(u.StaticMeshComponent)[0]; m = smc.get_editor_property('static_mesh')
                actors.append({'label': a.get_actor_label(), 'mesh': m.get_name() if m else None, 'dist_cm': round(d, 1),
                               'level': a.get_level().get_outer().get_name() if a.get_level() else None})
heights = []
for p in pts:
    h = u.SystemLibrary.line_trace_single(world, u.Vector(p[0], p[1], p[2] + 2000), u.Vector(p[0], p[1], p[2] - 2000), u.TraceTypeQuery.TRACE_TYPE_QUERY1,
                                          False, [], u.DrawDebugTrace.NONE, True)
    hr = h.to_tuple() if h else None
    heights.append(round(hr[4].z, 1) if hr and hr[0] else None)
slopes = []
for i in range(len(pts) - 1):
    if heights[i] is not None and heights[i + 1] is not None:
        run = math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
        slopes.append(round(math.degrees(math.atan2(heights[i + 1] - heights[i], run)), 1))
res = {'track_points_1m': pts, 'track_length_m': round(sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)) / 100, 1),
       'instances_near_track': dict(sorted(inst.items(), key=lambda kv: -kv[1]['1.5m'])), 'midground_3_12m': dict(sorted(mid.items(), key=lambda kv: -kv[1])),
       'static_mesh_actors_within_3m': sorted(actors, key=lambda r: r['dist_cm']), 'ground_z': heights, 'slope_deg_per_m': slopes}
json.dump(res, open(os.path.join(W2, 'trail_audit.json'), 'w'), indent=1)
print('TRAIL_AUDIT length %.1f m, instance groups near track %d, actors within 3 m %d, slope max %s' % (res['track_length_m'], len(inst), len(actors), max(slopes) if slopes else None))
for k, v in list(res['instances_near_track'].items())[:15]:
    print('  ', v, k)
