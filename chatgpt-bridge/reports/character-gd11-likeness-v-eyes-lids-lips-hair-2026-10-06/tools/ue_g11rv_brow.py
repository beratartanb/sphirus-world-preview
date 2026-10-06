"""GD11 pass V: thinner / sparser / hair-coloured variant of the user's M_SlightArch brow (same shape). Copies the Guardian library copy
GR_GD_Eyebrows_M_SlightArch (untouched) to GD11_FaceR_20261006/Grooms/GR_G11RV_Eyebrows_<v>, sets strand width, build-time curve decimation and
child MIs of the library hair materials (melanin / redness), then binds it to the candidate face with the library groom head as source.
builtins.G11RV_BROW = {'v', 'face', 'suffix', 'width', 'decim', 'mat': {param: value}}  -> binding GB_G11RR_EyebrowsCustom_<v>_<suffix>"""
import unreal as u, builtins, json
C = builtins.G11RV_BROW; EAL = u.EditorAssetLibrary; ME = u.MaterialEditingLibrary; AT = u.AssetToolsHelpers.get_asset_tools()
R = '/Game/Sphirus/CharacterLab/GD11_FaceR_20261006'; F = R+'/Grooms'; v = C['v']; out = {}
src = '/Game/Sphirus/CharacterLab/CharacterGuardian_20261001/Grooms/GR_GD_Eyebrows_M_SlightArch'; dst = f'{F}/GR_G11RV_Eyebrows_{v}'
if not EAL.does_asset_exist(dst): assert EAL.duplicate_asset(src, dst), src
g = u.load_asset(dst)
mats = g.get_editor_property('hair_groups_materials'); new = []
for i, ms in enumerate(list(mats)):
    par = ms.get_editor_property('material'); n = f'MI_G11RV_Brow{i}_{v}'; p = f'{R}/Skin/{n}'
    mi = u.load_asset(p) if EAL.does_asset_exist(p) else AT.create_asset(n, R+'/Skin', u.MaterialInstanceConstant, u.MaterialInstanceConstantFactoryNew())
    ME.set_material_instance_parent(mi, par); names = [str(x) for x in ME.get_scalar_parameter_names(mi)]; set_ = {}
    for k, val in C['mat'].items():
        if k in names: ME.set_material_instance_scalar_parameter_value(mi, k, val); set_[k] = val
    ME.update_material_instance(mi); EAL.save_loaded_asset(mi, False); ms.set_editor_property('material', mi); new.append(ms); out[n] = {'parent': par.get_path_name(), 'set': set_}
g.set_editor_property('hair_groups_materials', new)
rs = g.get_editor_property('hair_groups_rendering')
for i_ in range(len(rs)):   # array items are copies: write each back by index
    r = rs[i_]; gs = r.get_editor_property('geometry_settings'); gs.set_editor_property('hair_width', C['width']); gs.set_editor_property('hair_width_override', True); r.set_editor_property('geometry_settings', gs); rs[i_] = r
g.set_editor_property('hair_groups_rendering', rs)
lods = g.get_editor_property('hair_groups_lod')   # sparser: LOD0 curve decimation (the interpolation DecimationSettings do not persist from Python)
for i_ in range(len(lods)):
    gl = lods[i_]; ll = gl.get_editor_property('lods'); l0 = ll[0]; l0.set_editor_property('curve_decimation', C['decim']); ll[0] = l0; gl.set_editor_property('lods', ll); lods[i_] = gl
g.set_editor_property('hair_groups_lod', lods)
try: g.build_hair_groups_data() if hasattr(g, 'build_hair_groups_data') else None
except Exception as e: out['build_err'] = str(e)
out['groom'] = EAL.save_loaded_asset(g, False)
out['readback'] = {'width': [r.get_editor_property('geometry_settings').get_editor_property('hair_width') for r in g.get_editor_property('hair_groups_rendering')],
                   'decim': [gl.get_editor_property('lods')[0].get_editor_property('curve_decimation') for gl in g.get_editor_property('hair_groups_lod')],
                   'mats': [m.get_editor_property('material').get_path_name() for m in g.get_editor_property('hair_groups_materials')]}
bp = f'{R}/Face/Bindings/GB_G11RR_EyebrowsCustom_{v}_{C["suffix"]}'
if EAL.does_asset_exist(bp): EAL.delete_asset(bp)
b = u.GroomLibrary.create_new_groom_binding_asset_with_path(bp, g, u.load_asset(C['face']), 100, u.load_asset('/MetaHumanCharacter/Optional/Grooms/GroomMesh/SKM_Groom_Head_Legacy01'), 0)
out['binding'] = bool(b) and EAL.save_loaded_asset(b, False)
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]; print('G11RV_BROW', json.dumps(out))
