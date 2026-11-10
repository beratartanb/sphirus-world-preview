import unreal as u
from editor_toolset.toolsets.blueprint import BlueprintTools as B
print('DOC',B.find_node_types.__doc__[:700])
bp=u.load_asset('/Game/Sphirus/Player/GASP/BP_Sph_GASP_B'); g=B.get_graph(bp,'EventGraph')
for q in ('BeginPlay','OnLanded','Parent','Üst','PlayerInputState','CharacterInputState'):
    try: r=B.find_node_types(g,q); print('Q',q,[str(x) for x in r][:25])
    except Exception as e:
        try: r=B.find_node_types(bp,q); print('Q2',q,[str(x) for x in r][:25])
        except Exception as e2: print('QERR',q,str(e)[:150],str(e2)[:150])
c=u.get_default_object(u.load_object(None,'/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter.BP_Sph_GASPCharacter_C'))
for k in ('MovementStickMode','WalkSpeeds','RunSpeeds','SprintSpeeds','CrouchSpeeds','AnalogWalk/RunThreshold'):
    try: print('CDO',k,c.get_editor_property(k))
    except Exception as e: print('CDO',k,'ERR',str(e)[:80])
