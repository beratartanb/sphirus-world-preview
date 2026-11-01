"""probe_library.py (measure job, read-only): bounds / collision / nanite / triangles / materials of every candidate mesh under the
listed directories + parameter dumps of key material instances (landscape MI, cliff rock, ferns, fir leaves). -> recon/library.json"""
import unreal as u, json, pathlib
P = pathlib.Path(u.Paths.project_dir()) / 'Saved/Codex/ExteriorIdentity_XR3_20261031/recon'
DIRS = ['/Game/Calysto/World/Vegetation/Meshes', '/Game/PineForestPack/Meshes', '/Game/Fishermans_Cabin/Meshes/Foliage', '/Game/OakForestEnv/Meshes',
        '/Game/Environment_Set/Environment', '/Game/ForestFloor', '/Game/Modular_Rural_Cabin/Meshes', '/Game/Fishermans_Cabin/Meshes/Lamps',
        '/Game/Fishermans_Cabin/Meshes/Sign_Set', '/Game/Fishermans_Cabin/Meshes/Ropes', '/Game/Fishermans_Cabin/Meshes/Trap', '/Game/Fishermans_Cabin/Meshes/Wheelbarrow',
        '/Game/Fishermans_Cabin/Meshes/Sticks', '/Game/Fishermans_Cabin/Meshes/Outhouse', '/Game/Fishermans_Cabin/Meshes/Toolshed', '/Game/Fishermans_Cabin/Meshes/Wood_Box_Low',
        '/Game/Fishermans_Cabin/Meshes/Wooden_Crates', '/Game/Fishermans_Cabin/Meshes/Fishing_Gear_01', '/Game/Fishermans_Cabin/Meshes/Gardening_Set', '/Game/Fishermans_Cabin/Meshes/Rocks',
        '/Game/Fishermans_Cabin/Meshes/Landscape', '/Game/Fishermans_Cabin/Meshes/Mountains', '/Game/GrassPackVol1', '/Game/SmartTerrain']
out = {'meshes': {}, 'mats': {}}
for d in DIRS:
    for p in u.EditorAssetLibrary.list_assets(d, True, False):
        pk = p.split('.')[0]; n = pk.split('/')[-1]
        if not n.startswith('SM_') or 'Blueprint' in n or 'FoliageType' in n or 'LOD' in n:
            continue
        m = u.load_asset(pk)
        if not isinstance(m, u.StaticMesh):
            continue
        b = m.get_bounds()
        try:
            nan = bool(m.get_editor_property('nanite_settings').get_editor_property('enabled'))
        except Exception:
            nan = None
        try:
            tris = m.get_num_triangles(0); lods = m.get_num_lods()
        except Exception:
            tris, lods = -1, -1
        mats = []
        for s in m.get_editor_property('static_materials'):
            mi = s.get_editor_property('material_interface'); mats.append(mi.get_path_name().split('.')[0] if mi else None)
        out['meshes'][pk] = {'ext': [round(b.box_extent.x), round(b.box_extent.y), round(b.box_extent.z)], 'org': [round(b.origin.x), round(b.origin.y), round(b.origin.z)],
                             'nanite': nan, 'tris': tris, 'lods': lods, 'mats': mats, 'col': str(m.get_editor_property('body_setup').get_editor_property('collision_trace_flag')).split('.')[-1][:8] if m.get_editor_property('body_setup') else None}
MATS = ['/Game/GraceRanger/Environment/Exterior20260921/Materials/MI_EX_Integration_Valley', '/Game/GraceRanger/Environment/Exterior20260921/Materials/MI_EX_HouseValley',
        '/Game/GraceRanger/Environment/Exterior20260921/Materials/MI_EX_RefugeFirLeaves', '/Game/GraceRanger/Environment/Exterior20260921/Materials/MI_PR_FernLong01',
        '/Game/GraceRanger/Environment/Exterior20260921/Materials/MI_PR_PineTree01_FO', '/Game/GraceRanger/Environment/Exterior20260921/Materials/MI_EX_Pond',
        '/Game/GraceRanger/Environment/Exterior20260921/Materials/MI_EX_RefugeGroundRock03', '/Game/GraceRanger/Environment/Exterior20260921/Materials/MI_EX_CladdingAged']
reg = u.AssetRegistryHelpers.get_asset_registry()
for ad in reg.get_assets_by_path('/Game/PineForestPack/Materials', True):
    if str(ad.asset_name) in ('MI_CliffRock01', 'MI_PineCliff02', 'MI_PineCliff03', 'MI_ForestEmbankment01', 'MI_PineGroundRock01', 'MI_FallenTree01', 'MI_PineDeadTrunk01', 'MI_LandscapePineForest'):
        MATS.append(str(ad.package_name))
for ad in reg.get_assets_by_path('/Game/Calysto', True):
    if str(ad.asset_name) in ('MI_Black_Spruce', 'MI_Black_Spruce_Leaves', 'MI_Rock', 'MI_Speckled_Alder', 'MI_Trunk_01', 'MI_Landscape', 'MI_Calysto_Landscape'):
        MATS.append(str(ad.package_name))
for mp in MATS:
    mi = u.load_asset(mp)
    if not mi:
        out['mats'][mp] = None; continue
    r = {'class': mi.get_class().get_name()}
    try:
        r['parent'] = mi.get_editor_property('parent').get_path_name().split('.')[0]
        r['scalar'] = {str(p.parameter_info.name): round(p.parameter_value, 4) for p in mi.get_editor_property('scalar_parameter_values')}
        r['vector'] = {str(p.parameter_info.name): [round(p.parameter_value.r, 3), round(p.parameter_value.g, 3), round(p.parameter_value.b, 3), round(p.parameter_value.a, 3)] for p in mi.get_editor_property('vector_parameter_values')}
        r['texture'] = {str(p.parameter_info.name): (p.parameter_value.get_path_name().split('.')[0] if p.parameter_value else None) for p in mi.get_editor_property('texture_parameter_values')}
    except Exception as ex:
        r['err'] = repr(ex)
    out['mats'][mp] = r
(P / 'library.json').write_text(json.dumps(out, indent=1))
print('LIBRARY meshes', len(out['meshes']), 'mats', len(out['mats']))
