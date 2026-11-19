#!/bin/bash
# seqN.sh: frame-step robustness of the stop changes (data only, 30 and 60 Hz steps) on the evidence plan + jog-stop plan + stop plan.
#  V0 saved (brake 500/1100, sprint -> Dense run stops) | V1 brake 380/1100 (walk keeps its old brake), same remap
#  V2 brake 380/1100, sprint -> Dense sprint stops (runtime CM_ADD)
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; . Tools/UE59_20261116/plans.sh
R=/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases
CMA="exec(open(u.Paths.project_dir()+'Tools/UE59_20261118/cm_add.py',encoding='utf8').read())"
SP="[('',1.5,0),('W',3.0,0),('',2.0,0),('W LeftShift',3.0,0),('',2.5,0),('W',1.5,0),('W LeftShift',2.0,0),('',2.5,0),('W LeftShift',3.0,0),('W LeftShift',0.25,360),('',2.5,0),('W LeftShift LeftControl',4.0,0),('',3.0,0)]"
V0="pass"; V1="import builtins; builtins.VID_MOTION={'BrakeDecelLow':380.0,'BrakeDecelHigh':1100.0}"
V2="import builtins; builtins.VID_MOTION={'BrakeDecelLow':380.0,'BrakeDecelHigh':1100.0}; builtins.CM_ADD={'$R/Relaxed/PSD_Relaxed_Stand_Sprint_Stops':'$R/Dense/PSD_Dense_Stand_Sprint_Stops'}; $CMA"
echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
export VSIDE="(450,90,95,95,'pelvis')"
for v in ${VS:-V0 V1 V2}; do eval X=\$$v
  for hz in 30 60; do
    DFPS=$hz.0 bash Tools/UE59_20261118/run2.sh N_SP_${v}_$hz -6000 2000 92 0 "$SP" "$X"
    DFPS=$hz.0 bash Tools/UE59_20261118/run2.sh N_JS_${v}_$hz -6000 2000 92 0 "$(cat Saved/UE59Work/jstop_plan.txt)" "$X"
  done
done
unset VSIDE
echo "/Game/GraceRanger/Maps/L_GR_SphirusHouse" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
echo SEQN_DONE
