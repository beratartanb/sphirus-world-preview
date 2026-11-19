#!/bin/bash
# seqG.sh: saved-state verification after w_round20 (no runtime overrides), 60 Hz data + 30 Hz data step for the jog-stop plan.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; . Tools/UE59_20261116/plans.sh
echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
bash Tools/UE59_20261118/run2.sh G_JSTOP -6000 2000 92 0 "$(cat Saved/UE59Work/jstop_plan.txt)" "pass"
DFPS=30.0 bash Tools/UE59_20261118/run2.sh G_JSTOP30 -6000 2000 92 0 "$(cat Saved/UE59Work/jstop_plan.txt)" "pass"
bash Tools/UE59_20261118/run2.sh G_STOP -6000 2000 92 0 "$PLAN_STOP" "pass"
bash Tools/UE59_20261118/run2.sh G_BRAKE -6000 2000 92 0 "$PLAN_BRAKE" "pass"
bash Tools/UE59_20261118/run2.sh G_walk -6000 2000 92 0 "[('',2.0,0),('W',8.0,0),('',2.0,0)]" "pass"
bash Tools/UE59_20261118/run2.sh G_jw2 -6000 2000 92 0 "[('',2.0,0),('W LeftShift',2.0,0),('W',8.0,0),('',2.0,0)]" "pass"
bash Tools/UE59_20261118/run2.sh G_jw10 -6000 2000 92 0 "[('',2.0,0),('W LeftShift',10.0,0),('W',8.0,0),('',2.0,0)]" "pass"
echo "/Game/GraceRanger/Maps/L_GR_SphirusHouse" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
echo SEQG_DONE
