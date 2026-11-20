import unreal as u
exec(open(u.Paths.project_dir()+'Tools/UE59_20261120/c_wakecam.py',encoding='utf8').read())
print('SAVE hub',u.EditorAssetLibrary.save_loaded_asset(u.load_asset('/Game/GraceRanger/SF/Day/BP_GR_DayHub'),False))
w=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world(); print('SAVE map',u.EditorLoadingAndSavingUtils.save_packages([w.get_outermost()],False))
print('DIRTY',[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]+[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()])
