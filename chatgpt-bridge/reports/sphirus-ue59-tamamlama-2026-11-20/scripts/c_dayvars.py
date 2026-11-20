# c_dayvars.py: actor-reference variables on BP_GR_DayHub (MCP AddVariable has no object types)
import unreal as u
bp=u.load_asset('/Game/GraceRanger/SF/Day/BP_GR_DayHub')
have=[str(v.name) for v in u.BlueprintToolset.list_variables(bp,None)]
for n in ('GR_FireSt','GR_TeaSt'):
    if n in have: print('HAVE',n); continue
    t=u.EdGraphPinType(); t.import_text('(PinCategory="object",PinSubCategoryObject="/Script/CoreUObject.Class\'/Script/Engine.Actor\'")')
    print('ADD',n,u.BlueprintEditorLibrary.add_member_variable(bp,n,t)); u.BlueprintEditorLibrary.set_blueprint_variable_instance_editable(bp,n,True)
u.BlueprintEditorLibrary.compile_blueprint(bp); print('OK')
