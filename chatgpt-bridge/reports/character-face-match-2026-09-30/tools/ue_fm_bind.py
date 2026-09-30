"""FACE-MATCH pass: (re)build GroomBindings of the given grooms onto the isolated face derivative (new binding assets in the
lookdev Face folder; source grooms incl. the production eyebrow / eyelash grooms are only referenced, never modified).
builtins.FM_BIND = {'face': <face mesh path>, 'suffix': 'a', 'grooms': {'HairMain': <groom path>, ...}} -> fm_bindings_<suffix>.json"""
import unreal as u, json, pathlib, builtins
CFG = builtins.FM_BIND; EAL = u.EditorAssetLibrary; F = '/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Face/Bindings'; face = u.load_asset(CFG['face']); out = {}
for key, gpath in CFG['grooms'].items():
    g = u.load_asset(gpath); name = f'GB_FM_{key}_{CFG["suffix"]}'; path = F+'/'+name
    if EAL.does_asset_exist(path): EAL.delete_asset(path)
    b = u.GroomLibrary.create_new_groom_binding_asset_with_path(path, g, face, 100, None, 0); assert b, key
    out[key] = {'groom': gpath, 'binding': path, 'saved': EAL.save_loaded_asset(b, False)}
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
(pathlib.Path(u.Paths.project_dir()).resolve()/f'Saved/Codex/CharacterFaceMatch_20260930/fm_bindings_{CFG["suffix"]}.json').write_text(json.dumps(out, indent=1)); print('FM_BIND', json.dumps(out))
