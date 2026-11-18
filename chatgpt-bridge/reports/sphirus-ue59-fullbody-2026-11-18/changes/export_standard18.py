"""Existing Bridge mechanism with the 18 standard publication views, built from this pass's matched camera plan
(same poses as Saved/Codex/WoodlandFinal20260923/camera_plan.json). Bridge code itself is unchanged."""
import unreal as u, pathlib, json, math, time, chatgpt_bridge, importlib; importlib.reload(chatgpt_bridge)
P = pathlib.Path(u.Paths.project_dir()).resolve(); D = P / 'Saved/Codex/WoodlandFinal20260923'; O = P / 'Saved/Codex/FrontRefugeE2_20260925'
assert not u.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not u.EditorLoadingAndSavingUtils.get_dirty_content_packages()
by = {s['name'][3:].split('.')[0]: s for s in json.loads((D / 'camera_plan.json').read_text())}
names = [('00_current_view', 'house_exterior'), ('01_world_overview', 'oblique'), ('02_environment_angle_a', 'edge_west'), ('03_environment_angle_b', 'pond_path'),
         ('04_environment_angle_c', 'uphill_lookback'), ('05_top_overview', 'top'), ('06_house_exterior', 'house_exterior'), ('07_house_to_environment', 'house_to_pond'),
         ('08_water_to_house', 'pond_to_house'), ('09_house_to_forest', 'house_to_forest'), ('10_forest_to_house', 'house_rear'), ('11_forest_edge', 'edge_east'),
         ('12_house_to_pond_slope', 'house_slope'), ('13_pond_side_path', 'pond_path'), ('14_uphill_path', 'rear_trail'), ('15_uphill_forest_lookback', 'top_lookback'),
         ('16_small_front_footpath', 'front_path'), ('17_shoreline_gameplay', 'pond_shore')]
shots = [{'name': n + '.png', 'location': by[k]['location'], 'rotation': by[k]['rotation'], 'fov': by[k]['fov'],
          'camera_source': 'WoodlandFinal matched plan ' + k + ('; diagnostic only' if k in ('top', 'oblique') else '; eye height 170 cm')} for n, k in names]
assert len({s['name'] for s in shots}) == 18
settings = u.get_default_object(u.load_class(None, '/Script/UnrealEd.EditorLoadingSavingSettings')); prior = settings.get_editor_property('bAutoSaveEnable'); settings.set_editor_property('bAutoSaveEnable', False)
try:
    result = chatgpt_bridge.export_current_world(); assert chatgpt_bridge._active is not None; chatgpt_bridge._active.shots = shots
except Exception:
    settings.set_editor_property('bAutoSaveEnable', prior); raise
(O / 'latest_export.json').write_text(json.dumps({'path': result, 'start_epoch': time.time(), 'shots': shots, 'standard_view_count': 18}, indent=1))
import builtins
def finish(dt):
    if chatgpt_bridge._active is None:
        settings.set_editor_property('bAutoSaveEnable', prior); u.unregister_slate_post_tick_callback(builtins.AP_EXP)
builtins.AP_EXP = u.register_slate_post_tick_callback(finish)
print(result)
