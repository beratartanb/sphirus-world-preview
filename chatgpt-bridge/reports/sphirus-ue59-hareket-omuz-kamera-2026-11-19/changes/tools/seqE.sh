#!/bin/bash
# seqE.sh: jog/sprint brake deceleration vs stop clip (runtime VID_MOTION BrakeDecelLow/High), jog-stop + stop plans, 60 Hz data.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; . Tools/UE59_20261116/plans.sh
echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
B0="builtins.VID_MOTION={}"; B1="builtins.VID_MOTION={'BrakeDecelLow':380.0,'BrakeDecelHigh':1000.0}"; B2="builtins.VID_MOTION={'BrakeDecelLow':500.0,'BrakeDecelHigh':1100.0}"
for c in ${CS:-B0 B1 B2}; do eval X=\$$c
  bash Tools/UE59_20261118/run2.sh E_JSTOP_$c -6000 2000 92 0 "$(cat Saved/UE59Work/jstop_plan.txt)" "import builtins; $X"
  bash Tools/UE59_20261118/run2.sh E_STOP_$c -6000 2000 92 0 "$PLAN_STOP" "import builtins; $X"
done
echo "/Game/GraceRanger/Maps/L_GR_SphirusHouse" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
echo SEQE_DONE
