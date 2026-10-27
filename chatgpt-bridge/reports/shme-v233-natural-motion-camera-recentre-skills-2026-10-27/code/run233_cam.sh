#!/bin/bash
# run233_cam.sh : V2.33 camera direction build (after C1C_DONE). Editor A (fresh, reason: DA fields + component vars): profiles + comp vars;
# editor B (fresh, V2.30 OOM rule): SHM_UpdateCameraV21 only + the BP installer (input frame latch + the control-yaw writer); smoke run.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V233_20261027; export O=$D/chain.out; source $D/lib233.sh; R=Tools/SHME_V2_20261014/run_v2.sh
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; T=Tools/SHME_V233_20261027; MD=Saved/Codex/SHME_V233_20261027/checkpoint/manifests
until grep -aq "C1C_DONE" $O; do sleep 20; done
step() { echo "== $2 $(date +%T)" >> $O; out=$(env $3 bash $R "$1" "$2" 1500); echo "$out" | head -1 >> $O; echo "$out" | grep -aE "GUARD|WRITE_GUARD|REFUSED|Traceback|FAIL|_lasthitby_patched|CAMREC233|UP_TO_DATE" | head -4 | cut -c1-400 >> $O
  echo "$out" | head -1 | grep -qE "^OK" || { echo "CAM_FAILED $2 $(date +%T)" >> $O; exit 1; }; }
mani() { MSYS_NO_PATHCONV=1 "$PY" $T/manifest233.py "$@" >> $O 2>&1 || { echo "CAM_FAILED manifest $1" >> $O; exit 1; }; }
echo "CAM start $(date +%T) (reason: profile fields + component vars need a fresh editor)" >> $O
relaunch camA 30
step $V21/revert_noquit.py revert SHME_KIND=control
mani camA --assets /Game/GraceRanger/SHME/BP_SHM_ResponseProfile /Game/GraceRanger/SHME/BP_SHM_AnthropometryProfile /Game/GraceRanger/SHME/DA_SHM_Response_Default /Game/GraceRanger/SHME/DA_SHM_Anthropometry_Default /Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent
step $V1/build_profiles.py profiles "SHME_KIND=write SHME_MANIFEST=$MD/camA.json"
step $V1/build_comp_vars.py comp_vars "SHME_KIND=write SHME_MANIFEST=$MD/camA.json"
step $V2/save_comp.py save_comp "SHME_KIND=write SHME_MANIFEST=$MD/camA.json"
relaunch camB 30
step $V21/revert_noquit.py revert SHME_KIND=control
step $T/only_v233cam.py only SHME_KIND=control
step $V1/build_funcs.py funcs "SHME_KIND=write SHME_MANIFEST=$MD/camA.json"
step $V2/save_comp.py save_comp2 "SHME_KIND=write SHME_MANIFEST=$MD/camA.json"
step $V2/only_all.py only_all SHME_KIND=control
mani camB --assets /Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/BP_ExampleCharacter_MotionMatching /Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/BP_Player_MM /Game/GraceRanger/BP_GR_Player /Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player
step $D/req/camrec_install.py camrec "SHME_KIND=write SHME_MANIFEST=$MD/camB.json"
echo "CAM_BUILT $(date +%T)" >> $O
( cd Tools/SHME_V212_20261017 && bash v212_run.sh v233camsmoke_c30_calm c30_calm '{}' ',"state_mode":"production"' 2>&1 | tail -1 ) >> $O
echo "CAM_SMOKE $(grep -o '"status": "[A-Z_]*"\|"bp_errors": [0-9]*\|"bp_error_first": [^,]*' Saved/Codex/SHME_V1_20260925/v233camsmoke_c30_calm_pie.json | tr '\n' ' ')" >> $O
echo "CAM_DONE $(date +%T)" >> $O
