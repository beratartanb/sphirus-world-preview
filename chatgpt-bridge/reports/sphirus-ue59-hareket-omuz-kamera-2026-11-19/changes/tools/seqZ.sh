#!/bin/bash
# seqZ.sh: final evidence on the final saved configuration (brake 380/1100, relax terms, sprint -> Dense run stops, TightRaise 45,
# static sun shadow bias 0): seqL (shoulder/stops/light), full flow + load test + empty fire, saved-state stop data at 30/60 Hz.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; . Tools/UE59_20261116/plans.sh
bash Tools/UE59_20261119/seqL.sh
VSHOT=1 bash Tools/UE59_20261119/fin19.sh Z pieces flow loadfire emptyfire
SP="[('',1.5,0),('W',3.0,0),('',2.0,0),('W LeftShift',3.0,0),('',2.5,0),('W',1.5,0),('W LeftShift',2.0,0),('',2.5,0),('W LeftShift',3.0,0),('W LeftShift',0.25,360),('',2.5,0),('W LeftShift LeftControl',4.0,0),('',3.0,0)]"
echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
export VSIDE="(450,90,95,95,'pelvis')"
for hz in 30 60; do
  DFPS=$hz.0 bash Tools/UE59_20261118/run2.sh Z_SP_$hz -6000 2000 92 0 "$SP" "pass"
  DFPS=$hz.0 bash Tools/UE59_20261118/run2.sh Z_JS_$hz -6000 2000 92 0 "$(cat Saved/UE59Work/jstop_plan.txt)" "pass"
  DFPS=$hz.0 bash Tools/UE59_20261118/run2.sh Z_ST_$hz -6000 2000 92 0 "$PLAN_STOP" "pass"
  DFPS=$hz.0 bash Tools/UE59_20261118/run2.sh Z_BR_$hz -6000 2000 92 0 "$PLAN_BRAKE" "pass"
done
bash Tools/UE59_20261118/run2.sh Z_walk -6000 2000 92 0 "[('',2.0,0),('W',8.0,0),('',2.0,0)]" "pass"
bash Tools/UE59_20261118/run2.sh Z_jw2 -6000 2000 92 0 "[('',2.0,0),('W LeftShift',2.0,0),('W',8.0,0),('',2.0,0)]" "pass"
bash Tools/UE59_20261118/run2.sh Z_jw10 -6000 2000 92 0 "[('',2.0,0),('W LeftShift',10.0,0),('W',8.0,0),('',2.0,0)]" "pass"
TS="W J" bash Tools/UE59_20261119/seqH.sh final
unset VSIDE
echo "/Game/GraceRanger/Maps/L_GR_SphirusHouse" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
echo SEQZ_DONE
