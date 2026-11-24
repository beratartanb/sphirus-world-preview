# w_save_mr1.py (write, gated): movement realism pass 1 - ABP_Sph_GASP (hip / spine nodes) + BP_HybridA_Player (GR_Bob logic, defaults).
# alldef order is fixed: older default sets first, c_cr1_defaults and c_mr1_defaults LAST, then the values are read back before saving.
import unreal as u
exec(open(u.Paths.project_dir()+'Saved/UE59Work/r9/alldef.py',encoding='utf8').read())
c=u.get_default_object(u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player').generated_class())
rb={k:c.get_editor_property(k) for k in ('PS_AbdBase','PS_AbdRun','HIP_On','HIP_KYW','HIP_KOW','SH_KR','BOB_DipK','PS_FW')}; print('PRESAVE',rb); assert rb['PS_AbdBase']==8.5 and rb['PS_AbdRun']==13.5 and rb['HIP_On']==1.0, rb
for p in ('/Game/Sphirus/Player/GASP/ABP_Sph_GASP','/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'):
    a=u.load_asset(p); u.BlueprintEditorLibrary.compile_blueprint(a)
    try: r=u.EditorAssetLibrary.save_loaded_asset(a,False)
    except Exception as e: r='SAVE_EXC '+repr(e)[:120]
    print('SAVEMR1',p.split('/')[-1],r)
exec(open(u.Paths.project_dir()+'Saved/UE59Work/r9/rchk.py',encoding='utf8').read())
print('DIRTY',[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()],'MAPS',[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()])
