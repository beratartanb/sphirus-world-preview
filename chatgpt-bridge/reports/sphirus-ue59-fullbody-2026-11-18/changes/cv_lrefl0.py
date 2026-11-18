import unreal as u
W=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world()
D=dict({'r.Shadow.Virtual.Enable':1,'r.Lumen.DiffuseIndirect.Allow':1,'r.Lumen.Reflections.Allow':1,'r.SubsurfaceScattering':1,'r.HairStrands.Enable':1,'r.ContactShadows':1,'r.DistanceFieldShadowing':1,'r.Lumen.HardwareRayTracing':1,'r.LocalExposure':1}); D.update({'r.Lumen.Reflections.Allow':0})
for k,v in D.items(): u.SystemLibrary.execute_console_command(W,'%s %s'%(k,v))
print('CVSET',"lrefl0")
