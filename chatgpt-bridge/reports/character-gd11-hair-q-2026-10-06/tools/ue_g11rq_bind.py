"""GD11 hair pass Q: bind a P hair tag (Main + Loose) to the locked m2 face in the P candidate folder (no face rig, no groom edit).
builtins.G11RQ_BIND = {'tag': 'h52a', 'resave': False}; resave=True only re-saves the built bindings (second job)."""
import unreal as u, json, builtins
C = builtins.G11RQ_BIND; EAL = u.EditorAssetLibrary; V = '/Game/Sphirus/CharacterLab/GD11_HairQ_20261006'; BD = V+'/Face/Bindings'
face = u.load_asset('/Game/Sphirus/CharacterLab/GD11_HeadRefinementM_20261005/Face/SKM_G11RM_Face_m2'); src = u.load_asset('/Game/Sphirus/CharacterLab/CharacterGuardian2_20261001/Face/SKM_GD_FaceMesh_p'); assert face and src; out = {}
for part in ('Main', 'Loose'):
    g = u.load_asset(f"{V}/Hair/GR_LK_Hair_{part}_{C['tag']}"); assert g; path = f"{BD}/GB_G11RQ_Hair{part}_m2{C['tag']}"
    if C.get('resave'): b = u.load_asset(path)
    else:
        if EAL.does_asset_exist(path): EAL.delete_asset(path)
        b = u.GroomLibrary.create_new_groom_binding_asset_with_path(path, g, face, 100, src, 0)
    assert b, path; ok = EAL.save_loaded_asset(b, False); t = b.get_editor_property('target_skeletal_mesh')
    out[part] = {'binding': b.get_path_name(), 'saved': ok, 'target': t.get_path_name() if t else None}
print('G11RQ_BIND', json.dumps(out))
