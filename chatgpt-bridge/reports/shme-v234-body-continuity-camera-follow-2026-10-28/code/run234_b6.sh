#!/bin/bash
# run234_b6.sh : V2.34 B6 function build (exploration starts only in calm normal travel) + candidate C3 suite, real 180 vs back travel, stop clip source probe.
#   editor A (fresh; reason: new DA fields + new component variables must be compiled into fresh classes): profiles + comp vars + save
#   editor B (fresh; reason: V2.30 rule - a function build after a vars build in the same editor ballooned to 94 GB): SHM_UpdateCameraV21
#   only, census (probe234_camfn: setters present, nodes > 1000) BEFORE any save, BP_GR_Player locomotion readers, smoke + behaviour check,
#   then the first broken case + sound counter-case (sprint hard right / walk right, gamepad profile).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V234_20261028; export O=$D/chain.out; source $D/lib234.sh; R=Tools/SHME_V2_20261014/run_v2.sh
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; T=Tools/SHME_V234_20261028; T3=Tools/SHME_V233_20261027; MD=$D/checkpoint/manifests
step() { echo "== $2 $(date +%T)" >> $O; out=$(env $3 bash $R "$1" "$2" 1500); echo "$out" > $D/last_$2.out; echo "$out" | head -1 >> $O; echo "$out" | grep -aE "GUARD|REFUSED|Traceback|FAIL|CAMFN234|LOCO234|SMD233|_lasthitby_patched" | head -5 | cut -c1-600 >> $O
  echo "$out" | head -1 | grep -qE "^OK" || { echo "B6_FAILED $2 $(date +%T)" >> $O; exit 1; }
  echo "$out" | grep -q "FAIL DSL\|BUILD_FUNCS_FAILED" && { echo "B6_FAILED $2 (build fail)" >> $O; exit 1; }; }
mani() { MSYS_NO_PATHCONV=1 "$PY" $T/manifest234.py "$@" >> $O 2>&1 || { echo "B6_FAILED manifest $1" >> $O; exit 1; }; }
until grep -aq "^B5_DONE" $O; do sleep 20; done
echo "B6 start $(date +%T) (reason: function-only change; fresh editor because a function build after ~70 PIE runs risks the V2.30 memory balloon)" >> $O
relaunch b6 30
step $V21/revert_noquit.py revert SHME_KIND=control
mani locoD --assets /Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent /Game/GraceRanger/BP_GR_Player /Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player
step $T/only234_camroute.py only SHME_KIND=control
step $V1/build_funcs.py funcs "SHME_KIND=write SHME_MANIFEST=$MD/locoD.json"
step $T/probe234_route.py census SHME_KIND=measure
grep -a "ROUTE234" $D/last_census.out | tail -1 | grep -q '"ok": true' || { echo "B6_FAILED census (functions incomplete - nothing saved)" >> $O; exit 1; }
step $V2/save_comp.py save_comp2 "SHME_KIND=write SHME_MANIFEST=$MD/locoD.json"
step $V2/only_all.py only_all SHME_KIND=control
step $T3/save_manifest_dirty.py smd2 "SHME_KIND=write SHME_MANIFEST=$MD/locoD.json"
echo "B6_BUILT $(date +%T)" >> $O
step $T/clipstop234.py clipstop SHME_KIND=measure
grep -a -o "CLIPSTOP234 {.*" $D/last_clipstop.out > $D/clipstop234.json
export WARM=1 MEMPROBE=1
J="cam33_sturn:C3p:1 cam33_sturn:C3offp:1 cam33_wturn:C3p:1 cam33_wturn:C3offp:1 cam33_jturnj:C3p:1 cam34_jcor:C3p:1 cam34_wflow:C3p:1 cam34_jlook:C3p:1"
J="$J c29_combo:C3p:1 c29_combo:op:1 e29_chain:C3p:1 e29_chain:op:1 jstart:C3p:1 jstart:op:1 wstart:C3p:1 wstart:op:1 cam32_chain:C3p:1 jback:C3p:1 wdiag:C3p:1 wdiag:op:1"
J="$J s34_s180:C3p:1 s34_s180:op:1 j34_back180:C3p:1 j34_back180:op:1 e29_load:C3p:1 e29_load:op:1 s29_swl12:C3p:1 s29_swl12:op:1"
ab b6 "$J" $D/vars234.sh
echo "B6_DONE $(date +%T)" >> $O
