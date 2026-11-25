# w_save_mr3.py (write, gated): movement realism pass 3 - AC_Sph_Motion (DmBoostAdd, DmCoastDec), BP_HybridA_Player (braking-step coast,
# gait step-up scale, crouch jump gate, arm clearance + later pass-3 steps), ABP_Sph_GASP when listed in builtins.MR3SAVE_ABP.
# Only c_mr3_defaults is re-applied (other sessions' values are left as they are); pass-2 values are asserted, not rewritten.
import unreal as u, builtins
exec(open(u.Paths.project_dir()+'Tools/UE59_20261124/c_mr3_defaults.py',encoding='utf8').read())
c=u.get_default_object(u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player').generated_class())
m=u.get_default_object(u.load_asset('/Game/Sphirus/Player/Motion/AC_Sph_Motion').generated_class())
rb={k:c.get_editor_property(k) for k in ('PS_AbdBase','HIP_On','SL_On','HD_B','ID_On','CS_On','CS_Dec','CS_VMin','GU_Run','GU_Tempo','CA_On','CA_Tgt','CA_Rad')}; rb['RcOpen']=m.get_editor_property('RcOpen'); rb['DmBoostAdd']=m.get_editor_property('DmBoostAdd'); rb['DmCoastDec']=m.get_editor_property('DmCoastDec'); print('PRESAVE3',rb)
assert rb['PS_AbdBase']==8.5 and rb['HIP_On']==1.0 and rb['RcOpen']==150.0 and rb['SL_On']==1.0 and rb['HD_B']==1.0 and rb['ID_On']==1.0, rb
assert rb['CS_On']==1.0 and rb['CS_Dec']>100 and rb['GU_Run']>0.1 and rb['GU_Tempo']>0.05 and rb['CA_Rad']>5 and rb['DmBoostAdd']==0.0 and rb['DmCoastDec']==0.0, rb
L=['/Game/Sphirus/Player/Motion/AC_Sph_Motion','/Game/Sphirus/Player/Camera/AC_Sph_Camera']+list(getattr(builtins,'MR3SAVE_ABP',None) or [])+['/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player']
for p in L:
    a=u.load_asset(p); u.BlueprintEditorLibrary.compile_blueprint(a)
    try: r=u.EditorAssetLibrary.save_loaded_asset(a,False)
    except Exception as e: r='SAVE_EXC '+repr(e)[:120]
    print('SAVEMR3',p.split('/')[-1],r)
print('DIRTY',[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()],'MAPS',[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()])
