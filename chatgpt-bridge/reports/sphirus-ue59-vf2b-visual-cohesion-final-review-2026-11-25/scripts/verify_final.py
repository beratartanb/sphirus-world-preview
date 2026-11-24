# VF2B read-only verification after a clean editor reopen: everything this session saved, read from disk-loaded assets.
import unreal as u, re
mel = u.MaterialEditingLibrary
bp = u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'); cdo = u.get_default_object(bp.generated_class())
print('VFIN outfit top', [x.get_name() if x else None for x in cdo.get_editor_property('GR_OutfitTop')]); print('VFIN outfit low', [x.get_name() if x else None for x in cdo.get_editor_property('GR_OutfitLow')])
sds = u.get_engine_subsystem(u.SubobjectDataSubsystem)
for h in sds.k2_gather_subobject_data_for_blueprint(bp):
    o = u.SubobjectDataBlueprintFunctionLibrary.get_object(sds.k2_find_subobject_data_from_handle(h))
    if o and o.get_name().replace('_GEN_VARIABLE', '') == 'HairMain2': print('VFIN hair', o.get_editor_property('groom_asset').get_name(), re.search(r'bEnableSimulation=\w+', o.get_editor_property('simulation_settings').export_text()).group(0))
G = '/Game/Sphirus/CharacterLab/VF2_20261124/Garments/'
for n in ('SKM_Sph_RetroTop_VF2', 'SKM_Sph_CuffedShorts_VF2'):
    m = u.load_asset(G + n); print('VFIN', n, 'verts', u.get_editor_subsystem(u.SkeletalMeshEditorSubsystem).get_num_verts(m, 0), [x.material_interface.get_name() for x in m.materials], 'skel', m.skeleton.get_name())
print('VFIN shorts base usedWithSkeletalMesh', u.load_asset(G + 'M_Sph_CuffedShorts_VF2').get_editor_property('used_with_skeletal_mesh'), '| fabric shading', str(u.load_asset(G + 'M_Sph_Fabric_VF2').get_editor_property('shading_model')).split('.')[-1])
I = '/Game/SphirusHouse/LivedIn_R05/Materials/Instances/'
for n in ('MI_R3_Surface_lime', 'MI_R3_hearth_OriginalAtlas', 'MI_R3_Surface_masonry', 'MI_BR_ExteriorDeck'):
    m = u.load_asset(I + n); print('VFIN', n, 'parent', m.get_editor_property('parent').get_name(), {str(k): round(mel.get_material_instance_scalar_parameter_value(m, k), 2) for k in mel.get_scalar_parameter_names(m) if str(k) in ('MacroAmount', 'GrimeAmount', 'ReliefStrength', 'SootAmount', 'AshAmount')})
c = mel.get_material_instance_vector_parameter_value(u.load_asset('/Game/GraceRanger/Environment/GroundLayer20261111/Materials/MI_GL_GrassMedium01'), 'Translucency Color'); print('VFIN grass translucency', [round(v, 3) for v in (c.r, c.g, c.b)])
v = u.load_asset('/Game/Grooms/001_Messy_Bob/001_Messy_Bob/001_Messy_Bob'); print('VFIN vendor groom untouched', re.search(r'GravityPreloading=[0-9.]+', v.get_editor_property('hair_groups_physics')[0].export_text()).group(0))
print('VFIN dirty', [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()], [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()], '| level', u.EditorLevelLibrary.get_editor_world().get_name(), '| VF2H actors', len([a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors() if a.get_actor_label().startswith('VF2H_')]))
