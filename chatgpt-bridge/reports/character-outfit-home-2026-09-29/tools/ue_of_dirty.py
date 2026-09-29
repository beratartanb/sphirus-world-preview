import unreal as u, json
d = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
m = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()]
print(json.dumps({'dirty_content': d, 'dirty_maps': m, 'world': u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world().get_path_name()}))
