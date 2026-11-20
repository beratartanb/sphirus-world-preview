# w_tune2.py (write, gated): GaitUpAcc 0.55 -> 0.8 (straight run-up was 440 cm/s2 from ~150 cm/s on; the run start clip accelerates
# ~700 cm/s2) and VW_Neck1 -8 -> -6 (tempo tier head was 5.6 deg above level with -8).
import unreal as u, builtins
V={'GaitUpAcc':0.8}
c=u.get_default_object(u.load_asset('/Game/Sphirus/Player/Motion/AC_Sph_Motion').generated_class()); objs=[c]
g=u.load_asset('/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'); sds=u.get_engine_subsystem(u.SubobjectDataSubsystem)
for h in sds.k2_gather_subobject_data_for_blueprint(g):
    o=u.SubobjectDataBlueprintFunctionLibrary.get_object(u.SubobjectDataBlueprintFunctionLibrary.get_data(h))
    if o and 'SphMotion' in o.get_name(): objs.append(o)
for o in objs:
    for k,v in V.items(): print('SET',o.get_name(),k,o.get_editor_property(k),'->',v); o.set_editor_property(k,v)
for p in ('/Game/Sphirus/Player/Motion/AC_Sph_Motion','/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'):
    print('SAVE',p.split('/')[-1],u.EditorAssetLibrary.save_loaded_asset(u.load_asset(p),False))
builtins.P6V={'VW_Neck1':(-6.0,0.0,0.0)}
exec(open(u.Paths.project_dir()+'Tools/UE59_20261120/p6_values.py',encoding='utf8').read())
