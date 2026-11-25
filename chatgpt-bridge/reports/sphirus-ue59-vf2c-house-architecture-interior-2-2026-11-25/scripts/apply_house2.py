"""apply_house2.py (in memory; saved by w_house2.py): VF2C house surface layer v3.
Why v3: the v2 layer used three procedural Noise nodes and a 3-sample world-aligned normal (415 / 344 pixel instructions) and only reached the
interior partition walls. v3 uses ONE tiling noise texture and ONE planar stucco normal sample, and is also spliced into the two materials
that paint the envelope walls (their interior face is the living room / workshop / kitchen main wall).
Materials (each a DUPLICATE of its project source, one extra stage in front of base colour / roughness / normal):
  M_Sph_HL_Plaster_V3   <- M_HouseSurface                      -> MI_R3_Surface_lime
  M_Sph_HL_Hearth_V3    <- M_HouseSurface                      -> MI_R3_hearth_OriginalAtlas, MI_R3_Surface_masonry
  M_Sph_HL_LimeOak_V3   <- M_EX_Integration_ExposureLimeOak    -> MI_EX_Integration_OuterLimeOak
  M_Sph_HL_OuterLime_V3 <- M_EX_Integration_ExposureLime       -> MI_EX_Integration_OuterLime
builtins.VF2H2 = overrides. builtins.VF2H2_REVERT=True re-parents every instance to the parent recorded in house2_base.json."""
import unreal as u, builtins, json, os
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
E = u.EditorAssetLibrary; mel = u.MaterialEditingLibrary
C = dict(suffix=''); C.update(getattr(builtins, 'VF2H2', None) or {})
D = '/Game/Sphirus/House/VF2_20261125'; I = '/Game/SphirusHouse/LivedIn_R05/Materials/Instances/'; X_ = '/Game/GraceRanger/Environment/Exterior20260921/Materials/'
HS = '/Game/SphirusHouse/LivedIn_R05/Materials/M_HouseSurface'
PLAN = [  # material name, source, kind, [(instance, scalar params)]
    ('M_Sph_HL_Plaster_V3', HS, 'plaster', [(I + 'MI_R3_Surface_lime', dict(MacroAmount=0.5, GrimeAmount=0.6, GrimeHeight=40.0, ReliefStrength=0.5))]),
    ('M_Sph_HL_Hearth_V3', HS, 'hearth', [(I + 'MI_R3_hearth_OriginalAtlas', dict(SootAmount=1.25, AshAmount=0.8)), (I + 'MI_R3_Surface_masonry', dict(SootAmount=1.25, AshAmount=0.8))]),
    ('M_Sph_HL_LimeOak_V3', X_ + 'M_EX_Integration_ExposureLimeOak', 'plaster', [(X_ + 'MI_EX_Integration_OuterLimeOak', dict(MacroAmount=0.42, GrimeAmount=0.5, GrimeHeight=36.0, ReliefStrength=0.32))]),
    ('M_Sph_HL_OuterLime_V3', X_ + 'M_EX_Integration_ExposureLime', 'plaster', [(X_ + 'MI_EX_Integration_OuterLime', dict(MacroAmount=0.42, GrimeAmount=0.0, GrimeHeight=36.0, ReliefStrength=0.32))])]
BF = u.Paths.project_dir() + 'Tools/VF2C_20261125/house2_base.json'
ALL = [mi for _, _, _, L_ in PLAN for mi, _ in L_]
if not os.path.exists(BF): json.dump({p: u.load_asset(p).get_editor_property('parent').get_path_name().split('.')[0] for p in ALL}, open(BF, 'w'), indent=1)
base = json.load(open(BF))
if getattr(builtins, 'VF2H2_REVERT', False):
    out = []
    for p in ALL: m = u.load_asset(p); mel.set_material_instance_parent(m, u.load_asset(base[p])); mel.update_material_instance(m); out.append(m)
    builtins.VF2H2_TOUCHED = out; print('VF2H2 reverted', {p.split('/')[-1]: base[p].split('/')[-1] for p in ALL})
else:
    MUL, ADD, SUB, DIV, MAX = u.MaterialExpressionMultiply, u.MaterialExpressionAdd, u.MaterialExpressionSubtract, u.MaterialExpressionDivide, u.MaterialExpressionMax
    SAT = u.MaterialExpressionSaturate; BC, RG, NM = u.MaterialProperty.MP_BASE_COLOR, u.MaterialProperty.MP_ROUGHNESS, u.MaterialProperty.MP_NORMAL; X = 1400
    NOISE = u.load_asset('/Engine/EngineMaterials/Good64x64TilingNoiseHighFreq'); assert NOISE, 'engine noise texture'
    class G:
        def __init__(s, mat): s.m = mat
        def ex(s, cls, x, y): return mel.create_material_expression(s.m, cls, x, y)
        def sc(s, n, v, x, y):
            e = s.ex(u.MaterialExpressionScalarParameter, x, y); e.set_editor_property('parameter_name', n); e.set_editor_property('default_value', v); e.set_editor_property('group', 'VF2'); return e
        def vc(s, n, c, x, y):
            e = s.ex(u.MaterialExpressionVectorParameter, x, y); e.set_editor_property('parameter_name', n); e.set_editor_property('default_value', u.LinearColor(*c)); e.set_editor_property('group', 'VF2'); return e
        def cn(s, v, x, y):
            e = s.ex(u.MaterialExpressionConstant, x, y); e.set_editor_property('r', v); return e
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
        def src(s, prop):
            e = mel.get_material_property_input_node(s.m, prop); return e, (mel.get_material_property_input_node_output_name(s.m, prop) if e else '')
        def length(s, d, x, y):
            dd = s.ex(u.MaterialExpressionDotProduct, x, y); assert mel.connect_material_expressions(d, '', dd, 'A'); assert mel.connect_material_expressions(d, '', dd, 'B'); return s.one(u.MaterialExpressionSquareRoot, dd, x + 120, y)
        def planar(s, x, y):
            # wall-plane coordinates in cm: u = world x + y (walls are axis aligned), v = world z. One set of UVs for every sample of the layer.
            s.wp = s.ex(u.MaterialExpressionWorldPosition, x, y); uu = s.op(ADD, s.mask(s.wp, 'r', x + 200, y - 60), s.mask(s.wp, 'g', x + 200, y + 60), x + 380, y)
            s.wz = s.mask(s.wp, 'b', x + 200, y + 180); s.uv = s.op(u.MaterialExpressionAppendVector, uu, s.wz, x + 520, y + 60); return s.uv
        def tex(s, t, tile_cm, x, y, sampler):
            uvs = s.op(MUL, s.uv, s.cn(1.0 / tile_cm, x - 200, y + 90), x - 80, y); e = s.ex(u.MaterialExpressionTextureSample, x + 80, y); e.set_editor_property('texture', t); e.set_editor_property('sampler_type', sampler)
            assert mel.connect_material_expressions(uvs, '', e, 'UVs'); return e
    def build_plaster(m):
        g = G(m); b0, b0o = g.src(BC); r0, r0o = g.src(RG); n0, n0o = g.src(NM); assert b0 and r0, 'unexpected source graph'
        g.planar(X, 0); LIN = u.MaterialSamplerType.SAMPLERTYPE_LINEAR_GRAYSCALE
        nmac = g.tex(NOISE, 5200.0, X + 900, -200, LIN); nfine = g.tex(NOISE, 260.0, X + 900, 150, LIN)
        mac = g.op(ADD, g.cn(1.0, X + 1300, -300), g.op(MUL, g.op(SUB, nmac, g.cn(0.56, X + 1200, -120), X + 1320, -200, ao='R'), g.sc('MacroAmount', 0.4, X + 1200, -20), X + 1440, -160), X + 1560, -240)
        gh = g.sc('GrimeHeight', 38.0, X + 900, 700)
        def band(nm, fz, y):
            d = g.op(SUB, g.wz, g.sc(nm, fz, X + 900, y + 90), X + 1050, y); up = g.one(SAT, g.op(SUB, g.cn(1.0, X + 1160, y - 70), g.op(DIV, d, gh, X + 1180, y), X + 1300, y), X + 1420, y)
            ab = g.one(SAT, g.op(DIV, g.op(ADD, d, g.cn(5.0, X + 1160, y + 150), X + 1280, y + 130), g.cn(5.0, X + 1360, y + 200), X + 1420, y + 130), X + 1540, y + 130); return g.op(MUL, up, ab, X + 1660, y)
        gb = g.op(MAX, band('FloorZ1', 150.0, 520), band('FloorZ2', 490.0, 860), X + 1820, 680)
        gm = g.one(SAT, g.op(MUL, g.op(MUL, gb, gb, X + 1940, 680), g.op(ADD, nfine, g.cn(0.4, X + 1900, 820), X + 2020, 790, ao='R'), X + 2120, 700), X + 2240, 700)
        gt = g.op(MUL, gm, g.sc('GrimeAmount', 0.5, X + 2200, 860), X + 2360, 720)
        c1 = g.op(MUL, b0, mac, X + 2500, -200, ao=b0o); c2 = g.lerp(c1, g.op(MUL, c1, g.vc('GrimeColor', (0.60, 0.52, 0.42, 1), X + 2500, 60), X + 2660, -60), gt, X + 2820, -160)
        assert mel.connect_material_property(c2, '', BC)
        rv = g.one(SAT, g.op(ADD, g.op(ADD, r0, g.op(MUL, g.op(SUB, nmac, g.cn(0.5, X + 2500, 420), X + 2620, 380, ao='R'), g.cn(0.14, X + 2620, 470), X + 2740, 400), X + 2860, 340, ao=r0o), g.op(MUL, gt, g.cn(0.08, X + 2740, 560), X + 2860, 520), X + 2980, 400), X + 3100, 400)
        assert mel.connect_material_property(rv, '', RG)
        psz = g.sc('PlasterSize', 150.0, X + 600, 1350); uvn = g.op(DIV, g.uv, psz, X + 760, 1300); tn = g.ex(u.MaterialExpressionTextureSampleParameter2D, X + 920, 1300); tn.set_editor_property('parameter_name', 'PlasterNormal'); tn.set_editor_property('group', 'VF2')
        tn.set_editor_property('texture', u.load_asset('/Game/InfinityAssets/Texture/Materials/Wall/T_Stucco_Facade_N')); tn.set_editor_property('sampler_type', u.MaterialSamplerType.SAMPLERTYPE_NORMAL); assert mel.connect_material_expressions(uvn, '', tn, 'UVs')
        fl = g.ex(u.MaterialExpressionMaterialFunctionCall, X + 1300, 1300); fl.set_material_function(u.load_asset('/Engine/Functions/Engine_MaterialFunctions01/Texturing/FlattenNormal'))
        assert mel.connect_material_expressions(tn, 'RGB', fl, 'Normal'); assert mel.connect_material_expressions(g.op(SUB, g.cn(1.0, X + 1000, 1560), g.sc('ReliefStrength', 0.5, X + 1000, 1640), X + 1160, 1580), '', fl, 'Flatness')
        if n0:
            bl = g.ex(u.MaterialExpressionMaterialFunctionCall, X + 1600, 1200); bl.set_material_function(u.load_asset('/Engine/Functions/Engine_MaterialFunctions02/Utility/BlendAngleCorrectedNormals'))
            assert mel.connect_material_expressions(n0, n0o, bl, 'BaseNormal'); assert mel.connect_material_expressions(fl, '', bl, 'AdditionalNormal'); assert mel.connect_material_property(bl, '', NM)
        else: assert mel.connect_material_property(fl, '', NM)
    def build_hearth(m):
        g = G(m); b0, b0o = g.src(BC); r0, r0o = g.src(RG); assert b0 and r0
        g.planar(X, 0); wp = g.wp; nf = g.tex(NOISE, 110.0, X + 900, 0, u.MaterialSamplerType.SAMPLERTYPE_LINEAR_GRAYSCALE)
        def ell(nm, c, r, y, power):
            d = g.op(DIV, g.op(SUB, wp, g.vc(nm + 'Center', c + (0,), X, y + 150), X + 250, y), g.vc(nm + 'Radius', r + (0,), X + 250, y + 150), X + 420, y)
            mm = g.one(SAT, g.op(SUB, g.cn(1.0, X + 760, y - 70), g.length(g.mask(d, 'rgb', X + 500, y), X + 600, y), X + 880, y), X + 1000, y); pw = g.ex(u.MaterialExpressionPower, X + 1120, y)
            assert mel.connect_material_expressions(mm, '', pw, 'Base'); assert mel.connect_material_expressions(g.cn(power, X + 1000, y + 100), '', pw, 'Exp'); return pw
        front = ell('SootFront', (1392.0, 905.0, 252.0), (58.0, 92.0, 78.0), 500, 1.3); inside = ell('SootInside', (1452.0, 905.0, 196.0), (70.0, 56.0, 64.0), 900, 0.6)
        brk = g.op(ADD, g.op(MUL, nf, g.cn(0.9, X + 1200, 300), X + 1320, 260, ao='R'), g.cn(0.5, X + 1320, 360), X + 1440, 300)
        st = g.op(MUL, g.one(SAT, g.op(MUL, g.op(MAX, front, inside, X + 1300, 700), brk, X + 1560, 600), X + 1680, 600), g.sc('SootAmount', 1.25, X + 1680, 760), X + 1800, 640)
        vn = g.mask(g.ex(u.MaterialExpressionVertexNormalWS, X, 1400), 'b', X + 200, 1400); upf = g.one(SAT, g.op(MUL, g.op(SUB, vn, g.cn(0.6, X + 300, 1500), X + 420, 1420), g.cn(4.0, X + 420, 1520), X + 540, 1440), X + 660, 1440)
        ashm = g.op(MUL, g.op(MUL, ell('Ash', (1418.0, 905.0, 170.0), (40.0, 50.0, 30.0), 1700, 0.8), upf, X + 1300, 1500), g.one(SAT, g.op(ADD, nf, g.cn(0.25, X + 1200, 1640), X + 1320, 1620, ao='R'), X + 1440, 1620), X + 1560, 1520)
        at = g.op(MUL, ashm, g.sc('AshAmount', 0.8, X + 1560, 1700), X + 1700, 1540)
        c1 = g.lerp(b0, g.vc('SootColor', (0.035, 0.031, 0.028, 1), X + 1800, -60), st, X + 2000, -200, ao=b0o); c2 = g.lerp(c1, g.vc('AshColor', (0.33, 0.32, 0.31, 1), X + 2000, 60), at, X + 2200, -160)
        assert mel.connect_material_property(c2, '', BC)
        rv = g.lerp(r0, g.cn(0.93, X + 2000, 420), g.one(SAT, g.op(ADD, st, at, X + 1900, 520), X + 2020, 520), X + 2200, 400, ao=r0o); assert mel.connect_material_property(rv, '', RG)
    def stat(m):
        try: s = mel.get_statistics(m); return (s.num_pixel_shader_instructions, s.num_samplers)
        except Exception as e: return repr(e)[:40]
    touched = []
    for name, srcp, kind, insts in PLAN:
        p = D + '/' + name + C['suffix']; s0 = stat(u.load_asset(srcp))
        if E.does_asset_exist(p): m = u.load_asset(p); built = False
        else:
            m = u.AssetToolsHelpers.get_asset_tools().duplicate_asset(name + C['suffix'], D, u.load_asset(srcp)); assert m, name
            (build_plaster if kind == 'plaster' else build_hearth)(m); mel.recompile_material(m); built = True
        touched.append(m); print('VF2H2', name, 'built' if built else 'exists', '| pixel instructions/samplers source', s0, '-> layered', stat(m))
        for mp, sc in insts:
            mi = u.load_asset(mp); mel.set_material_instance_parent(mi, m)
            for k, v in sc.items(): mel.set_material_instance_scalar_parameter_value(mi, k, float(v))
            mel.update_material_instance(mi); touched.append(mi)
    for old in ('M_Sph_LimePlaster_VF2', 'M_Sph_HearthStone_VF2'):
        if E.does_asset_exist(D + '/' + old): print('VF2H2 v2 for comparison', old, stat(u.load_asset(D + '/' + old)))
    builtins.VF2H2_TOUCHED = touched; print('VF2H2 done', [t.get_name() for t in touched])
