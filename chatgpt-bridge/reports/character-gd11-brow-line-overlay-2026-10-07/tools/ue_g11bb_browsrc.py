"""pass BB (brow line): lower the library brow on the candidate face WITHOUT changing the face. The brow binding transfers roots from the
library source head (SKM_Groom_Head_Legacy01, same topology as the face) by triangle correspondence; a COPY of that source head with the brow
footprint raised by d cm makes the roots land d cm lower on the face. Library assets untouched; face untouched.
builtins.G11BB = {'face': path, 'variants': {'d25': 0.25, ...}, 'bs': binding suffix}"""
import unreal as u, json, builtins, math
C = builtins.G11BB; EAL = u.EditorAssetLibrary; q = u.GeometryScript_MeshQueries; l = u.GeometryScript_List; out = {}
LIB_SRC = '/MetaHumanCharacter/Optional/Grooms/GroomMesh/SKM_Groom_Head_Legacy01'; LIB_GROOM = '/Game/Sphirus/CharacterLab/CharacterGuardian_20261001/Grooms/GR_GD_Eyebrows_M_SlightArch'
D = '/Game/Sphirus/CharacterLab/GD11_FaceR_20261006'; MX = -0.23
def fresh(m):
    dm = u.DynamicMesh(); lod = u.GeometryScriptMeshReadLOD(); lod.lod_type = u.GeometryScriptLODType.SOURCE_MODEL; lod.lod_index = 0
    r = u.GeometryScript_AssetUtils.copy_mesh_from_skeletal_mesh(m, dm, u.GeometryScriptCopyMeshFromAssetOptions(), lod); assert 'SUCCESS' in str(r[-1] if isinstance(r, tuple) else r); return dm
def ss(t): t = min(max(t, 0.0), 1.0); return t*t*(3-2*t)
def plateau(v, a, b, m): return ss((v-(a-m))/m)*(1-ss((v-b)/m))
face = u.load_asset(C['face']); PF = l.convert_vector_list_to_array(q.get_all_vertex_positions(fresh(face), False)[1])
W = [plateau(abs(p.x-MX), 0.6, 6.0, 0.5)*plateau(p.z, 163.3, 166.3, 0.5)*ss((p.y-8.5)/0.8) for p in PF]
out['n_weighted'] = sum(1 for w in W if w > 0.01)
for tag, d in C['variants'].items():
    sp = f'{D}/Grooms/BrowSrc/SKM_G11BB_BrowSrc_{tag}'; gp = f'{D}/Grooms/GR_G11BB_Eyebrows_{tag}'; bp = f'{D}/Face/Bindings/GB_G11RR_EyebrowsCustom_{tag}_{C["bs"]}'
    for p in (sp, gp): assert not EAL.does_asset_exist(p), 'exists: ' + p
    src = EAL.duplicate_asset(LIB_SRC, sp); assert src; dm = fresh(src); PS = l.convert_vector_list_to_array(q.get_all_vertex_positions(dm, False)[1]); assert len(PS) == len(PF)
    mx = 0.0
    for i, w in enumerate(W):
        if w > 0.0005:
            p = PS[i]; u.GeometryScript_MeshEdits.set_vertex_position(dm, i, u.Vector(p.x, p.y, p.z+d*w), True); mx = max(mx, d*w)
    wl = u.GeometryScriptMeshWriteLOD(); wl.lod_index = 0; opt = u.GeometryScriptCopyMeshToAssetOptions()
    r = u.GeometryScript_AssetUtils.copy_mesh_to_skeletal_mesh(dm, src, opt, wl); ok = 'SUCCESS' in str(r[-1] if isinstance(r, tuple) else r)
    chk = l.convert_vector_list_to_array(q.get_all_vertex_positions(fresh(src), False)[1]); dz = max(chk[i].z-PS[i].z for i in range(len(PS)))
    g = EAL.duplicate_asset(LIB_GROOM, gp); assert g
    b = u.GroomLibrary.create_new_groom_binding_asset_with_path(bp, g, face, 100, src, 0)
    out[tag] = {'src_written': ok, 'src_max_raise_cm': round(dz, 3), 'set_max_cm': round(mx, 3), 'binding': bool(b), 'saved': [EAL.save_loaded_asset(x, False) for x in (src, g, b) if x]}
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]; print('G11BB', json.dumps(out))
