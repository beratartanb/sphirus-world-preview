"""apply_deck.py (in memory; saved by w_house2.py): balcony weather deck. Finding: the deck mesh has no usable UVs and its instance was a flat
mid-grey colour (0.42,0.40,0.34); in the sun, seen from the dim upper hall, it renders as a blank white sheet. Fix: a small world-aligned
board material (top-down planar mapping of the veranda board texture, darker weathered tint) so the surface carries planks and stays within
range. builtins.VF2DECK_REVERT restores the instance from Tools/VF2B_20261125/deck_base.json."""
import unreal as u, json, builtins
mel = u.MaterialEditingLibrary; E = u.EditorAssetLibrary; D = '/Game/Sphirus/House/VF2_20261125'
deck = u.load_asset('/Game/SphirusHouse/LivedIn_R05/Materials/Instances/MI_BR_ExteriorDeck'); b = json.load(open(u.Paths.project_dir() + 'Tools/VF2B_20261125/deck_base.json'))
mel.clear_all_material_instance_parameters(deck); touched = [deck]
if getattr(builtins, 'VF2DECK_REVERT', False):
    mel.set_material_instance_parent(deck, u.load_asset(b['parent']))
    for k, v in b['scalars'].items(): mel.set_material_instance_scalar_parameter_value(deck, k, v)
    for k, v in b['vectors'].items(): mel.set_material_instance_vector_parameter_value(deck, k, u.LinearColor(*v))
    for k, v in b['textures'].items(): mel.set_material_instance_texture_parameter_value(deck, k, u.load_asset(v) if v else None)
else:
    vb = u.load_asset('/Game/GraceRanger/Environment/Exterior20260921/Materials/MI_EX_VerandaBoards_Weathered'); tex = mel.get_material_instance_texture_parameter_value(vb, 'BaseColor'); assert tex, 'veranda board texture'
    MP = D + '/M_Sph_DeckBoards_VF2'
    if E.does_asset_exist(MP): m = u.load_asset(MP)
    else:
        m = u.AssetToolsHelpers.get_asset_tools().create_asset('M_Sph_DeckBoards_VF2', D, u.Material, u.MaterialFactoryNew())
        def ex(c, x, y): return mel.create_material_expression(m, c, x, y)
        wp = ex(u.MaterialExpressionWorldPosition, -1200, 0); xy = ex(u.MaterialExpressionComponentMask, -1000, 0); xy.set_editor_property('r', True); xy.set_editor_property('g', True); xy.set_editor_property('b', False); xy.set_editor_property('a', False); mel.connect_material_expressions(wp, '', xy, '')
        tl = ex(u.MaterialExpressionScalarParameter, -1000, 160); tl.set_editor_property('parameter_name', 'BoardTileCm'); tl.set_editor_property('default_value', 180.0)
        dv = ex(u.MaterialExpressionDivide, -820, 40); mel.connect_material_expressions(xy, '', dv, 'A'); mel.connect_material_expressions(tl, '', dv, 'B')
        ts = ex(u.MaterialExpressionTextureSampleParameter2D, -620, 0); ts.set_editor_property('parameter_name', 'Boards'); ts.set_editor_property('texture', tex); mel.connect_material_expressions(dv, '', ts, 'UVs')
        tn = ex(u.MaterialExpressionVectorParameter, -620, 260); tn.set_editor_property('parameter_name', 'Tint'); tn.set_editor_property('default_value', u.LinearColor(0.34, 0.33, 0.31, 1.0))
        ds = ex(u.MaterialExpressionDesaturation, -400, 0); mel.connect_material_expressions(ts, 'RGB', ds, ''); fr = ex(u.MaterialExpressionConstant, -620, 420); fr.set_editor_property('r', 0.45); mel.connect_material_expressions(fr, '', ds, 'Fraction')
        mu = ex(u.MaterialExpressionMultiply, -220, 60); mel.connect_material_expressions(ds, '', mu, 'A'); mel.connect_material_expressions(tn, '', mu, 'B'); mel.connect_material_property(mu, '', u.MaterialProperty.MP_BASE_COLOR)
        rg = ex(u.MaterialExpressionScalarParameter, -220, 300); rg.set_editor_property('parameter_name', 'Roughness'); rg.set_editor_property('default_value', 0.9); mel.connect_material_property(rg, '', u.MaterialProperty.MP_ROUGHNESS)
        mel.recompile_material(m)
    mel.set_material_instance_parent(deck, m); touched.append(m); print('DECK board texture', tex.get_name(), str(tex.get_editor_property('compression_settings')).split('.')[-1][:14], 'srgb', tex.get_editor_property('srgb'))
mel.update_material_instance(deck); builtins.VF2DECK_TOUCHED = touched; print('DECK parent', deck.get_editor_property('parent').get_name())
