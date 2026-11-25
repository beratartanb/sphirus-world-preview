# VF2C read-only verification after a clean editor reopen: everything this pass saved, read from disk-loaded assets and the reopened map.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/UE59_20261119/b59.py',encoding='utf8').read())
import unreal as u, re
mel = u.MaterialEditingLibrary; T_ = u.BlueprintToolset
a = u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Face/ABP_Hazel_Face')
print('VC face ABP variables', [str(v.name) for v in T_.list_variables(a, None)], '| anim graph nodes', len(T_.find_nodes(T_.get_graph(a, 'AnimGraph'))), '| event graph nodes', len(T_.find_nodes(T_.get_graph(a, 'EventGraph'))))
G = '/Game/Sphirus/CharacterLab/VF2_20261124/Garments/'
for n in ('SKM_Sph_RetroTop_VF2', 'SKM_Sph_CuffedShorts_VF2'):
    m = u.load_asset(G + n); b = m.get_bounds(); print('VC', n, 'verts', u.get_editor_subsystem(u.SkeletalMeshEditorSubsystem).get_num_verts(m, 0), 'half width %.1f' % b.box_extent.x, [x.material_interface.get_name() for x in m.materials])
mpc = u.load_asset(G + 'MPC_Sph_Cloth'); print('VC cloth collection', [str(p.get_editor_property('parameter_name')) for p in mpc.get_editor_property('vector_parameters')])
for n in ('MI_Sph_RetroTop_VF2', 'MI_Sph_CuffedShorts_VF2'):
    x = u.load_asset(G + n); print('VC', n, {k: round(mel.get_material_instance_scalar_parameter_value(x, k), 4) for k in ('MotionInertia', 'MotionDrag', 'MotionMax', 'MotionFlutter')}, 'WPO node', bool(mel.get_material_property_input_node(x.get_base_material(), u.MaterialProperty.MP_WORLD_POSITION_OFFSET)))
bp = u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'); cdo = u.get_default_object(bp.generated_class())
print('VC outfit', [x.get_name() if x else None for x in cdo.get_editor_property('GR_OutfitTop')][1], [x.get_name() if x else None for x in cdo.get_editor_property('GR_OutfitLow')][1])
for p in ('/Game/SphirusHouse/LivedIn_R05/Materials/Instances/MI_R3_Surface_lime', '/Game/SphirusHouse/LivedIn_R05/Materials/Instances/MI_R3_hearth_OriginalAtlas', '/Game/SphirusHouse/LivedIn_R05/Materials/Instances/MI_R3_Surface_masonry',
          '/Game/GraceRanger/Environment/Exterior20260921/Materials/MI_EX_Integration_OuterLimeOak', '/Game/GraceRanger/Environment/Exterior20260921/Materials/MI_EX_Integration_OuterLime', '/Game/SphirusHouse/LivedIn_R05/Materials/Instances/MI_BR_ExteriorDeck'):
    m = u.load_asset(p); par = m.get_editor_property('parent')
    try: s = mel.get_statistics(par); st = (s.num_pixel_shader_instructions, s.num_samplers)
    except Exception as e: st = 'compile?'
    print('VC', p.split('/')[-1], 'parent', par.get_name(), 'pixel instr/samplers', st)
acts = u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()
vf = [(x.get_actor_label(), x.static_mesh_component.get_editor_property('static_mesh').get_name(), [round(v) for v in (x.get_actor_location().x, x.get_actor_location().y, x.get_actor_location().z)]) for x in acts if x.get_actor_label().startswith('VF2C_')]
print('VC dressing actors', len(vf), vf)
n = 0
for x in acts:
    if isinstance(x, u.InstancedFoliageActor):
        for c in x.get_components_by_class(u.InstancedStaticMeshComponent): n += c.get_instance_count()
print('VC foliage instances', n, '(38474 before this pass) | actors', len(acts), '(1483 before)')
print('VC dirty', [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()], [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()], '| level', u.EditorLevelLibrary.get_editor_world().get_name())
