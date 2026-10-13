import unreal as u, json
bp = u.load_asset('/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/BP_Player_MM'); u.BlueprintEditorLibrary.compile_blueprint(bp); ok = u.EditorAssetLibrary.save_loaded_asset(bp, False)
for p in ('/Game/GraceRanger/BP_GR_Player', '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'):
    b2 = u.load_asset(p); u.BlueprintEditorLibrary.compile_blueprint(b2); u.EditorAssetLibrary.save_loaded_asset(b2, False)
print('GD45_SAVE', json.dumps({'saved': ok, 'dirty': [str(x.get_path_name()) for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()][:10]}), flush=True)
