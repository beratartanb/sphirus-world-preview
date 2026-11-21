import unreal as u
sds=u.get_engine_subsystem(u.SubobjectDataSubsystem); o=[]
for p in ('/Game/StoryFramework/Core/Blueprints/InteractableBase_BP','/Game/GraceRanger/SF/Day/BP_GR_DayStation'):
    g=u.load_asset(p)
    for h in sds.k2_gather_subobject_data_for_blueprint(g):
        x=u.SubobjectDataBlueprintFunctionLibrary.get_object(u.SubobjectDataBlueprintFunctionLibrary.get_data(h))
        if x: o.append('%s: %s [%s] parent %s'%(p.split('/')[-1],x.get_name(),x.get_class().get_name(),x.get_attach_parent().get_name() if hasattr(x,'get_attach_parent') and x.get_attach_parent() else '-'))
print('STCOMP\n'+'\n'.join(sorted(set(o))))
