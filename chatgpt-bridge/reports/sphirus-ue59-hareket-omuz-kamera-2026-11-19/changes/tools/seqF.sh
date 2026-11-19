#!/bin/bash
# seqF.sh: sprint stop: brake High 1100/1400 x Relaxed vs Dense (Neutral) sprint stops (runtime), stop plan, 60 Hz data.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; . Tools/UE59_20261116/plans.sh
R=/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases
CMA="exec(open(u.Paths.project_dir()+'Tools/UE59_20261118/cm_add.py',encoding='utf8').read())"
DS="builtins.CM_ADD={'$R/Relaxed/PSD_Relaxed_Stand_Sprint_Stops':'$R/Dense/PSD_Dense_Stand_Sprint_Stops'}; $CMA"
echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
F1="builtins.VID_MOTION={'BrakeDecelLow':500.0,'BrakeDecelHigh':1100.0}; $DS"
F2="builtins.VID_MOTION={'BrakeDecelLow':500.0,'BrakeDecelHigh':1400.0}"
F4="builtins.VID_MOTION={'BrakeDecelLow':500.0,'BrakeDecelHigh':1100.0}; builtins.CM_ADD={'$R/Relaxed/PSD_Relaxed_Stand_Sprint_Stops':'$R/Dense/PSD_Dense_Stand_Run_Stops'}; $CMA"
F5="builtins.VID_MOTION={'BrakeDecelLow':500.0,'BrakeDecelHigh':1400.0}; builtins.CM_ADD={'$R/Relaxed/PSD_Relaxed_Stand_Sprint_Stops':'$R/Dense/PSD_Dense_Stand_Run_Stops'}; $CMA"
F3="builtins.VID_MOTION={'BrakeDecelLow':500.0,'BrakeDecelHigh':1400.0}; $DS"
for c in ${CS:-F1 F2 F3}; do eval X=\$$c; bash Tools/UE59_20261118/run2.sh F_STOP_$c -6000 2000 92 0 "$PLAN_STOP" "import builtins; $X"; done
echo "/Game/GraceRanger/Maps/L_GR_SphirusHouse" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
echo SEQF_DONE
