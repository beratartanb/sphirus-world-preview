"""GD46: point the in-game pawn's Henley component (owner BP_Player_MM) at the re-settled garment mesh. Checkpoint copies of the three Blueprints
are taken by the chain script BEFORE this job runs. Sets Henley.skeletal_mesh_asset, keeps every other component unchanged, compiles and saves the
owner + the two child Blueprints. builtins.GD46_HENLEY = '/Game/...'. Writes data/swap_henley.json."""
import unreal as u, json, builtins, pathlib
NEW = builtins.GD46_HENLEY; R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/GD46_GarmentFit_20261013/data'
sds = u.get_engine_subsystem(u.SubobjectDataSubsystem); BFL = u.SubobjectDataBlueprintFunctionLibrary; EAL = u.EditorAssetLibrary
BP = '/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/BP_Player_MM'; bp = u.load_asset(BP); new = u.load_asset(NEW); assert new, NEW
rep = {'new': NEW, 'new_lods': None, 'new_materials': [str(m.material_slot_name) + ':' + (m.material_interface.get_name() if m.material_interface else 'None') for m in new.get_editor_property('materials')], 'new_morphs': [str(m) for m in new.get_all_morph_target_names()]}
objs = {}
for h in sds.k2_gather_subobject_data_for_blueprint(bp):
    o = BFL.get_object(BFL.get_data(h))
    if o is not None and isinstance(o, u.SkeletalMeshComponent): objs[o.get_name().replace('_GEN_VARIABLE', '')] = o
c = objs['Henley']; rep['before'] = c.get_skeletal_mesh_asset().get_path_name() if c.get_skeletal_mesh_asset() else None
c.modify(); c.set_skeletal_mesh_asset(new); rep['after'] = c.get_skeletal_mesh_asset().get_path_name()
rep['henley_props'] = {k: str(c.get_editor_property(k)) for k in ('anim_class', 'animation_mode', 'leader_pose_component', 'use_attach_parent_bound', 'visible')}
rep['shorts'] = objs['Shorts'].get_skeletal_mesh_asset().get_path_name() if 'Shorts' in objs and objs['Shorts'].get_skeletal_mesh_asset() else None
u.BlueprintEditorLibrary.compile_blueprint(bp); rep['owner_saved'] = EAL.save_loaded_asset(bp, False)
for p in ('/Game/GraceRanger/BP_GR_Player', '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'):
    b2 = u.load_asset(p); u.BlueprintEditorLibrary.compile_blueprint(b2); rep[p.rsplit('/', 1)[-1] + '_saved'] = EAL.save_loaded_asset(b2, False)
rep['dirty_after'] = [str(x.get_path_name()) for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()][:10]
json.dump(rep, open(O/'swap_henley.json', 'w'), indent=1); print('GD46_SWAP', json.dumps(rep)[:900], flush=True)
