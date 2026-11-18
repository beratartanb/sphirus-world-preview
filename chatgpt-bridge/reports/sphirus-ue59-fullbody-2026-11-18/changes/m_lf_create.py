# m_lf_create.py (write, gated): new light-function material for DirectionalLight_0: sun multiplier = lerp(1, InsideK, box mask of the
# house interior in absolute world space, soft edges). Parameters: BoxMin, BoxMax (cm), Soft (cm), InsideK.
import unreal as u
P = '/Game/Sphirus/Lighting/Day_20261118'; N = 'M_Sph_SunInterior_LF'
EAL = u.EditorAssetLibrary; MEL = u.MaterialEditingLibrary
if EAL.does_asset_exist(P + '/' + N): m = u.load_asset(P + '/' + N)
else: m = u.AssetToolsHelpers.get_asset_tools().create_asset(N, P, u.Material, u.MaterialFactoryNew())
m.set_editor_property('material_domain', u.MaterialDomain.MD_LIGHT_FUNCTION)
MEL.delete_all_material_expressions(m)
E = lambda cls, x, y: MEL.create_material_expression(m, cls, x, y)
wp = E(u.MaterialExpressionWorldPosition, -1400, 0)
def vparam(n, v, y):
    e = E(u.MaterialExpressionVectorParameter, -1400, y); e.set_editor_property('parameter_name', n); e.set_editor_property('default_value', u.LinearColor(*v, 0.0)); return e
def sparam(n, v, y):
    e = E(u.MaterialExpressionScalarParameter, -1400, y); e.set_editor_property('parameter_name', n); e.set_editor_property('default_value', v); return e
bmin = vparam('BoxMin', (50.0, 40.0, 120.0), 200); bmax = vparam('BoxMax', (1472.0, 1100.0, 1000.0), 400)
soft = sparam('Soft', 15.0, 600); k = sparam('InsideK', __import__('builtins').__dict__.get('LF_K', 0.2), 800)
# lo = saturate((wp - bmin) / soft), hi = saturate((bmax - wp) / soft), mask = lo.x*lo.y*lo.z*hi.x*hi.y*hi.z
s1 = E(u.MaterialExpressionSubtract, -1100, 100); MEL.connect_material_expressions(wp, '', s1, 'A'); MEL.connect_material_expressions(bmin, 'RGB', s1, 'B')
s2 = E(u.MaterialExpressionSubtract, -1100, 300); MEL.connect_material_expressions(bmax, 'RGB', s2, 'A'); MEL.connect_material_expressions(wp, '', s2, 'B')
d1 = E(u.MaterialExpressionDivide, -950, 100); MEL.connect_material_expressions(s1, '', d1, 'A'); MEL.connect_material_expressions(soft, '', d1, 'B')
d2 = E(u.MaterialExpressionDivide, -950, 300); MEL.connect_material_expressions(s2, '', d2, 'A'); MEL.connect_material_expressions(soft, '', d2, 'B')
t1 = E(u.MaterialExpressionSaturate, -800, 100); MEL.connect_material_expressions(d1, '', t1, '')
t2 = E(u.MaterialExpressionSaturate, -800, 300); MEL.connect_material_expressions(d2, '', t2, '')
mm = E(u.MaterialExpressionMultiply, -650, 200); MEL.connect_material_expressions(t1, '', mm, 'A'); MEL.connect_material_expressions(t2, '', mm, 'B')
def comp(ch, y):
    c = E(u.MaterialExpressionComponentMask, -500, y)
    for n in 'rgba': c.set_editor_property(n, n == ch)
    MEL.connect_material_expressions(mm, '', c, ''); return c
cx, cy, cz = comp('r', 100), comp('g', 200), comp('b', 300)
m1 = E(u.MaterialExpressionMultiply, -350, 150); MEL.connect_material_expressions(cx, '', m1, 'A'); MEL.connect_material_expressions(cy, '', m1, 'B')
m2 = E(u.MaterialExpressionMultiply, -200, 200); MEL.connect_material_expressions(m1, '', m2, 'A'); MEL.connect_material_expressions(cz, '', m2, 'B')
one = E(u.MaterialExpressionConstant, -200, 50); one.set_editor_property('r', 1.0)
lp = E(u.MaterialExpressionLinearInterpolate, -50, 150); MEL.connect_material_expressions(one, '', lp, 'A'); MEL.connect_material_expressions(k, '', lp, 'B'); MEL.connect_material_expressions(m2, '', lp, 'Alpha')
MEL.connect_material_property(lp, '', u.MaterialProperty.MP_EMISSIVE_COLOR)
MEL.recompile_material(m)
print('LFMAT', m.get_path_name(), m.get_editor_property('material_domain'), MEL.get_num_material_expressions(m))
print('SAVED', EAL.save_loaded_asset(m, False))
