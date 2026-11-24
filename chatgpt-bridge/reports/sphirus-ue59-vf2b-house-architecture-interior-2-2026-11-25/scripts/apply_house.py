"""apply_house.py (in memory; saved only by w_house.py): VF2B house pass v2, 2026-11-25. Material assets only, no map change.
Both new materials are DUPLICATES of the project material M_HouseSurface (so the existing look is kept exactly) with one extra stage
spliced in front of the base colour / roughness / normal outputs:
1. M_Sph_LimePlaster_VF2  -> MI_R3_Surface_lime (interior partition walls): world-space macro tone variation, a scuff/grime band above
   each floor, a trowelled stucco relief.
2. M_Sph_HearthStone_VF2  -> MI_R3_hearth_OriginalAtlas (stone fireplace): soot around and inside the firebox, ash on the hearth stone.
   (Decals do not show on M_HouseSurface surfaces, so the soot is part of the material.)
3. MI_BR_ExteriorDeck (balcony floor, rendered plain white): weathered boards from the veranda board instance.
The graphs are built once (when the material does not exist yet); every tunable is an instance parameter, so later runs only set values.
builtins.VF2H = overrides; builtins.VF2H_REVERT=True restores the three instances to their previous parents/values."""
import unreal as u, builtins, json, os
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
E = u.EditorAssetLibrary; mel = u.MaterialEditingLibrary
C = dict(macro=0.5, grime=0.6, grime_h=40.0, relief=0.55, size=150.0, soot=1.25, ash=0.8, deck_uv=3.0, deck=False, hearth_vec={'SootFrontRadius': (58.0, 92.0, 78.0, 0.0), 'SootInsideRadius': (70.0, 56.0, 64.0, 0.0)}); C.update(getattr(builtins, 'VF2H', None) or {})
D = '/Game/Sphirus/House/VF2_20261125'; SRC = '/Game/SphirusHouse/LivedIn_R05/Materials/M_HouseSurface'; I = '/Game/SphirusHouse/LivedIn_R05/Materials/Instances/'
lime = u.load_asset(I + 'MI_R3_Surface_lime'); hearth = u.load_asset(I + 'MI_R3_hearth_OriginalAtlas'); deck = u.load_asset(I + 'MI_BR_ExteriorDeck')
BF = u.Paths.project_dir() + 'Tools/VF2B_20261125/deck_base.json'
def setp(mi, sc={}, vc={}):
    for k, v in sc.items(): mel.set_material_instance_scalar_parameter_value(mi, k, float(v))
    for k, v in vc.items(): mel.set_material_instance_vector_parameter_value(mi, k, u.LinearColor(*v))
    mel.update_material_instance(mi)
if getattr(builtins, 'VF2H_REVERT', False):
    hs = u.load_asset(SRC)
    for m in (lime, hearth, u.load_asset(I + 'MI_R3_Surface_masonry')): mel.set_material_instance_parent(m, hs); mel.update_material_instance(m)
    b = json.load(open(BF)); mel.clear_all_material_instance_parameters(deck); mel.set_material_instance_parent(deck, u.load_asset(b['parent']))
    setp(deck, b['scalars'], b['vectors'])
    for k, v in b['textures'].items(): mel.set_material_instance_texture_parameter_value(deck, k, u.load_asset(v) if v else None)
    mel.update_material_instance(deck); builtins.VF2H_TOUCHED = [lime, hearth, deck]; print('VF2H reverted')
else:
    class G:
        def __init__(s, mat): s.m = mat
        def ex(s, cls, x, y): return mel.create_material_expression(s.m, cls, x, y)
        def sc(s, n, v, x, y):
            e = s.ex(u.MaterialExpressionScalarParameter, x, y); e.set_editor_property('parameter_name', n); e.set_editor_property('default_value', v); e.set_editor_property('group', 'VF2'); return e
        def vc(s, n, c, x, y):
            e = s.ex(u.MaterialExpressionVectorParameter, x, y); e.set_editor_property('parameter_name', n); e.set_editor_property('default_value', u.LinearColor(*c)); e.set_editor_property('group', 'VF2'); return e
        def cn(s, v, x, y):
            e = s.ex(u.MaterialExpressionConstant, x, y); e.set_editor_property('r', v); return e
        def c3(s, c, x, y):
            e = s.ex(u.MaterialExpressionConstant3Vector, x, y); e.set_editor_property('constant', u.LinearColor(c[0], c[1], c[2], 1)); return e
        def op(s, cls, a, b, x, y, ao='', bo=''):
            e = s.ex(cls, x, y); assert mel.connect_material_expressions(a, ao, e, 'A'), (cls, 'A'); assert mel.connect_material_expressions(b, bo, e, 'B'), (cls, 'B'); return e
        def one(s, cls, a, x, y, ao=''):
            e = s.ex(cls, x, y); assert mel.connect_material_expressions(a, ao, e, ''), cls; return e
        def lerp(s, a, b, t, x, y, ao='', bo=''):
            e = s.ex(u.MaterialExpressionLinearInterpolate, x, y); assert mel.connect_material_expressions(a, ao, e, 'A'); assert mel.connect_material_expressions(b, bo, e, 'B'); assert mel.connect_material_expressions(t, '', e, 'Alpha'); return e
        def mask(s, a, ch, x, y):
            e = s.ex(u.MaterialExpressionComponentMask, x, y)
            for k in 'rgba': e.set_editor_property(k, k in ch)
            assert mel.connect_material_expressions(a, '', e, ''); return e
        def noise(s, wp, scale, x, y, levels=2):
            n = s.ex(u.MaterialExpressionNoise, x + 80, y)   # default position = absolute world position, scaled by 'scale'
            n.set_editor_property('noise_function', u.NoiseFunction.NOISEFUNCTION_GRADIENT_TEX3D); n.set_editor_property('levels', levels); n.set_editor_property('output_min', 0.0); n.set_editor_property('output_max', 1.0)
            n.set_editor_property('turbulence', False); n.set_editor_property('scale', scale); return n
        def src(s, prop):
            e = mel.get_material_property_input_node(s.m, prop); return e, (mel.get_material_property_input_node_output_name(s.m, prop) if e else '')
        def length(s, d, x, y):
            dd = s.ex(u.MaterialExpressionDotProduct, x, y); assert mel.connect_material_expressions(d, '', dd, 'A'); assert mel.connect_material_expressions(d, '', dd, 'B'); return s.one(u.MaterialExpressionSquareRoot, dd, x + 120, y)
    MUL, ADD, SUB, DIV, MAX = u.MaterialExpressionMultiply, u.MaterialExpressionAdd, u.MaterialExpressionSubtract, u.MaterialExpressionDivide, u.MaterialExpressionMax
    SAT = u.MaterialExpressionSaturate; BC, RG, NM = u.MaterialProperty.MP_BASE_COLOR, u.MaterialProperty.MP_ROUGHNESS, u.MaterialProperty.MP_NORMAL; X = 1200
    def build_plaster(pm):
        g = G(pm); b0, b0o = g.src(BC); r0, r0o = g.src(RG); n0, n0o = g.src(NM); assert b0 and r0, 'unexpected source graph'
        wp = g.ex(u.MaterialExpressionWorldPosition, X, 0); nmac = g.noise(wp, 0.0042, X + 300, 0, 3); nfine = g.noise(wp, 0.034, X + 300, 250, 2)
        mac = g.op(ADD, g.cn(1.0, X + 700, -80), g.op(MUL, g.op(SUB, nmac, g.cn(0.56, X + 550, 80), X + 650, 20), g.sc('MacroAmount', 0.3, X + 550, 160), X + 760, 60), X + 880, 0)
        wz = g.mask(wp, 'b', X + 200, 520); gh = g.sc('GrimeHeight', 38.0, X + 200, 700)
        def band(nm, fz, y):
            d = g.op(SUB, wz, g.sc(nm, fz, X + 300, y + 90), X + 450, y); up = g.one(SAT, g.op(SUB, g.cn(1.0, X + 560, y - 70), g.op(DIV, d, gh, X + 580, y), X + 700, y), X + 820, y)
            ab = g.one(SAT, g.op(DIV, g.op(ADD, d, g.cn(5.0, X + 560, y + 150), X + 680, y + 130), g.cn(5.0, X + 760, y + 200), X + 820, y + 130), X + 940, y + 130); return g.op(MUL, up, ab, X + 1060, y)
        gb = g.op(MAX, band('FloorZ1', 150.0, 520), band('FloorZ2', 490.0, 860), X + 1220, 680)
        gm = g.one(SAT, g.op(MUL, g.op(MUL, gb, gb, X + 1340, 680), g.op(ADD, nfine, g.cn(0.4, X + 1300, 820), X + 1420, 790), X + 1520, 700), X + 1640, 700)
        gt = g.op(MUL, gm, g.sc('GrimeAmount', 0.5, X + 1600, 860), X + 1760, 720)
        c1 = g.op(MUL, b0, mac, X + 1900, -200, ao=b0o); c2 = g.lerp(c1, g.op(MUL, c1, g.vc('GrimeColor', (0.60, 0.52, 0.42, 1), X + 1900, 60), X + 2060, -60), gt, X + 2220, -160)
        assert mel.connect_material_property(c2, '', BC)
        rv = g.one(SAT, g.op(ADD, g.op(ADD, r0, g.op(MUL, g.op(SUB, nmac, g.cn(0.5, X + 1900, 420), X + 2020, 380), g.cn(0.14, X + 2020, 470), X + 2140, 400), X + 2260, 340, ao=r0o), g.op(MUL, gt, g.cn(0.08, X + 2140, 560), X + 2260, 520), X + 2380, 400), X + 2500, 400)
        assert mel.connect_material_property(rv, '', RG)
        fn = g.ex(u.MaterialExpressionMaterialFunctionCall, X + 1400, 1300); fn.set_material_function(u.load_asset('/Engine/Functions/Engine_MaterialFunctions01/Texturing/WorldAlignedNormal'))
        to = g.ex(u.MaterialExpressionTextureObjectParameter, X + 1000, 1300); to.set_editor_property('parameter_name', 'PlasterNormal'); to.set_editor_property('texture', u.load_asset('/Game/InfinityAssets/Texture/Materials/Wall/T_Stucco_Facade_N')); to.set_editor_property('group', 'VF2')
        psz = g.sc('PlasterSize', 150.0, X + 1000, 1450); v2 = g.op(u.MaterialExpressionAppendVector, psz, psz, X + 1120, 1450); v3 = g.op(u.MaterialExpressionAppendVector, v2, psz, X + 1240, 1450)
        assert mel.connect_material_expressions(to, '', fn, 'TextureObject'); assert mel.connect_material_expressions(v3, '', fn, 'TextureSize')
        fl = g.ex(u.MaterialExpressionMaterialFunctionCall, X + 1700, 1300); fl.set_material_function(u.load_asset('/Engine/Functions/Engine_MaterialFunctions01/Texturing/FlattenNormal'))
        assert mel.connect_material_expressions(fn, 'XYZ Texture', fl, 'Normal'); assert mel.connect_material_expressions(g.op(SUB, g.cn(1.0, X + 1400, 1560), g.sc('ReliefStrength', 0.5, X + 1400, 1640), X + 1560, 1580), '', fl, 'Flatness')
        if n0:
            bl = g.ex(u.MaterialExpressionMaterialFunctionCall, X + 2000, 1200); bl.set_material_function(u.load_asset('/Engine/Functions/Engine_MaterialFunctions02/Utility/BlendAngleCorrectedNormals'))
            assert mel.connect_material_expressions(n0, n0o, bl, 'BaseNormal'); assert mel.connect_material_expressions(fl, '', bl, 'AdditionalNormal'); assert mel.connect_material_property(bl, '', NM)
        else: assert mel.connect_material_property(fl, '', NM)
        print('VF2H plaster built; source nodes', b0.get_class().get_name(), b0o, r0.get_class().get_name(), n0.get_class().get_name() if n0 else None, 'tangent', pm.get_editor_property('tangent_space_normal'))
    def build_hearth(hm):
        g = G(hm); b0, b0o = g.src(BC); r0, r0o = g.src(RG); assert b0 and r0
        wp = g.ex(u.MaterialExpressionWorldPosition, X, 0); nf = g.noise(wp, 0.05, X + 300, 0, 3)
        def ell(nm, c, r, y, power):
            d = g.op(DIV, g.op(SUB, wp, g.vc(nm + 'Center', c + (0,), X, y + 150), X + 250, y), g.vc(nm + 'Radius', r + (0,), X + 250, y + 150), X + 420, y)
            m = g.one(SAT, g.op(SUB, g.cn(1.0, X + 760, y - 70), g.length(g.mask(d, 'rgb', X + 500, y), X + 600, y), X + 880, y), X + 1000, y); pw = g.ex(u.MaterialExpressionPower, X + 1120, y)
            assert mel.connect_material_expressions(m, '', pw, 'Base'); assert mel.connect_material_expressions(g.cn(power, X + 1000, y + 100), '', pw, 'Exp'); return pw
        front = ell('SootFront', (1392.0, 905.0, 252.0), (46.0, 78.0, 62.0), 500, 1.3)
        inside = ell('SootInside', (1452.0, 905.0, 196.0), (62.0, 52.0, 58.0), 900, 0.6)
        sm = g.one(SAT, g.op(MUL, g.op(MAX, front, inside, X + 1300, 700), g.op(ADD, g.op(MUL, nf, g.cn(0.9, X + 1200, 300), X + 1320, 260), g.cn(0.5, X + 1320, 360), X + 1440, 300), X + 1560, 600), X + 1680, 600)
        st = g.op(MUL, sm, g.sc('SootAmount', 0.9, X + 1680, 760), X + 1800, 640)
        vn = g.mask(g.ex(u.MaterialExpressionVertexNormalWS, X, 1400), 'b', X + 200, 1400); upf = g.one(SAT, g.op(MUL, g.op(SUB, vn, g.cn(0.6, X + 300, 1500), X + 420, 1420), g.cn(4.0, X + 420, 1520), X + 540, 1440), X + 660, 1440)
        ashm = g.op(MUL, g.op(MUL, ell('Ash', (1418.0, 905.0, 170.0), (40.0, 50.0, 30.0), 1700, 0.8), upf, X + 1300, 1500), g.one(SAT, g.op(ADD, nf, g.cn(0.25, X + 1200, 1640), X + 1320, 1620), X + 1440, 1620), X + 1560, 1520)
        at = g.op(MUL, ashm, g.sc('AshAmount', 0.7, X + 1560, 1700), X + 1700, 1540)
        c1 = g.lerp(b0, g.vc('SootColor', (0.035, 0.031, 0.028, 1), X + 1800, -60), st, X + 2000, -200, ao=b0o); c2 = g.lerp(c1, g.vc('AshColor', (0.33, 0.32, 0.31, 1), X + 2000, 60), at, X + 2200, -160)
        assert mel.connect_material_property(c2, '', BC)
        rv = g.lerp(r0, g.cn(0.93, X + 2000, 420), g.one(SAT, g.op(ADD, st, at, X + 1900, 520), X + 2020, 520), X + 2200, 400, ao=r0o); assert mel.connect_material_property(rv, '', RG)
        print('VF2H hearth built')
    def make(name, build):
        p = D + '/' + name
        if E.does_asset_exist(p): return u.load_asset(p)
        m = u.AssetToolsHelpers.get_asset_tools().duplicate_asset(name, D, u.load_asset(SRC)); assert m, name; build(m); mel.recompile_material(m); return m
    SUF = C.get('suffix', ''); pm = make('M_Sph_LimePlaster_VF2' + SUF, build_plaster); hm = make('M_Sph_HearthStone_VF2' + SUF, build_hearth)
    print('VF2H parents before', lime.get_editor_property('parent').get_name(), hearth.get_editor_property('parent').get_name(), deck.get_editor_property('parent').get_name())
    mel.set_material_instance_parent(lime, pm); setp(lime, {'MacroAmount': C['macro'], 'GrimeAmount': C['grime'], 'GrimeHeight': C['grime_h'], 'ReliefStrength': C['relief'], 'PlasterSize': C['size']})
    masonry = u.load_asset(I + 'MI_R3_Surface_masonry')   # chimney breast + firebox back wall
    for hmi in (hearth, masonry): mel.set_material_instance_parent(hmi, hm); setp(hmi, {'SootAmount': C['soot'], 'AshAmount': C['ash']}, C.get('hearth_vec', {}))
    if not os.path.exists(BF):
        json.dump({'parent': deck.get_editor_property('parent').get_path_name().split('.')[0],
                   'scalars': {str(n): mel.get_material_instance_scalar_parameter_value(deck, n) for n in mel.get_scalar_parameter_names(deck)},
                   'vectors': {str(n): (lambda c: [c.r, c.g, c.b, c.a])(mel.get_material_instance_vector_parameter_value(deck, n)) for n in mel.get_vector_parameter_names(deck)},
                   'textures': {str(n): (mel.get_material_instance_texture_parameter_value(deck, n).get_path_name().split('.')[0] if mel.get_material_instance_texture_parameter_value(deck, n) else None) for n in mel.get_texture_parameter_names(deck)}}, open(BF, 'w'), indent=1)
    b = json.load(open(BF)); print('VF2H deck before', b['parent'].split('/')[-1], {k: round(v, 2) for k, v in b['scalars'].items()}, {k: [round(x, 2) for x in v[:3]] for k, v in b['vectors'].items()}, {k: (v or '').split('/')[-1] for k, v in b['textures'].items()})
    vb = u.load_asset('/Game/GraceRanger/Environment/Exterior20260921/Materials/MI_EX_VerandaBoards_Weathered')
    print('VF2H veranda boards', vb.get_editor_property('parent').get_name(), {str(n): round(mel.get_material_instance_scalar_parameter_value(vb, n), 2) for n in mel.get_scalar_parameter_names(vb)})
    if C.get('deck', True):
        mel.clear_all_material_instance_parameters(deck); mel.set_material_instance_parent(deck, vb); setp(deck, {'UVScale': C['deck_uv']})
    builtins.VF2H_TOUCHED = [pm, hm, lime, hearth, masonry] + ([deck] if C.get('deck', True) else [])
    print('VF2H done', [(t.get_name(), mel.get_num_material_expressions(t) if isinstance(t, u.Material) else t.get_editor_property('parent').get_name()) for t in builtins.VF2H_TOUCHED])
