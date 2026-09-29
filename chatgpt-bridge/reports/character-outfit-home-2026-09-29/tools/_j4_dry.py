"""J4: build the garment skeletal meshes from the Blender geometry: DynamicMesh from buffers (per material id), normals
and tangents, skeleton bones copied from the current BR body mesh, skin weights transferred from the body surface
(inpaint method), then a NEW SkeletalMesh asset on the isolated ShoulderFix skeleton. No existing asset is modified."""
import unreal as u, pathlib, json, gzip, math, builtins, time
builtins.OF_GEO_FILE = "build_v3/outfit_geometry.json.gz"
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/OutfitHome_20260929'
GEO = json.loads(gzip.open(O/builtins.__dict__.get('OF_GEO_FILE', 'build_v2/outfit_geometry.json.gz'), 'rb').read())
DEST = '/Game/Sphirus/CharacterLab/Outfit_Home_20260929'; MD = DEST+'/Materials'
SKEL = u.load_asset('/Game/Sphirus/CharacterLab/ShoulderFix_20260928/Common/Female/Medium/NormalWeight/Body/metahuman_base_skel')
BODY = u.load_asset('/Game/Sphirus/CharacterLab/BodyRealism_20260929/SKM_BR_BodyMesh')
q = u.GeometryScript_MeshQueries; l = u.GeometryScript_List; BW = u.GeometryScript_BoneWeights; N = u.GeometryScript_Normals; ME_ = u.GeometryScript_MeshEdits
def pick(r, typ):
    r = r if isinstance(r, tuple) else (r,)
    return [x for x in r if isinstance(x, typ)][0]
body_dm = u.DynamicMesh(); lod = u.GeometryScriptMeshReadLOD(); lod.lod_type = u.GeometryScriptLODType.SOURCE_MODEL; lod.lod_index = 0
r = u.GeometryScript_AssetUtils.copy_mesh_from_skeletal_mesh(BODY, body_dm, u.GeometryScriptCopyMeshFromAssetOptions(), lod); assert 'SUCCESS' in str(r[-1])
assert BW.mesh_has_bone_weights(body_dm)[-1] if isinstance(BW.mesh_has_bone_weights(body_dm), tuple) else True
MATS = {'henley': ['MI_Home_Henley', 'MI_Home_Henley_Trim', 'MI_Home_Buttons'], 'trousers': ['MI_Home_Trousers', 'MI_Home_Trousers_Trim', 'MI_Home_Trousers_Trim', 'MI_Home_Drawstring']}
NAMES = {'henley': 'SKM_Home_Henley', 'trousers': 'SKM_Home_Trousers'}
report = {}
for g in ['henley', 'trousers']:
    t0 = time.time(); G = GEO[g]; P = G['positions']; T = G['triangles']; UVs = G['uv']; MI = G['material_ids']
    dm = u.DynamicMesh(); u.GeometryScript_Materials.enable_material_i_ds(dm)
    nmat = max(MI)+1
    for m in range(nmat):
        tris = [t for t, mi in zip(T, MI) if mi == m]
        if not tris: continue
        used = sorted({v for t in tris for v in t}); remap = {v: i for i, v in enumerate(used)}
        buf = u.GeometryScriptSimpleMeshBuffers()
        buf.set_editor_property('vertices', [u.Vector(*P[v]) for v in used])
        buf.set_editor_property('uv0', [u.Vector2D(*UVs[v]) for v in used])
        buf.set_editor_property('triangles', [u.IntVector(remap[a], remap[b], remap[c]) for a, b, c in tris])
        ME_.append_buffers_to_mesh(dm, buf, m, True)
    # weld the material-boundary duplicates back together (same position + same uv) so normals are continuous
    u.GeometryScript_MeshRepair.weld_mesh_edges(dm, u.GeometryScriptWeldEdgesOptions())
    opt = u.GeometryScriptCalculateNormalsOptions(); opt.set_editor_property('angle_weighted', True); opt.set_editor_property('area_weighted', True)
    N.set_per_vertex_normals(dm); N.recompute_normals(dm, opt); N.compute_tangents(dm, u.GeometryScriptTangentsOptions())
    nv = dm.get_vertex_count(); nt = dm.get_triangle_count()
    # skeleton + weights from the body
    BW.copy_bones_from_mesh(body_dm, dm, u.GeometryScriptCopyBonesFromMeshOptions())
    to = u.GeometryScriptTransferBoneWeightsOptions(); to.set_editor_property('transfer_method', u.TransferBoneWeightsMethod.INPAINT_WEIGHTS)
    to.set_editor_property('radius_percentage', 0.06); to.set_editor_property('normal_threshold', 45.0); to.set_editor_property('num_smoothing_iterations', 6); to.set_editor_property('smoothing_strength', 0.5)
    to.set_editor_property('output_target_mesh_bones', u.OutputTargetMeshBones.SOURCE_BONES)
    BW.transfer_bone_weights_from_mesh(body_dm, dm, to)
    # asset
    co = u.GeometryScriptCreateNewSkeletalMeshAssetOptions()
    co.set_editor_property('enable_recompute_normals', False); co.set_editor_property('enable_recompute_tangents', False); co.set_editor_property('use_original_vertex_order', True)
    r = u.GeometryScript_NewAssetUtils.create_new_skeletal_mesh_asset_from_mesh(dm, SKEL, DEST+'/'+NAMES[g], co)
    mesh = r[0] if isinstance(r, tuple) else r; ok = 'SUCCESS' in str(r[-1]); assert ok and mesh, r
    slots = []
    for i, n in enumerate(MATS[g]):
        sm = u.SkeletalMaterial(); sm.set_editor_property('material_interface', u.load_asset(MD+'/'+n)); sm.set_editor_property('material_slot_name', GEO[g]['materials'][i] if i < len(GEO[g]['materials']) else n); slots.append(sm)
    mesh.set_editor_property('materials', slots)
    # weights readback for the offline deformation evaluation
    bi = BW.get_all_bones_info(dm); bi = pick(bi, u.Array) if isinstance(bi, tuple) else bi
    bones = [str(b.get_editor_property('name')) for b in bi]
    W = []; miss = 0
    for v in range(nv):
        rr = BW.get_vertex_bone_weights(dm, v); arr = [x for x in (rr if isinstance(rr, tuple) else (rr,)) if isinstance(x, u.Array)]
        if not arr or len(arr[0]) == 0: miss += 1; W.append({}); continue
        W.append({bones[int(b.get_editor_property('bone_index'))]: float(b.get_editor_property('weight')) for b in arr[0]})
    V = l.convert_vector_list_to_array(q.get_all_vertex_positions(dm, False)[1]); TT = l.convert_triangle_list_to_array(q.get_all_triangle_indices(dm, False)[1])
    with gzip.open(O/f'asset_{g}_lod0.json.gz', 'wt') as f: json.dump({'positions': [[p.x, p.y, p.z] for p in V], 'triangles': [[t.x, t.y, t.z] for t in TT], 'weights': W}, f)
    mesh.set_editor_property('post_process_anim_blueprint', None)
    saved = u.EditorAssetLibrary.save_loaded_asset(mesh, False)
    report[g] = {'asset': mesh.get_path_name(), 'verts': nv, 'tris': nt, 'weights_missing': miss, 'bones_in_mesh': len(bones), 'materials': [str(s.get_editor_property('material_slot_name')) for s in mesh.get_editor_property('materials')],
                 'skeleton': mesh.get_editor_property('skeleton').get_path_name(), 'saved': saved, 'sec': round(time.time()-t0, 1)}
    print(g, report[g], flush=True)
report['dirty_after'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
(O/'j4_meshes.json').write_text(json.dumps(report, indent=1)); print(json.dumps(report, indent=1))
