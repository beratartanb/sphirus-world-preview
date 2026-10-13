"""GD47 PIE check (nothing saved). builtins.GD47P = {'tag', 'swap': {'HenleyCloth': CA path, 'ShortsCloth': CA path} or None, 'move': bool}
Timeline (frames after the pawn exists): idle shots of the CURRENT pawn (front34 / side / back via the player camera: control rotation orbit,
UE Python cannot spawn cameras into the PIE world) -> optional RUNTIME swap (ChaosClothComponents added to the PIE pawn instance, attached to
Manny, leader pose Manny, skinned Henley/Shorts hidden; the Blueprint is not touched) -> idle shots -> walk (input 0.4) / run (1.0) with
side / front34 / back shots, direction reversed every 150 frames -> stop -> settle shots. Records cloth component state, materials, speeds.
Writes data/pie_<tag>.json; shots Saved/Screenshots/WindowsEditor/gd47_<tag>_<shot>.png"""
import unreal as u, json, pathlib, math, builtins
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/GD47_ChaosCloth_20261014/data'
C = builtins.GD47P; TAG = 'gd47_' + C['tag']
cls = u.load_asset('/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player').generated_class()
ues = u.get_editor_subsystem(u.UnrealEditorSubsystem); les = u.get_editor_subsystem(u.LevelEditorSubsystem)
info = {'cfg': C, 'shots': [], 'events': []}; st = {'k': 0, 'phase': 'start', 'move': None}
def vec(v): return [round(v.x, 2), round(v.y, 2), round(v.z, 2)]
def comp(a, nm):
    for c in a.get_components_by_class(u.SceneComponent):
        if c.get_name() == nm or c.get_name().startswith(nm + '_'): return c
def finish():
    u.unregister_slate_post_tick_callback(hd)
    if les.is_in_play_in_editor(): les.editor_request_end_play()
    (O/('pie_%s.json' % C['tag'])).write_text(json.dumps(info, indent=1, default=str)); print('GD47_PIE_DONE', 'error' in info, json.dumps({k: info.get(k) for k in ('shots', 'cloth', 'error')}, default=str)[:1400], flush=True)
def view(az):   # camera azimuth relative to the character's facing (0 = in front of her): control-rotation orbit of the player camera.
    # NOTE: the GR camera honours it only after the pawn's components were reconstructed (adding an instance subobject) -> every run does that ('swap' with {} = dummy)
    st['az'] = az; a = st['a']; pc = st['pc']; yaw = a.get_actor_rotation().yaw
    pc.set_control_rotation(u.Rotator(roll=0.0, pitch=-8.0, yaw=yaw + az + 180.0))
def shot(name):
    a = st['a']; v = a.get_velocity(); sp = round(math.hypot(v.x, v.y), 1)
    try: ok = u.AutomationLibrary.take_high_res_screenshot(1920, 1080, TAG + '_' + name + '.png')
    except Exception as e: ok = 'ERR ' + str(e)[:120]
    info['shots'].append([name, bool(ok) if not isinstance(ok, str) else ok, sp, vec(a.get_actor_location())])
def cloth_state(tag):
    a = st['a']; rep = {}
    for nm in ('HenleyCloth', 'ShortsCloth', 'Henley', 'Shorts'):
        c = comp(a, nm) or st.get('added', {}).get(nm)
        if c is None: rep[nm] = None; continue
        e = {'name': c.get_name(), 'class': c.get_class().get_name(), 'visible': c.is_visible(), 'attach': c.get_attach_parent().get_name() if c.get_attach_parent() else None}
        try: e['leader'] = str(c.get_editor_property('leader_pose_component'))
        except Exception as ex: e['leader'] = 'ERR ' + str(ex)[:60]
        if isinstance(c, u.ChaosClothComponent):
            e['asset'] = c.get_cloth_asset().get_path_name() if c.get_cloth_asset() else None
            for f in ('is_simulation_enabled', 'is_simulation_suspended', 'get_enable_simulation'):
                if hasattr(c, f):
                    try: e[f] = getattr(c, f)()
                    except Exception as ex: e[f] = 'ERR ' + str(ex)[:60]
            e['materials'] = [c.get_material(i).get_name() if c.get_material(i) else None for i in range(c.get_num_materials())]
        rep[nm] = e
    info.setdefault('cloth', {})[tag] = rep
def swap():   # phase 1: add the components (adding instance subobjects re-runs the construction script: Manny is recreated -> bind later)
    a = st['a']; added = {}
    if not C['swap']:
        sds = u.get_engine_subsystem(u.SubobjectDataSubsystem); root = sds.k2_gather_subobject_data_for_instance(a)[0]
        nh, fail = sds.add_new_subobject(u.AddNewSubobjectParams(parent_handle=root, new_class=u.SceneComponent, blueprint_context=None)); added['dummy'] = str(fail)
    for nm, ca in C['swap'].items():
        sds = u.get_engine_subsystem(u.SubobjectDataSubsystem); root = sds.k2_gather_subobject_data_for_instance(a)[0]
        nh, fail = sds.add_new_subobject(u.AddNewSubobjectParams(parent_handle=root, new_class=u.ChaosClothComponent, blueprint_context=None))
        c = u.SubobjectDataBlueprintFunctionLibrary.get_object(u.SubobjectDataBlueprintFunctionLibrary.get_data(nh)); assert isinstance(c, u.ChaosClothComponent), (str(fail), c)
        try: sds.rename_subobject(nh, nm)
        except Exception as ex: info['events'].append(['rename_err', str(ex)[:80]])
        added[nm] = c.get_name()
    info['events'].append(['swap', st['k'] - st['k0'], added])
def bind():  # phase 2: fresh Manny, attach + leader pose + asset, hide the skinned garments
    a = st['a']; manny = comp(a, 'Manny'); rep = {'manny': manny.get_path_name()}
    if not C['swap']:
        if C.get('show_skinned'):   # baseline view of the promoted pawn: skinned garments back on, cloth hidden (runtime only)
            for nm, vis in (('HenleyCloth', False), ('ShortsCloth', False), ('Henley', True), ('Shorts', True)):
                c = comp(a, nm)
                if c: c.set_visibility(vis, False)
        info['events'].append(['bind', 'dummy only', bool(C.get('show_skinned'))]); return
    for nm, ca in C['swap'].items():
        c = comp(a, nm)
        if c is None: c = [x for x in a.get_components_by_class(u.ChaosClothComponent) if x.get_name() not in rep.values()][0]
        c.attach_to_component(manny, 'None', u.AttachmentRule.SNAP_TO_TARGET, u.AttachmentRule.SNAP_TO_TARGET, u.AttachmentRule.SNAP_TO_TARGET, False)
        c.set_cloth_asset(u.load_asset(ca)); c.set_leader_pose_component(manny, True); c.add_tick_prerequisite_component(manny)
        if hasattr(c, 'set_enable_simulation'): c.set_enable_simulation(True)
        c.force_next_update_teleport_and_reset(); rep[nm] = c.get_name(); st.setdefault('added', {})[nm] = c
    for nm in ('Henley', 'Shorts'): comp(a, nm).set_visibility(False, False)
    info['events'].append(['bind', st['k'] - st['k0'], rep])
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
            st['gw'] = gw; st['a'] = acts[0]; st['pc'] = u.GameplayStatics.get_player_controller(gw, 0); st['phase'] = 'run'; st['k0'] = st['k']; st['fwd0'] = st['a'].get_actor_forward_vector(); return
        a = st['a']; k = st['k'] - st['k0']
        if st['move'] is not None:
            s, sign = st['move']; f0 = st['fwd0']; a.add_movement_input(u.Vector(f0.x*sign, f0.y*sign, 0.0), s, True)
            if st.get('az') is not None: view(st['az'])   # the GR camera recentres behind a moving character: re-apply every frame
        S = st.setdefault('S', [])
        if not S:   # schedule: (frame, action, arg)
            t = C.get('t0', 420); S.append((t - 20, 'state', 'start'))
            if C.get('swap') is not None: S.append((t, 'swap', None)); S.append((t+4, 'bind', None)); S.append((t+10, 'state', 'after_swap')); t += 150
            for az, nm in ((35, 'front34'), (90, 'side'), (180, 'back'), (0, 'front')): S.append((t, 'view', az)); S.append((t+130, 'shot', 'idle_' + nm)); t += 140
            if C.get('burst'):
                S.append((t, 'move', (1.0, 1.0))); S.append((t+1, 'view', 90)); S.append((t+100, 'shot', 'burst_run')); t += 150
                S.append((t, 'move', (1.0, -1.0)))
                for dt_ in (6, 36, 66): S.append((t+dt_, 'shot', 'burst_rev_%02d' % dt_))
                t += 100; S.append((t, 'move', None))
                for dt_ in (4, 34, 64, 94): S.append((t+dt_, 'shot', 'burst_stop_%02d' % dt_))
                t += 110
            if C.get('move', True):
                for gait, sc in (('walk', 0.4), ('run', 1.0)):
                    S.append((t, 'move', (sc, 1.0))); t += 90
                    for az, nm in ((90, 'side'), (35, 'front34'), (180, 'back')): S.append((t, 'view', az)); S.append((t+90, 'shot', gait + '_' + nm)); t += 100
                    S.append((t, 'move', (sc, -1.0))); t += 30
                    S.append((t, 'view', 90)); S.append((t+90, 'shot', gait + '_rev_side')); t += 100
                S.append((t, 'move', None)); S.append((t+1, 'view', 90)); S.append((t+12, 'shot', 'stop_side_0.2s')); S.append((t+40, 'shot', 'stop_side_0.7s')); t += 100
                S.append((t, 'view', 35)); S.append((t+40, 'shot', 'settled_front34')); t += 60
            S.append((t, 'state', 'end')); S.append((t+5, 'end', None))
        while S and S[0][0] <= k:
            _, act, arg = S.pop(0)
            if act == 'view': view(arg)
            elif act == 'shot': shot(arg)
            elif act == 'swap': swap()
            elif act == 'bind': bind()
            elif act == 'state': cloth_state(arg)
            elif act == 'move': st['move'] = arg; info['events'].append(['move', k, arg])
            elif act == 'end': finish(); return
    except Exception as e:
        import traceback; info['error'] = traceback.format_exc()[-600:]; finish()
hd = u.register_slate_post_tick_callback(tick)
