# w_rev_save.py (write, gated): reversal softening defaults (CDO + SphMotion template) and save.
import unreal as u
V={'RevOn':True,'RevFricMin':0.25,'RevDecelLow':0.0,'RevDecelHigh':0.0,'RevSpLo':250.0,'RevSpHi':470.0}
c=u.get_default_object(u.load_asset('/Game/Sphirus/Player/Motion/AC_Sph_Motion').generated_class())
for k,v in V.items(): c.set_editor_property(k,v)
g=u.load_asset('/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'); sds=u.get_engine_subsystem(u.SubobjectDataSubsystem)
for h in sds.k2_gather_subobject_data_for_blueprint(g):
    o=u.SubobjectDataBlueprintFunctionLibrary.get_object(u.SubobjectDataBlueprintFunctionLibrary.get_data(h))
    if o and 'SphMotion' in o.get_name():
        for k,v in V.items(): o.set_editor_property(k,v)
        print('TEMPLATE',o.get_name(),{k:o.get_editor_property(k) for k in V})
for p in ('/Game/Sphirus/Player/Motion/AC_Sph_Motion','/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'):
    print('SAVE',p.split('/')[-1],u.EditorAssetLibrary.save_loaded_asset(u.load_asset(p),False))
print('DIRTY',[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()])
