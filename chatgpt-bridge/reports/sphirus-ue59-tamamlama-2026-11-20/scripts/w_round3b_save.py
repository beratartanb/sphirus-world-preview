# w_round3b_save.py (write, gated): final tempo maps after A/B (2026-11-20 round 3):
#  tempo stops  -> Relaxed run stops (with the latched stop scale: 0.42-0.62 s, stop contacts <= 14 cm; CM jog stops varied 0.32-0.83 s)
#  tempo forward starts -> PSD_Sph_N_Run_F_Starts (Neutral run starts; CM Start_Turn180 slid the planted foot 75 cm, Neutral 2-3 cm)
#  strafe starts -> PSD_Sph_N_<gait>_S_Starts (no reface clips).  StartCapOn stays False (turn-start cap rejected: 42 cm and 1.1 s).
import unreal as u, builtins
R_='/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/Relaxed/PSD_Relaxed_Stand_'; D='/Game/Sphirus/Player/GASP/DB/'
M={'PSD_Relaxed_Stand_Run_Stops':(None,R_+'Run_Stops'),'PSD_Relaxed_Stand_Run_F_Starts':(None,D+'PSD_Sph_N_Run_F_Starts')}
for d_ in ('B','LL','RL'):
    M['PSD_Relaxed_Stand_Walk_%s_Starts'%d_]=(D+'PSD_Sph_N_Walk_S_Starts',D+'PSD_Sph_N_Walk_S_Starts'); M['PSD_Relaxed_Stand_Run_%s_Starts'%d_]=(D+'PSD_Sph_N_Run_S_Starts',None)
builtins.R3_MAP=M; builtins.R3_MOTION={'StartCapOn':False,'StartTurnCos':-0.2}
exec(open(u.Paths.project_dir()+'Tools/UE59_20261120/c_round3.py',encoding='utf8').read())
for p in ('/Game/Sphirus/Player/Motion/AC_Sph_Motion','/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter','/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player','/Game/Sphirus/Player/GASP/ABP_Sph_GASP'):
    try: print('SAVE',p.split('/')[-1],u.EditorAssetLibrary.save_loaded_asset(u.load_asset(p),False))
    except Exception as e: print('SAVE_EXC',p.split('/')[-1],repr(e)[:90])
print('DIRTY',[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()])
