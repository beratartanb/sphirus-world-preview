import unreal as u
from editor_toolset.toolsets.blueprint import BlueprintTools as B
O=u.Paths.project_dir()+'Tools/GASP_20261109/'
print('DOC',B.read_graph_dsl.__doc__[:400])
for path,name,graphs in [('/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter','gaspchar',['EventGraph','GetDesiredGait','GetMovementInputScaleValue','SetupInput','SetupCamera','UpdateRotation_PreCMC','UpdateMovement_PreCMC','CalculateMaxSpeed','CalculateMaxAcceleration','CalculateBrakingDeceleration','CalculateGroundFriction','CalculateBrakingFriction','Get_PropertiesForAnimation']),('/Game/Sphirus/Player/GASP/BP_Sph_GASP_B','candB',['EventGraph'])]:
    bp=u.load_asset(path)
    for gn in graphs:
        try:
            g=B.get_graph(bp,gn); t=B.read_graph_dsl(g) if True else ''
        except Exception as e:
            try: t=B.read_graph_dsl(bp,gn)
            except Exception as e2: t='ERR %s | %s'%(str(e)[:200],str(e2)[:200])
        open(O+'dsl_%s_%s.txt'%(name,gn),'w',encoding='utf8').write(str(t)); print('DSL',name,gn,len(str(t)))
ia=u.load_asset('/Game/Sphirus/Player/Input/IA_Sph_Move'); ib=u.load_asset('/Game/Input/IA_Move')
print('IA types',ia.get_editor_property('value_type'),ib.get_editor_property('value_type'))
