"""Bridge export of the 5.9 working copy with exactly the 18 poses of the last published run (2026-11-12_014306, 5.8.4),
so the published views compare like with like. Bridge code unchanged except the 5.9 redraw-tool tolerance."""
import unreal as u, pathlib, json, time, importlib, chatgpt_bridge
importlib.reload(chatgpt_bridge)
P = pathlib.Path(u.Paths.project_dir()).resolve()
assert not u.EditorLoadingAndSavingUtils.get_dirty_map_packages() and not u.EditorLoadingAndSavingUtils.get_dirty_content_packages()
plan = json.loads((P / 'Saved/UE59Work/bridge/camera_plan_20261112.json').read_text())
shots = [{'name': s['name'], 'location': s['location'], 'rotation': s['rotation'], 'fov': s['fov'], 'camera_source': 'matched to published run 2026-11-12_014306: ' + s.get('camera_source', '')} for s in plan]
assert len(shots) == 18
result = chatgpt_bridge.export_current_world(); chatgpt_bridge._active.shots = shots
print('EXPORT18', result)
