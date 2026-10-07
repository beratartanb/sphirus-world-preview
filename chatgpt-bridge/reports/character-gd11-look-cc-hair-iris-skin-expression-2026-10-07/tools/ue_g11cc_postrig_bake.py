"""pass CC: post-rig shape bake. The MetaHuman auto-rig pulls the jaw angle / nape back to its template (SS4 kept 0.1 of 2 mm at the jaw
angle, 1/3 of the nape). This writes the lost edit directly into a DUPLICATE of the rigged face mesh (LOD0 source model) with GeometryScript;
the DNA link, skin weights and the 858 RigLogic morph targets must survive (checked and reported). ss4 itself is untouched.
builtins.G11CC_BAKE = {'src': face path, 'dst': new face path, 'ops': [{'type': 'normal'|'grab', 'c': [dx, y, z], 'r': [..], 'amt'|'d': .., 'sym': bool}]}"""
import unreal as u, json, builtins, math
C = builtins.G11CC_BAKE; EAL = u.EditorAssetLibrary; q = u.GeometryScript_MeshQueries; l = u.GeometryScript_List; N = u.GeometryScript_Normals; MX = -0.23; out = {}
def fresh(m):
    dm = u.DynamicMesh(); lod = u.GeometryScriptMeshReadLOD(); lod.lod_type = u.GeometryScriptLODType.SOURCE_MODEL; lod.lod_index = 0
    r = u.GeometryScript_AssetUtils.copy_mesh_from_skeletal_mesh(m, dm, u.GeometryScriptCopyMeshFromAssetOptions(), lod); assert 'SUCCESS' in str(r[-1] if isinstance(r, tuple) else r); return dm
def pick(r, typ):
    r = r if isinstance(r, tuple) else (r,); return [x for x in r if isinstance(x, typ)][0]
assert not EAL.does_asset_exist(C['dst']), 'exists: ' + C['dst']
src = u.load_asset(C['src']); out['morphs_src'] = len(src.get_editor_property('morph_targets'))
dst = EAL.duplicate_asset(C['src'], C['dst']); assert dst; out['morphs_dup'] = len(dst.get_editor_property('morph_targets'))
dm = fresh(dst); P = l.convert_vector_list_to_array(q.get_all_vertex_positions(dm, False)[1]); NV = l.convert_vector_list_to_array(pick(N.get_mesh_per_vertex_normals(dm), u.GeometryScriptVectorList))
D = [[0.0, 0.0, 0.0] for _ in P]
for op in C['ops']:
    for sd in ((1, -1) if op.get('sym') else (1,)):
        cx, cy, cz = MX+sd*op['c'][0], op['c'][1], op['c'][2]; rx, ry, rz = op['r']
        for i, p in enumerate(P):
            qq = ((p.x-cx)/rx)**2+((p.y-cy)/ry)**2+((p.z-cz)/rz)**2
            if qq >= 1.0: continue
            w = (1-qq)**2
            if op['type'] == 'normal': n = NV[i]; a = op['amt']*w; D[i][0] += a*n.x; D[i][1] += a*n.y; D[i][2] += a*n.z
            else: d = op['d']; D[i][0] += w*d[0]*sd; D[i][1] += w*d[1]; D[i][2] += w*d[2]
mx = 0.0; nm = 0
for i, d in enumerate(D):
    m = math.sqrt(d[0]**2+d[1]**2+d[2]**2)
    if m > 1e-5: p = P[i]; u.GeometryScript_MeshEdits.set_vertex_position(dm, i, u.Vector(p.x+d[0], p.y+d[1], p.z+d[2]), True); mx = max(mx, m); nm += 1
out['moved_verts'] = nm; out['max_cm'] = round(mx, 3)
wl = u.GeometryScriptMeshWriteLOD(); wl.lod_index = 0; opt = u.GeometryScriptCopyMeshToAssetOptions()
for k in ('enable_recompute_normals', 'enable_recompute_tangents'):
    try: opt.set_editor_property(k, False)
    except Exception: pass
r = u.GeometryScript_AssetUtils.copy_mesh_to_skeletal_mesh(dm, dst, opt, wl); out['written'] = 'SUCCESS' in str(r[-1] if isinstance(r, tuple) else r)
out['morphs_after'] = len(dst.get_editor_property('morph_targets'))
chk = l.convert_vector_list_to_array(q.get_all_vertex_positions(fresh(dst), False)[1]); out['readback_max_cm'] = round(max(math.dist([a.x, a.y, a.z], [b.x, b.y, b.z]) for a, b in zip(chk, P)), 3)
ud = dst.get_editor_property('asset_user_data') or []; out['user_data'] = [type(x).__name__ for x in ud]
out['saved'] = EAL.save_loaded_asset(dst, False); out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('G11CC_BAKE', json.dumps(out))
