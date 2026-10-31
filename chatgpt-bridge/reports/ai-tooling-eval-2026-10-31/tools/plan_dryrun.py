"""plan_dryrun.py (measure job, read-only): resolve plan_p1.json into exact instance transforms WITHOUT changing anything.
For every move: re-reads the live instance (component path + index), verifies mesh and location match the plan, samples the landscape
(foliage / other meshes ignored) at the old and new xy, keeps the instance's height offset above ground, keeps pitch/roll/scale, sets
the planned yaw, and lists conflicts (other instances >= 60 cm tall whose crowns would overlap the moved one by > 40 %).
Output: <PILOT>/plan_p1_resolved.json  (original + target transform per instance = the apply list AND the rollback list)
"""
import unreal as u, json, os, math

PILOT = r'C:\Users\berat\AppData\Local\Temp\claude\C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS\5f49a232-b001-47ad-8881-1eb04d9cb1c5\scratchpad\pilot'
plan = json.load(open(os.path.join(PILOT, 'plan_p1.json')))
env = json.load(open(os.path.join(PILOT, 'env_probe.json')))
world = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
actors = u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()
IFA = [a for a in actors if a.get_class().get_name() == 'InstancedFoliageActor']
comps = {c.get_path_name(): c for a in IFA for c in a.get_components_by_class(u.InstancedStaticMeshComponent)}


def ground(x, y):
    ign = list(IFA)
    for _ in range(10):
        t = u.SystemLibrary.line_trace_single(world, u.Vector(x, y, 6000), u.Vector(x, y, -3000), u.TraceTypeQuery.TRACE_TYPE_QUERY1, True, ign,
                                              u.DrawDebugTrace.NONE, True).to_tuple()
        if not t[0] or t[9] is None:
            return None
        if t[9].get_class().get_name() == 'Landscape':
            return t[4].z
        ign.append(t[9])
    return None


moved = {m['key'] for m in plan['moves']}
others = [i for i in env['instances'] if '%s|%d' % (i['comp'], i['idx']) not in moved and i['height_cm'] >= 60]
out = {'package': None, 'moves': [], 'problems': []}
for m in plan['moves']:
    c = comps.get(m['comp'])
    if c is None:
        out['problems'].append('component missing %s' % m['comp']); continue
    t = c.get_instance_transform(m['idx'], True)
    L, R, S = t.translation, t.rotation.rotator(), t.scale3d
    mesh = c.get_editor_property('static_mesh').get_name()
    ok = mesh == m['mesh'] and abs(L.x - m['from'][0]) < 2 and abs(L.y - m['from'][1]) < 2
    if not ok:
        out['problems'].append('mismatch %s idx %d (%s vs %s)' % (m['comp'], m['idx'], mesh, m['mesh'])); continue
    g0, g1 = ground(L.x, L.y), ground(m['to_xy'][0], m['to_xy'][1])
    off = (L.z - g0) if g0 is not None else 0.0
    z1 = (g1 + off) if g1 is not None else L.z
    conf = []
    for o in others:
        d = math.hypot(o['x'] - m['to_xy'][0], o['y'] - m['to_xy'][1]); rs = o['crown_r_cm'] + m['crown_r_cm']
        if rs > 0 and d < 0.6 * rs:
            conf.append({'mesh': o['mesh'], 'dist_cm': round(d, 1), 'overlap_ratio': round(1 - d / rs, 2)})
    out['package'] = c.get_outermost().get_name()
    out['moves'].append(dict(m, original={'loc': [L.x, L.y, L.z], 'rot_pyr': [R.pitch, R.yaw, R.roll], 'scale': [S.x, S.y, S.z]},
                             target={'loc': [m['to_xy'][0], m['to_xy'][1], round(z1, 2)], 'rot_pyr': [R.pitch, m['to_yaw'], R.roll], 'scale': [S.x, S.y, S.z]},
                             ground_from=g0, ground_to=g1, height_offset_cm=round(off, 1),
                             move_dist_cm=round(math.hypot(m['to_xy'][0] - L.x, m['to_xy'][1] - L.y), 1), conflicts=conf))
dirty = sorted(p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()) + sorted(p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_map_packages())
out['dirty_after'] = dirty
json.dump(out, open(os.path.join(PILOT, 'plan_p1_resolved.json'), 'w'), indent=1, default=str)
print('DRYRUN package %s moves %d problems %s dirty %s' % (out['package'], len(out['moves']), out['problems'], dirty))
for m in out['moves']:
    print('  %-18s %-26s move %6.0f cm  z %7.1f -> %7.1f  conflicts %d' % (m['group'], m['mesh'], m['move_dist_cm'], m['original']['loc'][2], m['target']['loc'][2], len(m['conflicts'])))
