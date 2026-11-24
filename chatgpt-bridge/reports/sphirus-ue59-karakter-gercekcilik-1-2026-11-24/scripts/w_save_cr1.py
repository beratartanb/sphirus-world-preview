# w_save_cr1.py (write, gated): save the character realism pass 1 edits one asset at a time; read back the values that matter.
import unreal as u
ME=u.MaterialEditingLibrary
P=['/Game/Sphirus/CharacterLab/Sph_20261108/Skin/MI_Sph8_Head_LOD1_VT','/Game/Sphirus/CharacterLab/Day_20261107/Skin/MI_Sph_Body_Home','/Game/Sphirus/CharacterLab/Sph_20261108/Built/MHC_Sph8/Face/Materials/MI_EyeL_Baked','/Game/Sphirus/CharacterLab/Sph_20261108/Built/MHC_Sph8/Face/Materials/MI_EyeR_Baked','/Game/Sphirus/CharacterLab/GD35_IdentityMaster_20261011/Looks/MI_GD35_BrowS_n4','/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player']
exec(open(u.Paths.project_dir()+'Saved/UE59Work/r9/alldef.py',encoding='utf8').read())
for p in P:
    a=u.load_asset(p)
    if isinstance(a,u.Blueprint): u.BlueprintEditorLibrary.compile_blueprint(a)
    try: r=u.EditorAssetLibrary.save_loaded_asset(a,False)
    except Exception as e: r='SAVE_EXC '+repr(e)[:120]
    print('SAVECR1',p.split('/')[-1],r)
m=u.load_asset(P[0]); print('RB head',{n:round(ME.get_material_instance_scalar_parameter_value(m,n),3) for n in ('Micro Skin Normal Strength','Normal Flatten','Scatter Distance Global Multiply Post-Bake','Roughness Global Multiply Post-Bake','Micro Skin Cavity Specular Multiply')})
m=u.load_asset(P[2]); print('RB eye',{n:round(ME.get_material_instance_scalar_parameter_value(m,n),3) for n in ('Iris Global Saturation','Iris Primary Color Value','Fake Reflection Intensity')})
bp=u.load_asset(P[5]); sds=u.get_engine_subsystem(u.SubobjectDataSubsystem)
for h in sds.k2_gather_subobject_data_for_blueprint(bp):
    ob=u.SubobjectDataBlueprintFunctionLibrary.get_object(sds.k2_find_subobject_data_from_handle(h))
    if ob and ob.get_name().startswith('HairMain2'): print('RB hair',ob.get_editor_property('simulation_settings').export_text()[:900],'| phys',ob.get_editor_property('physics_asset')); break
exec(open(u.Paths.project_dir()+'Saved/UE59Work/r9/rchk.py',encoding='utf8').read())
print('DIRTY',[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()],'MAPS',[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()])
