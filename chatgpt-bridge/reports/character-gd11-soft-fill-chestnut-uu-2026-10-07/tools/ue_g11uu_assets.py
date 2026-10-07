"""pass UU: skin k18 = k15 (no extra regional detail -> less 'muscular' shading) + the k17 matte settings; iris e3n = lighter brown (between e3g and e3m). New assets only."""
import unreal as u, json
EAL = u.EditorAssetLibrary; MEL = u.MaterialEditingLibrary; D = '/Game/Sphirus/CharacterLab/GD11_FaceR_20261006/Skin'; out = {}
for n in ('LOD0', 'LOD1', 'LOD2', 'LOD3', 'LOD4', 'LOD5to7'):
    dst = f'{D}/MI_LK_Face_{n}_VT_gqk18'; assert not EAL.does_asset_exist(dst); m = EAL.duplicate_asset(f'{D}/MI_LK_Face_{n}_VT_gqk15', dst)
    for k, v in {'Specular Global Multiply Post-Bake': 0.7, 'Roughness Global Multiply Post-Bake': 1.12}.items(): MEL.set_material_instance_scalar_parameter_value(m, k, v)
    out[dst] = EAL.save_loaded_asset(m, False)
for s in ('L', 'R'):
    dst = f'{D}/MI_G11CC_Eye{s}_e3n'; assert not EAL.does_asset_exist(dst); m = EAL.duplicate_asset(f'{D}/MI_G11RV_Eye{s}_e3g', dst)
    for k, v in {'Iris Primary Color Value': 1.05, 'Iris Secondary Color Value': 0.4, 'Iris Global Saturation': 0.86, 'Iris Shadow Details Amount': 0.58}.items(): MEL.set_material_instance_scalar_parameter_value(m, k, v)
    MEL.set_material_instance_vector_parameter_value(m, 'Iris Color Multiply', u.LinearColor(1.06, 0.8, 0.52, 1.0)); out[dst] = EAL.save_loaded_asset(m, False)
print('G11UU_ASSETS', json.dumps(out))
