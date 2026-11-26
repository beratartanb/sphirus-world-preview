# dump_uv.py (control, read-only): LOD0 positions, triangles and per-vertex UV0 of skeletal meshes -> json (builtins.DUV = [(path, out)])
import unreal as u, json, builtins
Q = u.GeometryScript_MeshQueries; L = u.GeometryScript_List; UV = u.GeometryScript_UVs
def pick(res, cls):
    for x in (res if isinstance(res, (tuple, list)) else [res]):
        if isinstance(x, cls): return x
for path, out in builtins.DUV:
    m = u.load_asset(path); dm = u.DynamicMesh(); lod = u.GeometryScriptMeshReadLOD(); lod.lod_type = u.GeometryScriptLODType.SOURCE_MODEL; lod.lod_index = 0
    u.GeometryScript_AssetUtils.copy_mesh_from_skeletal_mesh(m, dm, u.GeometryScriptCopyMeshFromAssetOptions(), lod)
    P = L.convert_vector_list_to_array(Q.get_all_vertex_positions(dm, False)[1])
    T = L.convert_triangle_list_to_array(pick(Q.get_all_triangle_indices(dm, False), u.GeometryScriptTriangleList))
    U = L.convert_uv_list_to_array(pick(UV.get_mesh_per_vertex_u_vs(dm, 0), u.GeometryScriptUVList))
    json.dump({'path': path, 'skel': m.skeleton.get_path_name(), 'v': [[round(p.x, 4), round(p.y, 4), round(p.z, 4)] for p in P], 't': [[t.x, t.y, t.z] for t in T],
               'uv': [[round(q.x, 6), round(q.y, 6)] for q in U]}, open(out, 'w'))
    print('DUV', path.split('/')[-1], len(P), len(T), len(U), m.skeleton.get_path_name())
