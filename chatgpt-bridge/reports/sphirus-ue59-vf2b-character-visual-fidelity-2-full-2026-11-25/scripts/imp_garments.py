# VF2B write job: project-owned refitted top + fabric material + shorts material instance. Vendor assets are only read.
# New packages (all under /Game/Sphirus/CharacterLab/VF2_20261124/Garments): SKM_Sph_RetroTop_VF2, M_Sph_Fabric_VF2, MI_Sph_RetroTop_VF2, MI_Sph_CuffedShorts_VF2
import unreal as u
E = u.EditorAssetLibrary; AT = u.AssetToolsHelpers.get_asset_tools(); mel = u.MaterialEditingLibrary
assert not u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(), 'PIE running'
D = '/Game/Sphirus/CharacterLab/VF2_20261124/Garments'
sk = u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Common/Female/Medium/NormalWeight/Body/metahuman_base_skel')
src = u.Paths.convert_relative_path_to_full(u.Paths.project_saved_dir()) + 'UE59Work/vf2b/bl/retro_top_vf2.fbx'
# ---- 1. skeletal mesh
t = u.AssetImportTask(); t.filename = src; t.destination_path = D; t.destination_name = 'SKM_Sph_RetroTop_VF2'; t.automated = True; t.save = False; t.replace_existing = True
o = u.FbxImportUI(); o.import_mesh = True; o.import_as_skeletal = True; o.mesh_type_to_import = u.FBXImportType.FBXIT_SKELETAL_MESH; o.skeleton = sk
o.import_materials = False; o.import_textures = False; o.import_animations = False; o.create_physics_asset = False; o.automated_import_should_detect_type = False
sd = o.skeletal_mesh_import_data; sd.set_editor_property('update_skeleton_reference_pose', False); sd.set_editor_property('use_t0_as_ref_pose', False); sd.set_editor_property('import_morph_targets', False)
sd.set_editor_property('normal_import_method', u.FBXNormalImportMethod.FBXNIM_COMPUTE_NORMALS)
t.options = o; AT.import_asset_tasks([t])
m = u.load_asset(D + '/SKM_Sph_RetroTop_VF2'); assert m, 'import failed'
old = u.load_asset('/Game/Sphirus/CharacterLab/Day_20261107/Garments/SKM_Sph_RetroTop')
b = m.get_bounds(); b0 = old.get_bounds()
print('IG new bounds o', [round(v, 1) for v in (b.origin.x, b.origin.y, b.origin.z)], 'e', [round(v, 1) for v in (b.box_extent.x, b.box_extent.y, b.box_extent.z)])
print('IG old bounds o', [round(v, 1) for v in (b0.origin.x, b0.origin.y, b0.origin.z)], 'e', [round(v, 1) for v in (b0.box_extent.x, b0.box_extent.y, b0.box_extent.z)])
print('IG skel', m.get_editor_property('skeleton').get_name(), 'verts', u.get_editor_subsystem(u.SkeletalMeshEditorSubsystem).get_num_verts(m, 0), 'slots', [str(x.material_slot_name) for x in m.materials])
assert abs(b.origin.z - b0.origin.z) < 6 and abs(b.box_extent.z - b0.box_extent.z) < 6, 'scale/axis mismatch'
# ---- 2. fabric material (cloth shading, vendor textures, fine weave detail, tint)
MP = D + '/M_Sph_Fabric_VF2'
if E.does_asset_exist(MP): mat = u.load_asset(MP); mel.delete_all_material_expressions(mat)
else: mat = AT.create_asset('M_Sph_Fabric_VF2', D, u.Material, u.MaterialFactoryNew())
mat.set_editor_property('shading_model', u.MaterialShadingModel.MSM_CLOTH); mat.set_editor_property('two_sided', True)
def ex(cls, x, y): return mel.create_material_expression(mat, cls, x, y)
def tex(name, path, x, y, st):
    e = ex(u.MaterialExpressionTextureSampleParameter2D, x, y); e.set_editor_property('parameter_name', name); e.set_editor_property('texture', u.load_asset(path)); e.set_editor_property('sampler_type', st); return e
def sc(name, v, x, y):
    e = ex(u.MaterialExpressionScalarParameter, x, y); e.set_editor_property('parameter_name', name); e.set_editor_property('default_value', v); return e
def vc(name, c, x, y):
    e = ex(u.MaterialExpressionVectorParameter, x, y); e.set_editor_property('parameter_name', name); e.set_editor_property('default_value', u.LinearColor(*c)); return e
T = '/Game/Fab/MetaHuman/Retro_top_blue/Textures/'
bc = tex('BaseColor', T + 'T_Retro_Top_BaseColor', -900, -300, u.MaterialSamplerType.SAMPLERTYPE_COLOR)
nm = tex('Normal', T + 'T_Retro_Top_Normal', -900, 0, u.MaterialSamplerType.SAMPLERTYPE_NORMAL)
orm = tex('ORM', T + 'T_Retro_Top_OcclusionRoughnessMetallic', -900, 300, u.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR)
dt = tex('WeaveNormal', '/Game/InfinityAssets/Texture/Materials/Fabric/T_Plain_Wool_Fabric_N', -900, 600, u.MaterialSamplerType.SAMPLERTYPE_NORMAL)
uv = ex(u.MaterialExpressionTextureCoordinate, -1300, 600); til = sc('WeaveTiling', 36.0, -1300, 700); muv = ex(u.MaterialExpressionMultiply, -1100, 640)
mel.connect_material_expressions(uv, '', muv, 'A'); mel.connect_material_expressions(til, '', muv, 'B'); mel.connect_material_expressions(muv, '', dt, 'UVs')
# base colour: desaturate a little, tint
tint = vc('Tint', (0.80, 0.84, 0.86, 1.0), -900, -500); des = ex(u.MaterialExpressionDesaturation, -600, -300); dsat = sc('Desaturation', 0.18, -900, -420)
mel.connect_material_expressions(bc, 'RGB', des, ''); mel.connect_material_expressions(dsat, '', des, 'Fraction')
mbc = ex(u.MaterialExpressionMultiply, -400, -300); mel.connect_material_expressions(des, '', mbc, 'A'); mel.connect_material_expressions(tint, '', mbc, 'B')
mel.connect_material_property(mbc, '', u.MaterialProperty.MP_BASE_COLOR)
# normals: flatten the coarse vendor normal (reads as towel), blend a fine weave on top
def flat(src, name, v, x, y):
    f = ex(u.MaterialExpressionMaterialFunctionCall, x, y); f.set_material_function(u.load_asset('/Engine/Functions/Engine_MaterialFunctions01/Texturing/FlattenNormal')); s = sc(name, v, x - 200, y + 120)
    mel.connect_material_expressions(src, 'RGB', f, 'Normal'); mel.connect_material_expressions(s, '', f, 'Flatness'); return f
fn = flat(nm, 'NormalFlatten', 0.45, -500, 0); fd = flat(dt, 'WeaveFlatten', 0.35, -500, 600)
bl = ex(u.MaterialExpressionMaterialFunctionCall, -200, 200); bl.set_material_function(u.load_asset('/Engine/Functions/Engine_MaterialFunctions02/Utility/BlendAngleCorrectedNormals'))
mel.connect_material_expressions(fn, '', bl, 'BaseNormal'); mel.connect_material_expressions(fd, '', bl, 'AdditionalNormal')
mel.connect_material_property(bl, '', u.MaterialProperty.MP_NORMAL)
# roughness / AO / cloth fuzz
rm = sc('RoughnessMul', 1.0, -900, 480); mr = ex(u.MaterialExpressionMultiply, -500, 320); mel.connect_material_expressions(orm, 'G', mr, 'A'); mel.connect_material_expressions(rm, '', mr, 'B')
rmin = sc('RoughnessMin', 0.72, -500, 440); mx = ex(u.MaterialExpressionMax, -300, 340); mel.connect_material_expressions(mr, '', mx, 'A'); mel.connect_material_expressions(rmin, '', mx, 'B')
mel.connect_material_property(mx, '', u.MaterialProperty.MP_ROUGHNESS); mel.connect_material_property(orm, 'R', u.MaterialProperty.MP_AMBIENT_OCCLUSION)
fz = vc('FuzzColor', (0.55, 0.60, 0.62, 1.0), -500, -700); mel.connect_material_property(fz, '', u.MaterialProperty.MP_SUBSURFACE_COLOR)
cl = sc('Cloth', 0.6, -500, -560); mel.connect_material_property(cl, '', u.MaterialProperty.MP_CUSTOM_DATA0)
mat.set_editor_property('used_with_skeletal_mesh', True) if hasattr(mat, 'used_with_skeletal_mesh') else None
try: mel.set_material_usage(mat, u.MaterialUsage.MATUSAGE_SKELETAL_MESH)
except Exception as e: print('IG usage', e)
mel.recompile_material(mat); mel.layout_material_expressions(mat)
print('IG material expressions', mel.get_num_material_expressions(mat))
# ---- 3. instances
def mi(name, parent):
    p = D + '/' + name
    x = u.load_asset(p) if E.does_asset_exist(p) else AT.create_asset(name, D, u.MaterialInstanceConstant, u.MaterialInstanceConstantFactoryNew())
    mel.set_material_instance_parent(x, parent); return x
mt = mi('MI_Sph_RetroTop_VF2', mat); mel.update_material_instance(mt)
vs = u.load_asset('/Game/Outfits/Relaxed_Cuffed_Shorts/Relaxed_Cuffed_Shorts/MT/MI_Relaxed_Cuffed_Shorts')
ms = mi('MI_Sph_CuffedShorts_VF2', vs.get_editor_property('parent'))
for n in mel.get_scalar_parameter_names(vs): mel.set_material_instance_scalar_parameter_value(ms, n, mel.get_material_instance_scalar_parameter_value(vs, n))
for n in mel.get_vector_parameter_names(vs): mel.set_material_instance_vector_parameter_value(ms, n, mel.get_material_instance_vector_parameter_value(vs, n))
for n in mel.get_texture_parameter_names(vs): mel.set_material_instance_texture_parameter_value(ms, n, mel.get_material_instance_texture_parameter_value(vs, n))
# cuffs / waistband: vendor lavender-blue (0.263,0.284,0.413) reads as sportswear trim; bring it into the garment's olive family, darker
mel.set_material_instance_vector_parameter_value(ms, 'COLOR2', u.LinearColor(0.070, 0.078, 0.058, 1.0))
mel.set_material_instance_vector_parameter_value(ms, 'COLOR3', u.LinearColor(0.120, 0.105, 0.085, 1.0))
mel.set_material_instance_scalar_parameter_value(ms, 'Roughness', 0.88); mel.set_material_instance_scalar_parameter_value(ms, 'STAIN', 0.16)
mel.set_material_instance_vector_parameter_value(ms, 'STAINCOLOR', u.LinearColor(0.42, 0.36, 0.28, 1.0))
mel.update_material_instance(ms)
sl = list(m.materials)
for x in sl: x.material_interface = mt
m.materials = sl
for a in ('SKM_Sph_RetroTop_VF2', 'M_Sph_Fabric_VF2', 'MI_Sph_RetroTop_VF2', 'MI_Sph_CuffedShorts_VF2'):
    print('IG saved', a, E.save_loaded_asset(u.load_asset(D + '/' + a), False))
print('IG dirty', [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()], [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()])
