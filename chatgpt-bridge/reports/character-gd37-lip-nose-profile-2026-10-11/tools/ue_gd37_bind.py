"""GD37 groom bindings onto the new face (GD37 folder only, never overwrites another pass): builtins.GD37_BIND = {'face': face SKM path, 'items':
[(groom path, binding path, source mesh path or None), ...]}. Uses GroomLibrary.create_new_groom_binding_asset_with_path (100 interpolation pts)."""
import unreal as u, json, builtins
C = builtins.GD37_BIND; EAL = u.EditorAssetLibrary; G = '/Game/Sphirus/CharacterLab/GD37_IdentityMaster_20261011'; face = u.load_asset(C['face']); assert face, C['face']; out = {}
for gp, bp, sp in C['items']:
    assert bp.startswith(G+'/'), 'GD37 guard ' + bp
    if EAL.does_asset_exist(bp): EAL.delete_asset(bp)
    b = u.GroomLibrary.create_new_groom_binding_asset_with_path(bp, u.load_asset(gp), face, 100, u.load_asset(sp) if sp else None, 0); assert b, bp
    out[bp.rsplit('/', 1)[-1]] = EAL.save_loaded_asset(b, False)
print('GD37_BIND', json.dumps(out))
