"""GUARDIAN-3: iris colour MIs (children of the project eye MIs; parents referenced only). builtins.GD3_EYES = {'tag', 'iris_mult': [r,g,b], 'primary_value': v}"""
import unreal as u, json, builtins
C = builtins.GD3_EYES; EAL = u.EditorAssetLibrary; ME = u.MaterialEditingLibrary; AT = u.AssetToolsHelpers.get_asset_tools(); F = '/Game/Sphirus/CharacterLab/CharacterGuardian3_20261001/Skin'; out = {}
for s in ('L', 'R'):
    par = u.load_asset(f'/Game/Sphirus/CharacterLab/ShoulderFix_20260928/Assembly/SHOULDER_FIX_NATIVE/Face/Materials/MI_Eye{s}_Baked'); n = f"MI_GD3_Eye{s}_{C['tag']}"; dst = F+'/'+n
    m = u.load_asset(dst) if EAL.does_asset_exist(dst) else AT.create_asset(n, F, u.MaterialInstanceConstant, u.MaterialInstanceConstantFactoryNew())
    ME.set_material_instance_parent(m, par); c = C['iris_mult']; ME.set_material_instance_vector_parameter_value(m, 'Iris Color Multiply', u.LinearColor(c[0], c[1], c[2], 1))
    ME.set_material_instance_scalar_parameter_value(m, 'Iris Primary Color Value', C['primary_value']); sc = C.get('sclera'); sc and ME.set_material_instance_vector_parameter_value(m, 'Sclera Color Multiply', u.LinearColor(sc[0], sc[1], sc[2], 1)); ME.update_material_instance(m); out[n] = EAL.save_loaded_asset(m, False)
print('GD3_EYES', json.dumps(out))
