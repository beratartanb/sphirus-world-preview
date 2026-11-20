# c_mapovr.py: override entries of the database maps on the class defaults (in-memory as control job; body of a write job when saved).
# OVR = {key_db_name: (normal_value_path or None, tempo_value_path or None)}
import unreal as u, builtins
R_='/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/Relaxed/PSD_Relaxed_Stand_'
OVR=getattr(builtins,'MAP_OVR',None) or {'PSD_Relaxed_Stand_Sprint_Stops':(R_+'Sprint_Stops',R_+'Sprint_Stops'),'PSD_Relaxed_Stand_Run_Stops':(None,R_+'Run_Stops')}
abp=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); ac=u.get_default_object(abp.generated_class())
bp=u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'); pc=u.get_default_object(bp.generated_class())
K=[x.get_name() for x in ac.get_editor_property('CM_Keys')]; NV=list(pc.get_editor_property('GR_NormVals')); TV=list(pc.get_editor_property('GR_TempoVals'))
for k,(n,t) in OVR.items():
    i=K.index(k)
    if n: NV[i]=u.load_asset(n); assert NV[i]
    if t: TV[i]=u.load_asset(t); assert TV[i]
ac.set_editor_property('CM_Vals',NV); pc.set_editor_property('GR_NormVals',NV); pc.set_editor_property('GR_TempoVals',TV)
print('MAPOVR',[(k,NV[K.index(k)].get_name(),TV[K.index(k)].get_name()) for k in OVR])
