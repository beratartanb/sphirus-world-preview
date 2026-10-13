"""GD45 PIE verification (nothing saved): PIE in the current editor map (the game map L_GR_SphirusHouse), read back the possessed BP_PBI_Player:
skeletal components (mesh, anim instance class, LOD, post-process instance + its BR_Neutral / LK_Neutral curve values on the body, leader pose at
runtime), garment follow check (spine_03 / thigh_l socket transforms of Henley / Shorts vs Manny after 120 ticks), grooms (asset, binding, visible),
then a high-res screenshot from the player camera. Writes data/pie_game.json."""
import unreal as u, json, pathlib
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/GD45_Promote_20261013/data'
cls = u.load_asset('/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player').generated_class()
ues = u.get_editor_subsystem(u.UnrealEditorSubsystem); les = u.get_editor_subsystem(u.LevelEditorSubsystem)
info = {'editor_map': ues.get_editor_world().get_path_name()}; st = {'k': 0, 'phase': 'start'}
def finish():
    u.unregister_slate_post_tick_callback(hd)
    if les.is_in_play_in_editor(): les.editor_request_end_play()
    (O/'pie_game.json').write_text(json.dumps(info, indent=1, default=str)); print('GD45_PIE_DONE', 'error' in info, flush=True)
def xf(c, sock):
    try: t = c.get_socket_transform(sock, u.RelativeTransformSpace.RTS_WORLD); return [round(v, 2) for v in (t.translation.x, t.translation.y, t.translation.z)]
    except Exception as e: return 'ERR ' + str(e)[:40]
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
            st['a'] = acts[0]; st['phase'] = 'run'; st['k0'] = st['k']; info['game_world'] = gw.get_path_name(); info['n_instances'] = len(acts); return
        if st['k']-st['k0'] == 60:
            try: u.SystemLibrary.execute_console_command(ues.get_game_world(), 'HighResShot 1920x1080 filename=' + str(O/'gd45_pie_player.png').replace('\\', '/'))
            except Exception as e: info['shot_error'] = str(e)[:100]
            return
        if st['k']-st['k0'] < 150: return
        a = st['a']; out = {'skeletal': {}, 'grooms': {}, 'pawn_class': a.get_class().get_path_name(), 'possessed': str(u.GameplayStatics.get_player_pawn(a, 0).get_name()) if u.GameplayStatics.get_player_pawn(a, 0) else None}
        comps = {c.get_name(): c for c in a.get_components_by_class(u.SkeletalMeshComponent)}
        for nm, c in comps.items():
            ai = c.get_anim_instance(); pp = c.get_post_process_instance() if hasattr(c, 'get_post_process_instance') else None; lp = c.get_editor_property('leader_pose_component')
            row = {'mesh': c.skeletal_mesh_asset.get_name() if c.skeletal_mesh_asset else None, 'lod': c.get_predicted_lod_level(), 'anim_instance': ai.get_class().get_name() if ai else None, 'post_process_instance': pp.get_class().get_name() if pp else None,
                   'pp_disabled': c.get_editor_property('disable_post_process_blueprint'), 'leader': lp.get_name() if lp else None, 'visible': c.is_visible(), 'parent': c.get_attach_parent().get_name() if c.get_attach_parent() else None}
            if pp is not None and nm == 'Manny': row['pp_curves'] = {k: round(pp.get_curve_value(k), 3) for k in ('BR_Neutral', 'LK_Neutral', 'RV_Bend30', 'SHC_150_l')}
            if ai is not None and nm == 'Manny': row['anim_curves'] = {k: round(ai.get_curve_value(k), 3) for k in ('BR_Neutral', 'LK_Neutral')}
            if nm in ('Manny', 'Henley', 'Shorts', 'Face', 'CharacterMesh0'): row['spine_03'] = xf(c, 'spine_03'); row['thigh_l'] = xf(c, 'thigh_l'); row['head'] = xf(c, 'head')
            out['skeletal'][nm] = row
        for g in a.get_components_by_class(u.GroomComponent):
            out['grooms'][g.get_name()] = {'groom': g.groom_asset.get_name() if g.groom_asset else None, 'binding': g.binding_asset.get_name() if g.binding_asset else None, 'visible': g.is_visible(), 'parent': g.get_attach_parent().get_name() if g.get_attach_parent() else None}
        info['readback'] = out; finish()
    except Exception as e:
        info['error'] = repr(e); finish()
hd = u.register_slate_post_tick_callback(tick); print('GD45_PIE_STARTED', flush=True)
