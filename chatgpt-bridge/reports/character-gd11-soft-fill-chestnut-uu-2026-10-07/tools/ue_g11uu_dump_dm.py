"""pass UU: dump the LOD0 source-model vertex positions of a face SKM (GeometryScript dynamic-mesh order) to json."""
import unreal as u, json, builtins
C = builtins.G11UU_DUMP; q = u.GeometryScript_MeshQueries; l = u.GeometryScript_List
dm = u.DynamicMesh(); lod = u.GeometryScriptMeshReadLOD(); lod.lod_type = u.GeometryScriptLODType.SOURCE_MODEL; lod.lod_index = 0
u.GeometryScript_AssetUtils.copy_mesh_from_skeletal_mesh(u.load_asset(C['face']), dm, u.GeometryScriptCopyMeshFromAssetOptions(), lod)
P = l.convert_vector_list_to_array(q.get_all_vertex_positions(dm, False)[1]); json.dump([[round(p.x, 5), round(p.y, 5), round(p.z, 5)] for p in P], open(C['out'], 'w'))
print('DUMP_DM', len(P))
