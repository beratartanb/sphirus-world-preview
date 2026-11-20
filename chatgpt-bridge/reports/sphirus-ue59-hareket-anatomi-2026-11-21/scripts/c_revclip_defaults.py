# c_revclip_defaults.py (control, in-memory): clip-bound reversal defaults on AC_Sph_Motion CDO + the SphMotion template of
# BP_Sph_GASPCharacter. builtins.RCV overrides.
import unreal as u, builtins
V={'RcOn':True,'RcLatch':0.12,'RcMin':150.0,'RcAnalogMin':150.0,'RcTz':0.5,'RcSpMin':250.0,'RcMax':2600.0,'RcFric':0.02,'RcExitDur':0.9,'RcExitK':1.08,'RcExitAdd':25.0,'RcK':1.0}
V.update(getattr(builtins,'RCV',None) or {})
objs=[u.get_default_object(u.load_asset('/Game/Sphirus/Player/Motion/AC_Sph_Motion').generated_class())]
g=u.load_asset('/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'); sds=u.get_engine_subsystem(u.SubobjectDataSubsystem)
for h in sds.k2_gather_subobject_data_for_blueprint(g):
    o=u.SubobjectDataBlueprintFunctionLibrary.get_object(u.SubobjectDataBlueprintFunctionLibrary.get_data(h))
    if o and 'SphMotion' in o.get_name(): objs.append(o)
for o in objs:
    for k,v in V.items(): o.set_editor_property(k,v)
    print('RCDEF',o.get_name(),{k:o.get_editor_property(k) for k in ('RcOn','RcMin','RcMax','RcFric')})
