"""inspect_probes226.py (editor job): V2.26 query-only inspection probes on the real R05 workshop masks.
Measured (v226t3 ins_ws, gaze telemetry): the gaze trace hits the west wall (Architecture_01_GROUND_G_West) at x ~42 while the masks sit at
x = 33 - the mask meshes are flush with / inside the wall's collision, so no visibility trace can ever reach them. Contract: each mask gets a
small SphereComponent (radius 20, QueryOnly, blocks ONLY the Visibility channel, ignores pawn / camera / everything else, tag GR_Inspect)
placed 25 cm in front of the mask toward the room. The gaze sphere trace hits the probe first; ComponentHasTag -> candidate; the focus
point stays the actor's bounds origin. No scene collision is changed; the probe cannot block the player (Pawn ignored) or the camera
(Camera ignored). Saves only the owning level package. Rollback: remove components tagged GR_Inspect (builtins.V226_PROBE_REMOVE).
builtins.V226_PROBE_SAVE saves (default dry). Prints PROBE226 {...}."""
import unreal as u, json, builtins
SAVE = bool(getattr(builtins, 'V226_PROBE_SAVE', False)); REMOVE = bool(getattr(builtins, 'V226_PROBE_REMOVE', False)); TAG = 'GR_Inspect'
OFFSET = float(getattr(builtins, 'V226_PROBE_OFFSET', 25.0)); RADIUS = float(getattr(builtins, 'V226_PROBE_RADIUS', 20.0))
LABELS = ['R05_Workshop_Mask_Silent', 'R05_Workshop_Mask_Gilded', 'R05_Workshop_Mask_Cerulean', 'R05_Workshop_Mask_Cracked']
ROOM = u.Vector(1.0, 0.0, 0.0)   # the masks hang on the west wall (x = 33); the room is toward +x
ELS = u.get_editor_subsystem(u.UnrealEditorSubsystem); assert ELS.get_game_world() is None, 'PIE running'
out = {'save': SAVE, 'remove': REMOVE, 'actors': {}}; levels = set()
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
    nm = a.get_actor_label()
    if nm not in LABELS: continue
    pkg = a.get_outer().get_outermost(); levels.add(pkg.get_name())
    have = [c for c in a.get_components_by_class(u.SphereComponent) if TAG in [str(t) for t in c.component_tags]]
    rec = {'level': pkg.get_name(), 'had': len(have)}
    if REMOVE:
        for c in have: a.modify(True); c.destroy_component(c)
        rec['removed'] = len(have)
    elif not have:
        a.modify(True)
        sds = u.get_engine_subsystem(u.SubobjectDataSubsystem); handles = sds.k2_gather_subobject_data_for_instance(a)
        root_h = None
        for h in handles:
            obj_ = u.SubobjectDataBlueprintFunctionLibrary.get_object(sds.k2_find_subobject_data_from_handle(h))
            if obj_ and obj_ == a.get_editor_property('root_component'): root_h = h
        if root_h is None: root_h = handles[0]
        params = u.AddNewSubobjectParams(parent_handle=root_h, new_class=u.SphereComponent, blueprint_context=None)
        nh, fail = sds.add_new_subobject(params)
        assert not str(fail), ('add_new_subobject', str(fail))
        c = u.SubobjectDataBlueprintFunctionLibrary.get_object(sds.k2_find_subobject_data_from_handle(nh))
        assert isinstance(c, u.SphereComponent), type(c)
        c.set_sphere_radius(RADIUS, False)
        c.set_world_location(a.get_actor_location() + ROOM * OFFSET, False, False)
        c.set_collision_enabled(u.CollisionEnabled.QUERY_ONLY)
        c.set_collision_object_type(u.CollisionChannel.ECC_WORLD_DYNAMIC)
        c.set_collision_response_to_all_channels(u.CollisionResponseType.ECR_IGNORE)
        c.set_collision_response_to_channel(u.CollisionChannel.ECC_VISIBILITY, u.CollisionResponseType.ECR_BLOCK)
        c.set_editor_property('component_tags', [u.Name(TAG)])
        c.set_editor_property('hidden_in_game', True)
        rec['added'] = c.get_name()
    probes = [c for c in a.get_components_by_class(u.SphereComponent) if TAG in [str(t) for t in c.component_tags]]
    rec['probes'] = [{'name': c.get_name(), 'loc': [round(v, 1) for v in (c.get_world_location().x, c.get_world_location().y, c.get_world_location().z)], 'r': c.get_scaled_sphere_radius(),
                      'vis': str(c.get_collision_response_to_channel(u.CollisionChannel.ECC_VISIBILITY)).split('.')[-1], 'pawn': str(c.get_collision_response_to_channel(u.CollisionChannel.ECC_PAWN)).split('.')[-1],
                      'cam': str(c.get_collision_response_to_channel(u.CollisionChannel.ECC_CAMERA)).split('.')[-1]} for c in probes]
    out['actors'][nm] = rec
out['found'] = len(out['actors']); out['levels'] = sorted(levels)
if SAVE and out['found'] == 4:
    out['saved'] = [[p_, bool(u.EditorLoadingAndSavingUtils.save_packages([u.load_package(p_)], False))] for p_ in sorted(levels)]
    out['dirty_after'] = [p_.get_name() for p_ in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('PROBE226 ' + json.dumps(out, default=str))
