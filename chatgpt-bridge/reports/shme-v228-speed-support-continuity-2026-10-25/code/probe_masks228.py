"""probe_masks228.py (editor job, READ-ONLY): the inspectable mask actors (tag GR_Inspect on the actor or a component): actor label /
object name, actor location (pivot), GetActorBounds origin with all components and with colliding components only, the static mesh
component bounds origin, the probe sphere component (tag GR_Inspect) world location and radius, and the vector probe -> mesh origin. Tells
whether the V2.26 focus (actor bounds origin) is shifted by the probe and what an explicit focus point should be. Prints MASKS228."""
import unreal as u, json
out = []
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
    comps = a.get_components_by_class(u.ActorComponent)
    probes = [c for c in comps if c.component_has_tag('GR_Inspect')]
    if not (a.actor_has_tag('GR_Inspect') or probes): continue
    d = {'label': a.get_actor_label(), 'name': a.get_name(), 'actor_tag': bool(a.actor_has_tag('GR_Inspect')), 'loc': [round(x, 1) for x in a.get_actor_location().to_tuple()]}
    o, e = a.get_actor_bounds(False, False); d['bounds_all'] = [round(x, 1) for x in o.to_tuple()]; d['ext_all'] = [round(x, 1) for x in e.to_tuple()]
    o2, e2 = a.get_actor_bounds(True, False); d['bounds_colliding'] = [round(x, 1) for x in o2.to_tuple()]
    meshes = [c for c in comps if isinstance(c, u.StaticMeshComponent)]
    if meshes:
        mo, me, mr = u.SystemLibrary.get_component_bounds(meshes[0]); d['mesh_bounds_origin'] = [round(x, 1) for x in mo.to_tuple()]; d['mesh_ext'] = [round(x, 1) for x in me.to_tuple()]
        d['mesh_comp_loc'] = [round(x, 1) for x in meshes[0].get_world_location().to_tuple()]
    for c in probes:
        pd = {'class': c.get_class().get_name(), 'loc': [round(x, 1) for x in c.get_world_location().to_tuple()]}
        try: pd['radius'] = float(c.get_unscaled_sphere_radius())
        except Exception: pass
        try: pd['collision_enabled'] = str(c.get_collision_enabled())
        except Exception: pass
        if meshes:
            mo = u.SystemLibrary.get_component_bounds(meshes[0])[0]; pl = c.get_world_location(); pd['probe_to_mesh'] = [round(mo.x - pl.x, 1), round(mo.y - pl.y, 1), round(mo.z - pl.z, 1)]
        d.setdefault('probes', []).append(pd)
    out.append(d)
print('MASKS228 ' + json.dumps(out, default=str))
