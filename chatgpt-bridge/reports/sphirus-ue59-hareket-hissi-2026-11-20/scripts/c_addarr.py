# c_addarr.py (in-memory): object-array member variables on BP_HybridA_Player (MCP AddVariable has no object types)
import unreal as u
bp=u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player')
for n in ('GR_TempoVals','GR_NormVals'):
    t=u.EdGraphPinType(); t.import_text('(PinCategory="object",PinSubCategoryObject="/Script/CoreUObject.Class\'/Script/PoseSearch.PoseSearchDatabase\'",ContainerType=Array)')
    try: print('ADD',n,u.BlueprintEditorLibrary.add_member_variable(bp,n,t))
    except Exception as e: print('ERR',n,repr(e)[:200])
u.BlueprintEditorLibrary.compile_blueprint(bp)
c=u.get_default_object(bp.generated_class())
for n in ('GR_TempoVals','GR_NormVals'):
    try: print('HAS',n,type(c.get_editor_property(n)).__name__, c.get_editor_property(n))
    except Exception as e: print('NOPROP',n,repr(e)[:120])
