# reopen_p4.py (control, read-only): after relaunch, pass-4 state read from disk
import unreal as u
c = u.get_default_object(u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player').generated_class())
m = u.get_default_object(u.load_asset('/Game/Sphirus/Player/Motion/AC_Sph_Motion').generated_class())
ks = ('CS_On','CS_StepUp','CS_DecSlope','CS_SlopeTan','SH_On','SH_VStill','ATH_On','ATH_K','ATH_Air','AW_On','AW_Arm','AW_Yaw','AW_Head','TR_On','PS_AbdBwd','PS_AbdFwdJog','CA_RadP','CA_Max')
print('REOPENP4 player', {k: c.get_editor_property(k) for k in ks})
print('REOPENP4 motion', {k: m.get_editor_property(k) for k in ('AL_Deg','AL_DegB','AL_Ref','AL_Rate')})
sub = u.get_engine_subsystem(u.SubobjectDataSubsystem); bp = u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player')
print('REOPENP4 comps', [o.get_name() for o in [u.SubobjectDataBlueprintFunctionLibrary.get_object(sub.k2_find_subobject_data_from_handle(h)) for h in sub.k2_gather_subobject_data_for_blueprint(bp)] if o and 'Travers' in o.get_class().get_name()])
print('REOPENP4 dirty', [x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()])
