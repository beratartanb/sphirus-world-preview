"""J2: bake SHOULDER_HIGH_ELEVATION_CORRECTIVE morph targets into the isolated mesh copies (LOD0 source model).
Morph deltas (bind space, cm) come from shc_design.py. Normal deltas: local recompute on base vs morphed positions,
added to the asset normals only inside the morph region (outside: asset normal -> zero normal delta)."""
import unreal as u, pathlib, json, math
C = pathlib.Path(u.Paths.project_dir()).resolve()/'Saved/Codex/CharacterShoulderFix_20260928'; S = C.parent/'CharacterFinal_20260929'
dst = '/Game/Sphirus/CharacterLab/ShoulderFix_20260928/HighElevCorrective'
MESH = {'Body': '/Game/Sphirus/CharacterLab/CharacterFinal_20260929/Body/SKM_CF_BodyMesh', 'Head': '/Game/Sphirus/CharacterLab/CharacterFinal_20260929/Body/SKM_CF_FaceMesh'}
import builtins
data = json.loads((S/builtins.SHC_MORPH_FILE).read_text())
q = u.GeometryScript_MeshQueries; l = u.GeometryScript_List; N = u.GeometryScript_Normals; Sel = u.GeometryScript_MeshSelection
def fresh(m):
    dm = u.DynamicMesh(); lod = u.GeometryScriptMeshReadLOD(); lod.lod_type = u.GeometryScriptLODType.SOURCE_MODEL; lod.lod_index = 0
    r = u.GeometryScript_AssetUtils.copy_mesh_from_skeletal_mesh(m, dm, u.GeometryScriptCopyMeshFromAssetOptions(), lod)
    assert 'SUCCESS' in str(r[-1]), r; return dm
def vnormals(dm):
    r = N.get_mesh_per_vertex_normals(dm); r = r if isinstance(r, tuple) else (r,)
    lst = [x for x in r if isinstance(x, u.GeometryScriptVectorList)][0]
    return l.convert_vector_list_to_array(lst)
def pick(r, typ):
    r = r if isinstance(r, tuple) else (r,)
    return [x for x in r if isinstance(x, typ)][0]
def region_sel(dm, vids, grow=2):
    s = Sel.convert_index_array_to_mesh_selection(dm, vids, u.GeometryScriptMeshSelectionType.VERTICES)
    s = pick(s, u.GeometryScriptMeshSelection)
    s = Sel.expand_contract_mesh_selection(dm, s, grow, False, False)
    s = pick(s, u.GeometryScriptMeshSelection)
    s = Sel.convert_mesh_selection(dm, s, u.GeometryScriptMeshSelectionType.TRIANGLES, True)
    s = pick(s, u.GeometryScriptMeshSelection)
    vs = Sel.convert_mesh_selection(dm, s, u.GeometryScriptMeshSelectionType.VERTICES, True)
    vs = pick(vs, u.GeometryScriptMeshSelection)
    ids = Sel.convert_mesh_selection_to_index_array(dm, vs)
    ids = [x for x in (ids if isinstance(ids, tuple) else (ids,)) if isinstance(x, (list, u.Array))][0]
    return s, list(ids)
def apply_pos(dm, deltas, base):
    for vid, d in deltas.items():
        p = base[vid]; N_ = u.Vector(p.x+d[0], p.y+d[1], p.z+d[2])
        u.GeometryScript_MeshEdits.set_vertex_position(dm, vid, N_, True)
out = {}
PARTS_TO_RUN = [p for p in MESH if p in __import__('builtins').__dict__.get('SHC_PARTS', list(MESH))]
for part, path in [(p, MESH[p]) for p in PARTS_TO_RUN]:
    mesh = u.load_asset(path); rep = {}
    for name, dd in data[part].items():
        deltas = {int(k): v for k, v in dd.items()}
        base_dm = fresh(mesh); base = l.convert_vector_list_to_array(q.get_all_vertex_positions(base_dm, False)[1]); N0 = vnormals(base_dm)
        dmA = fresh(mesh); dmB = fresh(mesh); apply_pos(dmB, deltas, base)
        selA, rv = region_sel(dmA, list(deltas)); selB, rv2 = region_sel(dmB, list(deltas)); assert rv == rv2
        opt = u.GeometryScriptCalculateNormalsOptions()
        N.recompute_normals_for_mesh_selection(dmA, selA, opt); N.recompute_normals_for_mesh_selection(dmB, selB, opt)
        NA = vnormals(dmA); NB = vnormals(dmB)
        final = list(N0)
        for v in rv:
            n = [N0[v].x+NB[v].x-NA[v].x, N0[v].y+NB[v].y-NA[v].y, N0[v].z+NB[v].z-NA[v].z]; ln = math.sqrt(sum(x*x for x in n)) or 1
            final[v] = u.Vector(n[0]/ln, n[1]/ln, n[2]/ln)
        vl = u.GeometryScriptVectorList(); l.convert_array_to_vector_list(final) if False else None
        vl = l.convert_array_to_vector_list(final) if hasattr(l, 'convert_array_to_vector_list') else None
        vl = pick(vl, u.GeometryScriptVectorList) if vl is not None else None
        N.set_mesh_per_vertex_normals(dmB, vl)
        opts = u.GeometryScriptCopyMorphTargetToAssetOptions(); opts.set_editor_property('copy_normals', True); opts.set_editor_property('overwrite_existing_target', True)
        wl = u.GeometryScriptMeshWriteLOD(); wl.lod_index = 0
        r = u.GeometryScript_AssetUtils.copy_morph_target_to_skeletal_mesh(dmB, mesh, name, opts, wl)
        ok = 'SUCCESS' in str(r[-1] if isinstance(r, tuple) else r)
        maxd = max(math.sqrt(sum(x*x for x in d)) for d in deltas.values())*10
        rep[name] = {'verts': len(deltas), 'normal_region_verts': len(rv), 'max_bind_delta_mm': round(maxd, 3), 'ok': ok}
        print(part, name, rep[name], flush=True)
    rep['morph_count_after'] = len(mesh.get_editor_property('morph_targets'))
    rep['morph_names'] = [m.get_name() for m in mesh.get_editor_property('morph_targets') if m.get_name().startswith('SHC_')]
    after = l.convert_vector_list_to_array(q.get_all_vertex_positions(fresh(mesh), False)[1])
    rep['base_positions_unchanged_max_cm'] = max(math.dist([a.x, a.y, a.z], [b.x, b.y, b.z]) for a, b in zip(after, base))
    rep['saved'] = u.EditorAssetLibrary.save_loaded_asset(mesh, False)
    out[part] = rep
out['dirty_after'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
(S/('j2_'+builtins.SHC_MORPH_FILE)).write_text(json.dumps(out, indent=1)); print(json.dumps(out, indent=1))
