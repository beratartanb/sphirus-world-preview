# c_gov6_defaults.py (control, in-memory): governor defaults on the AC_Sph_Motion CDO + SphMotion template. builtins.GOV overrides.
import unreal as u, builtins
V={'KRelax':3.0,'StBoostMax':1400.0,'StBoostDur':0.9,'StBoostOn':True}
V.update(getattr(builtins,'GOV',None) or {})
objs=[u.get_default_object(u.load_asset('/Game/Sphirus/Player/Motion/AC_Sph_Motion').generated_class())]
g=u.load_asset('/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'); sds=u.get_engine_subsystem(u.SubobjectDataSubsystem)
for h in sds.k2_gather_subobject_data_for_blueprint(g):
    o=u.SubobjectDataBlueprintFunctionLibrary.get_object(u.SubobjectDataBlueprintFunctionLibrary.get_data(h))
    if o and 'SphMotion' in o.get_name(): objs.append(o)
for o in objs:
    for k,v in V.items(): o.set_editor_property(k,v)
    print('GOVDEF',o.get_name(),{k:o.get_editor_property(k) for k in V})
