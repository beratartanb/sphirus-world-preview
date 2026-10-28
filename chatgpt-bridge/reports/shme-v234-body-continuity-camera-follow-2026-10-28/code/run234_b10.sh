#!/bin/bash
# run234_b10.sh : V2.34 B10 build (release gap keeps the reversal family, exploration start gate) + candidate G suite.
#   editor A (fresh; reason: new DA fields + new component variables must be compiled into fresh classes): profiles + comp vars + save
#   editor B (fresh; reason: V2.30 rule - a function build after a vars build in the same editor ballooned to 94 GB): SHM_UpdateCameraV21
#   only, census (probe234_camfn: setters present, nodes > 1000) BEFORE any save, BP_GR_Player locomotion readers, smoke + behaviour check,
#   then the first broken case + sound counter-case (sprint hard right / walk right, gamepad profile).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V234_20261028; export O=$D/chain.out; source $D/lib234.sh; R=Tools/SHME_V2_20261014/run_v2.sh
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; T=Tools/SHME_V234_20261028; T3=Tools/SHME_V233_20261027; MD=$D/checkpoint/manifests
step() { echo "== $2 $(date +%T)" >> $O; out=$(env $3 bash $R "$1" "$2" 1500); echo "$out" > $D/last_$2.out; echo "$out" | head -1 >> $O; echo "$out" | grep -aE "GUARD|REFUSED|Traceback|FAIL|CAMFN234|LOCO234|SMD233|_lasthitby_patched" | head -5 | cut -c1-600 >> $O
  echo "$out" | head -1 | grep -qE "^OK" || { echo "B10_FAILED $2 $(date +%T)" >> $O; exit 1; }
  echo "$out" | grep -q "FAIL DSL\|BUILD_FUNCS_FAILED" && { echo "B10_FAILED $2 (build fail)" >> $O; exit 1; }; }
mani() { MSYS_NO_PATHCONV=1 "$PY" $T/manifest234.py "$@" >> $O 2>&1 || { echo "B10_FAILED manifest $1" >> $O; exit 1; }; }
until grep -aq "^B9_DONE\|^B9_FAILED" $O; do sleep 20; done
echo "B10 start $(date +%T) (reason: new component var SHM234_GapT needs a fresh editor; then camera + routing functions alone in a fresh editor)" >> $O
relaunch b10A 30
step $V21/revert_noquit.py revert SHME_KIND=control
mani locoF --assets /Game/GraceRanger/SHME/BP_SHM_ResponseProfile /Game/GraceRanger/SHME/BP_SHM_AnthropometryProfile /Game/GraceRanger/SHME/DA_SHM_Response_Default /Game/GraceRanger/SHME/DA_SHM_Anthropometry_Default /Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent /Game/GraceRanger/BP_GR_Player /Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player
step $V1/build_comp_vars.py comp_vars "SHME_KIND=write SHME_MANIFEST=$MD/locoF.json"
step $V2/save_comp.py save_comp "SHME_KIND=write SHME_MANIFEST=$MD/locoF.json"
step $T3/save_manifest_dirty.py smd "SHME_KIND=write SHME_MANIFEST=$MD/locoF.json"
relaunch b10B 30
step $V21/revert_noquit.py revert SHME_KIND=control
step $T/only234_camroute.py only SHME_KIND=control
step $V1/build_funcs.py funcs "SHME_KIND=write SHME_MANIFEST=$MD/locoF.json"
step $T/probe234_route.py census SHME_KIND=measure
grep -a "ROUTE234" $D/last_census.out | tail -1 | grep -q '"ok": true' || { echo "B10_FAILED census (functions incomplete - nothing saved)" >> $O; exit 1; }
step $V2/save_comp.py save_comp2 "SHME_KIND=write SHME_MANIFEST=$MD/locoF.json"
step $V2/only_all.py only_all SHME_KIND=control
step $T3/save_manifest_dirty.py smd2 "SHME_KIND=write SHME_MANIFEST=$MD/locoF.json"
echo "B10_BUILT $(date +%T)" >> $O
export WARM=1 MEMPROBE=1
J="j30_rel_3200:G:1 j30_rel_3450:G:1 j30_rel_3450:o:1 j30_slow:G:1 j34_chain1:G:1 jstart:G:1 jstart:o:1 wstart:G:1 wstart:o:1 c29_combo:G:1 e29_chain:G:1 e29_load:G:1 jback:G:1 wdiag:G:1 s29_swl12:G:1 cam_corr:Gp:1 cam_corr:op:1"
J="$J cam33_sturn:Gp:1 cam33_sturn:Goffp:1 cam33_wturn:Gp:1 cam33_wturn:Goffp:1 cam33_jturnj:Gp:1 cam33_jturnj:G:1 cam34_wflow:Gp:1 cam34_jlook:Gp:1 cam34_jcor:Gp:1 cam32_chain:Gp:1 cam32_wallturn:Gp:1 ins_ws:Gp:1 cam33_back:Gp:1 cam33_idlelook:Gp:1 cam34_wdrift:Gp:1 cam34_jrot:Gp:1"
ab b10 "$J" $D/vars234.sh
echo "B10_DONE $(date +%T)" >> $O
