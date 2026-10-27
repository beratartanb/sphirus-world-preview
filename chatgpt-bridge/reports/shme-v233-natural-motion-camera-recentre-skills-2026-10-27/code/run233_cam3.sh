#!/bin/bash
# run233_cam2.sh : V2.33 REPAIR - SHM_UpdateCameraV21 was saved EMPTY at 14:47 (its DSL build failed; the chain only checked the job status).
# Fresh editor (reason: second funcs build), rebuild with the fixed DSL, node census, smoke. build_funcs.py now raises on any FAIL.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V233_20261027; export O=$D/chain.out; source $D/lib233.sh; R=Tools/SHME_V2_20261014/run_v2.sh
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; T=Tools/SHME_V233_20261027; MD=Saved/Codex/SHME_V233_20261027/checkpoint/manifests
step() { echo "== $2 $(date +%T)" >> $O; out=$(env $3 bash $R "$1" "$2" 1500); echo "$out" | head -1 >> $O; echo "$out" | grep -aE "GUARD|REFUSED|Traceback|FAIL|_lasthitby|CAMFN233" | head -4 | cut -c1-400 >> $O
  echo "$out" | head -1 | grep -qE "^OK" || { echo "CAM3_FAILED $2 $(date +%T)" >> $O; exit 1; }; echo "$out" | grep -q "FAIL DSL\|BUILD_FUNCS_FAILED" && { echo "CAM3_FAILED $2 (build fail)" >> $O; exit 1; }; }
echo "CAM3 start $(date +%T) (reason: recentre self-inhibition fix (look gate minus own delta), funcs build = fresh editor)" >> $O
relaunch camD 30
step $V21/revert_noquit.py revert SHME_KIND=control
step $T/only_v233cam.py only SHME_KIND=control
step $V1/build_funcs.py funcs "SHME_KIND=write SHME_MANIFEST=$MD/camA.json"
step $T/probe233_camfn.py census SHME_KIND=measure
grep -a "CAMFN233" $O | tail -1 | grep -q '"CamOrbit": [1-9]' || { echo "CAM3_FAILED census (orbit nodes missing)" >> $O; exit 1; }
step $V2/save_comp.py save_comp "SHME_KIND=write SHME_MANIFEST=$MD/camA.json"
step $V2/only_all.py only_all SHME_KIND=control
( cd Tools/SHME_V212_20261017 && bash v212_run.sh v233camsmoke3_cam32_s90 cam32_s90 '{}' ',"state_mode":"production"' 2>&1 | tail -1 ) >> $O
echo "CAM3_SMOKE $(grep -o '"status": "[A-Z_]*"\|"bp_errors": [0-9]*' Saved/Codex/SHME_V1_20260925/v233camsmoke3_cam32_s90_pie.json | tr '\n' ' ')" >> $O
echo "CAM3_DONE $(date +%T)" >> $O
