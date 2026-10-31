"""contact_check.py (measure, read-only): ground contact of the P1 moved instances at their ORIGINAL and TARGET transforms.
For each move: the mesh bounds (local) are placed with the instance transform; along the longest horizontal local axis 9 points on the
mesh's lowest local z are compared with the landscape height (foliage and other meshes ignored):
  gap_cm = bottom - ground  (> 0 floating, < 0 buried).  For upright plants only the pivot-to-ground offset is reported as well.
Original vs target values are listed side by side, so a moved trunk can be judged against how it sat before.
Output: <PILOT>/contact_check.json"""
import unreal as u, json, os, math

PILOT = r'C:\Users\berat\AppData\Local\Temp\claude\C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS\5f49a232-b001-47ad-8881-1eb04d9cb1c5\scratchpad\pilot'
plan = json.load(open(os.path.join(PILOT, 'plan_p1_resolved.json')))
world = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
IFA = [a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors() if a.get_class().get_name() == 'InstancedFoliageActor']
meshes = {c.static_mesh.get_name(): c.static_mesh for a in IFA for c in a.get_components_by_class(u.InstancedStaticMeshComponent) if c.static_mesh}


def ground(x, y):
    ign = list(IFA)
    for _ in range(10):
        t = u.SystemLibrary.line_trace_single(world, u.Vector(x, y, 6000), u.Vector(x, y, -3000), u.TraceTypeQuery.TRACE_TYPE_QUERY1, True, ign, u.DrawDebugTrace.NONE, True).to_tuple()
        if not t[0] or t[9] is None:
            return None
        if t[9].get_class().get_name() == 'Landscape':
            return t[4].z
        ign.append(t[9])
    return None


def probe(mesh, d):
    b = mesh.get_bounds(); o, e = b.origin, b.box_extent
    T = u.Transform(location=u.Vector(*d['loc']), rotation=u.Rotator(pitch=d['rot_pyr'][0], yaw=d['rot_pyr'][1], roll=d['rot_pyr'][2]), scale=u.Vector(*d['scale']))
    long_x = e.x >= e.y
    pts = []
    for k in range(9):
        f = -1 + 2 * k / 8.0
        lp = u.Vector(o.x + (f * e.x if long_x else 0), o.y + (0 if long_x else f * e.y), o.z - e.z)
        wp = u.MathLibrary.transform_location(T, lp)
        g = ground(wp.x, wp.y)
        pts.append(None if g is None else round(wp.z - g, 1))
    gp = ground(d['loc'][0], d['loc'][1])
    v = [p for p in pts if p is not None]
    return {'gap_cm_along_long_axis': pts, 'min_gap': min(v) if v else None, 'max_gap': max(v) if v else None,
            'pivot_minus_ground_cm': None if gp is None else round(d['loc'][2] - gp, 1), 'long_axis_len_cm': round(2 * (e.x if long_x else e.y) * d['scale'][0], 1)}


out = []
for m in plan['moves']:
    if m['group'] == 'G4_lookback_window':
        continue
    mesh = meshes.get(m['mesh'])
    if not mesh:
        out.append({'mesh': m['mesh'], 'err': 'mesh not found'}); continue
    out.append({'group': m['group'], 'mesh': m['mesh'], 'original': probe(mesh, m['original']), 'target': probe(mesh, m['target'])})
json.dump(out, open(os.path.join(PILOT, 'contact_check.json'), 'w'), indent=1)
for r in out:
    if 'err' in r:
        print(r); continue
    o, t = r['original'], r['target']
    print('%-15s %-26s ORIG gap %6s..%6s pivot %6s | TARGET gap %6s..%6s pivot %6s  len %s' % (r['group'], r['mesh'], o['min_gap'], o['max_gap'], o['pivot_minus_ground_cm'],
                                                                                               t['min_gap'], t['max_gap'], t['pivot_minus_ground_cm'], t['long_axis_len_cm']))
