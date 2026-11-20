import builtins, unreal as u
R_='/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/Relaxed/PSD_Relaxed_Stand_'
builtins.VID_PAWN={'GR_TempoOn':bool(getattr(builtins,'PRE_TEMPO',True))}
builtins.NORM_ADD={'PSD_Relaxed_Stand_Sprint_Stops':R_+'Sprint_Stops'}
builtins.TEMPO_ADD={'PSD_Relaxed_Stand_Sprint_Stops':R_+'Sprint_Stops','PSD_Relaxed_Stand_Run_Stops':R_+'Run_Stops'}
try: exec(open(u.Paths.project_dir()+'Tools/UE59_20261120/cm_set.py',encoding='utf8').read())
except Exception as e: open(u.Paths.project_dir()+'Saved/UE59Work/pre_err.txt','w').write(repr(e))
