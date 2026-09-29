"""READ-ONLY: extract exact source-model LOD0 topology, UV sets, material IDs and reference skeleton of the current
BodyRealism candidate meshes for the Blender artist-sculpt round-trip. Saves nothing."""
import unreal as u, json, pathlib, gzip, time
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/BodyRealismArtist_20260929/extract'; O.mkdir(parents=True, exist_ok=True)
q = u.GeometryScript_MeshQueries; l = u.GeometryScript_List; UV = u.GeometryScript_UVs
MESH = {'Body': '/Game/Sphirus/CharacterLab/BodyRealism_20260929/SKM_BR_BodyMesh', 'Head': '/Game/Sphirus/CharacterLab/BodyRealism_20260929/SKM_BR_FaceMesh'}
def pick(r, typ):
    r = r if isinstance(r, tuple) else (r,)
    return [x for x in r if isinstance(x, typ)][0]
rep = {}
for part, path in MESH.items():
    t0 = time.time(); m = u.load_asset(path)
    dm = u.DynamicMesh(); lod = u.GeometryScriptMeshReadLOD(); lod.lod_type = u.GeometryScriptLODType.SOURCE_MODEL; lod.lod_index = 0
    r = u.GeometryScript_AssetUtils.copy_mesh_from_skeletal_mesh(m, dm, u.GeometryScriptCopyMeshFromAssetOptions(), lod); assert 'SUCCESS' in str(r[-1])
    V = l.convert_vector_list_to_array(q.get_all_vertex_positions(dm, False)[1])
    T = l.convert_triangle_list_to_array(q.get_all_triangle_indices(dm, False)[1])
    tid = q.get_all_triangle_i_ds(dm); tid = l.convert_index_list_to_array(pick(tid, u.GeometryScriptIndexList))
    vid = l.convert_index_list_to_array(pick(q.get_all_vertex_i_ds(dm), u.GeometryScriptIndexList))
    d = {'positions': [[v.x, v.y, v.z] for v in V], 'triangles': [[t.x, t.y, t.z] for t in T],
         'compact': {'vid': list(vid) == list(range(len(V))), 'tid': list(tid) == list(range(len(T)))}}
    nuv = int(pick(q.get_num_uv_sets(dm), int)) if isinstance(q.get_num_uv_sets(dm), tuple) else int(q.get_num_uv_sets(dm))
    d['uv_sets'] = []
    for s in range(nuv):
        tri_el = []
        for ti in range(len(T)):
            iv = pick(UV.get_mesh_triangle_uv_element_i_ds(dm, s, ti), u.IntVector); tri_el.append([iv.x, iv.y, iv.z])
        ids = sorted({e for t in tri_el for e in t}); pos = {}
        for e in ids:
            rr = UV.get_mesh_uv_element_position(dm, s, e); v2 = pick(rr, u.Vector2D); pos[e] = [v2.x, v2.y]
        d['uv_sets'].append({'tri_elements': tri_el, 'elements': {str(k): v for k, v in pos.items()}})
    try:
        mid = u.GeometryScript_Materials.get_all_triangle_material_i_ds(dm)
        d['material_ids'] = list(l.convert_index_list_to_array(pick(mid, u.GeometryScriptIndexList)))
    except Exception as e: d['material_ids_error'] = str(e)
    d['materials'] = [str(s.get_editor_property('material_slot_name')) for s in m.get_editor_property('materials')]
    sk = m.get_editor_property('skeleton'); pose = u.AnimPoseExtensions.get_reference_pose(sk)
    names = [str(n) for n in u.AnimPoseExtensions.get_bone_names(pose)]; bones = []
    for n in names:
        x = u.AnimPoseExtensions.get_ref_bone_pose(pose, n, u.AnimPoseSpaces.WORLD)
        loc = x.translation; rq = x.rotation
        try: par = str(m.get_bone_parent(n))
        except Exception as e: par = 'ERR:'+str(e)
        bones.append({'name': n, 'parent': par, 't': [loc.x, loc.y, loc.z], 'q': [rq.x, rq.y, rq.z, rq.w]})
    d['skeleton'] = {'path': sk.get_path_name(), 'bones': bones}
    with gzip.open(O/f'{part}_topology_uv_skel.json.gz', 'wt') as f: json.dump(d, f, separators=(',', ':'))
    rep[part] = {'verts': len(V), 'tris': len(T), 'compact': d['compact'], 'uv_sets': nuv,
                 'uv_elements': [len(s['elements']) for s in d['uv_sets']], 'materials': d['materials'],
                 'mat_ids': len(d.get('material_ids', [])), 'mat_err': d.get('material_ids_error'), 'bones': len(bones),
                 'parent_sample': bones[1]['parent'] if len(bones) > 1 else None, 'sec': round(time.time()-t0, 1)}
    print(part, rep[part], flush=True)
rep['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
(O/'extract_report.json').write_text(json.dumps(rep, indent=1)); print(json.dumps(rep, indent=1))
