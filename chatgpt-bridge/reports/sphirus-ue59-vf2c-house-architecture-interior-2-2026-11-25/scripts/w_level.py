# w_level.py (write, gated): workshop dressing + front-yard litter on a clean map, then save the dirty house level(s).
import unreal as u
S = u.EditorLoadingAndSavingUtils; assert not S.get_dirty_map_packages(), 'map already dirty'
exec(open(u.Paths.project_dir() + 'Tools/VF2C_20261125/apply_dress.py', encoding='utf8').read())
exec(open(u.Paths.project_dir() + 'Tools/VF2C_20261125/apply_world.py', encoding='utf8').read())
print('WL dirty before', [p.get_name() for p in S.get_dirty_map_packages()], [p.get_name() for p in S.get_dirty_content_packages()])
print('WL save levels', u.get_editor_subsystem(u.LevelEditorSubsystem).save_all_dirty_levels())
print('WL dirty after', [p.get_name() for p in S.get_dirty_map_packages()], [p.get_name() for p in S.get_dirty_content_packages()])
