# w_save_p13.py (write, gated): B13 body + garments wiring (c_b13_wire) + pass-4/5 defaults, compile and save BP_HybridA_Player (+ AC_Sph_Motion).
import unreal as u
assert not u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(), 'PIE running'
D = u.Paths.project_dir()
for p in ('/Game/Sphirus/Player/Motion/AC_Sph_Motion', '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'):
    a = u.load_asset(p); u.BlueprintEditorLibrary.compile_blueprint(a)
exec(open(D + 'Tools/UE59_20261126/c_b13_wire.py', encoding='utf8').read())
exec(open(D + 'Tools/UE59_20261126/c_p5_defaults.py', encoding='utf8').read())
for p in ('/Game/Sphirus/Player/Motion/AC_Sph_Motion', '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'):
    print('SAVEP13', p.split('/')[-1], u.EditorAssetLibrary.save_loaded_asset(u.load_asset(p), False))
print('DIRTY', [x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()])
