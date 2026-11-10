exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
exec(open(u.Paths.project_dir()+'Tools/GASP_20261109/gdump.py',encoding='utf8').read())
O=u.Paths.project_dir()+'Tools/GASP_20261109/'
for path,name,gs in [('/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter','gaspchar',['EventGraph','GetDesiredGait','GetMovementInputScaleValue','SetupCamera','UpdateRotation_PreCMC','UpdateMovement_PreCMC','CalculateMaxSpeed','CalculateMaxAcceleration','CalculateBrakingDeceleration','CalculateGroundFriction','CalculateBrakingFriction','CanSprint']),('/Game/Sphirus/Player/GASP/BP_Sph_GASP_B','candB',['EventGraph'])]:
    bp=u.load_asset(path)
    for gn in gs:
        g=B.get_graph(bp,gn); print('DUMP',name,gn,gdump(g,O+'g_%s_%s.txt'%(name,gn)))
