"""Diagnose bone-weight transfer on the final geometry without creating assets (read-only)."""
import unreal as u, pathlib, json, gzip
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/OutfitHome_20260929'
GEO = json.loads(gzip.open(O/'build_final/outfit_geometry.json.gz', 'rb').read())
BODY = u.load_asset('/Game/Sphirus/CharacterLab/BodyRealism_20260929/SKM_BR_BodyMesh'); BW = u.GeometryScript_BoneWeights; ME_ = u.GeometryScript_MeshEdits
body_dm = u.DynamicMesh(); lod = u.GeometryScriptMeshReadLOD(); lod.lod_type = u.GeometryScriptLODType.SOURCE_MODEL; lod.lod_index = 0
u.GeometryScript_AssetUtils.copy_mesh_from_skeletal_mesh(BODY, body_dm, u.GeometryScriptCopyMeshFromAssetOptions(), lod)
def build(G, weld):
    P = G['positions']; T = G['triangles']; UVs = G['uv']; MI = G['material_ids']
    dm = u.DynamicMesh(); u.GeometryScript_Materials.enable_material_i_ds(dm)
    for m in range(max(MI)+1):
        tris = [t for t, mi in zip(T, MI) if mi == m]
        if not tris: continue
        used = sorted({v for t in tris for v in t}); remap = {v: i for i, v in enumerate(used)}
        buf = u.GeometryScriptSimpleMeshBuffers(); buf.set_editor_property('vertices', [u.Vector(*P[v]) for v in used]); buf.set_editor_property('uv0', [u.Vector2D(*UVs[v]) for v in used])
        buf.set_editor_property('triangles', [u.IntVector(remap[a], remap[b], remap[c]) for a, b, c in tris]); ME_.append_buffers_to_mesh(dm, buf, m, True)
    if weld: u.GeometryScript_MeshRepair.weld_mesh_edges(dm, u.GeometryScriptWeldEdgesOptions())
    return dm
def has(dm):
    r = BW.mesh_has_bone_weights(dm); return bool(r[-1]) if isinstance(r, tuple) else bool(r)
res = {}
for g in ['trousers', 'trousers_lod1', 'henley']:
    for weld in (False, True):
        for method in ('INPAINT_WEIGHTS', 'CLOSEST_POINT_ON_SURFACE'):
            dm = build(GEO[g], weld); BW.copy_bones_from_mesh(body_dm, dm, u.GeometryScriptCopyBonesFromMeshOptions())
            to = u.GeometryScriptTransferBoneWeightsOptions(); to.set_editor_property('transfer_method', getattr(u.TransferBoneWeightsMethod, method)); to.set_editor_property('output_target_mesh_bones', u.OutputTargetMeshBones.SOURCE_BONES)
            if method == 'INPAINT_WEIGHTS':
                to.set_editor_property('radius_percentage', 0.06); to.set_editor_property('normal_threshold', 45.0); to.set_editor_property('num_smoothing_iterations', 6); to.set_editor_property('smoothing_strength', 0.5)
            BW.transfer_bone_weights_from_mesh(body_dm, dm, to)
            key = g+' weld='+str(weld)+' '+method; res[key] = {'has_weights': has(dm), 'verts': dm.get_vertex_count(), 'tris': dm.get_triangle_count()}
            print(key, res[key], flush=True)
(O/'j4_diag.json').write_text(json.dumps(res, indent=1)); print(json.dumps(res))
