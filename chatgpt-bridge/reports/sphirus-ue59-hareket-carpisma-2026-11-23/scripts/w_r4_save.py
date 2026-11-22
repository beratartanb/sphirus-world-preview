# w_r4_save.py (write, gated): save the round-4 in-memory edits listed in Saved/UE59Work/save_list.txt, then the current map if dirty.
import unreal as u
for p in open(u.Paths.project_dir()+'Saved/UE59Work/save_list.txt',encoding='utf8').read().split():
    a=u.load_asset(p)
    try: print('SAVE',p.split('/')[-1],u.EditorAssetLibrary.save_loaded_asset(a,False))
    except Exception as e: print('SAVE_EXC',p.split('/')[-1],repr(e)[:90])
dm=[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()]
if dm:
    w=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world(); print('SAVE map',w.get_outermost().get_name(),u.EditorLoadingAndSavingUtils.save_packages([w.get_outermost()],False))
print('DIRTY',[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]+[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()])
