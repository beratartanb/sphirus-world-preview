#!/bin/bash
# seqL.sh: evidence on the SAVED final state, all videos at a 30 Hz fixed step encoded at 30 fps (= real speed, checked by vtime.py).
#  shoulder  upper-body review from front 3/4, side, back 3/4 (seqB plan) -> B_final_a35/a90/a150 (before = B_base_* from seqB, recorded
#            before the posture-layer change)
#  stops     full-body side camera (450 cm, aimed at the pelvis, feet in frame): walk stop, jog stop, walk->jog->stop, 90 turn into stop,
#            sprint stop. before = runtime revert of the 2026-11-19 stop changes (brake 380/780, Relaxed sprint stops) | after = saved
#  light     kitchen -> rear door exit route (player camera), saved state
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"
R=/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases
CMA="exec(open(u.Paths.project_dir()+'Tools/UE59_20261118/cm_add.py',encoding='utf8').read())"
BEF="import builtins; builtins.VID_MOTION={'BrakeDecelLow':380.0,'BrakeDecelHigh':780.0}; builtins.CM_ADD={'$R/Relaxed/PSD_Relaxed_Stand_Sprint_Stops':'$R/Relaxed/PSD_Relaxed_Stand_Sprint_Stops'}; $CMA"
SP="[('',1.5,0),('W',3.0,0),('',2.0,0),('W LeftShift',3.0,0),('',2.5,0),('W',1.5,0),('W LeftShift',2.0,0),('',2.5,0),('W LeftShift',3.0,0),('W LeftShift',0.25,360),('',2.5,0),('W LeftShift LeftControl',4.0,0),('',3.0,0)]"
for p in ${PARTS:-shoulder stops light}; do case $p in
 shoulder) bash Tools/UE59_20261119/seqB.sh final pass;;
 stops) echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt
   SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
   VSHOT=1 VSIDE="(450,90,95,95,'pelvis')" bash Tools/UE59_20261118/run2.sh L_stops_before -6000 2000 92 0 "$SP" "$BEF"
   VSHOT=1 VSIDE="(450,90,95,95,'pelvis')" bash Tools/UE59_20261118/run2.sh L_stops_after -6000 2000 92 0 "$SP" "pass";;
 light) echo "/Game/GraceRanger/Maps/L_GR_SphirusHouse" > Saved/Codex/Day_20261107/loadmap.txt
   SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
   VSHOT=1 bash Tools/UE59_20261118/run2.sh L_lightexit_final 1080 200 245 180 "$(cat Tools/UE59_20261118/light_exit.txt)" "pass"
   VSHOT=1 bash Tools/UE59_20261118/run2.sh L_lightpatch_final 520 160 241 180 "$(cat Tools/UE59_20261118/light_patch.txt)" "pass";;
esac; done
echo "/Game/GraceRanger/Maps/L_GR_SphirusHouse" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
echo SEQL_DONE
