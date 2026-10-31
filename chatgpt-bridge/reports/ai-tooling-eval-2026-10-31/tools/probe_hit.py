"""probe_hit.py (measure, read-only): what a vertical Visibility trace hits first above the trail start points, and the landscape z there."""
import unreal as u, json

world = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
ifa = [a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors() if a.get_class().get_name() == 'InstancedFoliageActor']
out = []
for x, y in ((3074.0, -1692.0), (3104.8, -1886.0), (2984.7, -2458.9), (2654.1, -2958.1)):
    h = u.SystemLibrary.line_trace_single(world, u.Vector(x, y, 5000), u.Vector(x, y, -3000), u.TraceTypeQuery.TRACE_TYPE_QUERY1, True, [], u.DrawDebugTrace.NONE, True)
    t = h.to_tuple()
    comp = t[10]
    row = {'xy': [x, y], 'first_z': round(t[4].z, 1), 'actor': t[9].get_actor_label() if t[9] else None,
           'component': comp.get_name() if comp else None, 'mesh': (comp.get_editor_property('static_mesh').get_name() if comp and hasattr(comp, 'static_mesh') or (comp and comp.get_class().get_name().endswith('StaticMeshComponent')) else None),
           'item': t[13]}
    g = u.SystemLibrary.line_trace_single(world, u.Vector(x, y, 5000), u.Vector(x, y, -3000), u.TraceTypeQuery.TRACE_TYPE_QUERY1, True, ifa, u.DrawDebugTrace.NONE, True).to_tuple()
    row['ground_ignoring_foliage_z'] = round(g[4].z, 1) if g[0] else None
    row['ground_actor'] = g[9].get_actor_label() if g[0] and g[9] else None
    if comp and comp.get_class().get_name().endswith('InstancedStaticMeshComponent') and t[13] is not None and t[13] >= 0:
        tr = comp.get_instance_transform(t[13], True)
        row['instance_loc'] = [round(tr.translation.x, 1), round(tr.translation.y, 1), round(tr.translation.z, 1)]
        row['instance_scale'] = [round(tr.scale3d.x, 2), round(tr.scale3d.y, 2), round(tr.scale3d.z, 2)]
    out.append(row)
print('PROBE_HIT', json.dumps(out, default=str))
