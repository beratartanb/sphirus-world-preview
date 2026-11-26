# reopen_p6.py (control, read-only): state after a restart - B13 body/garments, bun hair + scalp cover, pass-5 values.
import unreal as u
bp = u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'); c = u.get_default_object(bp.generated_class())
print('REOPEN6 vals', {k: round(c.get_editor_property(k), 2) for k in ('PS_ShL', 'PS_ShF', 'PS_B3', 'TR_PkDecay', 'TR_On', 'SH_On', 'ATH_On', 'AW_On', 'CS_On')})
print('REOPEN6 outfits', sorted({x.get_name() for x in c.get_editor_property('GR_OutfitTop')} | {x.get_name() for x in c.get_editor_property('GR_OutfitLow')}))
sub = u.get_engine_subsystem(u.SubobjectDataSubsystem); out = {}
for h in sub.k2_gather_subobject_data_for_blueprint(bp):
    o = u.SubobjectDataBlueprintFunctionLibrary.get_object(sub.k2_find_subobject_data_from_handle(h)); n = o.get_name().split('_GEN')[0]
    if isinstance(o, u.SkeletalMeshComponent): out[n] = o.get_skeletal_mesh_asset().get_name() if o.get_skeletal_mesh_asset() else None
    elif isinstance(o, u.GroomComponent): out[n] = (o.get_editor_property('groom_asset').get_name() if o.get_editor_property('groom_asset') else None, o.get_editor_property('binding_asset').get_name() if o.get_editor_property('binding_asset') else None)
    elif isinstance(o, u.StaticMeshComponent): out[n] = o.get_editor_property('static_mesh').get_name() if o.get_editor_property('static_mesh') else None
print('REOPEN6 comps', out)
G = u.GeometryScript_AssetUtils; dm = u.DynamicMesh(); lod = u.GeometryScriptMeshReadLOD(); lod.lod_type = u.GeometryScriptLODType.SOURCE_MODEL
G.copy_mesh_from_skeletal_mesh(u.load_asset('/Game/Sphirus/CharacterLab/B13_20261126/Body/SKM_Sph_B13_BodyMesh'), dm, u.GeometryScriptCopyMeshFromAssetOptions(), lod)
print('REOPEN6 body verts', len(u.GeometryScript_List.convert_vector_list_to_array(u.GeometryScript_MeshQueries.get_all_vertex_positions(dm, False)[1])))
print('REOPEN6 dirty', [x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()])
