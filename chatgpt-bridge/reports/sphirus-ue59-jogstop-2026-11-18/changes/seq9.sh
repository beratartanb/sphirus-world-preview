#!/bin/bash
# seq9.sh: jog-stop root cause test (runtime only, no asset write). The Relaxed run stops (375 cm/s, ~625 cm/s2, like the PhysBrake
# jog brake) are remapped to the abrupt Dense run stops (~1650 cm/s2); the only gentle stop left is the Relaxed sprint stop.
# J0 saved state | J1 Relaxed run stops unmapped | J2 J1 + Relaxed walk stops unmapped. Jog-stop plan, then stop/brake plans for J0/J2.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; . Tools/UE59_20261116/plans.sh
R=/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/Relaxed
CMA="exec(open(u.Paths.project_dir()+'Tools/UE59_20261118/cm_add.py',encoding='utf8').read())"
J1="builtins.CM_ADD={'$R/PSD_Relaxed_Stand_Run_Stops':'$R/PSD_Relaxed_Stand_Run_Stops'}; $CMA"
J2="builtins.CM_ADD={'$R/PSD_Relaxed_Stand_Run_Stops':'$R/PSD_Relaxed_Stand_Run_Stops','$R/PSD_Relaxed_Stand_Walk_Stops':'$R/PSD_Relaxed_Stand_Walk_Stops'}; $CMA"
echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
export VSIDE="(260,90,20,95,'pelvis')"
for v in ${VARS:-J0 J1 J2}; do case $v in J0) X=pass;; J1) X="$J1";; J2) X="$J2";; esac
  bash Tools/UE59_20261118/run2.sh T9_JSTOP_$v -6000 2000 92 0 "$(cat Saved/UE59Work/jstop_plan.txt)" "$X"
done
for v in ${SVARS:-J0 J2}; do case $v in J0) X=pass;; J1) X="$J1";; J2) X="$J2";; esac
  bash Tools/UE59_20261118/run2.sh T9_STOP_$v -6000 2000 92 0 "$PLAN_STOP" "$X"
  bash Tools/UE59_20261118/run2.sh T9_BRAKE_$v -6000 2000 92 0 "$PLAN_BRAKE" "$X"
done
unset VSIDE
echo "/Game/GraceRanger/Maps/L_GR_SphirusHouse" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
echo SEQ9_DONE
