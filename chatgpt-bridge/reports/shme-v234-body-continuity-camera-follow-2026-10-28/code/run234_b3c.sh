#!/bin/bash
# run234_b3.sh : V2.34 B3 build (release-repress keep in SHM_UpdateRouting) + chain 1 / release-repress runs + sprint upper-body owner isolation + clip source stage.
#   editor A (fresh; reason: new DA fields + new component variables must be compiled into fresh classes): profiles + comp vars + save
#   editor B (fresh; reason: V2.30 rule - a function build after a vars build in the same editor ballooned to 94 GB): SHM_UpdateCameraV21
#   only, census (probe234_camfn: setters present, nodes > 1000) BEFORE any save, BP_GR_Player locomotion readers, smoke + behaviour check,
#   then the first broken case + sound counter-case (sprint hard right / walk right, gamepad profile).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V234_20261028; export O=$D/chain.out; source $D/lib234.sh; R=Tools/SHME_V2_20261014/run_v2.sh
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; T=Tools/SHME_V234_20261028; T3=Tools/SHME_V233_20261027; MD=$D/checkpoint/manifests
step() { echo "== $2 $(date +%T)" >> $O; out=$(env $3 bash $R "$1" "$2" 1500); echo "$out" > $D/last_$2.out; echo "$out" | head -1 >> $O; echo "$out" | grep -aE "GUARD|REFUSED|Traceback|FAIL|CAMFN234|LOCO234|SMD233|_lasthitby_patched" | head -5 | cut -c1-600 >> $O
  echo "$out" | head -1 | grep -qE "^OK" || { echo "B3_FAILED $2 $(date +%T)" >> $O; exit 1; }
  echo "$out" | grep -q "FAIL DSL\|BUILD_FUNCS_FAILED" && { echo "B3_FAILED $2 (build fail)" >> $O; exit 1; }; }
mani() { MSYS_NO_PATHCONV=1 "$PY" $T/manifest234.py "$@" >> $O 2>&1 || { echo "B3_FAILED manifest $1" >> $O; exit 1; }; }
echo "B3c start $(date +%T) (continuation in the same editor: the census demanded exactly one FamilyTime setter; the source writes it twice by design - functions complete, not yet saved)" >> $O
step $T/probe234_route.py census SHME_KIND=measure
grep -a "ROUTE234" $D/last_census.out | tail -1 | grep -q '"ok": true' || { echo "B3_FAILED census (functions incomplete - nothing saved)" >> $O; exit 1; }
step $V2/save_comp.py save_comp2 "SHME_KIND=write SHME_MANIFEST=$MD/locoC.json"
step $V2/only_all.py only_all SHME_KIND=control
step $T3/save_manifest_dirty.py smd2 "SHME_KIND=write SHME_MANIFEST=$MD/locoC.json"
echo "B3_BUILT $(date +%T)" >> $O
step $T/clipstage234.py clipstage SHME_KIND=measure
grep -a -o "CLIPSTAGE234 {.*" $D/last_clipstage.out > $D/clipstage234.json
export WARM=1 MEMPROBE=1
J="j30_rel_3200:o:1 j30_rel_3200:Ro:1 j30_rel_3450:o:1 j30_rel_3450:Ro:1 j30_slow:o:1 j30_slow:Ro:1 jstart:Ro:1 wstart:Ro:1 jback:Ro:1 j34_sbcancel:o:1 j34_chain1:o:1 j34_chain1:Ro:1 j34_chain1:R:1"
J="$J d_sprint:o:1 d_sprint:sc:1 d_sprint:scPBI:1 d_sprint:scSS:1 d_sprint:scCL:1 d_sprint:scAPA:1 d_sprint:scFP:1 d_sprint:scALL:1"
ab b3 "$J" $D/vars234.sh
"$PY" $T/check234.py v234b3_j30_rel_3200_Ro_r1 >> $O 2>&1
echo "B3_DONE $(date +%T)" >> $O
