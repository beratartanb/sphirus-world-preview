"""dbcopy237_bias.py (editor job): candidate copies of a pose-search database with another continuing_pose_cost_bias (the entry list is kept
by duplicate_asset; no clip is edited). builtins.V237_CB = {'src': path, 'copies': [[new_path, bias], ...]}. Prints CB237 {...}."""
import unreal as u, json, builtins
EAL = u.EditorAssetLibrary; c = builtins.V237_CB; out = {'src': c['src'], 'made': []}
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
for p, b in c['copies']:
    if not EAL.does_asset_exist(p): assert EAL.duplicate_asset(c['src'], p), p
    db = u.load_asset(p); db.set_editor_property('continuing_pose_cost_bias', float(b)); ok = EAL.save_asset(p, False)
    out['made'].append({'db': p, 'bias': db.get_editor_property('continuing_pose_cost_bias'), 'entries': db.get_num_animation_assets(), 'saved': ok})
print('CB237 ' + json.dumps(out))
