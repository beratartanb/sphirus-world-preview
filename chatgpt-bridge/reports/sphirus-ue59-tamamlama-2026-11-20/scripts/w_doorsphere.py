# w_doorsphere.py (write, gated): store the door sphere instance overrides (c_doorsphere.py) in the house content sublevel.
import unreal as u
exec(open(u.Paths.project_dir()+'Tools/UE59_20261120/c_doorsphere.py',encoding='utf8').read())
p=u.load_package('/Game/GraceRanger/Maps/L_GR_CurrentHouseContent'); p.mark_package_dirty() if hasattr(p,'mark_package_dirty') else None
print('SAVE',u.EditorLoadingAndSavingUtils.save_packages([p],False))
print('DIRTY',[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]+[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()])
