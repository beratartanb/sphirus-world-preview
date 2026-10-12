"""GD40 (copy of ue_lk_bake_body.py): bake the GD40 body tone morph (morph_gd40_body_lod<L>.json, 'Body' part) into the isolated SKM_GD40_BodyMesh, LOD 0..3
(same method as rv_ue_bake.py: position deltas + local normal-delta recompute inside the morph region). Base geometry is
verified unchanged. builtins.GD40_BODY_DIR = <abs dir with the json files>."""
import unreal as u, pathlib, json, math, builtins
D = pathlib.Path(builtins.GD40_BODY_DIR); MESH = "/Game/Sphirus/CharacterLab/GD40_Body_20261012/Body/SKM_GD40_BodyMesh"
q = u.GeometryScript_MeshQueries; l = u.GeometryScript_List; N = u.GeometryScript_Normals; Sel = u.GeometryScript_MeshSelection
def pick(r, typ):
    r = r if isinstance(r, tuple) else (r,); return [x for x in r if isinstance(x, typ)][0]
def fresh(m, L):
    dm = u.DynamicMesh(); lod = u.GeometryScriptMeshReadLOD(); lod.lod_type = u.GeometryScriptLODType.SOURCE_MODEL; lod.lod_index = L
    r = u.GeometryScript_AssetUtils.copy_mesh_from_skeletal_mesh(m, dm, u.GeometryScriptCopyMeshFromAssetOptions(), lod); assert 'SUCCESS' in str(r[-1]), r; return dm
def vnormals(dm): return l.convert_vector_list_to_array(pick(N.get_mesh_per_vertex_normals(dm), u.GeometryScriptVectorList))
def region_sel(dm, vids, grow=2):
    s = pick(Sel.convert_index_array_to_mesh_selection(dm, vids, u.GeometryScriptMeshSelectionType.VERTICES), u.GeometryScriptMeshSelection)
    s = pick(Sel.expand_contract_mesh_selection(dm, s, grow, False, False), u.GeometryScriptMeshSelection)
    s = pick(Sel.convert_mesh_selection(dm, s, u.GeometryScriptMeshSelectionType.TRIANGLES, True), u.GeometryScriptMeshSelection)
    vs = pick(Sel.convert_mesh_selection(dm, s, u.GeometryScriptMeshSelectionType.VERTICES, True), u.GeometryScriptMeshSelection)
    ids = Sel.convert_mesh_selection_to_index_array(dm, vs); ids = [x for x in (ids if isinstance(ids, tuple) else (ids,)) if isinstance(x, (list, u.Array))][0]
    return s, list(ids)
mesh = u.load_asset(MESH); out = {}
for L in range(4):
    f = D/f'morph_gd40_body_lod{L}.json'
    if not f.exists(): continue
    data = json.loads(f.read_text())['Body']; rep = {}
    for name, dd in data.items():
        deltas = {int(k): v for k, v in dd.items()}
        base_dm = fresh(mesh, L); base = l.convert_vector_list_to_array(q.get_all_vertex_positions(base_dm, False)[1]); N0 = vnormals(base_dm)
        assert max(deltas) < len(base), ('vertex index out of range', L, max(deltas), len(base))
        dmA = fresh(mesh, L); dmB = fresh(mesh, L)
        for vid, d in deltas.items(): p = base[vid]; u.GeometryScript_MeshEdits.set_vertex_position(dmB, vid, u.Vector(p.x+d[0], p.y+d[1], p.z+d[2]), True)
        selA, rv = region_sel(dmA, list(deltas)); selB, rv2 = region_sel(dmB, list(deltas)); assert rv == rv2
        opt = u.GeometryScriptCalculateNormalsOptions(); N.recompute_normals_for_mesh_selection(dmA, selA, opt); N.recompute_normals_for_mesh_selection(dmB, selB, opt)
        NA = vnormals(dmA); NB_ = vnormals(dmB); final = list(N0)
        for v in rv:
            n = [N0[v].x+NB_[v].x-NA[v].x, N0[v].y+NB_[v].y-NA[v].y, N0[v].z+NB_[v].z-NA[v].z]; ln = math.sqrt(sum(x*x for x in n)) or 1; final[v] = u.Vector(n[0]/ln, n[1]/ln, n[2]/ln)
        N.set_mesh_per_vertex_normals(dmB, pick(l.convert_array_to_vector_list(final), u.GeometryScriptVectorList))
        opts = u.GeometryScriptCopyMorphTargetToAssetOptions(); opts.set_editor_property('copy_normals', True); opts.set_editor_property('overwrite_existing_target', True)
        wl = u.GeometryScriptMeshWriteLOD(); wl.lod_index = L
        r = u.GeometryScript_AssetUtils.copy_morph_target_to_skeletal_mesh(dmB, mesh, name, opts, wl)
        after = l.convert_vector_list_to_array(q.get_all_vertex_positions(fresh(mesh, L), False)[1])
        rep[name] = {'verts': len(deltas), 'max_mm': round(max(math.sqrt(sum(x*x for x in d)) for d in deltas.values())*10, 3), 'ok': 'SUCCESS' in str(r[-1] if isinstance(r, tuple) else r),
                     'base_unchanged_max_cm': max(math.dist([a.x, a.y, a.z], [b.x, b.y, b.z]) for a, b in zip(after, base))}
    out[f'lod{L}'] = rep; print(L, rep, flush=True)
out['morphs'] = [m.get_name() for m in mesh.get_editor_property('morph_targets')][-5:]
out['saved'] = u.EditorAssetLibrary.save_loaded_asset(mesh, False); out['dirty_after'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
(D/'ue_bake_body.json').write_text(json.dumps(out, indent=1)); print('GD40_BAKE_BODY', json.dumps(out))
