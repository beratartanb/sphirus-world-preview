"""probe_assets.py (measure job, read-only): editor world/dirty state + bounds/collision/material of candidate structural meshes for XR2."""
import unreal as u, json, pathlib
P = pathlib.Path(u.Paths.project_dir()) / 'Saved/Codex/ExteriorWorld_XR2_20261031/recon'
E = u.get_editor_subsystem(u.UnrealEditorSubsystem)
S = u.EditorLoadingAndSavingUtils
out = {'world': E.get_editor_world().get_path_name(), 'pie': E.get_game_world() is not None,
       'dirty': sorted([p.get_name() for p in S.get_dirty_content_packages()] + [p.get_name() for p in S.get_dirty_map_packages()]),
       'levels': [l.get_outer().get_name() for l in E.get_editor_world().get_editor_property('levels')] if hasattr(E.get_editor_world(), 'levels') else 'n/a'}
names = [p for p in u.EditorAssetLibrary.list_assets("/Game/PineForestPack/Meshes", True, False) if any(k in p for k in ("Cliff", "FallenTree", "DeadTrunk", "Embankment", "RockyGround", "GroundRock", "FallenBranches", "PineStone"))]; names = [p.split(".")[0] for p in names]
reg = u.AssetRegistryHelpers.get_asset_registry()
extra = []
extra += ['/Game/Fishermans_Cabin/Meshes/Wooden_Dock/SM_Wooden_Dock_0%d' % i for i in (1, 2, 3)] + ['/Game/Fishermans_Cabin/Meshes/Boat/SM_Boat_%02d' % i for i in range(1, 13)] + ['/Game/Fishermans_Cabin/Meshes/Wood_Cutting_Set/SM_Wood_Cutting_Set_%02d' % i for i in range(1, 13)]
for d in ('/Game/OakForestEnv/Meshes', '/Game/Calysto/World', '/Game/Environment_Set/Environment'):
    for ad in reg.get_assets_by_path(d, True):
        n = str(ad.asset_name)
        if ad.asset_class_path.asset_name == 'StaticMesh' and any(k in n.lower() for k in ('boulder', 'embank', 'cliff', 'fallen', 'big_rock', 'middle_rock', 'trunk', 'dead_tree', 'log')):
            extra.append(str(ad.package_name))
M = {}
for n in names + extra:
    m = u.load_asset(n)
    if not m:
        M[n] = None; continue
    b = m.get_bounds(); bs = m.get_editor_property('body_setup')
    try:
        ct = str(bs.get_editor_property('collision_trace_flag')).split('.')[-1] if bs else None
        agg = bs.get_editor_property('agg_geom') if bs else None
        nconv = len(agg.get_editor_property('convex_elems')) if agg else -1
        nbox = len(agg.get_editor_property('box_elems')) if agg else -1
    except Exception as ex:
        ct, nconv, nbox = repr(ex), -1, -1
    mats = []
    try:
        mats = [s.get_editor_property('material_interface').get_path_name().split('.')[-1] for s in m.get_editor_property('static_materials')]
    except Exception:
        pass
    M[n] = {'ext': [round(b.box_extent.x), round(b.box_extent.y), round(b.box_extent.z)], 'org': [round(b.origin.x), round(b.origin.y), round(b.origin.z)],
            'trace': ct, 'convex': nconv, 'box': nbox, 'nanite': bool(m.get_editor_property('nanite_settings').get_editor_property('enabled')), 'mats': mats[:3]}
out['meshes'] = M
(P / 'probe_assets.json').write_text(json.dumps(out, indent=1))
print('PROBE', json.dumps(out)[:3000])
