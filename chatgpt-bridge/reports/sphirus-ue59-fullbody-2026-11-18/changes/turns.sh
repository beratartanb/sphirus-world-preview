#!/bin/bash
# turns.sh <suffix> [extra prelude] : flat test map, saved player, exact-angle flicks 45/90/135/180 L/R for walk, jog, sprint
# (hiprec + vid recorder, 60 Hz data step, side camera), then the stop/brake plans. TS="W J S STOP BRAKE" selects parts.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; P="$PWD"; S=$1; X=${2:-pass}; . Tools/UE59_20261116/plans.sh
echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$P/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
HR="exec(open(u.Paths.project_dir()+'Tools/UE59_20261116/hiprec.py',encoding='utf8').read())"
export VSIDE="(260,90,20,95,'pelvis')"
for g in ${TS:-W J S STOP BRAKE}; do case $g in
  W) bash Tools/UE59_20261118/run2.sh T_W_$S -6000 2000 92 0 "$PLAN_HIPW" "builtins.HR_LABEL='T_W_$S'; builtins.HR_TMAX=33.5; $X; $HR";;
  J) bash Tools/UE59_20261118/run2.sh T_J_$S -6000 2000 92 0 "$PLAN_HIPJ" "builtins.HR_LABEL='T_J_$S'; builtins.HR_TMAX=33.5; $X; $HR";;
  S) bash Tools/UE59_20261118/run2.sh T_S_$S -6000 2000 92 0 "$PLAN_HIPS" "builtins.HR_LABEL='T_S_$S'; builtins.HR_TMAX=33.5; $X; $HR";;
  STOP) bash Tools/UE59_20261118/run2.sh T_STOP_$S -6000 2000 92 0 "$PLAN_STOP" "$X";;
  BRAKE) bash Tools/UE59_20261118/run2.sh T_BRAKE_$S -6000 2000 92 0 "$PLAN_BRAKE" "$X";;
esac; done
echo "/Game/GraceRanger/Maps/L_GR_SphirusHouse" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$P/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
