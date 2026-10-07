import unreal as u, json
EAL = u.EditorAssetLibrary; MEL = u.MaterialEditingLibrary; D = '/Game/Sphirus/CharacterLab/GD11_FaceR_20261006/Skin'; out = {}
EYE = {'Iris Primary Color Value': 0.9, 'Iris Secondary Color Value': 0.32, 'Iris Global Saturation': 0.82, 'Iris Shadow Details Amount': 0.62}
for s in ('L', 'R'):
    dst = f'{D}/MI_G11CC_Eye{s}_e3m'; assert not EAL.does_asset_exist(dst); m = EAL.duplicate_asset(f'{D}/MI_G11RV_Eye{s}_e3g', dst)
    for k, v in EYE.items(): MEL.set_material_instance_scalar_parameter_value(m, k, v)
    MEL.set_material_instance_vector_parameter_value(m, 'Iris Color Multiply', u.LinearColor(0.98, 0.72, 0.48, 1.0)); out[dst] = EAL.save_loaded_asset(m, False)
print('IRIS_M', json.dumps(out))
