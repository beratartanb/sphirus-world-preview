# w_clipk_save.py (write, gated): store ClipHiRef/ClipHiMin, the stop database map (sprint + tempo -> Relaxed run stops) and save.
import unreal as u
exec(open(u.Paths.project_dir()+'Tools/UE59_20261120/c_clipk_def.py',encoding='utf8').read())
for p in ('/Game/Sphirus/Player/Motion/AC_Sph_Motion','/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter','/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player','/Game/Sphirus/Player/GASP/ABP_Sph_GASP'):
    a=u.load_asset(p)
    try: print('SAVE',p.split('/')[-1],u.EditorAssetLibrary.save_loaded_asset(a,False))
    except Exception as e: print('SAVE_EXC',p.split('/')[-1],repr(e)[:100])
print('DIRTY',[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()])
