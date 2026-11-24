# VF2B write job: project-owned copy of the shorts base material with the skeletal-mesh usage flag stored on disk
# (the vendor base has used_with_skeletal_mesh=False, so a packaged build would fall back to the default material).
import unreal as u
E = u.EditorAssetLibrary; mel = u.MaterialEditingLibrary
assert not u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(), 'PIE running'
D = '/Game/Sphirus/CharacterLab/VF2_20261124/Garments/'
vs = u.load_asset('/Game/Outfits/Relaxed_Cuffed_Shorts/Relaxed_Cuffed_Shorts/MT/MI_Relaxed_Cuffed_Shorts'); vb = vs.get_base_material()
print('F2 vendor switches', [str(n) for n in mel.get_static_switch_parameter_names(vs)], 'vendor base flags skel', vb.get_editor_property('used_with_skeletal_mesh'), 'morph', vb.get_editor_property('used_with_morph_targets'))
BP = D + 'M_Sph_CuffedShorts_VF2'
nb = u.load_asset(BP) if E.does_asset_exist(BP) else E.duplicate_asset(vb.get_path_name().split('.')[0], BP)
assert nb, 'duplicate failed'
nb.set_editor_property('used_with_skeletal_mesh', True); mel.recompile_material(nb)
ms = u.load_asset(D + 'MI_Sph_CuffedShorts_VF2'); mel.clear_all_material_instance_parameters(ms); mel.set_material_instance_parent(ms, nb)
for n in mel.get_scalar_parameter_names(vs): mel.set_material_instance_scalar_parameter_value(ms, n, mel.get_material_instance_scalar_parameter_value(vs, n))
for n in mel.get_vector_parameter_names(vs): mel.set_material_instance_vector_parameter_value(ms, n, mel.get_material_instance_vector_parameter_value(vs, n))
mel.set_material_instance_vector_parameter_value(ms, 'COLOR2', u.LinearColor(0.070, 0.078, 0.058, 1.0))
mel.set_material_instance_vector_parameter_value(ms, 'COLOR3', u.LinearColor(0.120, 0.105, 0.085, 1.0))
mel.set_material_instance_scalar_parameter_value(ms, 'Roughness', 0.88); mel.set_material_instance_scalar_parameter_value(ms, 'STAIN', 0.16)
mel.set_material_instance_vector_parameter_value(ms, 'STAINCOLOR', u.LinearColor(0.42, 0.36, 0.28, 1.0))
mel.update_material_instance(ms)
print('F2 new base flag', nb.get_editor_property('used_with_skeletal_mesh'), 'mi parent', ms.get_editor_property('parent').get_name())
for a in ('M_Sph_CuffedShorts_VF2', 'MI_Sph_CuffedShorts_VF2'): print('F2 saved', a, E.save_loaded_asset(u.load_asset(D + a), False))
print('F2 dirty', [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()])
