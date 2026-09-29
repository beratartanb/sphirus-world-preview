"""J2 (idempotent): textile master material (Cloth shading model, two-sided, MaterialAttributes so the Cloth/fuzz pins are
reachable) + instances. Unique BC/N/RA + tiling detail weave normal (angle-corrected blend), tint, roughness multiplier,
fuzz colour, cloth amount. Recompile happens in J3 (separate job: re-entrancy)."""
import unreal as u, json
ME = u.MaterialEditingLibrary; AT = u.AssetToolsHelpers.get_asset_tools()
DEST = '/Game/Sphirus/CharacterLab/CharacterFinal_20260929/Outfit'; TX = DEST+'/Textures'; MD = DEST+'/Materials'
mat = u.load_asset(MD+'/M_SPH_Textile') if u.EditorAssetLibrary.does_asset_exist(MD+'/M_SPH_Textile') else AT.create_asset('M_SPH_Textile', MD, u.Material, u.MaterialFactoryNew())
ME.delete_all_material_expressions(mat)
mat.set_editor_property('shading_model', u.MaterialShadingModel.MSM_CLOTH); mat.set_editor_property('two_sided', True); mat.set_editor_property('use_material_attributes', True)
def node(cls, x, y): return ME.create_material_expression(mat, cls, x, y)
def texparam(name, path, x, y, sampler):
    n = node(u.MaterialExpressionTextureSampleParameter2D, x, y); n.set_editor_property('parameter_name', name); n.set_editor_property('texture', u.load_asset(path)); n.set_editor_property('sampler_type', sampler); return n
def sparam(name, val, x, y): n = node(u.MaterialExpressionScalarParameter, x, y); n.set_editor_property('parameter_name', name); n.set_editor_property('default_value', val); return n
def vparam(name, col, x, y): n = node(u.MaterialExpressionVectorParameter, x, y); n.set_editor_property('parameter_name', name); n.set_editor_property('default_value', u.LinearColor(*col)); return n
bc = texparam('BaseColorTex', TX+'/T_Henley_BC', -1100, -400, u.MaterialSamplerType.SAMPLERTYPE_COLOR)
nm = texparam('NormalTex', TX+'/T_Henley_N', -1100, 0, u.MaterialSamplerType.SAMPLERTYPE_NORMAL)
ra = texparam('RoughAOTex', TX+'/T_Henley_RA', -1100, 300, u.MaterialSamplerType.SAMPLERTYPE_MASKS)
dn = texparam('DetailNormalTex', TX+'/T_Detail_Jersey_N', -1100, 650, u.MaterialSamplerType.SAMPLERTYPE_NORMAL)
tc = node(u.MaterialExpressionTextureCoordinate, -1500, 650); tiling = sparam('DetailTiling', 28.0, -1500, 760)
mulUV = node(u.MaterialExpressionMultiply, -1300, 680); ME.connect_material_expressions(tc, '', mulUV, 'A'); ME.connect_material_expressions(tiling, '', mulUV, 'B'); ME.connect_material_expressions(mulUV, '', dn, 'UVs')
tint = vparam('Tint', (1, 1, 1, 1), -800, -550); mulBC = node(u.MaterialExpressionMultiply, -600, -400); ME.connect_material_expressions(bc, '', mulBC, 'A'); ME.connect_material_expressions(tint, '', mulBC, 'B')
dstr = sparam('DetailNormalStrength', 0.6, -800, 850); flat = node(u.MaterialExpressionConstant3Vector, -800, 950); flat.set_editor_property('constant', u.LinearColor(0, 0, 1, 1))
lerpN = node(u.MaterialExpressionLinearInterpolate, -600, 750); ME.connect_material_expressions(flat, '', lerpN, 'A'); ME.connect_material_expressions(dn, '', lerpN, 'B'); ME.connect_material_expressions(dstr, '', lerpN, 'Alpha')
blend = node(u.MaterialExpressionMaterialFunctionCall, -400, 250); blend.set_editor_property('material_function', u.load_asset('/Engine/Functions/Engine_MaterialFunctions02/Utility/BlendAngleCorrectedNormals'))
ME.connect_material_expressions(nm, '', blend, 'BaseNormal'); ME.connect_material_expressions(lerpN, '', blend, 'AdditionalNormal')
rmul = sparam('RoughnessMult', 1.0, -800, 450); mulR = node(u.MaterialExpressionMultiply, -600, 400); ME.connect_material_expressions(ra, 'R', mulR, 'A'); ME.connect_material_expressions(rmul, '', mulR, 'B')
spec = sparam('Specular', 0.25, -800, 550); fuzz = vparam('FuzzColor', (0.35, 0.32, 0.28, 1), -800, 1100); cloth = sparam('Cloth', 0.55, -800, 1250)
mma = node(u.MaterialExpressionMakeMaterialAttributes, -100, 0)
ME.connect_material_expressions(mulBC, '', mma, 'BaseColor'); ME.connect_material_expressions(blend, '', mma, 'Normal'); ME.connect_material_expressions(mulR, '', mma, 'Roughness')
ME.connect_material_expressions(ra, 'G', mma, 'AmbientOcclusion'); ME.connect_material_expressions(spec, '', mma, 'Specular'); ME.connect_material_expressions(fuzz, '', mma, 'SubsurfaceColor'); ME.connect_material_expressions(cloth, '', mma, 'ClearCoat')
ME.connect_material_property(mma, '', u.MaterialProperty.MP_MATERIAL_ATTRIBUTES)
ME.layout_material_expressions(mat); u.EditorAssetLibrary.save_loaded_asset(mat, False)
INST = {'MI_Home2_Henley': {'tex': ('T_Henley_BC', 'T_Henley_N', 'T_Henley_RA', 'T_Detail_Jersey_N'), 'tint': (0.97, 0.93, 0.86), 'rough': 1.04, 'tiling': 36.0, 'fuzz': (0.55, 0.50, 0.42), 'cloth': 0.65, 'dstr': 0.5},
        'MI_Home2_Henley_Trim': {'tex': ('T_Henley_BC', 'T_Henley_N', 'T_Henley_RA', 'T_Detail_Jersey_N'), 'tint': (0.94, 0.94, 0.93), 'rough': 1.0, 'tiling': 40.0, 'fuzz': (0.5, 0.46, 0.4), 'cloth': 0.6, 'dstr': 0.7},
        'MI_Home2_Shorts': {'tex': ('T_Shorts_BC', 'T_Shorts_N', 'T_Shorts_RA', 'T_Detail_Twill_N'), 'tint': (1.25, 1.2, 1.15), 'rough': 1.02, 'tiling': 38.0, 'fuzz': (0.16, 0.15, 0.14), 'cloth': 0.5, 'dstr': 0.45},
        'MI_Home2_Shorts_Trim': {'tex': ('T_Shorts_BC', 'T_Shorts_N', 'T_Shorts_RA', 'T_Detail_Twill_N'), 'tint': (0.92, 0.92, 0.92), 'rough': 1.0, 'tiling': 40.0, 'fuzz': (0.12, 0.12, 0.12), 'cloth': 0.45, 'dstr': 0.6},
        'MI_Home2_Drawstring': {'tex': ('T_Shorts_BC', 'T_Shorts_N', 'T_Shorts_RA', 'T_Detail_Twill_N'), 'tint': (4.2, 3.4, 2.6), 'rough': 1.05, 'tiling': 90.0, 'fuzz': (0.3, 0.26, 0.2), 'cloth': 0.7, 'dstr': 0.9},
        'MI_Home2_Buttons': {'tex': ('T_Henley_BC', 'T_Henley_N', 'T_Henley_RA', 'T_Detail_Jersey_N'), 'tint': (0.42, 0.30, 0.20), 'rough': 0.55, 'tiling': 1.0, 'fuzz': (0.1, 0.08, 0.06), 'cloth': 0.0, 'dstr': 0.0}}
out = {}
for name, p in INST.items():
    mi = u.load_asset(MD+'/'+name) if u.EditorAssetLibrary.does_asset_exist(MD+'/'+name) else AT.create_asset(name, MD, u.MaterialInstanceConstant, u.MaterialInstanceConstantFactoryNew())
    ME.set_material_instance_parent(mi, mat)
    for pn, tn in zip(('BaseColorTex', 'NormalTex', 'RoughAOTex', 'DetailNormalTex'), p['tex']): ME.set_material_instance_texture_parameter_value(mi, pn, u.load_asset(TX+'/'+tn))
    ME.set_material_instance_vector_parameter_value(mi, 'Tint', u.LinearColor(*p['tint'], 1)); ME.set_material_instance_vector_parameter_value(mi, 'FuzzColor', u.LinearColor(*p['fuzz'], 1))
    for pn, key in (('RoughnessMult', 'rough'), ('DetailTiling', 'tiling'), ('Cloth', 'cloth'), ('DetailNormalStrength', 'dstr')): ME.set_material_instance_scalar_parameter_value(mi, pn, p[key])
    out[name] = u.EditorAssetLibrary.save_loaded_asset(mi, False)
print(json.dumps({'master': mat.get_path_name(), 'instances': out}))
