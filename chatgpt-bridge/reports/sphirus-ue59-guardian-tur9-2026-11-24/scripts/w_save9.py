# w_save9.py (write, gated): save the round-9 in-memory edits one asset at a time.
# ABP_Sph_GASP (SphSelTime, PlantSettings_Turns + selection), AC_Sph_Motion, BP_Sph_GASPCharacter, BP_HybridA_Player.
import unreal as u
P=['/Game/Sphirus/Player/GASP/ABP_Sph_GASP','/Game/Sphirus/Player/Motion/AC_Sph_Motion','/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter','/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player']
for p in P:
    a=u.load_asset(p)
    if isinstance(a,u.Blueprint): u.BlueprintEditorLibrary.compile_blueprint(a)
    try: r=u.EditorAssetLibrary.save_loaded_asset(a,False)
    except Exception as e: r='SAVE_EXC '+repr(e)[:120]
    print('SAVE9',p.split('/')[-1],r)
exec(open(u.Paths.project_dir()+'Saved/UE59Work/r9/rchk.py',encoding='utf8').read())
print('DIRTY',[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()])
