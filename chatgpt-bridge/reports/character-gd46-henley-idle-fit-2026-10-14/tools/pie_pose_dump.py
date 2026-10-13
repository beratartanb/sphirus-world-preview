"""GD46 (garment fit): PIE readback of the in-game idle pose (nothing saved). After the pawn settles in idle: every Manny bone in COMPONENT
space (quat x,y,z,w / translation / scale, the dfm capture format), the body's always-on morph weights, the Henley's morph (corrective) weights,
the posed Henley render mesh (RENDER_DATA positions, component space) for validating the offline skinning, and three automation screenshots
from a spawned camera (front 3/4, side, back) so the garment can be judged from the front too. Writes data/pie_pose.json (+ .gz mesh)."""
import unreal as u, json, gzip, pathlib, math, builtins
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/GD46_GarmentFit_20261013/data'; O.mkdir(parents=True, exist_ok=True)
TAG = builtins.__dict__.get('GD46_TAG', 'gd46_pose')
cls = u.load_asset('/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player').generated_class()
ues = u.get_editor_subsystem(u.UnrealEditorSubsystem); les = u.get_editor_subsystem(u.LevelEditorSubsystem)
info = {'editor_map': ues.get_editor_world().get_path_name(), 'shots': []}; st = {'k': 0, 'phase': 'start'}
def vec(v): return [round(v.x, 4), round(v.y, 4), round(v.z, 4)]
def tr(t): return {'translation': vec(t.translation), 'rotation': [round(x, 6) for x in (t.rotation.x, t.rotation.y, t.rotation.z, t.rotation.w)], 'scale': vec(t.scale3d)}
def finish():
    u.unregister_slate_post_tick_callback(hd)
    if les.is_in_play_in_editor(): les.editor_request_end_play()
    (O/('pie_%s.json' % TAG)).write_text(json.dumps(info, indent=1, default=str)); print('GD46_POSE_DONE', 'error' in info, json.dumps(info.get('summary', {}))[:600], flush=True)
def comp(a, nm):
    for c in a.get_components_by_class(u.SceneComponent):
        if c.get_name() == nm: return c
def shot(name, cam):
    try:
        ok = u.AutomationLibrary.take_high_res_screenshot(1920, 1080, TAG + '_' + name + '.png', cam) if cam is not None else u.AutomationLibrary.take_high_res_screenshot(1920, 1080, TAG + '_' + name + '.png'); info['shots'].append([name, bool(ok)])
    except Exception as e: info['shots'].append([name, 'ERR ' + str(e)[:120]])
def make_cam(gw, a, name, az_deg, dist, height, look_h):
    loc = a.get_actor_location(); yaw = a.get_actor_rotation().yaw; ang = math.radians(yaw + az_deg)
    pos = u.Vector(loc.x + dist*math.cos(ang), loc.y + dist*math.sin(ang), loc.z + height); tgt = u.Vector(loc.x, loc.y, loc.z + look_h)
    rot = u.MathLibrary.find_look_at_rotation(pos, tgt); cam = u.get_editor_subsystem(u.EditorActorSubsystem).spawn_actor_from_class(u.CameraActor, pos, rot, transient=True) if False else gw.spawn_actor(u.CameraActor, pos, rot) if hasattr(gw, 'spawn_actor') else u.EditorLevelLibrary.spawn_actor_from_class(u.CameraActor, pos, rot)
    cc = cam.get_component_by_class(u.CameraComponent); cc.set_field_of_view(40.0); return cam
def tick(dt):
    try:
        st['k'] += 1
        if st['phase'] == 'start': les.editor_request_begin_play(); st['phase'] = 'wait'; return
        gw = ues.get_game_world()
        if st['phase'] == 'wait':
            if gw is None:
                if st['k'] > 1200: info['error'] = 'PIE did not start'; finish()
                return
            acts = u.GameplayStatics.get_all_actors_of_class(gw, cls)
            if not acts: return
            st['a'] = acts[0]; st['phase'] = 'run'; st['k0'] = st['k']; info['n_instances'] = len(acts); return
        a = st['a']; k = st['k'] - st['k0']
        if k == 150:   # cameras are optional (UE Python cannot always spawn into the PIE world); fall back to the player view
            st['cams'] = {}
            for nm, az, d_, h_, lh in (('front34', 35, 260, 60, 110), ('side', 90, 260, 55, 110), ('back', 180, 260, 60, 110), ('front', 0, 240, 55, 112)):
                try: st['cams'][nm] = make_cam(gw, a, nm, az, d_, h_, lh)
                except Exception as e: info.setdefault('cam_errors', []).append(nm + ': ' + str(e)[:120])
            if 'front34' in st['cams']: shot('front34', st['cams']['front34'])
            else: shot('player', None)
        elif k == 190 and 'side' in st['cams']: shot('side', st['cams']['side'])
        elif k == 230 and 'back' in st['cams']: shot('back', st['cams']['back'])
        elif k == 270 and 'front' in st['cams']: shot('front', st['cams']['front'])
        elif k == 300:
            b = comp(a, 'Manny'); h = comp(a, 'Henley'); f = comp(a, 'Face'); s = comp(a, 'Shorts')
            info['pawn'] = {'location': vec(a.get_actor_location()), 'yaw': round(a.get_actor_rotation().yaw, 3), 'forward': vec(a.get_actor_forward_vector())}
            info['manny_world'] = tr(b.get_world_transform()); info['manny_mesh'] = b.get_skeletal_mesh_asset().get_path_name()
            names = [str(n) for n in b.get_all_socket_names() if b.get_bone_index(n) >= 0]
            info['bones'] = {n: tr(b.get_socket_transform(n, u.RelativeTransformSpace.RTS_COMPONENT)) for n in names}
            info['body_morphs'] = {m: round(b.get_morph_target(m), 4) for m in ('BR_Neutral', 'LK_Neutral')}
            hm = h.get_skeletal_mesh_asset(); info['henley_mesh'] = hm.get_path_name(); info['henley_morphs'] = {str(m): round(h.get_morph_target(str(m)), 4) for m in hm.get_all_morph_target_names()}
            info['henley_leader'] = str(h.get_editor_property('leader_pose_component'))
            info['face_mesh'] = f.get_skeletal_mesh_asset().get_path_name() if f else None; info['shorts_mesh'] = s.get_skeletal_mesh_asset().get_path_name() if s else None
            meshes = {}
            for nm, c in (('Henley', h), ('Manny', b)):
                dm = u.DynamicMesh(); opts = u.GeometryScriptCopyMeshFromComponentOptions(); rl_ = u.GeometryScriptMeshReadLOD(); rl_.lod_type = u.GeometryScriptLODType.RENDER_DATA; rl_.lod_index = 0; opts.requested_lod = rl_
                res = u.GeometryScript_SceneUtils.copy_mesh_from_component(c, dm, opts, False)
                P = u.GeometryScript_List.convert_vector_list_to_array(u.GeometryScript_MeshQueries.get_all_vertex_positions(dm, False)[1])
                meshes[nm] = {'result': str(res[-1]), 'n': len(P), 'positions': [[round(p.x, 3), round(p.y, 3), round(p.z, 3)] for p in P]}
            gzip.open(O/('pie_posed_meshes_%s.json.gz' % TAG), 'wt').write(json.dumps(meshes)); info['posed_meshes'] = {k: v['n'] for k, v in meshes.items()}
            info['summary'] = {'bones': len(info['bones']), 'body_morphs': info['body_morphs'], 'henley_morphs_nonzero': {k: v for k, v in info['henley_morphs'].items() if abs(v) > 0.001}, 'shots': info['shots'], 'posed': info['posed_meshes']}
            finish()
    except Exception as e:
        info['error'] = str(e)[:400]; finish()
hd = u.register_slate_post_tick_callback(tick)
