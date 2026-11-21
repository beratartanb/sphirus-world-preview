import unreal as u
d=[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]; m=[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()]
open(u.Paths.project_dir()+'Saved/UE59Work/r5/dirty.txt','w').write('\n'.join(d)+'\nMAPS '+' '.join(m)); print('DIRTYN',len(d),len(m))
