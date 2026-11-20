# c_round3.py: round-3 defaults (in memory as control job; body of the gated write job w_round3_save.py).
import unreal as u, builtins
MV=dict({'StLatch':0.1,'StKMin':0.5,'StKMax':1.8,'StKOn':True,'StartDur':0.7,'StartAdd':30.0,'StartCapK':1.0,'StartCapOn':False,'RevOn':False}, **(getattr(builtins,'R3_MOTION',None) or {}))
PV=dict({'GR_BackK':1.0,'GR_StopHoldMin':470.0}, **(getattr(builtins,'R3_PLAYER',None) or {}))
c=u.get_default_object(u.load_asset('/Game/Sphirus/Player/Motion/AC_Sph_Motion').generated_class()); objs=[c]
g=u.load_asset('/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'); sds=u.get_engine_subsystem(u.SubobjectDataSubsystem)
for h in sds.k2_gather_subobject_data_for_blueprint(g):
    o=u.SubobjectDataBlueprintFunctionLibrary.get_object(u.SubobjectDataBlueprintFunctionLibrary.get_data(h))
    if o and 'SphMotion' in o.get_name(): objs.append(o)
for o in objs:
    for k,v in MV.items(): o.set_editor_property(k,v)
print('MOTION',len(objs),{k:c.get_editor_property(k) for k in MV})
bp=u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'); pc=u.get_default_object(bp.generated_class())
for k,v in PV.items(): pc.set_editor_property(k,v)
print('PLAYER',{k:pc.get_editor_property(k) for k in PV})
builtins.MAP_OVR=getattr(builtins,'R3_MAP',None) or {'PSD_Relaxed_Stand_Run_Stops':(None,'/Game/Sphirus/Player/GASP/CM/DB/PSD_CM_Jog_Stops')}
exec(open(u.Paths.project_dir()+'Tools/UE59_20261120/c_mapovr.py',encoding='utf8').read())
