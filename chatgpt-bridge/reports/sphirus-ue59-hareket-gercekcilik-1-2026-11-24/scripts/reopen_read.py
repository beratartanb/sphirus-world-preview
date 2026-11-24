import unreal as u
c=u.get_default_object(u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player').generated_class())
print('REOPEN player',{k:round(c.get_editor_property(k),3) for k in ('PS_AbdBase','PS_AbdRun','HIP_On','HIP_LP','HIP_KSp','HIP_KYW','HIP_KYR','HIP_KYS','HIP_KOW','HIP_KOR','HIP_KOS','SH_KR','SH_KS','PS_FW','BOB_DipK','BOB_DipFree','BOB_DipMax')})
a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); print('REOPEN abp vars',[str(v.name) for v in u.BlueprintToolset.list_variables(a,None) if str(v.name) in ('SphHipRot','SphSpineRot','SphBob','PlantSettings_Turns','SphSelTime')])
ME=u.MaterialEditingLibrary; m=u.load_asset('/Game/Sphirus/CharacterLab/Sph_20261108/Skin/MI_Sph8_Head_LOD1_VT'); print('REOPEN head',{n:round(ME.get_material_instance_scalar_parameter_value(m,n),3) for n in ('Micro Skin Normal Strength','Normal Flatten','Scatter Distance Global Multiply Post-Bake')})
sds=u.get_engine_subsystem(u.SubobjectDataSubsystem); bp=u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player')
for h in sds.k2_gather_subobject_data_for_blueprint(bp):
    ob=u.SubobjectDataBlueprintFunctionLibrary.get_object(sds.k2_find_subobject_data_from_handle(h))
    if ob and ob.get_name().startswith('HairMain2'): print('REOPEN hair sim on','bEnableSimulation=True' in ob.get_editor_property('simulation_settings').export_text()); break
exec(open(u.Paths.project_dir()+'Saved/UE59Work/r9/rchk.py',encoding='utf8').read())
print('REOPEN dirty',[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()],[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()])
