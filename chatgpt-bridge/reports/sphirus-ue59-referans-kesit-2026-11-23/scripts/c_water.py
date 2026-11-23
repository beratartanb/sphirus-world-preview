# c_water.py (control, in-memory only): MI_EX_Pond scalar parameters from builtins.R2G_WATER (dict). Prints old -> new.
import unreal as u, builtins
V = getattr(builtins, 'R2G_WATER', None) or {}
m = u.load_asset('/Game/GraceRanger/Environment/Exterior20260921/Materials/MI_EX_Pond'); L = u.MaterialEditingLibrary
print('WATER_OLD', {k: round(L.get_material_instance_scalar_parameter_value(m, k), 4) for k in ('Specular', 'Roughness', 'Calm Normal Amplitude', 'Murkiness')})
for k, v in V.items(): print('SET', k, L.set_material_instance_scalar_parameter_value(m, k, v))
if V: L.update_material_instance(m)
print('WATER_NEW', {k: round(L.get_material_instance_scalar_parameter_value(m, k), 4) for k in ('Specular', 'Roughness', 'Calm Normal Amplitude', 'Murkiness')})
