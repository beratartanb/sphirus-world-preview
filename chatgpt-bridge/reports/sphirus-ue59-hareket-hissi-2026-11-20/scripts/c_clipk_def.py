# c_clipk_def.py: ClipHiRef / ClipHiMin defaults on AC_Sph_Motion CDO + the SphMotion template of BP_Sph_GASPCharacter; sprint stop map.
import unreal as u, builtins
V=getattr(builtins,'CLIPK_DEF',None) or {'ClipHiRef':375.0,'ClipHiMin':470.0}
c=u.get_default_object(u.load_asset('/Game/Sphirus/Player/Motion/AC_Sph_Motion').generated_class())
for k,v in V.items(): c.set_editor_property(k,v)
g=u.load_asset('/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'); sds=u.get_engine_subsystem(u.SubobjectDataSubsystem); n=0
for h in sds.k2_gather_subobject_data_for_blueprint(g):
    o=u.SubobjectDataBlueprintFunctionLibrary.get_object(u.SubobjectDataBlueprintFunctionLibrary.get_data(h)) if hasattr(u,'SubobjectDataBlueprintFunctionLibrary') else None
    if o and 'SphMotion' in o.get_name():
        for k,v in V.items(): o.set_editor_property(k,v)
        n+=1; print('TEMPLATE',o.get_name(),{k:o.get_editor_property(k) for k in V})
print('CLIPKDEF cdo',{k:c.get_editor_property(k) for k in V},'templates',n)
R_='/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/Relaxed/PSD_Relaxed_Stand_'
builtins.MAP_OVR={'PSD_Relaxed_Stand_Sprint_Stops':(R_+'Run_Stops',R_+'Run_Stops'),'PSD_Relaxed_Stand_Run_Stops':(None,R_+'Run_Stops')}
exec(open(u.Paths.project_dir()+'Tools/UE59_20261120/c_mapovr.py',encoding='utf8').read())
