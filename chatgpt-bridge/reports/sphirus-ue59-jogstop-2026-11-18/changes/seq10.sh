#!/bin/bash
# seq10.sh: sprint-stop cost bias A/B (runtime remap to unsaved Sphirus test copies), on top of J2 (Relaxed run + walk stops unmapped).
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; . Tools/UE59_20261116/plans.sh
R=/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/Relaxed; T=/Game/Sphirus/Player/GASP/DB/Test
CMA="exec(open(u.Paths.project_dir()+'Tools/UE59_20261118/cm_add.py',encoding='utf8').read())"
mk(){ echo "builtins.CM_ADD={'$R/PSD_Relaxed_Stand_Run_Stops':'$R/PSD_Relaxed_Stand_Run_Stops','$R/PSD_Relaxed_Stand_Walk_Stops':'$R/PSD_Relaxed_Stand_Walk_Stops','$R/PSD_Relaxed_Stand_Sprint_Stops':'$T/PSD_Sph_R_Sprint_Stops_$1'}; $CMA"; }
echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
export VSIDE="(260,90,20,95,'pelvis')"
for b in ${BS:-B40 B15 B05}; do
  bash Tools/UE59_20261118/run2.sh T10_JSTOP_$b -6000 2000 92 0 "$(cat Saved/UE59Work/jstop_plan.txt)" "$(mk $b)"
  bash Tools/UE59_20261118/run2.sh T10_STOP_$b -6000 2000 92 0 "$PLAN_STOP" "$(mk $b)"
done
unset VSIDE
echo "/Game/GraceRanger/Maps/L_GR_SphirusHouse" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
echo SEQ10_DONE
