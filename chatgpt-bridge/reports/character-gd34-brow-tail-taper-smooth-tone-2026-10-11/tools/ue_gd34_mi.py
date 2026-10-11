"""GD34: neutral-brown brow colour MI_GD34_BrowS_l1n = duplicate of the GD33 l1 brow MI (melanin 0.65, redness 0.45) with hairRedness 0.30
(front-view brow colour measured warmer than the reference: R/G 1.8-2.2 vs 1.6, B/G 0.53-0.64 vs 0.70). GD34 folder, refuses to overwrite."""
import unreal as u, json
SRC = '/Game/Sphirus/CharacterLab/GD33_IdentityMaster_20261011/Looks/MI_GD33_BrowS_l1'; DST = '/Game/Sphirus/CharacterLab/GD34_IdentityMaster_20261011/Looks/MI_GD34_BrowS_l1n'
EAL = u.EditorAssetLibrary; MEL = u.MaterialEditingLibrary; assert not EAL.does_asset_exist(DST)
m = EAL.duplicate_asset(SRC, DST); MEL.set_material_instance_scalar_parameter_value(m, 'hairRedness', 0.30); EAL.save_loaded_asset(m, False)
print('GD34_MI', json.dumps({k: round(MEL.get_material_instance_scalar_parameter_value(m, k), 3) for k in ('hairMelanin', 'hairRedness', 'RedVariation')}))
