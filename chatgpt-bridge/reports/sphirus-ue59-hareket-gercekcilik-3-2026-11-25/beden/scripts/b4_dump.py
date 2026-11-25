# b4_dump.py (control, read-only): dumps a skeletal mesh source model (all LODs): vertex positions, triangles, UV0 per triangle corner
# is NOT needed; per-vertex top-4 bone weights (names), reference-pose component-space bone positions.
# builtins.B4_DUMP = {'mesh': path, 'out': abs json path, 'lods': [0,1,..]}
import unreal as u, json, builtins
C = builtins.B4_DUMP; m = u.load_asset(C['mesh']); q = u.GeometryScript_MeshQueries; l = u.GeometryScript_List; BW = u.GeometryScript_BoneWeights if hasattr(u, 'GeometryScript_BoneWeights') else None
out = {'mesh': C['mesh'], 'lods': {}}
def fresh(i):
    dm = u.DynamicMesh(); lod = u.GeometryScriptMeshReadLOD(); lod.lod_type = u.GeometryScriptLODType.SOURCE_MODEL; lod.lod_index = i
    r = u.GeometryScript_AssetUtils.copy_mesh_from_skeletal_mesh(m, dm, u.GeometryScriptCopyMeshFromAssetOptions(), lod); return dm, str(r)
sk = m.skeleton; ref = sk.get_reference_pose()
names = [str(n) for n in ref.get_bone_names()] if hasattr(ref, 'get_bone_names') else []
out['bones'] = {}
for n in names:
    try: t = ref.get_ref_bone_pose(n, u.AnimPoseSpaces.WORLD); p = t.translation; out['bones'][n] = [p.x, p.y, p.z]
    except Exception as e: out['bones_err'] = repr(e)[:200]; break
for i in C['lods']:
    dm, r = fresh(i)
    if 'SUCCESS' not in r: out['lods'][str(i)] = {'err': r[:200]}; continue
    P = l.convert_vector_list_to_array(q.get_all_vertex_positions(dm, False)[1])
    T = [list(x) for x in [(t.x, t.y, t.z) for t in l.convert_index_list_to_array(q.get_all_triangle_ids(dm)[1])]] if False else None
    tris = []
    tl = q.get_all_triangle_indices(dm, False) if hasattr(q, 'get_all_triangle_indices') else None
    if tl is not None:
        arr = l.convert_triangle_list_to_array(tl[1] if isinstance(tl, tuple) else tl)
        tris = [[t.x, t.y, t.z] for t in arr]
    d = {'v': [[round(p.x, 4), round(p.y, 4), round(p.z, 4)] for p in P], 't': tris}
    if i == 0 and BW:
        try:
            bi = BW.get_all_bones_info(dm); bi = [x for x in (bi if isinstance(bi, (list, tuple, u.Array)) else [bi]) if isinstance(x, (list, u.Array))]
            bi = bi[0] if bi else []
            d['mesh_bones'] = [str(b.name) for b in bi]
            d['mesh_bone_world'] = [[b.global_transform.translation.x, b.global_transform.translation.y, b.global_transform.translation.z] for b in bi] if bi and hasattr(bi[0], 'global_transform') else []
        except Exception as e: d['mesh_bones_err'] = repr(e)[:200]
        W = []; err = None
        for vi in range(len(P)):
            try:
                r2 = BW.get_vertex_bone_weights(dm, vi, u.GeometryScriptBoneWeightProfile())
                ws = [x for x in (r2 if isinstance(r2, (list, tuple, u.Array)) else []) if hasattr(x, 'bone_index')]
                if not ws and isinstance(r2, tuple): ws = [x for y in r2 if isinstance(y, (list, u.Array)) for x in y]
                W.append([[int(x.bone_index), round(float(x.weight), 3)] for x in sorted(ws, key=lambda x: -x.weight)[:4]])
            except Exception as e: err = repr(e)[:200]; break
        d['w'] = W; d['w_err'] = err
    out['lods'][str(i)] = d
out['bone_index_names'] = names
json.dump(out, open(C['out'], 'w')); print('B4DUMP', C['mesh'].split('/')[-1], {k: (len(v.get('v', [])), len(v.get('t', [])), len(v.get('w', []) if 'w' in v else []), v.get('w_err') or v.get('err')) for k, v in out['lods'].items()}, 'bones', len(out['bones']), out.get('bones_err'))
