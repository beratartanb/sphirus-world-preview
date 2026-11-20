# w_fireplace.py (write, gated): final hearth flame placement + fire light inside the firebox; saves the persistent house map.
import unreal as u, builtins
builtins.FIRE_POS={'GR_Day_FireFX':(1457,905,220,1.0),'GR_Day_FireFX2':(1458,880,216,1.0),'GR_Day_FireFX3':(1456,893,218,1.0),'GR_Day_FireFX4':(1456,917,218,1.0),'GR_Day_FireFX5':(1458,930,216,1.0)}
builtins.FIRE_LI={'GR_Day_FireLight':{'loc':(1395.0,905.0,215.0)}}  # light stays in front of the hearth (inside the firebox it blew the stone out to white)
exec(open(u.Paths.project_dir()+'Tools/UE59_20261120/c_fireplace.py',encoding='utf8').read())
w=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world(); p=w.get_outermost(); print('PKG',p.get_name())
print('SAVE',u.EditorLoadingAndSavingUtils.save_packages([p],False))
print('DIRTY',[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]+[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()])
