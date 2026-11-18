#!/bin/bash
# seq12.sh: verification of the SAVED jog-stop fix (w_jstop19) + matched before/after videos.
# BEFORE = runtime revert: chooser bands 170/400 and Relaxed run/walk stops remapped to Dense again (= the 2026-11-18 saved state).
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; . Tools/UE59_20261116/plans.sh
R=/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases
CMA="exec(open(u.Paths.project_dir()+'Tools/UE59_20261118/cm_add.py',encoding='utf8').read())"
CHS="exec(open(u.Paths.project_dir()+'Tools/UE59_20261118b/ch_set.py',encoding='utf8').read())"
BEF="import builtins; builtins.CH_EDGES=(170,400); $CHS; builtins.CM_ADD={'$R/Relaxed/PSD_Relaxed_Stand_Run_Stops':'$R/Dense/PSD_Dense_Stand_Run_Stops','$R/Relaxed/PSD_Relaxed_Stand_Walk_Stops':'$R/Dense/PSD_Dense_Stand_Walk_Stops'}; $CMA"
AFT="import builtins; builtins.CH_EDGES=(200,440); $CHS"
echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
export VSIDE="(260,90,20,95,'pelvis')"
for p in ${PARTS:-data video}; do case $p in
 data)
  bash Tools/UE59_20261118/run2.sh T12_JSTOP_saved -6000 2000 92 0 "$(cat Saved/UE59Work/jstop_plan.txt)" "pass"
  DFPS=30.0 bash Tools/UE59_20261118/run2.sh T12_JSTOP_saved30 -6000 2000 92 0 "$(cat Saved/UE59Work/jstop_plan.txt)" "pass"
  bash Tools/UE59_20261118/run2.sh T12_STOP_saved -6000 2000 92 0 "$PLAN_STOP" "pass"
  bash Tools/UE59_20261118/run2.sh T12_BRAKE_saved -6000 2000 92 0 "$PLAN_BRAKE" "pass"
  bash Tools/UE59_20261118/run2.sh T12_JSTOP_before -6000 2000 92 0 "$(cat Saved/UE59Work/jstop_plan.txt)" "$BEF";;
 video)
  P="[('',2.0,0),('W LeftShift',3.0,0),('',2.5,0),('W LeftShift',3.3,0),('',2.5,0),('W LeftShift',3.0,0),('W LeftShift',0.5,90),('',2.5,0),('W',3.0,0),('',2.5,0)]"
  VSHOT=1 bash Tools/UE59_20261118/run2.sh V19_jstop_before -6000 2000 92 0 "$P" "$BEF"
  VSHOT=1 bash Tools/UE59_20261118/run2.sh V19_jstop_after -6000 2000 92 0 "$P" "$AFT"
  unset VSIDE
  VSHOT=1 bash Tools/UE59_20261118/run2.sh V19_jstop_pc_before -6000 2000 92 0 "$P" "$BEF"
  VSHOT=1 bash Tools/UE59_20261118/run2.sh V19_jstop_pc_after -6000 2000 92 0 "$P" "$AFT";;
esac; done
unset VSIDE
printf "import builtins; builtins.CH_EDGES=(200,440)\nexec(open(__import__('unreal').Paths.project_dir()+'Tools/UE59_20261118b/ch_set.py',encoding='utf8').read())\n" > Tools/UE59_20261118b/ch_saved.py
SHME_OWNER=emb SHME_KIND=measure bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/UE59_20261118b/ch_saved.py" emb_probe 60 2>&1 | grep CHSET
SHME_OWNER=emb SHME_KIND=measure bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/UE59_20261118/dirty.py" emb_probe 60 2>&1 | grep DIRTY
echo "/Game/GraceRanger/Maps/L_GR_SphirusHouse" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
echo SEQ12_DONE
