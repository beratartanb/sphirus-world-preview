# w_save_list.py (write, gated): save the packages listed in Saved/UE59Work/save_list.txt (edited in memory by MCP / control jobs)
import unreal as u
for p in open(u.Paths.project_dir()+'Saved/UE59Work/save_list.txt',encoding='utf8').read().split():
    a=u.load_asset(p)
    try: print('SAVE',p.split('/')[-1],u.EditorAssetLibrary.save_loaded_asset(a,False))
    except Exception as e: print('SAVE_EXC',p.split('/')[-1],repr(e)[:90])
print('DIRTY',[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()])
