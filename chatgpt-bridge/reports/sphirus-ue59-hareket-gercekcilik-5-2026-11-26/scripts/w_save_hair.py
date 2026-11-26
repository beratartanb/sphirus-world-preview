# w_save_hair.py (write, gated): c_hair_bun (bun hair on the player), compile and save BP_HybridA_Player.
import unreal as u
assert not u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(), 'PIE running'
D = u.Paths.project_dir(); P = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'
exec(open(D + 'Tools/UE59_20261126/c_hair_bun.py', encoding='utf8').read())
a = u.load_asset(P); u.BlueprintEditorLibrary.compile_blueprint(a)
print('SAVEHAIR', u.EditorAssetLibrary.save_loaded_asset(a, False)); print('DIRTY', [x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()])
