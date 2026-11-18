import unreal as u
d = [p.get_name() for p in (u.EditorLoadingAndSavingUtils.get_dirty_content_packages() + u.EditorLoadingAndSavingUtils.get_dirty_map_packages())]
print('DIRTY', d)
