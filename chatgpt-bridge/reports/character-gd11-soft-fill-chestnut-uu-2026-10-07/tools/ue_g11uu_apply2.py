"""pass UU: duplicate a rigged face SKM and add per-vertex displacements (LOD0 source model, dynamic-mesh order) - the post-rig residual bake.
Checks morph count and DNA user data. v2: normals are recomputed inside the moved region (+2 rings) and tangents rebuilt, otherwise the moved skin keeps stale normals and renders dark patches (uu11b). builtins.G11UU_APPLY = {'src', 'dst', 'disp_json'}"""
import unreal as u, json, builtins, math
C = builtins.G11UU_APPLY; EAL = u.EditorAssetLibrary; q = u.GeometryScript_MeshQueries; l = u.GeometryScript_List; out = {}
def fresh(m):
    dm = u.DynamicMesh(); lod = u.GeometryScriptMeshReadLOD(); lod.lod_type = u.GeometryScriptLODType.SOURCE_MODEL; lod.lod_index = 0
    r = u.GeometryScript_AssetUtils.copy_mesh_from_skeletal_mesh(m, dm, u.GeometryScriptCopyMeshFromAssetOptions(), lod); assert 'SUCCESS' in str(r[-1] if isinstance(r, tuple) else r); return dm
assert not EAL.does_asset_exist(C['dst']), 'exists: ' + C['dst']
dst = EAL.duplicate_asset(C['src'], C['dst']); assert dst; out['morphs_before'] = len(dst.get_editor_property('morph_targets'))
dm = fresh(dst); P = l.convert_vector_list_to_array(q.get_all_vertex_positions(dm, False)[1]); disp = json.load(open(C['disp_json'])); mx = 0.0
for j, dx, dy, dz in disp:
    p = P[j]; u.GeometryScript_MeshEdits.set_vertex_position(dm, j, u.Vector(p.x+dx, p.y+dy, p.z+dz), True); mx = max(mx, math.sqrt(dx*dx+dy*dy+dz*dz))
Sel = u.GeometryScript_MeshSelection; N = u.GeometryScript_Normals
def pick(r, typ):
    r = r if isinstance(r, tuple) else (r,); return [x for x in r if isinstance(x, typ)][0]
s_ = pick(Sel.convert_index_array_to_mesh_selection(dm, [d[0] for d in disp], u.GeometryScriptMeshSelectionType.VERTICES), u.GeometryScriptMeshSelection)
s_ = pick(Sel.expand_contract_mesh_selection(dm, s_, 2, False, False), u.GeometryScriptMeshSelection)
s_ = pick(Sel.convert_mesh_selection(dm, s_, u.GeometryScriptMeshSelectionType.TRIANGLES, True), u.GeometryScriptMeshSelection)
N.recompute_normals_for_mesh_selection(dm, s_, u.GeometryScriptCalculateNormalsOptions()); out['normals_recomputed'] = True
wl = u.GeometryScriptMeshWriteLOD(); wl.lod_index = 0
opt = u.GeometryScriptCopyMeshToAssetOptions()
for k_, v_ in (('enable_recompute_normals', False), ('enable_recompute_tangents', True)):
    try: opt.set_editor_property(k_, v_); out['opt_'+k_] = v_
    except Exception as e_: out['opt_'+k_] = 'n/a'
r = u.GeometryScript_AssetUtils.copy_mesh_to_skeletal_mesh(dm, dst, opt, wl); out['written'] = 'SUCCESS' in str(r[-1] if isinstance(r, tuple) else r)
out['n'] = len(disp); out['max_cm'] = round(mx, 3); out['morphs_after'] = len(dst.get_editor_property('morph_targets')); out['user_data'] = [type(x).__name__ for x in (dst.get_editor_property('asset_user_data') or [])]
out['saved'] = EAL.save_loaded_asset(dst, False); out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]; print('G11UU_APPLY', json.dumps(out))
