#!/bin/bash
# run233_cam4.sh : V2.33 recentre fix (pure-bind order + stored look timer) - editor A (fresh: new component var) comp vars; editor B (fresh,
# funcs alone) SHM_UpdateCameraV21 + census + smoke + the two recentre diagnosis runs.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V233_20261027; export O=$D/chain.out; source $D/lib233.sh; R=Tools/SHME_V2_20261014/run_v2.sh
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; T=Tools/SHME_V233_20261027; MD=Saved/Codex/SHME_V233_20261027/checkpoint/manifests
step() { echo "== $2 $(date +%T)" >> $O; out=$(env $3 bash $R "$1" "$2" 1500); echo "$out" | head -1 >> $O; echo "$out" | grep -aE "GUARD|REFUSED|Traceback|FAIL|CAMFN233" | head -4 | cut -c1-400 >> $O
  echo "$out" | head -1 | grep -qE "^OK" || { echo "CAM4_FAILED $2 $(date +%T)" >> $O; exit 1; }; echo "$out" | grep -q "FAIL DSL\|BUILD_FUNCS_FAILED" && { echo "CAM4_FAILED $2 (build fail)" >> $O; exit 1; }; }
echo "CAM4 start $(date +%T) (reason: new component var MoveLatchStateN + function rebuild)" >> $O
relaunch camE 30
step $V21/revert_noquit.py revert SHME_KIND=control
step $V1/build_comp_vars.py comp_vars "SHME_KIND=write SHME_MANIFEST=$MD/camA.json"
step $V2/save_comp.py save_comp "SHME_KIND=write SHME_MANIFEST=$MD/camA.json"
relaunch camF 30
step $V21/revert_noquit.py revert SHME_KIND=control
step $T/only_v233cam.py only SHME_KIND=control
step $V1/build_funcs.py funcs "SHME_KIND=write SHME_MANIFEST=$MD/camA.json"
step $T/probe233_camfn.py census SHME_KIND=measure
grep -a "CAMFN233" $O | tail -1 | grep -q '"CamOrbit": [1-9]' || { echo "CAM4_FAILED census" >> $O; exit 1; }
step $V2/save_comp.py save_comp2 "SHME_KIND=write SHME_MANIFEST=$MD/camA.json"
step $V2/only_all.py only_all SHME_KIND=control
cd Tools/SHME_V212_20261017
for s in cam33_wturn cam33_wturn_w; do bash v212_run.sh v233kdiag4_$s $s '{"CamRecEnabled":true}' ',"state_mode":"candidate","cvars":["CamRecVel","CamRecDelta","CamRecState","MoveLatchState","MoveLatchYaw"]' 2>&1 | tail -1 >> ../../$O; done
cd ../..
"$PY" $T/rec233.py v233kdiag4_cam33_wturn v233kdiag4_cam33_wturn_w >> $O 2>&1
echo "CAM4_DONE $(date +%T)" >> $O
