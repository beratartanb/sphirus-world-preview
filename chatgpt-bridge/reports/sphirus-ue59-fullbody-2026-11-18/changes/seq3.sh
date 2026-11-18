#!/bin/bash
# seq3.sh: stop verification (saved state vs runtime old sprint-stop family) + light route path check (data only)
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"
OLD="builtins.CM_ADD={'/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/Relaxed/PSD_Relaxed_Stand_Sprint_Stops':'/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/Relaxed/PSD_Relaxed_Stand_Sprint_Stops'}; exec(open(u.Paths.project_dir()+'Tools/UE59_20261118/cm_add.py',encoding='utf8').read())"
echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
export VSIDE="(260,90,20,95,'pelvis')"
bash Tools/UE59_20261118/run2.sh T_JSTOP_new -6000 2000 92 0 "$(cat Saved/UE59Work/jstop_plan.txt)" "pass"
bash Tools/UE59_20261118/run2.sh T_JSTOP_old -6000 2000 92 0 "$(cat Saved/UE59Work/jstop_plan.txt)" "$OLD"
. Tools/UE59_20261116/plans.sh
bash Tools/UE59_20261118/run2.sh T_STOP_new -6000 2000 92 0 "$PLAN_STOP" "pass"
bash Tools/UE59_20261118/run2.sh T_BRAKE_new -6000 2000 92 0 "$PLAN_BRAKE" "pass"
unset VSIDE
echo "/Game/GraceRanger/Maps/L_GR_SphirusHouse" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
bash Tools/UE59_20261118/run2.sh L_route_check 397 100 241 -150 "$(cat Tools/UE59_20261118/light_route.txt)" "pass"
echo SEQ3_DONE
