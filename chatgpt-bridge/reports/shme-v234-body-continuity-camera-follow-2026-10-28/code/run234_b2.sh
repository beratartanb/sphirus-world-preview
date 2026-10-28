#!/bin/bash
# run234_b2.sh : V2.34 B2 build (phase envelope, body-facing gate, real-turn side, walk follow rate, release hold) + the camera/input suite.
#   editor A (fresh; reason: new DA fields + new component variables must be compiled into fresh classes): profiles + comp vars + save
#   editor B (fresh; reason: V2.30 rule - a function build after a vars build in the same editor ballooned to 94 GB): SHM_UpdateCameraV21
#   only, census (probe234_camfn: setters present, nodes > 1000) BEFORE any save, BP_GR_Player locomotion readers, smoke + behaviour check,
#   then the first broken case + sound counter-case (sprint hard right / walk right, gamepad profile).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V234_20261028; export O=$D/chain.out; source $D/lib234.sh; R=Tools/SHME_V2_20261014/run_v2.sh
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; T=Tools/SHME_V234_20261028; T3=Tools/SHME_V233_20261027; MD=$D/checkpoint/manifests
step() { echo "== $2 $(date +%T)" >> $O; out=$(env $3 bash $R "$1" "$2" 1500); echo "$out" > $D/last_$2.out; echo "$out" | head -1 >> $O; echo "$out" | grep -aE "GUARD|REFUSED|Traceback|FAIL|CAMFN234|LOCO234|SMD233|_lasthitby_patched" | head -5 | cut -c1-600 >> $O
  echo "$out" | head -1 | grep -qE "^OK" || { echo "B2_FAILED $2 $(date +%T)" >> $O; exit 1; }
  echo "$out" | grep -q "FAIL DSL\|BUILD_FUNCS_FAILED" && { echo "B2_FAILED $2 (build fail)" >> $O; exit 1; }; }
mani() { MSYS_NO_PATHCONV=1 "$PY" $T/manifest234.py "$@" >> $O 2>&1 || { echo "B2_FAILED manifest $1" >> $O; exit 1; }; }
echo "B2 start $(date +%T) (reason: new DA fields CamEnv* / CamRecFaceMax / CamRecTurnSide / CamRecWalkRate + component vars CamEnv* need a fresh editor)" >> $O
relaunch b2A 30
step $V21/revert_noquit.py revert SHME_KIND=control
mani locoB --assets /Game/GraceRanger/SHME/BP_SHM_ResponseProfile /Game/GraceRanger/SHME/BP_SHM_AnthropometryProfile /Game/GraceRanger/SHME/DA_SHM_Response_Default /Game/GraceRanger/SHME/DA_SHM_Anthropometry_Default /Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent /Game/GraceRanger/BP_GR_Player /Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player
step $V1/build_profiles.py profiles "SHME_KIND=write SHME_MANIFEST=$MD/locoB.json"
step $V1/build_comp_vars.py comp_vars "SHME_KIND=write SHME_MANIFEST=$MD/locoB.json"
step $V2/save_comp.py save_comp "SHME_KIND=write SHME_MANIFEST=$MD/locoB.json"
step $T3/save_manifest_dirty.py smd "SHME_KIND=write SHME_MANIFEST=$MD/locoB.json"
echo "B2 editor B $(date +%T) (reason: function build alone in a fresh editor - V2.30 OOM rule)" >> $O
relaunch b2B 30
step $V21/revert_noquit.py revert SHME_KIND=control
step $T3/only_v233cam.py only SHME_KIND=control
step $V1/build_funcs.py funcs "SHME_KIND=write SHME_MANIFEST=$MD/locoB.json"
step $T/probe234_camfn.py census SHME_KIND=measure
grep -a "CAMFN234" $D/last_census.out | tail -1 | grep -q '"ok": true' || { echo "B2_FAILED census (function incomplete - nothing saved)" >> $O; exit 1; }
step $V2/save_comp.py save_comp2 "SHME_KIND=write SHME_MANIFEST=$MD/locoB.json"
step $V2/only_all.py only_all SHME_KIND=control
step $T3/save_manifest_dirty.py smd2 "SHME_KIND=write SHME_MANIFEST=$MD/locoB.json"
echo "B2_BUILT $(date +%T)" >> $O
export WARM=1 MEMPROBE=1
ab b2 "cam33_sturn:Cp:1" $D/vars234.sh
"$PY" $T/check234.py v234b2_cam33_sturn_Cp_r1 >> $O 2>&1
grep -a "CHECK234 v234b2_cam33_sturn_Cp_r1" $O | tail -1 | grep -q "state {0: [0-9]*, 1: [1-9]" || { echo "B2_FAILED behaviour NOT_TRIGGERED" >> $O; exit 1; }
J="cam33_sturn:op:1 cam33_sturn:Coffp:1 cam33_wturn:Cp:1 cam33_wturn:Coffp:1 cam33_jturnj:Cp:1 cam33_jturnj:Coffp:1 cam33_jturnj:C:1"
J="$J cam34_jlook:Cp:1 cam34_jlook:op:1 cam34_slook:Cp:1 cam34_jrot:Cp:1 cam34_jrot:Coffp:1 cam34_jcor:Cp:1 cam34_jcor:Coffp:1 cam34_wflow:Cp:1 cam34_wflow:Coffp:1 cam34_wflow:C:1 cam34_wflow:op:1"
J="$J cam34_wdrift:Cp:1 cam34_jrel:Cp:1 cam33_back:Cp:1 cam33_idlelook:Cp:1 cam32_wallturn:Cp:1 cam32_wallturn:op:1 cam32_wallturn:CnoEp:1 cam_corr:Cp:1 ins_ws:Cp:1"
J="$J e29_chain:Cp:1 e29_chain:op:1 cam32_chain:Cp:1 cam32_chain:op:1 cam32_chain:CnoEp:1 c29_combo:Cp:1 c29_combo:op:1 jback:Cp:1 jback:op:1"
ab b2 "$J" $D/vars234.sh
echo "B2_DONE $(date +%T)" >> $O
