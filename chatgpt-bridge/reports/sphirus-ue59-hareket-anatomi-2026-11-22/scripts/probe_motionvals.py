import unreal as u
g=u.load_asset('/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'); sds=u.get_engine_subsystem(u.SubobjectDataSubsystem); o=None
for h in sds.k2_gather_subobject_data_for_blueprint(g):
    x=u.SubobjectDataBlueprintFunctionLibrary.get_object(u.SubobjectDataBlueprintFunctionLibrary.get_data(h))
    if x and 'SphMotion' in x.get_name(): o=x
out={}
for k in ('RevOn','RevFricMin','RevSpLo','RevSpHi','RevDecelLow','RevDecelHigh','RcOn','RcFric','RcSpMin','RcMin','RcMax','RcTz','TurnFricOn','PhysBrake','StKOn','ClipBrakeOn','BrakeDecelLow','BrakeDecelHigh'):
    try: out[k]=o.get_editor_property(k)
    except Exception as e: out[k]='?'
print('MVALS',out)
