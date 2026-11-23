# w_light.py (write, gated): lighting change set of the 2026-11-23 world pass (see apply_light.py), then save both house levels.
import unreal as u
exec(open(u.Paths.project_dir()+'Tools/R2G2_20261123/apply_light.py',encoding='utf8').read())
S=u.EditorLoadingAndSavingUtils
print('DIRTY_BEFORE',[p.get_name() for p in S.get_dirty_map_packages()],[p.get_name() for p in S.get_dirty_content_packages()])
print('SAVE_LEVELS',u.get_editor_subsystem(u.LevelEditorSubsystem).save_all_dirty_levels())
print('DIRTY_AFTER',[p.get_name() for p in S.get_dirty_map_packages()],[p.get_name() for p in S.get_dirty_content_packages()])
