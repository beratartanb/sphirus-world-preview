"""GUARDIAN face pass: isolated brow = duplicate of the production Eyebrows_M_Slit groom (read-only source) with thinner strands and a
lighter auburn-brown child MI; bound to the candidate face. builtins.GD_BS = {'face', 'suffix', 'width', 'melanin', 'redness', 'name'}"""
import unreal as u, builtins, json
C = builtins.GD_BS; EAL = u.EditorAssetLibrary; ME = u.MaterialEditingLibrary; AT = u.AssetToolsHelpers.get_asset_tools()
F = '/Game/Sphirus/CharacterLab/CharacterGuardian_20261001/Grooms'; B = '/Game/Sphirus/CharacterLab/CharacterGuardian_20261001/Face/Bindings'; out = {}
dst = f"{F}/GR_GD_Eyebrows_{C['name']}"
if not EAL.does_asset_exist(dst): assert EAL.duplicate_asset('/Game/MetaHumans/MH_MainCharacter/Grooms/Eyebrows_M_Slit', dst)
mp = f"{F}/MI_GD_Eyebrows_{C['name']}"; mi = u.load_asset(mp) if EAL.does_asset_exist(mp) else AT.create_asset(f"MI_GD_Eyebrows_{C['name']}", F, u.MaterialInstanceConstant, u.MaterialInstanceConstantFactoryNew())
ME.set_material_instance_parent(mi, u.load_asset('/Game/MetaHumans/MH_MainCharacter/Grooms/MI_WI_Eyebrows_M_Slit_Hair'))
ME.set_material_instance_scalar_parameter_value(mi, 'hairMelanin', C['melanin']); ME.set_material_instance_scalar_parameter_value(mi, 'hairRedness', C['redness']); ME.update_material_instance(mi); EAL.save_loaded_asset(mi, False)
g = u.load_asset(dst); mats = g.get_editor_property('hair_groups_materials'); mats[0].set_editor_property('material', mi); g.set_editor_property('hair_groups_materials', mats)
import re
rs = g.get_editor_property('hair_groups_rendering'); new = []
for r in rs:
    t = re.sub(r'HairWidth=[0-9.]+', 'HairWidth=%.6f' % C['width'], r.export_text()); r2 = u.HairGroupsRendering(); r2.import_text(t); new.append(r2)
g.set_editor_property('hair_groups_rendering', new); EAL.save_loaded_asset(g, False)
out['width'] = [r.get_editor_property('geometry_settings').get_editor_property('hair_width') for r in g.get_editor_property('hair_groups_rendering')]
bp = f"{B}/GB_GD_Brow{C['name']}_{C['suffix']}"
b = u.load_asset(bp) if EAL.does_asset_exist(bp) else u.GroomLibrary.create_new_groom_binding_asset_with_path(bp, g, u.load_asset(C['face']), 100, None, 0)
out['binding'] = bool(b) and EAL.save_loaded_asset(b, False); out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]; print('GD_BS', json.dumps(out))
