"""GD15: bind MetaHuman LIBRARY grooms (authored on SKM_Groom_Head_Legacy01/02) to a candidate face with the library groom head as SOURCE mesh.
Library grooms are DUPLICATED INTO THE GD15 FOLDER (never into older candidate folders); an optional per-duplicate material map replaces the
duplicate's hair-group materials (GD15 MIs). builtins.GD15_LB = {'face', 'suffix', 'bind_folder', 'groom_folder', 'prefix',
'items': [(kind 'Eyebrows'|'Eyelashes', style, {slot_name: MI path} or None, dup_suffix or '')]}"""
import unreal as u, builtins, json
C = builtins.GD15_LB; EAL = u.EditorAssetLibrary; F = C['groom_folder']; B = C['bind_folder']; out = {}
assert F.startswith('/Game/Sphirus/CharacterLab/GD15_IdentityMaster_') and B.startswith('/Game/Sphirus/CharacterLab/GD15_IdentityMaster_'), 'GD15 guard'
face = u.load_asset(C['face'])
SRC = {'Eyebrows': ('/MetaHumanCharacter/Optional/Grooms/GroomMesh/SKM_Groom_Head_Legacy01', 0), 'Eyelashes': ('/MetaHumanCharacter/Optional/Grooms/GroomMesh/SKM_Groom_Head_Legacy02', 8)}
MX = -0.23
def _ss(t): t = min(max(t, 0.0), 1.0); return t*t*(3-2*t)
def _pl(v, a, b, m): return _ss((v-(a-m))/m)*(1-_ss((v-b)/m))
def _fresh(m):
    dm = u.DynamicMesh(); lod = u.GeometryScriptMeshReadLOD(); lod.lod_type = u.GeometryScriptLODType.SOURCE_MODEL; lod.lod_index = 0
    u.GeometryScript_AssetUtils.copy_mesh_from_skeletal_mesh(m, dm, u.GeometryScriptCopyMeshFromAssetOptions(), lod); return dm
def brow_proxy(sm, d, tag):
    """2026-10-09 GD15 (GD11 pass-BB method): GD15 COPY of the style's source head with the brow footprint moved by d cm in z; binding through it
    lands the roots -d on the unchanged face (d < 0 raises the brow). Footprint weights from the FACE positions (same 33,845-vertex topology)."""
    sp = f"{F}/BrowSrc/SKM_GD15_BrowSrc_{sm.rsplit('/', 1)[-1]}_{tag}"
    if EAL.does_asset_exist(sp): return sp, 'exists'
    lq = u.GeometryScript_MeshQueries; ll = u.GeometryScript_List
    PF = ll.convert_vector_list_to_array(lq.get_all_vertex_positions(_fresh(face), False)[1])
    src = EAL.duplicate_asset(sm, sp); assert src; dm = _fresh(src); PS = ll.convert_vector_list_to_array(lq.get_all_vertex_positions(dm, False)[1]); assert len(PS) == len(PF), (len(PS), len(PF))
    n = 0
    for i, p in enumerate(PF):
        w = _pl(abs(p.x-MX), 0.6, 6.0, 0.5)*_pl(p.z, 163.3, 166.3, 0.5)*_ss((p.y-8.5)/0.8)
        if w > 0.0005: q_ = PS[i]; u.GeometryScript_MeshEdits.set_vertex_position(dm, i, u.Vector(q_.x, q_.y, q_.z+d*w), True); n += 1
    wl = u.GeometryScriptMeshWriteLOD(); wl.lod_index = 0
    r = u.GeometryScript_AssetUtils.copy_mesh_to_skeletal_mesh(dm, src, u.GeometryScriptCopyMeshToAssetOptions(), wl)
    EAL.save_loaded_asset(src, False); return sp, {'moved': n, 'write': str(r[-1] if isinstance(r, tuple) else r)[-40:]}
for it in C['items']:
    kind, st, mats, ds = it[:4]; shift = it[4] if len(it) > 4 else None
    src = f'/MetaHumanCharacter/Optional/Grooms/GroomAssets/{kind}/{kind}_{st}/{kind}_{st}'; dst = f'{F}/GR_GD15_{kind}_{st}{ds}'
    if not EAL.does_asset_exist(dst):
        assert EAL.duplicate_asset(src, dst), src
        g = u.load_asset(dst)
        if mats:
            arr = g.get_editor_property('hair_groups_materials'); new = []
            for x in arr:
                nm = str(x.get_editor_property('slot_name'))
                if nm in mats: x.set_editor_property('material', u.load_asset(mats[nm]))
                new.append(x)
            g.set_editor_property('hair_groups_materials', new)
        EAL.save_loaded_asset(g, False)
    g = u.load_asset(dst); sm, sec = SRC[kind]
    pb = u.load_asset(f'/MetaHumanCharacter/Optional/Grooms/Bindings/{kind}/{kind}_{st}_Binding')   # 2026-10-09: per-style source head (Legacy01 vs Legacy02)
    if pb:
        ssm = pb.get_editor_property('source_skeletal_mesh') or pb.get_editor_property('target_skeletal_mesh')
        if ssm: sm = ssm.get_path_name().split('.')[0]
        try: sec = int(pb.get_editor_property('matching_section'))
        except Exception: pass
    pinfo = None
    if shift: sm, pinfo = brow_proxy(sm, shift['d'], shift['tag'])
    bp = f'{B}/{C.get("prefix", "GB_GD15")}_{kind}{st}{ds}_{C["suffix"]}'
    if EAL.does_asset_exist(bp): EAL.delete_asset(bp)
    b = u.GroomLibrary.create_new_groom_binding_asset_with_path(bp, g, face, 100, u.load_asset(sm), sec)
    out[f'{kind}_{st}{ds}'] = {'groom': dst, 'binding': bp, 'ok': bool(b) and EAL.save_loaded_asset(b, False), 'source': sm, 'section': sec, 'proxy': pinfo, 'mats': [[str(x.get_editor_property('slot_name')), x.get_editor_property('material').get_path_name() if x.get_editor_property('material') else None] for x in g.get_editor_property('hair_groups_materials')]}
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]; print('GD15_LB', json.dumps(out))
