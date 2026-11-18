import unreal as u, time
W=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world()
D=dict({'r.Shadow.Virtual.Enable':1,'r.Lumen.DiffuseIndirect.Allow':1,'r.AntiAliasingMethod':4}); D.update({})
for k,v in D.items(): u.SystemLibrary.execute_console_command(W,'%s %s'%(k,v))
exec(open(u.Paths.project_dir()+'Tools/Neck_20261114/nk.py',encoding='utf8').read()); cam('q34',300,38,0,'spine_03')
print('CVSET2',"def")
