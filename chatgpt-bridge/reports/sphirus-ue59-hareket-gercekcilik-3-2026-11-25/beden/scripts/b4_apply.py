# b4_apply.py (write, gated): bakes a per-vertex delta (b4_body.py) into the source models of a DUPLICATE skeletal mesh with
# GeometryScript (skin weights, UVs, sections, morph targets and asset user data survive: same vertex ids, positions only).
# builtins.B4_APPLY = [{'src': path, 'dst': new path, 'delta': abs json {'lods': {'0': [[dx,dy,dz],..], ..}}}, ..]
# The source asset is never written. dst must not exist (checked) unless 'reuse': True (then it is re-baked from src positions).
import unreal as u, json, builtins, math
EAL = u.EditorAssetLibrary; q = u.GeometryScript_MeshQueries; l = u.GeometryScript_List; ME = u.GeometryScript_MeshEdits
assert not u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(), 'PIE running'
def fresh(m, i):
    dm = u.DynamicMesh(); lod = u.GeometryScriptMeshReadLOD(); lod.lod_type = u.GeometryScriptLODType.SOURCE_MODEL; lod.lod_index = i
    r = u.GeometryScript_AssetUtils.copy_mesh_from_skeletal_mesh(m, dm, u.GeometryScriptCopyMeshFromAssetOptions(), lod); assert 'SUCCESS' in str(r), str(r)[:200]; return dm
for job in builtins.B4_APPLY:
    out = {'dst': job['dst']}; src = u.load_asset(job['src']); D = json.load(open(job['delta']))['lods']
    if EAL.does_asset_exist(job['dst']):
        assert job.get('reuse'), 'exists: ' + job['dst']; dst = u.load_asset(job['dst'])
    else:
        dst = EAL.duplicate_asset(job['src'], job['dst']); assert dst
    out['morphs'] = len(dst.get_editor_property('morph_targets') or [])
    for k, dl in sorted(D.items(), key=lambda x: int(x[0])):
        i = int(k); dms = fresh(src, i); P = l.convert_vector_list_to_array(q.get_all_vertex_positions(dms, False)[1])
        assert len(P) == len(dl), ('vertex count', i, len(P), len(dl))
        dm = fresh(src, i); mx = 0.0; n = 0; N = u.GeometryScript_Normals
        N0 = l.convert_vector_list_to_array(N.get_mesh_per_vertex_normals(dm, True)[1])
        for vi, (p, d) in enumerate(zip(P, dl)):
            m = math.sqrt(d[0] * d[0] + d[1] * d[1] + d[2] * d[2])
            if m > 1e-5: ME.set_vertex_position(dm, vi, u.Vector(p.x + d[0], p.y + d[1], p.z + d[2]), True); mx = max(mx, m); n += 1
        # normals: recomputed where the surface moved, original normals kept where it did not (neck seam, hands, feet: no seam line)
        if job.get('keep_normals'): N1 = None
        else: N.recompute_normals(dm, u.GeometryScriptCalculateNormalsOptions())
        N1 = None if job.get('keep_normals') else l.convert_vector_list_to_array(N.get_mesh_per_vertex_normals(dm, True)[1]); NN = []
        for a, b, d in (zip(N0, N1, dl) if N1 else []):
            w = min(1.0, math.sqrt(d[0] * d[0] + d[1] * d[1] + d[2] * d[2]) / 0.3); v = u.Vector(a.x * (1 - w) + b.x * w, a.y * (1 - w) + b.y * w, a.z * (1 - w) + b.z * w)
            ln = math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z) or 1.0; NN.append(u.Vector(v.x / ln, v.y / ln, v.z / ln))
        vl = u.GeometryScriptVectorList(); vl.set_editor_property('list', NN) if hasattr(vl, 'list') else None
        try: vl = l.convert_array_to_vector_list(NN)
        except Exception: pass
        if N1: N.set_mesh_per_vertex_normals(dm, vl)
        wl = u.GeometryScriptMeshWriteLOD(); wl.lod_index = i; opt = u.GeometryScriptCopyMeshToAssetOptions()
        for kk, vv in (('enable_recompute_normals', False), ('enable_recompute_tangents', True), ('emit_transaction', False)):
            try: opt.set_editor_property(kk, vv)
            except Exception: pass
        r = u.GeometryScript_AssetUtils.copy_mesh_to_skeletal_mesh(dm, dst, opt, wl)
        chk = l.convert_vector_list_to_array(q.get_all_vertex_positions(fresh(dst, i), False)[1])
        err = max(math.dist([a.x + d[0], a.y + d[1], a.z + d[2]], [b.x, b.y, b.z]) for a, b, d in zip(P, chk, dl))
        out['lod%d' % i] = {'moved': n, 'max_cm': round(mx, 2), 'written': 'SUCCESS' in str(r), 'readback_err_cm': round(err, 4), 'verts': len(P)}
    out['morphs_after'] = len(dst.get_editor_property('morph_targets') or []); out['user_data'] = [type(x).__name__ for x in (dst.get_editor_property('asset_user_data') or [])]
    out['physics'] = dst.get_editor_property('physics_asset').get_path_name() if dst.get_editor_property('physics_asset') else None
    out['saved'] = EAL.save_loaded_asset(dst, False)
    print('B4APPLY', json.dumps(out))
print('B4APPLY dirty', [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()])
