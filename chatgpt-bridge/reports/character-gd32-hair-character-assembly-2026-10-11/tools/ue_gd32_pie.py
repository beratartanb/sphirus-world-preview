"""GD32 PIE check of the evaluation level: loads L_GD32_Eval_G31 (saved state), starts PIE, finds the BP_GD32_Character_G31 instance in the
GAME world and reads back: every groom component's groom / binding asset, visibility and groom LOD count, the face anim instance class, each
skeletal component's mesh, predicted LOD and materials; PIE is then stopped. Nothing is saved. Writes data/pie_check.json."""
import unreal as u, json, pathlib
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/GD32_Identity_20261011/data'
MAP = '/Game/Sphirus/CharacterLab/GD32_IdentityMaster_20261011/Maps/L_GD32_Eval_G31'
u.EditorLoadingAndSavingUtils.load_map(MAP)
cls = u.load_asset('/Game/Sphirus/CharacterLab/GD32_IdentityMaster_20261011/Assembly/BP_GD32_Character_G31').generated_class()
ues = u.get_editor_subsystem(u.UnrealEditorSubsystem); les = u.get_editor_subsystem(u.LevelEditorSubsystem)
info = {'map': MAP}; st = {'k': 0, 'phase': 'start'}
def finish():
    u.unregister_slate_post_tick_callback(hd)
    if les.is_in_play_in_editor(): les.editor_request_end_play()
    (O/'pie_check.json').write_text(json.dumps(info, indent=1, default=str)); print('GD32_PIE_DONE', 'error' in info)
def tick(dt):
    try:
        st['k'] += 1
        if st['phase'] == 'start': les.editor_request_begin_play(); st['phase'] = 'wait'; return
        gw = ues.get_game_world()
        if st['phase'] == 'wait':
            if gw is None:
                if st['k'] > 900: info['error'] = 'PIE did not start'; finish()
                return
            acts = u.GameplayStatics.get_all_actors_of_class(gw, cls)
            if not acts: return
            st['a'] = acts[0]; st['phase'] = 'run'; st['k0'] = st['k']; info['game_world'] = gw.get_path_name(); info['n_instances'] = len(acts); return
        t = st['k']-st['k0']
        if t < 90: return   # let the face ABP, groom bindings and streaming settle
        a = st['a']; out = {'skeletal': {}, 'grooms': {}}
        for c in a.get_components_by_class(u.SkeletalMeshComponent):
            ai = c.get_anim_instance()
            out['skeletal'][c.get_name()] = {'mesh': c.skeletal_mesh_asset.get_name() if c.skeletal_mesh_asset else None, 'predicted_lod': c.get_predicted_lod_level(), 'visible': c.is_visible(),
                                             'anim_instance': ai.get_class().get_name() if ai else None, 'materials': [c.get_material(i).get_name() if c.get_material(i) else None for i in range(c.get_num_materials())]}
        for g in a.get_components_by_class(u.GroomComponent):
            out['grooms'][g.get_name()] = {'groom': g.groom_asset.get_name() if g.groom_asset else None, 'binding': g.binding_asset.get_name() if g.binding_asset else None, 'visible': g.is_visible(),
                                           'attach_parent': g.get_attach_parent().get_name() if g.get_attach_parent() else None}
            try: out['grooms'][g.get_name()]['num_lods'] = g.get_num_lods()
            except Exception: pass
        info['readback'] = out; info['ticks'] = t; finish()
    except Exception as e:
        info['error'] = repr(e); finish()
hd = u.register_slate_post_tick_callback(tick); print('GD32_PIE_STARTED')
