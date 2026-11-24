# w_save_mr2.py (write, gated): movement realism pass 2 - ABP_Sph_GASP (neck node, spine translation pin), BP_HybridA_Player (GR_Bob /
# GR_Foot / GR_Posture logic, defaults), AC_Sph_Motion (RcOpen 150). alldef order fixed (c_mr2_defaults LAST); values read back before saving.
import unreal as u
exec(open(u.Paths.project_dir()+'Saved/UE59Work/r9/alldef.py',encoding='utf8').read())
c=u.get_default_object(u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player').generated_class())
m=u.get_default_object(u.load_asset('/Game/Sphirus/Player/Motion/AC_Sph_Motion').generated_class())
rb={k:c.get_editor_property(k) for k in ('PS_AbdBase','PS_AbdRun','HIP_On','HIP_KYW','SH_KR','SL_On','SL_V0','HD_K','HD_B','HD_T','HIP_GY','HIP_Rate','ID_On','ID_KS','BOB_DipK','PS_FW')}; rb['RcOpen']=m.get_editor_property('RcOpen'); print('PRESAVE',rb)
assert rb['PS_AbdBase']==8.5 and rb['PS_AbdRun']==13.5 and rb['HIP_On']==1.0 and rb['RcOpen']==150.0 and rb['SL_On']==1.0 and rb['HD_B']==1.0 and rb['HD_K']==0.0 and rb['HIP_Rate']==150.0 and rb['ID_On']==1.0, rb
for p in ('/Game/Sphirus/Player/Motion/AC_Sph_Motion','/Game/Sphirus/Player/GASP/ABP_Sph_GASP','/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'):
    a=u.load_asset(p); u.BlueprintEditorLibrary.compile_blueprint(a)
    try: r=u.EditorAssetLibrary.save_loaded_asset(a,False)
    except Exception as e: r='SAVE_EXC '+repr(e)[:120]
    print('SAVEMR2',p.split('/')[-1],r)
exec(open(u.Paths.project_dir()+'Saved/UE59Work/r9/rchk.py',encoding='utf8').read())
print('DIRTY',[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()],'MAPS',[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()])
