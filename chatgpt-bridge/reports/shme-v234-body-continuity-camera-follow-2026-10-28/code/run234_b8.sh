#!/bin/bash
# run234_b8.sh : V2.34 B8 camera function build (exploration only >= 0.5 s into the normal family) + stop closing-step dry run + combined candidate F suite.
#   editor A (fresh; reason: new DA fields + new component variables must be compiled into fresh classes): profiles + comp vars + save
#   editor B (fresh; reason: V2.30 rule - a function build after a vars build in the same editor ballooned to 94 GB): SHM_UpdateCameraV21
#   only, census (probe234_camfn: setters present, nodes > 1000) BEFORE any save, BP_GR_Player locomotion readers, smoke + behaviour check,
#   then the first broken case + sound counter-case (sprint hard right / walk right, gamepad profile).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V234_20261028; export O=$D/chain.out; source $D/lib234.sh; R=Tools/SHME_V2_20261014/run_v2.sh
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; T=Tools/SHME_V234_20261028; T3=Tools/SHME_V233_20261027; MD=$D/checkpoint/manifests
step() { echo "== $2 $(date +%T)" >> $O; out=$(env $3 bash $R "$1" "$2" 1500); echo "$out" > $D/last_$2.out; echo "$out" | head -1 >> $O; echo "$out" | grep -aE "GUARD|REFUSED|Traceback|FAIL|CAMFN234|LOCO234|SMD233|_lasthitby_patched" | head -5 | cut -c1-600 >> $O
  echo "$out" | head -1 | grep -qE "^OK" || { echo "B8_FAILED $2 $(date +%T)" >> $O; exit 1; }
  echo "$out" | grep -q "FAIL DSL\|BUILD_FUNCS_FAILED" && { echo "B8_FAILED $2 (build fail)" >> $O; exit 1; }; }
mani() { MSYS_NO_PATHCONV=1 "$PY" $T/manifest234.py "$@" >> $O 2>&1 || { echo "B8_FAILED manifest $1" >> $O; exit 1; }; }
echo "B8 start $(date +%T) (reason: camera function change; fresh editor - function build after ~100 PIE runs, V2.30 memory rule)" >> $O
relaunch b8 30
step $V21/revert_noquit.py revert SHME_KIND=control
mani locoE --assets /Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent /Game/GraceRanger/BP_GR_Player /Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player
step $T3/only_v233cam.py only SHME_KIND=control
step $V1/build_funcs.py funcs "SHME_KIND=write SHME_MANIFEST=$MD/locoE.json"
step $T/probe234_route.py census SHME_KIND=measure
grep -a "ROUTE234" $D/last_census.out | tail -1 | grep -q '"ok": true' || { echo "B8_FAILED census (functions incomplete - nothing saved)" >> $O; exit 1; }
step $V2/save_comp.py save_comp2 "SHME_KIND=write SHME_MANIFEST=$MD/locoE.json"
step $V2/only_all.py only_all SHME_KIND=control
step $T3/save_manifest_dirty.py smd2 "SHME_KIND=write SHME_MANIFEST=$MD/locoE.json"
echo "B8_BUILT $(date +%T)" >> $O
step $D/req/sc_dry.py sc_dry SHME_KIND=measure
export WARM=1 MEMPROBE=1
J="j30_rel_3200:F:1 j30_rel_3450:F:1 j30_rel_3450:o:1 j30_slow:F:1 j34_chain1:F:1 jstart:F:1 jstart:o:1 wstart:F:1 c29_combo:F:1 c29_combo:o:1 e29_chain:F:1 e29_load:F:1 jback:F:1 wdiag:F:1 wdiag:o:1 s29_swl12:F:1"
J="$J cam33_sturn:Fp:1 cam33_sturn:Foffp:1 cam33_wturn:Fp:1 cam33_wturn:Foffp:1 cam33_jturnj:Fp:1 cam33_jturnj:F:1 cam34_wflow:Fp:1 cam34_jlook:Fp:1 cam34_jcor:Fp:1 cam32_chain:Fp:1 cam32_wallturn:Fp:1 cam_corr:Fp:1 ins_ws:Fp:1 cam33_back:Fp:1 cam33_idlelook:Fp:1 map_r1:Fp:1 map_r1:op:1"
ab b8 "$J" $D/vars234.sh
echo "B8_DONE $(date +%T)" >> $O
