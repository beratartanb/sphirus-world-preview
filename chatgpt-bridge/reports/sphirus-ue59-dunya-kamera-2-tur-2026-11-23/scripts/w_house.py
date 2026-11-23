# w_house.py (write, gated): facade material language + rear work garden + entry runner of the 2026-11-23 world pass, then save the house levels.
import unreal as u, builtins
builtins.R2G_FACADE={'ground':'lime','gables':'cladding'}
exec(open(u.Paths.project_dir()+'Tools/R2G2_20261123/apply_facade.py',encoding='utf8').read())
exec(open(u.Paths.project_dir()+'Tools/R2G2_20261123/apply_dress.py',encoding='utf8').read())
S=u.EditorLoadingAndSavingUtils
print('DIRTY_BEFORE',[p.get_name() for p in S.get_dirty_map_packages()],[p.get_name() for p in S.get_dirty_content_packages()])
print('SAVE_LEVELS',u.get_editor_subsystem(u.LevelEditorSubsystem).save_all_dirty_levels())
print('DIRTY_AFTER',[p.get_name() for p in S.get_dirty_map_packages()],[p.get_name() for p in S.get_dirty_content_packages()])
