"""READ-ONLY: compare source-model LOD0 vertex/triangle lists along the candidate chain (no save)."""
import unreal as u, json, pathlib, hashlib
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/BodyRealismArtist_20260929/extract'
q = u.GeometryScript_MeshQueries; l = u.GeometryScript_List
ar = u.AssetRegistryHelpers.get_asset_registry()
cands = []
for root in ['/Game/Sphirus/CharacterLab', '/Game/Character/MainCharacter']:
    for a in ar.get_assets_by_path(root, recursive=True):
        if str(a.asset_class_path.asset_name) == 'SkeletalMesh': cands.append(str(a.package_name)+'.'+str(a.asset_name))
res = {}
for p in cands:
    try:
        m = u.load_asset(p); dm = u.DynamicMesh(); lod = u.GeometryScriptMeshReadLOD(); lod.lod_type = u.GeometryScriptLODType.SOURCE_MODEL; lod.lod_index = 0
        r = u.GeometryScript_AssetUtils.copy_mesh_from_skeletal_mesh(m, dm, u.GeometryScriptCopyMeshFromAssetOptions(), lod)
        V = l.convert_vector_list_to_array(q.get_all_vertex_positions(dm, False)[1]); T = l.convert_triangle_list_to_array(q.get_all_triangle_indices(dm, False)[1])
        th = hashlib.sha1(json.dumps([[t.x, t.y, t.z] for t in T]).encode()).hexdigest()[:12]
        vh = hashlib.sha1(json.dumps([[round(v.x, 4), round(v.y, 4), round(v.z, 4)] for v in V]).encode()).hexdigest()[:12]
        res[p] = {'v': len(V), 't': len(T), 'tri_hash': th, 'pos_hash': vh}
    except Exception as e: res[p] = {'err': str(e)[:200]}
res['_dirty'] = [x.get_path_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
(O/'tri_trace.json').write_text(json.dumps(res, indent=1)); print(json.dumps(res, indent=1))
