"""export_bridge_pfr.py (editor job, map saved, no dirty packages): the existing ChatGPTBridge export with the 18 standard publication
views taken from THIS pass's real player-camera poses (cap/views_<tag>/views_log.json, the same poses as the before/after stills)
plus the pass's top / oblique diagnostic cameras. Bridge code itself is unchanged (pattern of Tools/FrontRefugeE2_20260925/export_standard.py).
builtins.PFR_VIEWS_TAG selects the views folder (default 'final'). Output: Saved/Codex/PineForestRedesign_20261104/latest_export.json"""
import unreal as u, pathlib, json, time, builtins, chatgpt_bridge
P = pathlib.Path(u.Paths.project_dir()).resolve(); O = P / 'Saved/Codex/PineForestRedesign_20261104'; TAG = getattr(builtins, 'PFR_VIEWS_TAG', 'final')
S_ = u.EditorLoadingAndSavingUtils; dm_ = [p.get_name() for p in S_.get_dirty_map_packages()]; dc_ = [p.get_name() for p in S_.get_dirty_content_packages()]
assert not dc_, 'dirty content packages: %s' % dc_[:4]
assert not dm_ or getattr(builtins, 'PFR_ALLOW_DIRTY_MAP', False), 'dirty map packages: %s' % dm_   # only a load-time flag may be waived, and it is recorded
(O / 'bridge_export_dirty.json').write_text(json.dumps({'dirty_maps': dm_, 'dirty_content': dc_, 'allowed': bool(getattr(builtins, 'PFR_ALLOW_DIRTY_MAP', False))}))
log = json.loads((O / 'cap' / ('views_%s' % TAG) / 'views_log.json').read_text()); by = {v['name']: v for v in log['views'] if v.get('cam')}
TOP = {'top': ([0, 1000, 21000], [-90.0, 90.0, 0.0], 60.0), 'oblique_SE': ([9500, -8500, 7500], [-30.0, 130.0, 0.0], 60.0)}   # topview_pfr.py poses
names = [('00_current_view', 'P0_refuge_front_path'), ('01_world_overview', 'oblique_SE'), ('02_environment_angle_a', 'P2_rockshelf_fwd'),
         ('03_environment_angle_b', 'P3_glade_fwd'), ('04_environment_angle_c', 'D11_saddle_fwd'), ('05_top_overview', 'top'),
         ('06_house_exterior', 'P0_refuge_house_back'), ('07_house_to_environment', 'P1_landing_from_veranda'), ('08_water_to_house', 'P1_landing_back'),
         ('09_house_to_forest', 'P0_refuge_fwd'), ('10_forest_to_house', 'P2_rockshelf_back'), ('11_forest_edge', 'D08_narrows_fwd'),
         ('12_house_to_pond_slope', 'D02_houseSE_fwd'), ('13_pond_side_path', 'P1_landing_fwd'), ('14_uphill_path', 'D10_climb_fwd'),
         ('15_uphill_forest_lookback', 'D10_climb_back'), ('16_small_front_footpath', 'D13_backyard_fwd'), ('17_shoreline_gameplay', 'P1_landing_boat')]
shots = []
for n, k in names:
    if k in TOP:
        loc, rot, fov = TOP[k]; src = 'PFR top-view diagnostic camera ' + k
    else:
        v = by[k]; loc = [float(x) for x in v['cam']]; rot = [float(v['cam_rot'][0]), float(v['cam_rot'][1]), 0.0]; fov = float(v['fov'])
        src = 'PFR station %s: real GraceRanger player camera pose (PIE, boom + collision as in game), views_%s' % (k, TAG)
    shots.append({'name': n + '.png', 'location': loc, 'rotation': rot, 'fov': fov, 'camera_source': src})
assert len({s['name'] for s in shots}) == 18
settings = u.get_default_object(u.load_class(None, '/Script/UnrealEd.EditorLoadingSavingSettings')); prior = settings.get_editor_property('bAutoSaveEnable'); settings.set_editor_property('bAutoSaveEnable', False)
try:
    result = chatgpt_bridge.export_current_world(); assert chatgpt_bridge._active is not None; chatgpt_bridge._active.shots = shots
except Exception:
    settings.set_editor_property('bAutoSaveEnable', prior); raise
(O / 'latest_export.json').write_text(json.dumps({'path': result, 'start_epoch': time.time(), 'shots': shots, 'standard_view_count': 18, 'views_tag': TAG}, indent=1))


def finish(dt):
    if chatgpt_bridge._active is None:
        settings.set_editor_property('bAutoSaveEnable', prior); u.unregister_slate_post_tick_callback(builtins.PFR_EXP)
        (O / 'latest_export_done.json').write_text(json.dumps({'path': result, 'finished': time.strftime('%Y-%m-%d %H:%M:%S')}))


builtins.PFR_EXP = u.register_slate_post_tick_callback(finish)
print('PFR_BRIDGE_EXPORT', result)
