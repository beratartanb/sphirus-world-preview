"""GD35: neutral (ash) brown brow colour variants, duplicates of the GD33 l1 brow MI (melanin 0.65), GD35 folder, refuse to overwrite:
 n2 = hairRedness 0.15; n3 = hairRedness 0.15 + Desat 0.35 (MI_Hair desaturation, l1 has 0.10). The reference brow core reads neutral
 (front R/G 1.59, B/G 0.71) while the GD34 brow read 1.75-2.2 / 0.53-0.65 with the forehead skin already matching the reference."""
import unreal as u, json
SRC = '/Game/Sphirus/CharacterLab/GD33_IdentityMaster_20261011/Looks/MI_GD33_BrowS_l1'; G = '/Game/Sphirus/CharacterLab/GD35_IdentityMaster_20261011/Looks'
EAL = u.EditorAssetLibrary; MEL = u.MaterialEditingLibrary; out = {}
for tag, vals in (('n2', {'hairRedness': 0.15}), ('n3', {'hairRedness': 0.15, 'Desat': 0.35})):
    dst = f'{G}/MI_GD35_BrowS_{tag}'; assert not EAL.does_asset_exist(dst); m = EAL.duplicate_asset(SRC, dst)
    for k, v in vals.items(): MEL.set_material_instance_scalar_parameter_value(m, k, v)
    EAL.save_loaded_asset(m, False); out[tag] = {k: round(MEL.get_material_instance_scalar_parameter_value(m, k), 3) for k in ('hairMelanin', 'hairRedness', 'Desat')}
print('GD35_MI', json.dumps(out))
