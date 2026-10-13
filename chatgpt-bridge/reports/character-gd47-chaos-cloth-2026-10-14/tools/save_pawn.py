"""GD47: compile + save BP_Player_MM (after the MCP construction-script edit) and its two child Blueprints; report dirty packages."""
import unreal as u, json
EAL = u.EditorAssetLibrary; rep = {}
for p in ('/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/BP_Player_MM', '/Game/GraceRanger/BP_GR_Player', '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'):
    b = u.load_asset(p); u.BlueprintEditorLibrary.compile_blueprint(b); rep[p.rsplit('/', 1)[-1]] = EAL.save_loaded_asset(b, False)
rep['dirty'] = [str(x.get_path_name()) for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()][:10]
print('GD47_SAVE', json.dumps(rep), flush=True)
