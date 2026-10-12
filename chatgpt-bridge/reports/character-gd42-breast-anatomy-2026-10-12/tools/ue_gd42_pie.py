"""GD38 PIE check (copy of the GD33 job): the saved L_GD38_Eval_G31 is loaded, PIE started, the BP_GD38_Character_G31 instance read back in the GAME
world: groom / binding / visibility, face animation mode + the rest-pose asset, the RigLogic control curve values the face anim instance
evaluates (eyeUpperLidUp L/R expected 0.6), skeletal LODs. PIE stopped, nothing saved. Writes data/pie_check.json."""
import unreal as u, json, pathlib
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/GD42_Breast_20261012/data'
MAP = '/Game/Sphirus/CharacterLab/GD42_Breast_20261012/Maps/L_GD42_Eval_Body'
u.EditorLoadingAndSavingUtils.load_map(MAP)
cls = u.load_asset('/Game/Sphirus/CharacterLab/GD42_Breast_20261012/Assembly/BP_GD42_Character_Body').generated_class()
ues = u.get_editor_subsystem(u.UnrealEditorSubsystem); les = u.get_editor_subsystem(u.LevelEditorSubsystem)
info = {'map': MAP}; st = {'k': 0, 'phase': 'start'}
CURVES = ['CTRL_expressions_eyeUpperLidUpL', 'CTRL_expressions_eyeUpperLidUpR', 'CTRL_expressions_browRaiseInL', 'CTRL_expressions_eyeBlinkL']
def finish():
    u.unregister_slate_post_tick_callback(hd)
    if les.is_in_play_in_editor(): les.editor_request_end_play()
    (O/'pie_check.json').write_text(json.dumps(info, indent=1, default=str)); print('GD42_PIE_DONE', 'error' in info)
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
        if st['k']-st['k0'] < 90: return
        a = st['a']; out = {'skeletal': {}, 'grooms': {}}
        for c in a.get_components_by_class(u.SkeletalMeshComponent):
            ai = c.get_anim_instance(); row = {'mesh': c.skeletal_mesh_asset.get_name() if c.skeletal_mesh_asset else None, 'predicted_lod': c.get_predicted_lod_level(), 'anim_mode': str(c.get_animation_mode()), 'anim_instance': ai.get_class().get_name() if ai else None}
            if c.get_name() == 'Face':
                ad = c.get_editor_property('animation_data'); row['anim_to_play'] = ad.anim_to_play.get_name() if ad.anim_to_play else None
                row['curves'] = {k: (round(ai.get_curve_value(k), 4) if ai else None) for k in CURVES}
            out['skeletal'][c.get_name()] = row
        for g in a.get_components_by_class(u.GroomComponent):
            out['grooms'][g.get_name()] = {'groom': g.groom_asset.get_name() if g.groom_asset else None, 'binding': g.binding_asset.get_name() if g.binding_asset else None, 'visible': g.is_visible(), 'attach_parent': g.get_attach_parent().get_name() if g.get_attach_parent() else None}
        info['readback'] = out; finish()
    except Exception as e:
        info['error'] = repr(e); finish()
hd = u.register_slate_post_tick_callback(tick); print('GD42_PIE_STARTED')
