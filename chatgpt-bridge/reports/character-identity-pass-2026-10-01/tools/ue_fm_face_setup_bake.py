"""FACE-MATCH pass: isolated face derivative + neutral-shape bake.
  - duplicates the (read-only) revision face mesh SKM_RV_FaceMesh -> <lookdev>/Face/<name> (once); the duplicate keeps the same
    skeleton (shared Face_Archetype_Skeleton copy, NOT modified) and post-process ABP (ABP_RV_Face_PostProcess, referenced, NOT
    modified): DNA / RigLogic / 858 expression morphs / joints are untouched
  - overwrites the derivative's BR_Neutral morph (always-on via the existing Modify Curve) on LOD 0..7 with the files
    morph_fm_face_lod<L>.json ('Head' part: original collar deltas + likeness deltas), normals re-derived locally (rv_ue_bake method)
  - verifies base geometry unchanged per LOD and the morph count unchanged
builtins.FM_FACE = {'dir': <abs dir of json>, 'name': 'SKM_FM_FaceMesh_a'}"""
import unreal as u, pathlib, json, math, builtins
CFG = builtins.FM_FACE; D = pathlib.Path(CFG['dir']); F = CFG.get('folder', '/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Face'); SRC = '/Game/Sphirus/CharacterLab/CharacterRevision_20260930/Body/SKM_RV_FaceMesh'
EAL = u.EditorAssetLibrary; path = F+'/'+CFG['name']; out = {'dirty_before': [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]}
if not EAL.does_asset_exist(path): assert EAL.duplicate_asset(SRC, path); out['created'] = True
mesh = u.load_asset(path); out['morphs_before'] = len(mesh.get_editor_property('morph_targets')); out['pp_abp'] = mesh.post_process_anim_blueprint.get_path_name() if mesh.post_process_anim_blueprint else None
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
for L in range(8):
    f = D/f'morph_fm_face_lod{L}.json'
    if not f.exists(): continue
    deltas = {int(k): v for k, v in json.loads(f.read_text())['Head']['BR_Neutral'].items()}
    base_dm = fresh(mesh, L); base = l.convert_vector_list_to_array(q.get_all_vertex_positions(base_dm, False)[1]); N0 = vnormals(base_dm)
    assert max(deltas) < len(base), ('index out of range', L, max(deltas), len(base))
    dmA = fresh(mesh, L); dmB = fresh(mesh, L)
    for vid, d in deltas.items(): p = base[vid]; u.GeometryScript_MeshEdits.set_vertex_position(dmB, vid, u.Vector(p.x+d[0], p.y+d[1], p.z+d[2]), True)
    selA, rv = region_sel(dmA, list(deltas)); selB, rv2 = region_sel(dmB, list(deltas)); assert rv == rv2
    opt = u.GeometryScriptCalculateNormalsOptions(); N.recompute_normals_for_mesh_selection(dmA, selA, opt); N.recompute_normals_for_mesh_selection(dmB, selB, opt)
    NA = vnormals(dmA); NB_ = vnormals(dmB); final = list(N0)
    for v in rv:
        n = [N0[v].x+NB_[v].x-NA[v].x, N0[v].y+NB_[v].y-NA[v].y, N0[v].z+NB_[v].z-NA[v].z]; ln = math.sqrt(sum(x*x for x in n)) or 1; final[v] = u.Vector(n[0]/ln, n[1]/ln, n[2]/ln)
    if L == 0 and (D/'seam_normals_lod0.json').exists():   # head collar boundary: take the body's vertex normal at the weld (continuous shading across the seam)
        for k_, n_ in json.loads((D/'seam_normals_lod0.json').read_text()).items(): final[int(k_)] = u.Vector(*n_)
        out['seam_normal_override'] = True
    N.set_mesh_per_vertex_normals(dmB, pick(l.convert_array_to_vector_list(final), u.GeometryScriptVectorList))
    opts = u.GeometryScriptCopyMorphTargetToAssetOptions(); opts.set_editor_property('copy_normals', True); opts.set_editor_property('overwrite_existing_target', True)
    wl = u.GeometryScriptMeshWriteLOD(); wl.lod_index = L
    r = u.GeometryScript_AssetUtils.copy_morph_target_to_skeletal_mesh(dmB, mesh, 'BR_Neutral', opts, wl)
    after = l.convert_vector_list_to_array(q.get_all_vertex_positions(fresh(mesh, L), False)[1])
    out[f'lod{L}'] = {'verts': len(deltas), 'max_mm': round(max(math.sqrt(sum(x*x for x in d)) for d in deltas.values())*10, 3), 'ok': 'SUCCESS' in str(r[-1] if isinstance(r, tuple) else r),
                      'base_unchanged_max_cm': max(math.dist([a.x, a.y, a.z], [b.x, b.y, b.z]) for a, b in zip(after, base))}
    print(L, out[f'lod{L}'], flush=True)
out['morphs_after'] = len(mesh.get_editor_property('morph_targets'))
out['saved'] = EAL.save_loaded_asset(mesh, False); out['dirty_after'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
(D/'ue_face_bake.json').write_text(json.dumps(out, indent=1)); print('FM_FACE_BAKE', json.dumps({k: v for k, v in out.items() if not k.startswith('lod')}))
