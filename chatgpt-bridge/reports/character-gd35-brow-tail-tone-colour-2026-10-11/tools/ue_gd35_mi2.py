"""GD35: one more neutral step n4 = GD33 l1 brow MI with hairRedness 0.05 + Desat 0.55 (n3: 0.15 / 0.35 still read warmer than the reference)."""
import unreal as u, json
SRC = '/Game/Sphirus/CharacterLab/GD33_IdentityMaster_20261011/Looks/MI_GD33_BrowS_l1'; DST = '/Game/Sphirus/CharacterLab/GD35_IdentityMaster_20261011/Looks/MI_GD35_BrowS_n4'
EAL = u.EditorAssetLibrary; MEL = u.MaterialEditingLibrary; assert not EAL.does_asset_exist(DST); m = EAL.duplicate_asset(SRC, DST)
for k, v in {'hairRedness': 0.05, 'Desat': 0.55}.items(): MEL.set_material_instance_scalar_parameter_value(m, k, v)
EAL.save_loaded_asset(m, False); print('GD35_MI2', json.dumps({k: round(MEL.get_material_instance_scalar_parameter_value(m, k), 3) for k in ('hairMelanin', 'hairRedness', 'Desat')}))
