#!/bin/bash
# run233_cam4.sh : V2.33 recentre fix (pure-bind order + stored look timer) - editor A (fresh: new component var) comp vars; editor B (fresh,
# funcs alone) SHM_UpdateCameraV21 + census + smoke + the two recentre diagnosis runs.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V233_20261027; export O=$D/chain.out; source $D/lib233.sh; R=Tools/SHME_V2_20261014/run_v2.sh
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; T=Tools/SHME_V233_20261027; MD=Saved/Codex/SHME_V233_20261027/checkpoint/manifests
step() { echo "== $2 $(date +%T)" >> $O; out=$(env $3 bash $R "$1" "$2" 1500); echo "$out" | head -1 >> $O; echo "$out" | grep -aE "GUARD|REFUSED|Traceback|FAIL|CAMFN233|CAMDEV233" | head -4 | cut -c1-400 >> $O
  echo "$out" | head -1 | grep -qE "^OK" || { echo "CAM5_FAILED $2 $(date +%T)" >> $O; exit 1; }; echo "$out" | grep -q "FAIL DSL\|BUILD_FUNCS_FAILED" && { echo "CAM5_FAILED $2 (build fail)" >> $O; exit 1; }; }
echo "CAM5 start $(date +%T) (reason: new component var CamRecScale (device profile inside the component) + function rebuild)" >> $O
relaunch camG 30
step $V21/revert_noquit.py revert SHME_KIND=control
step $V1/build_comp_vars.py comp_vars "SHME_KIND=write SHME_MANIFEST=$MD/camA2.json"
step $V2/save_comp.py save_comp "SHME_KIND=write SHME_MANIFEST=$MD/camA2.json"
step $T/save_manifest_dirty.py smd "SHME_KIND=write SHME_MANIFEST=$MD/camA2.json"
relaunch camH 30
step $V21/revert_noquit.py revert SHME_KIND=control
step $T/only_v233cam.py only SHME_KIND=control
step $V1/build_funcs.py funcs "SHME_KIND=write SHME_MANIFEST=$MD/camA2.json"
step $T/probe233_camfn.py census SHME_KIND=measure
grep -a "CAMFN233" $O | tail -1 | grep -q '"CamOrbit": [1-9]' || { echo "CAM5_FAILED census" >> $O; exit 1; }
step $V2/save_comp.py save_comp2 "SHME_KIND=write SHME_MANIFEST=$MD/camA2.json"
step $V2/only_all.py only_all SHME_KIND=control
step $D/req/camdev_install.py camdev "SHME_KIND=write SHME_MANIFEST=$MD/camB.json"
grep -a "CAMDEV233" $O | tail -1 | grep -q '"ok": true' || { echo "CAM5_FAILED camdev" >> $O; exit 1; }
cd Tools/SHME_V212_20261017
bash v212_run.sh v233kdev2_cam33_wturn_mouse cam33_wturn '{"CamRecEnabled":true}' ',"state_mode":"candidate"' 2>&1 | tail -1 >> ../../$O
bash v212_run.sh v233kdev2_cam33_wturn_pad cam33_wturn '{"CamRecEnabled":true}' ',"state_mode":"candidate","pawn_flags":{"GR233_RecMouseScale":1.0}' 2>&1 | tail -1 >> ../../$O
cd ../..
"$PY" $T/rec233.py v233kdev2_cam33_wturn_mouse v233kdev2_cam33_wturn_pad >> $O 2>&1
echo "CAM5_DONE $(date +%T)" >> $O
