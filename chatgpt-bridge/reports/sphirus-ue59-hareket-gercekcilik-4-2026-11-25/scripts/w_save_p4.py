# w_save_p4.py (write, gated): movement pass 4 - applies c_p4_defaults, compiles and saves AC_Sph_Motion and BP_HybridA_Player
# (AC_Sph_Traversal was saved by w_trav_create). Pass-3 values are asserted, not rewritten.
import unreal as u
assert not u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(), 'PIE running'
exec(open(u.Paths.project_dir() + 'Tools/UE59_20261125/c_p4_defaults.py', encoding='utf8').read())
c = u.get_default_object(u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player').generated_class())
assert c.get_editor_property('CS_On') == 1.0 and c.get_editor_property('CA_On') == 1.0 and c.get_editor_property('TLM_On') == 1.0
for p in ('/Game/Sphirus/Player/Motion/AC_Sph_Motion', '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'):
    a = u.load_asset(p); u.BlueprintEditorLibrary.compile_blueprint(a)
    if 'HybridA' in p: exec(open(u.Paths.project_dir() + 'Tools/UE59_20261125/c_p4_defaults.py', encoding='utf8').read())
    print('SAVEP4', p.split('/')[-1], u.EditorAssetLibrary.save_loaded_asset(a, False))
print('DIRTY', [x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()], 'MAPS', [x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()])
