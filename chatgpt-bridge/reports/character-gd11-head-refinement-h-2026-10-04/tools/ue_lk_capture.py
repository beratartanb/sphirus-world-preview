"""CharacterFinal capture harness (from ue_of_capture.py): stability-gated scene captures of the candidate rig (+ garments,
+ groom). capture_request.json cases: name, view (front/side/back/front3q/rear3q or 'custom' with cam=[x,y,z,yaw,pitch]),
fov, animation, time, garments (bool), hide [names], materials ('real'|'clay'), light ('neutral'|'grazing'|'grazing_top'|'rearR'|'rearL'),
measure (bool: dump posed body + garment geometry), lod."""
import unreal, pathlib, json, gzip, time, builtins, traceback
R = pathlib.Path(unreal.Paths.project_dir()).resolve(); E = R/'Saved/Codex/CharacterLookdev_20260930/captures'; Q = builtins.SPH_LK_QA
cfg = json.loads((E/'capture_request.json').read_text()); cases = cfg['cases']; label = cfg['label']
b = Q['components']['Body']; h = Q['components']['Head']
assert not getattr(builtins, 'SPH_LK_CAPTURE', {}).get('running', False)
state = {'running': True, 'i': 0, 'phase': 0, 'results': []}; builtins.SPH_LK_CAPTURE = state
def vec(v): return [v.x, v.y, v.z]
def tr(t): return {'translation': vec(t.translation), 'rotation': [t.rotation.x, t.rotation.y, t.rotation.z, t.rotation.w], 'scale': vec(t.scale3d)}
def meshread(name, lodp):
    d = E/'posed_geometry'; d.mkdir(exist_ok=True); allc = dict(Q['components']); allc.update(Q['garments'])
    for part, c in allc.items():
        if not c.is_visible(): continue
        dm = unreal.DynamicMesh(); opts = unreal.GeometryScriptCopyMeshFromComponentOptions(); lod = unreal.GeometryScriptMeshReadLOD(); lod.lod_type = unreal.GeometryScriptLODType.RENDER_DATA; lod.lod_index = lodp; opts.requested_lod = lod
        res = unreal.GeometryScript_SceneUtils.copy_mesh_from_component(c, dm, opts, True); assert 'SUCCESS' in str(res[-1])
        q = unreal.GeometryScript_MeshQueries; l = unreal.GeometryScript_List; v = l.convert_vector_list_to_array(q.get_all_vertex_positions(dm, False)[1]); t = l.convert_triangle_list_to_array(q.get_all_triangle_indices(dm, False)[1])
        with gzip.open(d/(name+'_'+part+'.json.gz'), 'wt', encoding='utf-8') as f: json.dump({'positions': [vec(p) for p in v], 'triangles': [[i.x, i.y, i.z] for i in t]}, f, separators=(',', ':'))
def set_light(mode):
    """studio (neutral review) | grazing (materials) | gameplay (sun + sky) -- character-presentation-lighting.md"""
    L = Q['lights']; rr_ = mode in ('rearR', 'rearL'); st = mode in ('studio', 'neutral') or rr_; gz_ = mode.startswith('grazing') or rr_; gp = mode == 'gameplay'   # rearR / rearL (refinement F): full studio + the spot from behind that side (lit back / behind-ear hair)
    for n in ('key', 'fill', 'rim'): L[n][0].set_intensity(L[n][1] if st else (L[n][1]*0.06 if gz_ else 0.0))
    L['grazing'][0].set_intensity(L['grazing'][1] if gz_ else 0.0); L['sun'][0].set_intensity(L['sun'][1] if gp else 0.0)
    Q['sky'].set_intensity(0.55 if st else (0.12 if gz_ else 1.0))
    if mode == 'sky':   # refinement H: symmetric diagnostic light - all directional rect / spot / sun lights off, only the uniform sky light
        for n in ('key', 'fill', 'rim'): L[n][0].set_intensity(0.0)
        L['grazing'][0].set_intensity(0.0); L['sun'][0].set_intensity(0.0); Q['sky'].set_intensity(float(__import__('os').environ.get('LK_SKY', '18.0')))
    if mode == 'front':   # refinement H: SYMMETRIC diagnostic light - only the spot, placed on the face's midline in front (key / fill / rim / sun off)
        for n in ('key', 'fill', 'rim'): L[n][0].set_intensity(0.0)
        L['sun'][0].set_intensity(0.0); L['grazing'][0].set_intensity(L['grazing'][1]); Q['sky'].set_intensity(0.3)
    if mode == 'interior':   # softer interior light (final-art check): low-contrast key / fill, faint rim, dim sky, no sun / grazing
        for n, k in (('key', 0.3), ('fill', 0.8), ('rim', 0.12)): L[n][0].set_intensity(L[n][1]*k)
        Q['sky'].set_intensity(0.3)
    g = Q['grazing_actor']
    if mode == 'grazing': g.set_actor_location(unreal.Vector(-300, 60, 125), False, False)
    elif mode == 'grazing_top': g.set_actor_location(unreal.Vector(-40, 110, 330), False, False)
    elif mode == 'grazing_rear': g.set_actor_location(unreal.Vector(300, -80, 120), False, False)
    elif mode == 'front': g.set_actor_location(unreal.Vector(-0.23, 320, 175), False, False)
    elif mode == 'rearR': g.set_actor_location(unreal.Vector(-230, -210, 180), False, False)
    elif mode == 'rearL': g.set_actor_location(unreal.Vector(230, -210, 180), False, False)
    tz = case_target_z[0]
    g.set_actor_rotation(unreal.MathLibrary.find_look_at_rotation(g.get_actor_location(), unreal.Vector(0, 0, tz)), False)
case_target_z = [105.0]
def mat_for(part, c, i, real):
    if not real: return Q['clay']
    ov = Q.get('overrides', {}).get(part, {})
    if i in ov and ov[i]: return ov[i]
    if isinstance(c, unreal.ChaosClothComponent): return c.get_material(i)   # cloth asset keeps its own materials
    return c.skeletal_mesh_asset.get_editor_property('materials')[i].get_editor_property('material_interface')
def tick(dt):
    try:
        if state['i'] == len(cases):
            state['running'] = False; unreal.unregister_slate_post_tick_callback(handle); set_light('studio'); (E/(label+'_results.json')).write_text(json.dumps(state['results'], indent=2)); return
        case = cases[state['i']]; name = case['name']; view = case['view']
        if state['phase'] == 0:
            real = case.get('materials', 'real') == 'real'
            for part, c in Q['components'].items():
                for i in range(c.get_num_materials()): c.set_material(i, mat_for(part, c, i, real))
            for g, c in Q['garments'].items():
                c.set_visibility(bool(case.get('garments', True)) and g not in case.get('hide', []), False); c.set_forced_lod(case.get('lod_g', case.get('lod', 0))+1)
                if not isinstance(c, unreal.ChaosClothComponent): c.set_editor_property('disable_morph_target', bool(case.get('garment_nomorph', False)))
                for i in range(c.get_num_materials()): c.set_material(i, mat_for(g, c, i, real))
            for g, gc in Q['grooms'].items(): gc.set_visibility(bool(case.get('hair', True)) and g not in case.get('hide', []), False)
            for g, gc in Q['grooms'].items():
                try: gc.set_forced_lod(int(case.get('groom_lod', -1)))   # -1 = automatic (screen size)
                except Exception: pass
            for part, c in Q['components'].items(): c.set_visibility(part not in case.get('hide', []), False); c.set_forced_lod(case.get('lod', 0)+1)
            case_target_z[0] = case.get('light_target_z', 105.0); set_light(case.get('light', 'studio'))
            b.clear_morph_targets()
            for mz in case.get('morph_zero', []): b.set_morph_target(mz, 0.0, False)   # soft-tissue BEFORE view: manual override of the curve-driven morphs
            b.get_owner().set_actor_location(unreal.Vector(0, 0, 0), False, False)
            a = unreal.load_asset(case['animation']) if case.get('animation') else None; b.play_animation(a, False)
            if a and case.get('play') is not None:   # corrective pass: animation in flight (cloth inertia): run from 'play' at real rate, capture at 'time'
                b.set_position(case['play'], False); b.set_play_rate(case.get('rate', 1.0)); state['dyn'] = True; state['dyn_start'] = time.time()
            elif a: b.set_position(case['time'], False); b.set_play_rate(0)
            for g_, c_ in Q['garments'].items():   # corrective pass: Chaos Cloth restarts from the new start pose (no tangling across pose jumps)
                if isinstance(c_, unreal.ChaosClothComponent): c_.force_next_update_teleport_and_reset()
            if case.get('face_anim'):   # facial-rig validation: RigLogic control curves on the head (post-process ABP still evaluates)
                fa = unreal.load_asset(case['face_anim']); h.set_animation_mode(unreal.AnimationMode.ANIMATION_SINGLE_NODE); h.play_animation(fa, False); h.set_position(case.get('face_time', 0.0), False); h.set_play_rate(0)
            elif h.get_animation_mode() != unreal.AnimationMode.ANIMATION_BLUEPRINT: h.set_animation_mode(unreal.AnimationMode.ANIMATION_BLUEPRINT)
            cams = {'front': (0, 700, -90, 0), 'side': (700, 0, 180, 0), 'back': (0, -700, 90, 0), 'rear3q': (400, -574.456, 124.85, 0), 'front3q': (-400, 574.456, -55.15, 0)}
            if view == 'custom': x, y, z, yaw, pitch = case['cam']
            else: x, y, yaw, pitch = cams[view]; x += case.get('cam_dx', 0); z = case.get('camera_z', 92)
            Q['capture'].set_actor_location(unreal.Vector(x, y, z), False, False); Q['capture'].set_actor_rotation(unreal.Rotator(yaw=yaw, pitch=pitch, roll=0), False); Q['cc'].set_editor_property('fov_angle', case.get('fov', 15.5))
            state['phase'] = 1; state['frames'] = 0; state['start'] = time.time()
        state['frames'] += 1; Q['cc'].capture_scene()
        if state.get('dyn'):
            if b.get_position() < case['time'] and time.time()-state['dyn_start'] < 20: return
            b.set_play_rate(0); state['dyn'] = False; state['dyn_hold'] = 0
            if case.get('track') or case.get('cam_follow'):
                pv = b.get_socket_location('pelvis'); c_ = case['cam'] if view == 'custom' else None
                if c_: Q['capture'].set_actor_location(unreal.Vector(pv.x+c_[0], pv.y+c_[1], c_[2]), False, False)
        if state.get('dyn_hold') is not None:
            state['dyn_hold'] += 1
            if state['dyn_hold'] < 4: return
            state['dyn_hold'] = None; image = name+'_'+view+'.png'; unreal.RenderingLibrary.export_render_target(Q['world'], Q['rt'], str(E), image)
            row = {**case, 'image': image, 'dynamic': True, 'anim_pos': b.get_position()}; state['results'].append(row); (E/(name+'_'+view+'.json')).write_text(json.dumps(row, indent=2)); state['i'] += 1; state['phase'] = 0; return
        if state['frames'] < case.get('min_frames', 60) or time.time()-state['start'] < case.get('min_seconds', 1.2): return
        def snap(): return {p: {n: vec(c.get_bone_transform(n).translation) for n in ['hand_l', 'hand_r', 'upperarm_l', 'upperarm_r', 'clavicle_l', 'neck_01', 'head', 'upperarm_out_l', 'thigh_l', 'calf_l']} for p, c in Q['components'].items()}
        cur = snap(); prev = state.get('snap'); state['snap'] = cur
        def d(a, b_): return max(sum((x-y)**2 for x, y in zip(a[k], b_[k]))**.5 for k in a)
        stable = prev is not None and d(cur['Body'], prev['Body']) < 1e-5 and d(cur['Head'], prev['Head']) < 1e-5
        if not stable:
            state['settle'] = 0
            if state['frames'] < 600: return
            raise RuntimeError('unstable '+name)
        # settle: keep capturing the stable pose for a few more ticks before reading the render target (a scene capture
        # issued this tick is not guaranteed to be in the RT yet: exporting immediately produced one-case-stale images)
        if case.get('track_head') and not state.get('tracked'):   # head-framed motion shots: camera = head bone + the authored offset (cam relative to a z=159 head)
            hb = b.get_socket_location('head'); c_ = case['cam']
            Q['capture'].set_actor_location(unreal.Vector(hb.x+c_[0], hb.y+c_[1], hb.z+(c_[2]-159.0)), False, False); state['tracked'] = True; state['settle'] = 0; state['track_offset'] = [hb.x, hb.y, hb.z]; return
        if case.get('track') and not state.get('tracked'):   # root-motion clips: re-centre the camera on the pelvis (x, y), then settle again
            pv = b.get_socket_location('pelvis'); cl = Q['capture'].get_actor_location()
            Q['capture'].set_actor_location(unreal.Vector(cl.x+pv.x, cl.y+pv.y, cl.z), False, False); state['tracked'] = True; state['settle'] = 0; state['track_offset'] = [pv.x, pv.y]; return
        state['settle'] = state.get('settle', 0)+1
        if state['settle'] < 6: return
        state['snap'] = None; state['settle'] = 0; trk = state.pop('track_offset', None); state['tracked'] = False
        image = name+'_'+view+'.png'; unreal.RenderingLibrary.export_render_target(Q['world'], Q['rt'], str(E), image)
        row = {**case, 'image': image, 'gate_frames': state['frames'], 'bone_transforms': {}, 'track_offset': trk}
        if case.get('bones'):
            names = [str(n) for n in b.get_all_socket_names() if b.get_bone_index(n) >= 0]; row['bone_transforms']['Body'] = {n: tr(b.get_bone_transform(n)) for n in names}
        if case.get('measure'): meshread(name, case.get('lod', 0))
        state['results'].append(row); (E/(name+'_'+view+'.json')).write_text(json.dumps(row, indent=2)); state['i'] += 1; state['phase'] = 0
        (E/'capture_progress.json').write_text(json.dumps({'label': label, 'completed': state['i'], 'total': len(cases)}))
    except Exception:
        state['running'] = False; unreal.unregister_slate_post_tick_callback(handle); set_light('studio'); (E/(label+'_error.txt')).write_text(traceback.format_exc())
handle = unreal.register_slate_post_tick_callback(tick); print('CF_CAPTURE_STARTED', label, len(cases))
