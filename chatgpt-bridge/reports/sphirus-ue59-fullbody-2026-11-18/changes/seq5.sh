#!/bin/bash
# seq5.sh: frame-step sensitivity of the jog stop selection (saved state): JSTOP plan at 30 and 36 Hz data steps (60 Hz done in seq3)
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"
echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
export VSIDE="(260,90,20,95,'pelvis')"
DFPS=30.0 bash Tools/UE59_20261118/run2.sh T_JSTOP_30 -6000 2000 92 0 "$(cat Saved/UE59Work/jstop_plan.txt)" "pass"
DFPS=36.0 bash Tools/UE59_20261118/run2.sh T_JSTOP_36 -6000 2000 92 0 "$(cat Saved/UE59Work/jstop_plan.txt)" "pass"
echo SEQ5_DONE
