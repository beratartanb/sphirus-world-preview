"""GD45 cleanup: the garments now follow Manny through the construction-script leader pose; their interim anim class (retarget ABP) is redundant -> None. Compile + save owner and children."""
import unreal as u, json
sds = u.get_engine_subsystem(u.SubobjectDataSubsystem); BFL = u.SubobjectDataBlueprintFunctionLibrary; EAL = u.EditorAssetLibrary
bp = u.load_asset('/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/BP_Player_MM'); done = []
for h in sds.k2_gather_subobject_data_for_blueprint(bp):
    o = BFL.get_object(BFL.get_data(h))
    if o is None or not isinstance(o, u.SkeletalMeshComponent): continue
    nm = o.get_name().replace('_GEN_VARIABLE', '')
    if nm in ('Henley', 'Shorts'): o.modify(); o.set_editor_property('anim_class', None); done.append(nm)
u.BlueprintEditorLibrary.compile_blueprint(bp); ok = EAL.save_loaded_asset(bp, False)
for p in ('/Game/GraceRanger/BP_GR_Player', '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'):
    b2 = u.load_asset(p); u.BlueprintEditorLibrary.compile_blueprint(b2); EAL.save_loaded_asset(b2, False)
print('GD45_CLEAR', json.dumps({'cleared': done, 'saved': ok, 'dirty': [str(x.get_path_name()) for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()][:10]}), flush=True)
