#!/bin/bash
# seq11.sh: stop speed bands of the Stand Idles chooser fitted to Sphirus gaits (walk 180 / jog 415 / sprint 585), runtime only.
# C1 = bands 200/440 with the saved remaps | C2 = C1 + Relaxed run/walk stops unmapped (J2). Chooser restored to 170/400 at the end.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; . Tools/UE59_20261116/plans.sh
R=/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/Relaxed
CMA="exec(open(u.Paths.project_dir()+'Tools/UE59_20261118/cm_add.py',encoding='utf8').read())"
CHS="exec(open(u.Paths.project_dir()+'Tools/UE59_20261118b/ch_set.py',encoding='utf8').read())"
J2="builtins.CM_ADD={'$R/PSD_Relaxed_Stand_Run_Stops':'$R/PSD_Relaxed_Stand_Run_Stops','$R/PSD_Relaxed_Stand_Walk_Stops':'$R/PSD_Relaxed_Stand_Walk_Stops'}; $CMA"
echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
export VSIDE="(260,90,20,95,'pelvis')"
for v in ${VARS:-C1 C2}; do case $v in
  C1) X="import builtins; builtins.CH_EDGES=(200,440); $CHS";;
  C2) X="import builtins; builtins.CH_EDGES=(200,440); $CHS; $J2";;
  C3) X="import builtins; builtins.CH_EDGES=(300,500); $CHS; $J2";; esac
  bash Tools/UE59_20261118/run2.sh T11_JSTOP_$v -6000 2000 92 0 "$(cat Saved/UE59Work/jstop_plan.txt)" "$X"
  bash Tools/UE59_20261118/run2.sh T11_STOP_$v -6000 2000 92 0 "$PLAN_STOP" "$X"
  bash Tools/UE59_20261118/run2.sh T11_BRAKE_$v -6000 2000 92 0 "$PLAN_BRAKE" "$X"
done
unset VSIDE
SHME_OWNER=emb SHME_KIND=measure bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/UE59_20261118b/ch_restore.py" emb_probe 60 2>&1 | grep CHSET
echo "/Game/GraceRanger/Maps/L_GR_SphirusHouse" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
echo SEQ11_DONE
