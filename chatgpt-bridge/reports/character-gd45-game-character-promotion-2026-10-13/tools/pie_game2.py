"""GD45 PIE verification #2 (nothing saved): PIE in the current editor map (L_GR_SphirusHouse), read back the possessed BP_PBI_Player after the
bindings / garment-animation fix: skeletal components (mesh, anim instance, LOD, post-process + body shape curves, socket transforms to prove the
garments follow the body), grooms (asset, binding, visible, bound at runtime), automation screenshot. Writes data/pie_game2.json."""
import unreal as u, json, pathlib
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/GD45_Promote_20261013/data'
cls = u.load_asset('/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player').generated_class()
ues = u.get_editor_subsystem(u.UnrealEditorSubsystem); les = u.get_editor_subsystem(u.LevelEditorSubsystem)
info = {'editor_map': ues.get_editor_world().get_path_name()}; st = {'k': 0, 'phase': 'start'}
def finish():
    u.unregister_slate_post_tick_callback(hd)
    if les.is_in_play_in_editor(): les.editor_request_end_play()
    (O/'pie_game2.json').write_text(json.dumps(info, indent=1, default=str)); print('GD45_PIE2_DONE', 'error' in info, flush=True)
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
        if st['k']-st['k0'] == 90:
            try: u.AutomationLibrary.take_high_res_screenshot(1920, 1080, 'gd45_pie_player.png'); info['shot'] = 'requested'
            except Exception as e: info['shot_error'] = str(e)[:100]
            return
        if st['k']-st['k0'] < 200: return
        a = st['a']; out = {'skeletal': {}, 'grooms': {}, 'pawn_class': a.get_class().get_path_name()}
        comps = {c.get_name(): c for c in a.get_components_by_class(u.SkeletalMeshComponent)}
        for nm, c in comps.items():
            if nm not in ('Manny', 'Face', 'Henley', 'Shorts', 'CharacterMesh0'): continue
            ai = c.get_anim_instance(); pp = c.get_post_process_instance(); lp = c.get_editor_property('leader_pose_component')
            row = {'mesh': c.skeletal_mesh_asset.get_name() if c.skeletal_mesh_asset else None, 'lod': c.get_predicted_lod_level(), 'anim_instance': ai.get_class().get_name() if ai else None, 'post_process_instance': pp.get_class().get_name() if pp else None,
                   'leader': lp.get_name() if lp else None, 'visible': c.is_visible(), 'parent': c.get_attach_parent().get_name() if c.get_attach_parent() else None, 'spine_03': xf(c, 'spine_03'), 'thigh_l': xf(c, 'thigh_l'), 'head': xf(c, 'head'), 'hand_l': xf(c, 'hand_l')}
            if pp is not None and nm == 'Manny': row['pp_curves'] = {k: round(pp.get_curve_value(k), 3) for k in ('BR_Neutral', 'LK_Neutral', 'RV_Bend30', 'RV_Hip075_l')}
            out['skeletal'][nm] = row
        for g in a.get_components_by_class(u.GroomComponent):
            e = {'groom': g.groom_asset.get_name() if g.groom_asset else None, 'binding': g.binding_asset.get_name() if g.binding_asset else None, 'visible': g.is_visible(), 'parent': g.get_attach_parent().get_name() if g.get_attach_parent() else None}
            for p_ in ('attachment_name', 'use_cards', 'simulation_settings'):
                try: v = g.get_editor_property(p_); e[p_] = str(v)[:60]
                except Exception: pass
            out['grooms'][g.get_name()] = e
        info['readback'] = out; finish()
    except Exception as e:
        info['error'] = repr(e); finish()
hd = u.register_slate_post_tick_callback(tick); print('GD45_PIE2_STARTED', flush=True)
