"""GD32 assembly, finishing step: LevelEditorSubsystem.new_level() saved an EMPTY L_GD32_Eval_G31 but left the editor in /Temp/Untitled_1, where
ue_gd32_assembly.py then placed the character, studio rig and cameras (save_current_level refused: no filename). This step checks that the
editor world is that untitled world with the GD32 actors, removes the empty map created minutes earlier by the same job (GD32 folder, no
actors), saves the untitled world as L_GD32_Eval_G31 and writes the read-back (data/assembly_check.json)."""
import unreal as u, json, pathlib, os
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/GD32_Identity_20261011/data'
G = '/Game/Sphirus/CharacterLab/GD32_IdentityMaster_20261011'; BP_PATH = G+'/Assembly/BP_GD32_Character_G31'; MAP_PATH = G+'/Maps/L_GD32_Eval_G31'
EAL = u.EditorAssetLibrary; eas = u.get_editor_subsystem(u.EditorActorSubsystem); world = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
labels = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
assert world.get_path_name().startswith('/Temp/'), world.get_path_name()
assert 'GD32_Character_G31' in labels and 'CAM_REF_front' in labels and 'LKQA_key' in labels, sorted(labels)[:20]
f = R/'Content/Sphirus/CharacterLab/GD32_IdentityMaster_20261011/Maps/L_GD32_Eval_G31.umap'; assert f.stat().st_size < 60000, f.stat().st_size
assert EAL.delete_asset(MAP_PATH) and not EAL.does_asset_exist(MAP_PATH), 'could not remove the empty map'
assert u.EditorLoadingAndSavingUtils.save_map(world, MAP_PATH), 'save_map failed'
sds = u.get_engine_subsystem(u.SubobjectDataSubsystem); BFL = u.SubobjectDataBlueprintFunctionLibrary; chk = {'blueprint': BP_PATH, 'map': MAP_PATH, 'components': {}}
for hdl in sds.k2_gather_subobject_data_for_blueprint(u.load_asset(BP_PATH)):
    o = BFL.get_object(BFL.get_data(hdl))
    if isinstance(o, u.SkeletalMeshComponent):
        chk['components'][o.get_name()] = {'mesh': o.get_editor_property('skeletal_mesh_asset').get_path_name(), 'forced_lod_model': o.get_editor_property('forced_lod_model'),
            'override_materials': {i: m.get_name() for i, m in enumerate(o.get_editor_property('override_materials')) if m}, 'anim_mode': str(o.get_editor_property('animation_mode')), 'anim_class': str(o.get_editor_property('anim_class'))}
    elif isinstance(o, u.GroomComponent):
        chk['components'][o.get_name()] = {'groom': o.get_editor_property('groom_asset').get_path_name(), 'binding': o.get_editor_property('binding_asset').get_path_name()}
world = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world(); chk['saved_world'] = world.get_path_name()
acts = eas.get_all_level_actors(); chk['level_actors'] = sorted(a.get_actor_label() for a in acts); cams = {}
for a in acts:
    if a.get_actor_label().startswith('CAM_'):
        l = a.get_actor_location(); r = a.get_actor_rotation(); cams[a.get_actor_label()] = [round(l.x, 3), round(l.y, 3), round(l.z, 3), round(r.yaw, 3), round(r.pitch, 3), a.get_component_by_class(u.CameraComponent).field_of_view]
chk['cameras'] = dict(sorted(cams.items())); chk['map_file_bytes'] = f.stat().st_size if f.exists() else None
(O/'assembly_check.json').write_text(json.dumps(chk, indent=1, default=str)); print('GD32_ASSEMBLY_FINISH_OK', chk['saved_world'], len(chk['level_actors']), len(cams))
