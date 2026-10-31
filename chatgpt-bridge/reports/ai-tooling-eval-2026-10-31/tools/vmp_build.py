"""vmp_build.py (WRITE job under a manifest; NEVER saves): build / remove the Environment Visual Master Pass trial in memory.
builtins.VMP_MODE in {'build', 'remove'}; spec = <VMP>/trial_spec.json (generated offline by vmp_spec.py).
build : spawns StaticMeshActors and DecalActors from EXISTING project assets into the persistent level, label prefix 'VMP_', folder
        'VMP_Trial'. Each item: mesh/decal, trail-frame position already resolved to world xy, z = landscape (foliage and other meshes
        ignored) + item 'dz' (negative = sunk into the ground), yaw/pitch/roll, scale. Decals project along the -slope normal (box depth <= 30 cm); see the v2 note in the body.
remove: destroys every actor whose label starts with 'VMP_'. Production actors and foliage are never touched by this job.
Output: <VMP>/build_<mode>.json"""
import unreal as u, json, os, builtins, math

VMP = r'C:\Users\berat\AppData\Local\Temp\claude\C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS\5f49a232-b001-47ad-8881-1eb04d9cb1c5\scratchpad\vmp'
MODE = getattr(builtins, 'VMP_MODE')
E = u.get_editor_subsystem(u.UnrealEditorSubsystem); assert E.get_game_world() is None, 'PIE running'
AS = u.get_editor_subsystem(u.EditorActorSubsystem)
world = E.get_editor_world()
actors = AS.get_all_level_actors()
res = {'mode': MODE, 'spawned': [], 'removed': 0, 'problems': []}
if MODE == 'remove':
    vm = [a for a in actors if a.get_actor_label().startswith('VMP_')]
    for a in vm:
        AS.destroy_actor(a)
    res['removed'] = len(vm)
else:
    assert not any(a.get_actor_label().startswith('VMP_') for a in actors), 'trial already built - remove first'
    spec = json.load(open(os.path.join(VMP, getattr(builtins, 'VMP_SPEC', 'trial_spec.json'))))
    IFA = [a for a in actors if a.get_class().get_name() == 'InstancedFoliageActor']

    def ground(x, y):
        ign = list(IFA)
        for _ in range(12):
            t = u.SystemLibrary.line_trace_single(world, u.Vector(x, y, 6000), u.Vector(x, y, -3000), u.TraceTypeQuery.TRACE_TYPE_QUERY1, True, ign, u.DrawDebugTrace.NONE, True).to_tuple()
            if not t[0] or t[9] is None:
                return None
            if t[9].get_class().get_name() == 'Landscape':
                return t[4].z
            ign.append(t[9])
        return None

    def normal(x, y, d=45.0):
        zx0, zx1, zy0, zy1 = ground(x - d, y), ground(x + d, y), ground(x, y - d), ground(x, y + d)
        if None in (zx0, zx1, zy0, zy1):
            return u.Vector(0, 0, 1)
        n = u.Vector(-(zx1 - zx0) / (2 * d), -(zy1 - zy0) / (2 * d), 1.0)
        return n.normal()

    # v2 (after the TRIAL2 look check): flat props (root patches, mossy roots, branches, small stones) follow the slope instead of
    # hovering on the downhill edge; decals project along the slope normal with a short box so they stop painting existing rocks;
    # soft props get no collision like the native soft foliage (the GR camera probes also read Visibility, so 'ignore Camera' alone
    # still pulled the boom in behind trial ferns); hard props (rocks, trunk, stump) keep collision and only ignore the Camera channel.
    SOFT = ('SM_Fern', 'SM_DeadBranch', 'SM_SmallStones', 'tkwqbbofa', 'wgxjfhr')
    ALIGN = ('SM_DeadBranch', 'SM_SmallStones', 'tkwqbbofa', 'wgxjfhr')
    cache = {}
    with u.ScopedEditorTransaction('VMP trial build (unsaved test)'):
        for k, it in enumerate(spec['items']):
            x, y = it['xy']; gz = ground(x, y)
            if gz is None:
                res['problems'].append('no ground %s' % it['label']); continue
            loc = u.Vector(x, y, gz + it.get('dz', 0.0))
            rot = u.Rotator(pitch=it.get('pitch', 0.0), yaw=it.get('yaw', 0.0), roll=it.get('roll', 0.0))
            fwd = u.Vector(math.cos(math.radians(it.get('yaw', 0.0))), math.sin(math.radians(it.get('yaw', 0.0))), 0.0)
            soft = any(k in it['asset'] for k in SOFT)
            if it['kind'] == 'mesh' and any(k in it['asset'] for k in ALIGN):
                rot = u.MathLibrary.make_rot_from_zx(normal(x, y), fwd)
            asset = cache.get(it['asset']) or u.load_asset(it['asset']); cache[it['asset']] = asset
            if asset is None:
                res['problems'].append('asset missing %s' % it['asset']); continue
            if it['kind'] == 'mesh':
                a = AS.spawn_actor_from_object(asset, loc, rot)
                a.set_actor_scale3d(u.Vector(*it.get('scale', [1, 1, 1])))
                # trial props keep pawn collision but ignore the Camera channel, so the spring arm never snaps into the head on a log/rock
                smc = a.get_component_by_class(u.StaticMeshComponent)
                if smc:
                    if soft:
                        smc.set_collision_enabled(u.CollisionEnabled.NO_COLLISION)
                    else:
                        smc.set_collision_response_to_channel(u.CollisionChannel.ECC_CAMERA, u.CollisionResponseType.ECR_IGNORE)
                    smc.set_editor_property('receives_decals', False)
            else:   # decal
                a = AS.spawn_actor_from_class(u.DecalActor, loc, u.MathLibrary.make_rot_from_xz(normal(x, y, 80.0) * -1.0, fwd))
                dc = a.get_component_by_class(u.DecalComponent)
                dc.set_decal_material(asset)
                dc.set_editor_property('decal_size', u.Vector(min(it.get('depth', 30.0), 30.0), it['size'][1], it['size'][0]))
                if 'sort' in it:
                    dc.set_editor_property('sort_order', it['sort'])
            a.set_actor_label('VMP_%03d_%s' % (k, it['label']))
            a.set_folder_path('VMP_Trial')
            res['spawned'].append({'label': a.get_actor_label(), 'asset': it['asset'], 'loc': [round(loc.x, 1), round(loc.y, 1), round(loc.z, 1)], 'yaw': it.get('yaw', 0.0), 'rot': [round(a.get_actor_rotation().pitch, 1), round(a.get_actor_rotation().yaw, 1), round(a.get_actor_rotation().roll, 1)], 'soft': soft})
S = u.EditorLoadingAndSavingUtils
res['dirty'] = sorted([p.get_name() for p in S.get_dirty_content_packages()] + [p.get_name() for p in S.get_dirty_map_packages()])
json.dump(res, open(os.path.join(VMP, 'build_%s.json' % MODE), 'w'), indent=1, default=str)
print('VMP_%s spawned %d removed %d problems %d dirty %s' % (MODE.upper(), len(res['spawned']), res['removed'], len(res['problems']), res['dirty']))
