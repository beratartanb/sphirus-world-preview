import unreal as u
exec(open(u.Paths.project_dir()+'Tools/UE59_20261120/c_daylinks.py',encoding='utf8').read())
w=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world(); print('SAVE',u.EditorLoadingAndSavingUtils.save_packages([w.get_outermost()],False))
print('DIRTY',[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]+[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()])
