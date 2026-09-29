"""Outfit capture harness (from ue_shc_capture.py): stability-gated scene captures of the BR rig + garments.
capture_request.json cases: name, view (front/side/back/front3q/rear3q or 'custom' with cam=[x,y,z,yaw,pitch]), fov,
animation, time, garments (bool), materials ('real'|'clay'), measure (bool: dump posed body + garment geometry), lod."""
import unreal, pathlib, json, gzip, time, builtins, traceback
R = pathlib.Path(unreal.Paths.project_dir()).resolve(); E = R/'Saved/Codex/OutfitHome_20260929/captures'; Q = builtins.SPH_OF_QA
cfg = json.loads((E/'capture_request.json').read_text()); cases = cfg['cases']; label = cfg['label']
b = Q['components']['Body']; h = Q['components']['Head']
assert not getattr(builtins, 'SPH_OF_CAPTURE', {}).get('running', False)
state = {'running': True, 'i': 0, 'phase': 0, 'results': []}; builtins.SPH_OF_CAPTURE = state
def vec(v): return [v.x, v.y, v.z]
def tr(t): return {'translation': vec(t.translation), 'rotation': [t.rotation.x, t.rotation.y, t.rotation.z, t.rotation.w], 'scale': vec(t.scale3d)}
def meshread(name, lodp):
    d = E/'posed_geometry'; d.mkdir(exist_ok=True); allc = dict(Q['components']); allc.update(Q['garments'])
    for part, c in allc.items():
        dm = unreal.DynamicMesh(); opts = unreal.GeometryScriptCopyMeshFromComponentOptions(); lod = unreal.GeometryScriptMeshReadLOD(); lod.lod_type = unreal.GeometryScriptLODType.RENDER_DATA; lod.lod_index = lodp; opts.requested_lod = lod
        res = unreal.GeometryScript_SceneUtils.copy_mesh_from_component(c, dm, opts, True); assert 'SUCCESS' in str(res[-1])
        q = unreal.GeometryScript_MeshQueries; l = unreal.GeometryScript_List; v = l.convert_vector_list_to_array(q.get_all_vertex_positions(dm, False)[1]); t = l.convert_triangle_list_to_array(q.get_all_triangle_indices(dm, False)[1])
        with gzip.open(d/(name+'_'+part+'.json.gz'), 'wt', encoding='utf-8') as f: json.dump({'positions': [vec(p) for p in v], 'triangles': [[i.x, i.y, i.z] for i in t]}, f, separators=(',', ':'))
def tick(dt):
    try:
        if state['i'] == len(cases):
            state['running'] = False; unreal.unregister_slate_post_tick_callback(handle); (E/(label+'_results.json')).write_text(json.dumps(state['results'], indent=2)); return
        case = cases[state['i']]; name = case['name']; view = case['view']
        if state['phase'] == 0:
            real = case.get('materials', 'real') == 'real'
            for part, c in Q['components'].items():
                m = c.skeletal_mesh_asset
                for i in range(c.get_num_materials()): c.set_material(i, m.get_editor_property('materials')[i].get_editor_property('material_interface') if real else Q['clay'])
            for g, c in Q['garments'].items():
                c.set_visibility(bool(case.get('garments', True)) and g not in case.get('hide', []), False); c.set_forced_lod(case.get('lod', 0)+1)
                m = c.skeletal_mesh_asset
                for i in range(c.get_num_materials()): c.set_material(i, m.get_editor_property('materials')[i].get_editor_property('material_interface') if real else Q['clay'])
            for part, c in Q['components'].items(): c.set_visibility(part not in case.get('hide', []), False); c.set_forced_lod(case.get('lod', 0)+1)
            b.get_owner().set_actor_location(unreal.Vector(0, 0, 0), False, False)
            a = unreal.load_asset(case['animation']) if case.get('animation') else None; b.play_animation(a, False)
            if a: b.set_position(case['time'], False); b.set_play_rate(0)
            cams = {'front': (0, 700, -90, 0), 'side': (700, 0, 180, 0), 'back': (0, -700, 90, 0), 'rear3q': (400, -574.456, 124.85, 0), 'front3q': (-400, 574.456, -55.15, 0)}
            if view == 'custom': x, y, z, yaw, pitch = case['cam']
            else: x, y, yaw, pitch = cams[view]; x += case.get('cam_dx', 0); z = case.get('camera_z', 100)
            Q['capture'].set_actor_location(unreal.Vector(x, y, z), False, False); Q['capture'].set_actor_rotation(unreal.Rotator(yaw=yaw, pitch=pitch, roll=0), False); Q['cc'].set_editor_property('fov_angle', case.get('fov', 8))
            state['phase'] = 1; state['frames'] = 0; state['start'] = time.time()
        state['frames'] += 1; Q['cc'].capture_scene()
        if state['frames'] < 60 or time.time()-state['start'] < 1.2: return
        def snap(): return {p: {n: vec(c.get_bone_transform(n).translation) for n in ['hand_l', 'hand_r', 'upperarm_l', 'upperarm_r', 'clavicle_l', 'neck_01', 'head', 'upperarm_out_l', 'thigh_l', 'calf_l']} for p, c in Q['components'].items()}
        cur = snap(); prev = state.get('snap'); state['snap'] = cur
        def d(a, b_): return max(sum((x-y)**2 for x, y in zip(a[k], b_[k]))**.5 for k in a)
        stable = prev is not None and d(cur['Body'], prev['Body']) < 1e-5 and d(cur['Head'], prev['Head']) < 1e-5
        if not stable:
            if state['frames'] < 600: return
            raise RuntimeError('unstable '+name)
        state['snap'] = None
        image = name+'_'+view+'.png'; unreal.RenderingLibrary.export_render_target(Q['world'], Q['rt'], str(E), image)
        row = {**case, 'image': image, 'gate_frames': state['frames'], 'bone_transforms': {}}
        if case.get('bones'):
            names = [str(n) for n in b.get_all_socket_names() if b.get_bone_index(n) >= 0]; row['bone_transforms']['Body'] = {n: tr(b.get_bone_transform(n)) for n in names}
        if case.get('measure'): meshread(name, case.get('lod', 0))
        state['results'].append(row); (E/(name+'_'+view+'.json')).write_text(json.dumps(row, indent=2)); state['i'] += 1; state['phase'] = 0
        (E/'capture_progress.json').write_text(json.dumps({'label': label, 'completed': state['i'], 'total': len(cases)}))
    except Exception:
        state['running'] = False; unreal.unregister_slate_post_tick_callback(handle); (E/(label+'_error.txt')).write_text(traceback.format_exc())
handle = unreal.register_slate_post_tick_callback(tick); print('OUTFIT_CAPTURE_STARTED', label, len(cases))
