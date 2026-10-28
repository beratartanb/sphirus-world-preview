#!/bin/bash
# run234_b1.sh : V2.34 locomotion frame build + first decision runs.
#   editor A (fresh; reason: new DA fields + new component variables must be compiled into fresh classes): profiles + comp vars + save
#   editor B (fresh; reason: V2.30 rule - a function build after a vars build in the same editor ballooned to 94 GB): SHM_UpdateCameraV21
#   only, census (probe234_camfn: setters present, nodes > 1000) BEFORE any save, BP_GR_Player locomotion readers, smoke + behaviour check,
#   then the first broken case + sound counter-case (sprint hard right / walk right, gamepad profile).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V234_20261028; export O=$D/chain.out; source $D/lib234.sh; R=Tools/SHME_V2_20261014/run_v2.sh
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; T=Tools/SHME_V234_20261028; T3=Tools/SHME_V233_20261027; MD=$D/checkpoint/manifests
step() { echo "== $2 $(date +%T)" >> $O; out=$(env $3 bash $R "$1" "$2" 1500); echo "$out" > $D/last_$2.out; echo "$out" | head -1 >> $O; echo "$out" | grep -aE "GUARD|REFUSED|Traceback|FAIL|CAMFN234|LOCO234|SMD233|_lasthitby_patched" | head -5 | cut -c1-600 >> $O
  echo "$out" | head -1 | grep -qE "^OK" || { echo "B1_FAILED $2 $(date +%T)" >> $O; exit 1; }
  echo "$out" | grep -q "FAIL DSL\|BUILD_FUNCS_FAILED" && { echo "B1_FAILED $2 (build fail)" >> $O; exit 1; }; }
mani() { MSYS_NO_PATHCONV=1 "$PY" $T/manifest234.py "$@" >> $O 2>&1 || { echo "B1_FAILED manifest $1" >> $O; exit 1; }; }
echo "B1c start $(date +%T) (continuation: the install check read a 600-char truncated line; LOCO234 ok/saved in the job output)" >> $O
step $T3/save_manifest_dirty.py smd2 "SHME_KIND=write SHME_MANIFEST=$MD/locoA.json"
echo "B1_BUILT $(date +%T)" >> $O
# smoke (production must be unchanged: knobs off) + behaviour check (knob on: the new state must really change)
export WARM=1 MEMPROBE=1
ab b1 "cam33_sturn:o:1 cam33_sturn:Lxp:1" $D/vars234.sh
"$PY" $T/check234.py v234b1_cam33_sturn_o_r1 v234b1_cam33_sturn_Lxp_r1 >> $O 2>&1
grep -a "CHECK234 v234b1_cam33_sturn_Lxp_r1" $O | tail -1 | grep -q "state {0: [0-9]*, 1: [1-9]" || { echo "B1_FAILED behaviour: exploration never active (NOT_TRIGGERED)" >> $O; exit 1; }
# first decision set: broken case (production camera turns the body / speed) vs counter-case (camera off), and the new frame
ab b1 "cam33_sturn:op:1 cam33_sturn:ooffp:1 cam33_sturn:Lp:1 cam33_sturn:LxWp:1 cam33_sturn:LxWoffp:1 cam33_wturn:oWp:1 cam33_wturn:ooffp:1 cam33_wturn:LxWp:1 cam33_wturn:LxWoffp:1" $D/vars234.sh
echo "B1_DONE $(date +%T)" >> $O
