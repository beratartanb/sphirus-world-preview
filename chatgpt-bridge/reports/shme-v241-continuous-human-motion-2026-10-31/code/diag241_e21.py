"""diag241_e21.py (editor job, write manifest = PSD_SHM240_E21 only) - V2.41 DIAGNOSTIC: keep only the given clips in E21
(builtins.V241_E21 = {'keep': ['SHM239_Tk_R_P10_K2_Opp']}) to separate 'MM picks the wrong contact clip' from 'the query pose is ahead
of the clip time'. Restore = manifest backup. Prints E21D {...}."""
import unreal as u, json, builtins
EAL = u.EditorAssetLibrary
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
c = dict(getattr(builtins, 'V241_E21', {})); P = '/Game/GraceRanger/SHME/Animations/V240/PSD_SHM240_E21'
db = u.load_asset(P); out = {'before': [db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets())], 'methods': [m for m in dir(db) if 'anim' in m.lower()]}
keep = set(c.get('keep', []))
for i in reversed(range(db.get_num_animation_assets())):
    if db.get_animation_asset(i).get_name() not in keep:
        db.remove_animation_asset_at(i)
assert EAL.save_asset(P, False)
out['after'] = [db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets())]
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('E21D ' + json.dumps(out))
