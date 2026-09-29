import builtins; builtins.OF_GEO_FILE = 'build_final/outfit_geometry.json.gz'
"""J4: build the garment skeletal meshes from the Blender geometry: DynamicMesh from buffers (per material id), welded,
normals/tangents, skeleton bones copied from the current BR body mesh, skin weights transferred from the body surface
(inpaint, closest-point fallback for small separate parts), LOD0 + Blender-decimated LOD1, then a NEW SkeletalMesh
asset on the isolated ShoulderFix skeleton. Material slots assigned afterwards. No existing asset is modified
(a previous candidate at the same path is deleted first: isolated folder only)."""
import unreal as u, pathlib, json, gzip, builtins, time
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/OutfitHome_20260929'
GEO = json.loads(gzip.open(O/builtins.__dict__.get('OF_GEO_FILE', 'build_final/outfit_geometry.json.gz'), 'rb').read())
DEST = '/Game/Sphirus/CharacterLab/Outfit_Home_20260929'; MD = DEST+'/Materials'
SKEL = u.load_asset('/Game/Sphirus/CharacterLab/ShoulderFix_20260928/Common/Female/Medium/NormalWeight/Body/metahuman_base_skel')
BODY = u.load_asset('/Game/Sphirus/CharacterLab/BodyRealism_20260929/SKM_BR_BodyMesh')
q = u.GeometryScript_MeshQueries; l = u.GeometryScript_List; BW = u.GeometryScript_BoneWeights; N = u.GeometryScript_Normals; ME_ = u.GeometryScript_MeshEdits
def pick(r, typ):
    r = r if isinstance(r, tuple) else (r,)
    return [x for x in r if isinstance(x, typ)][0]
def fresh_body():
    # the source mesh is re-read for every garment: a transfer issued after a skeletal-mesh asset creation crashed the
    # engine (bone index table of the previous asset) when the same source DynamicMesh was reused
    bd = u.DynamicMesh(); lod = u.GeometryScriptMeshReadLOD(); lod.lod_type = u.GeometryScriptLODType.SOURCE_MODEL; lod.lod_index = 0
    r = u.GeometryScript_AssetUtils.copy_mesh_from_skeletal_mesh(BODY, bd, u.GeometryScriptCopyMeshFromAssetOptions(), lod); assert 'SUCCESS' in str(r[-1]); return bd
body_dm = fresh_body()
MATS = {'henley': ['MI_Home_Henley', 'MI_Home_Henley_Trim', 'MI_Home_Buttons'], 'trousers': ['MI_Home_Trousers', 'MI_Home_Trousers_Trim', 'MI_Home_Trousers_Trim', 'MI_Home_Drawstring']}
NAMES = {'henley': 'SKM_Home_Henley', 'trousers': 'SKM_Home_Trousers'}
def build_dm(G):
    """one buffer append (vertices split only at UV seams, as exported), then per-material triangle selections; no weld
    or compaction (compact_mesh after weld corrupted the bone attribute -> engine crash in the next transfer)"""
    P = G['positions']; T = G['triangles']; UVs = G['uv']; MI = G['material_ids']
    dm = u.DynamicMesh(); u.GeometryScript_Materials.enable_material_i_ds(dm)
    buf = u.GeometryScriptSimpleMeshBuffers()
    buf.set_editor_property('vertices', [u.Vector(*p) for p in P]); buf.set_editor_property('uv0', [u.Vector2D(*t) for t in UVs])
    buf.set_editor_property('triangles', [u.IntVector(a, c, b) for a, b, c in T])   # Blender (right-handed, outward) -> UE: mirror flips the winding
    r = ME_.append_buffers_to_mesh(dm, buf, 0, True)
    newid = list(l.convert_index_list_to_array(pick(r, u.GeometryScriptIndexList)))   # input triangle -> new triangle id (-1 = rejected, non-manifold)
    rejected = [t for t, nid in enumerate(newid) if nid < 0]
    G['_rejected_triangles'] = rejected
    assert len(rejected) <= max(1, len(T)//1000), ('too many non-manifold triangles rejected', len(rejected))
    Sel = u.GeometryScript_MeshSelection
    for m in range(1, max(MI)+1):
        ids = [newid[t] for t, mi in enumerate(MI) if mi == m and newid[t] >= 0]
        if not ids: continue
        sel = pick(Sel.convert_index_array_to_mesh_selection(dm, ids, u.GeometryScriptMeshSelectionType.TRIANGLES), u.GeometryScriptMeshSelection)
        u.GeometryScript_Materials.set_material_id_for_mesh_selection(dm, sel, m)
    opt = u.GeometryScriptCalculateNormalsOptions(); opt.set_editor_property('angle_weighted', True); opt.set_editor_property('area_weighted', True)
    N.set_per_vertex_normals(dm); N.recompute_normals(dm, opt); N.compute_tangents(dm, u.GeometryScriptTangentsOptions())
    assert dm.get_vertex_count() == len(P) and dm.get_triangle_count() == len(T)-len(rejected), ('buffer append changed counts', dm.get_vertex_count(), len(P), dm.get_triangle_count(), len(T))
    if rejected: print('rejected non-manifold triangles', len(rejected), [T[t] for t in rejected[:3]], flush=True)
    return dm
def missing_ids(dm):
    out = []
    for v in range(dm.get_vertex_count()):
        rr = BW.get_vertex_bone_weights(dm, v); arr = [x for x in (rr if isinstance(rr, tuple) else (rr,)) if isinstance(x, u.Array)]
        if not arr or len(arr[0]) == 0: out.append(v)
    return out
def has_weights(dm):
    r = BW.mesh_has_bone_weights(dm); return bool(r[-1]) if isinstance(r, tuple) else bool(r)
WEIGHTS = json.loads(gzip.open(O/builtins.__dict__.get('OF_WEIGHTS_FILE', 'build_final/outfit_weights.json.gz'), 'rb').read())
def weight_dm(dm, label='', key=None):
    """skin weights authored offline (closest point on the body + smoothing, blender_outfit_weights.py); the engine
    transfer crashed on these meshes. Bone attributes come from the body mesh so indices match the skeleton."""
    BW.copy_bones_from_mesh(body_dm, dm, u.GeometryScriptCopyBonesFromMeshOptions())
    bi = BW.get_all_bones_info(dm); bi = pick(bi, u.Array) if isinstance(bi, tuple) else bi
    bidx = {str(b.get_editor_property('name')): i for i, b in enumerate(bi)}
    BW.mesh_create_bone_weights(dm, True)
    Wg = WEIGHTS[key]; n = dm.get_vertex_count(); assert len(Wg) == n, ('weight count mismatch', label, len(Wg), n)
    G = GEO[key]; rej = set(G.get('_rejected_triangles', []))
    missing = 0; unknown = set()
    for v in range(n):
        arr = []
        for bname, w in Wg[v].items():
            if bname in bidx: bw = u.GeometryScriptBoneWeight(); bw.set_editor_property('bone_index', bidx[bname]); bw.set_editor_property('weight', float(w)); arr.append(bw)
            else: unknown.add(bname)
        if not arr: missing += 1; continue
        BW.set_vertex_bone_weights(dm, v, arr)
    print(label, 'weights set; missing', missing, 'of', n, 'unknown bones', sorted(unknown)[:5], flush=True)
    assert has_weights(dm) and missing == 0, ('offline weights incomplete', label, missing)
    return 0, missing
def readback(dm, path):
    bi = BW.get_all_bones_info(dm); bi = pick(bi, u.Array) if isinstance(bi, tuple) else bi; bones = [str(b.get_editor_property('name')) for b in bi]
    W = []
    for v in range(dm.get_vertex_count()):
        rr = BW.get_vertex_bone_weights(dm, v); arr = [x for x in (rr if isinstance(rr, tuple) else (rr,)) if isinstance(x, u.Array)]
        W.append({bones[int(b.get_editor_property('bone_index'))]: float(b.get_editor_property('weight')) for b in arr[0]} if arr and len(arr[0]) else {})
    V = l.convert_vector_list_to_array(q.get_all_vertex_positions(dm, False)[1]); TT = l.convert_triangle_list_to_array(q.get_all_triangle_indices(dm, False)[1])
    with gzip.open(path, 'wt') as f: json.dump({'positions': [[p.x, p.y, p.z] for p in V], 'triangles': [[t.x, t.y, t.z] for t in TT], 'weights': W}, f)
    return len(bones)
report = {}
# phase 1: build + weight every LOD of every garment (a transfer issued after an asset creation crashes the engine)
built = {}
for g in ['henley', 'trousers']:
    t0 = time.time(); body_dm = fresh_body()
    dm = build_dm(GEO[g]); m1, m2 = weight_dm(dm, g+' LOD0', g); dm1 = build_dm(GEO[g+'_lod1']); l1a, l1b = weight_dm(dm1, g+' LOD1', g+'_lod1')
    built[g] = (dm, dm1, m1, m2, l1a, l1b, t0)
# phase 2: assets
for g in ['henley', 'trousers']:
    dm, dm1, m1, m2, l1a, l1b, t0 = built[g]
    co = u.GeometryScriptCreateNewSkeletalMeshAssetOptions(); co.set_editor_property('enable_recompute_normals', False); co.set_editor_property('enable_recompute_tangents', False); co.set_editor_property('use_original_vertex_order', True); co.set_editor_property('use_mesh_bone_proportions', True)   # bind pose = the body's (mesh bone attributes), not the generic skeleton ref pose
    path = DEST+'/'+NAMES[g]
    if u.EditorAssetLibrary.does_asset_exist(path): assert u.EditorAssetLibrary.delete_asset(path)
    r = u.GeometryScript_NewAssetUtils.create_new_skeletal_mesh_asset_from_mesh_lods([dm, dm1], SKEL, path, co)
    mesh = r[0] if isinstance(r, tuple) else r; assert mesh and 'SUCCESS' in str(r[-1]), r
    slots = []
    for i, n in enumerate(MATS[g]):
        sm = u.SkeletalMaterial(); sm.set_editor_property('material_interface', u.load_asset(MD+'/'+n)); sm.set_editor_property('material_slot_name', GEO[g]['materials'][i]); slots.append(sm)
    mesh.set_editor_property('materials', slots); mesh.set_editor_property('post_process_anim_blueprint', None)
    nb = readback(dm, O/f'asset_{g}_lod0.json.gz')
    saved = u.EditorAssetLibrary.save_loaded_asset(mesh, False)
    report[g] = {'asset': mesh.get_path_name(), 'rejected_triangles': len(GEO[g].get('_rejected_triangles', [])), 'lod0': [dm.get_vertex_count(), dm.get_triangle_count()], 'lod1': [dm1.get_vertex_count(), dm1.get_triangle_count()], 'unweighted_after_inpaint': m1, 'unweighted_final': m2, 'lod1_unweighted_final': l1b,
                 'bones_in_mesh': nb, 'materials': [str(s.get_editor_property('material_slot_name')) for s in mesh.get_editor_property('materials')], 'skeleton': mesh.get_editor_property('skeleton').get_path_name(), 'saved': saved, 'sec': round(time.time()-t0, 1)}
    print(g, report[g], flush=True)
dirty = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
report['dirty_after'] = dirty; report['saved_dirty_in_dest'] = {p: u.EditorAssetLibrary.save_asset(p, False) for p in dirty if p.startswith(DEST)}
(O/'j4_meshes.json').write_text(json.dumps(report, indent=1)); print(json.dumps(report, indent=1))
