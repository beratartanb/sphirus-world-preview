# c_motion5_defaults.py (control, in-memory): round-5 defaults on AC_Sph_Motion CDO + SphMotion template (builtins.M5V overrides)
# and ClavDeg (breathing shoulder amplitude) on the body ABP.
import unreal as u, builtins
V={'TlOn':True,'TlG45':0.93,'TlG90':0.76,'TlG135':0.52,'TlDecay':300.0,'TlSpLo':150.0,'TlSpHi':400.0,'TlPeak':0.0,'TlG':1.0,
   'StartCapOn':False,'TlArm':0.9,'StSoftT':0.18,'StSoftK':0.5,
   'CtCap':100000.0,'CtA':0.0,'CtBrake':1300.0,'DmOn':True,'DmMax':2600.0,'DmMargin':15.0,'DmT':0.0,'DmK':1.0,'DmDecel':0.0}
V.update(getattr(builtins,'M5V',None) or {})
objs=[u.get_default_object(u.load_asset('/Game/Sphirus/Player/Motion/AC_Sph_Motion').generated_class())]
g=u.load_asset('/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'); sds=u.get_engine_subsystem(u.SubobjectDataSubsystem)
for h in sds.k2_gather_subobject_data_for_blueprint(g):
    o=u.SubobjectDataBlueprintFunctionLibrary.get_object(u.SubobjectDataBlueprintFunctionLibrary.get_data(h))
    if o and 'SphMotion' in o.get_name(): objs.append(o)
for o in objs:
    for k,v in V.items(): o.set_editor_property(k,v)
print('M5DEF',{k:objs[-1].get_editor_property(k) for k in ('TlOn','TlG90','StartCapOn','TlArm','StSoftT','StSoftK','DmOn','DmMax')})
b=u.get_default_object(u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP').generated_class()); print('ClavDeg was',b.get_editor_property('ClavDeg')); b.set_editor_property('ClavDeg',2.5)
