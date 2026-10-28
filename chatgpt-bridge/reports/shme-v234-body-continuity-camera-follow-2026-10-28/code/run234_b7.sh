#!/bin/bash
# run234_b7.sh : V2.34 B7 (same editor as B6): ABP release-repress reversal-DB keep install + release-repress / reversal counter-case runs.
#   editor A (fresh; reason: new DA fields + new component variables must be compiled into fresh classes): profiles + comp vars + save
#   editor B (fresh; reason: V2.30 rule - a function build after a vars build in the same editor ballooned to 94 GB): SHM_UpdateCameraV21
#   only, census (probe234_camfn: setters present, nodes > 1000) BEFORE any save, BP_GR_Player locomotion readers, smoke + behaviour check,
#   then the first broken case + sound counter-case (sprint hard right / walk right, gamepad profile).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V234_20261028; export O=$D/chain.out; source $D/lib234.sh; R=Tools/SHME_V2_20261014/run_v2.sh
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; T=Tools/SHME_V234_20261028; T3=Tools/SHME_V233_20261027; MD=$D/checkpoint/manifests
step() { echo "== $2 $(date +%T)" >> $O; out=$(env $3 bash $R "$1" "$2" 1500); echo "$out" > $D/last_$2.out; echo "$out" | head -1 >> $O; echo "$out" | grep -aE "GUARD|REFUSED|Traceback|FAIL|CAMFN234|LOCO234|SMD233|_lasthitby_patched" | head -5 | cut -c1-600 >> $O
  echo "$out" | head -1 | grep -qE "^OK" || { echo "B7_FAILED $2 $(date +%T)" >> $O; exit 1; }
  echo "$out" | grep -q "FAIL DSL\|BUILD_FUNCS_FAILED" && { echo "B7_FAILED $2 (build fail)" >> $O; exit 1; }; }
mani() { MSYS_NO_PATHCONV=1 "$PY" $T/manifest234.py "$@" >> $O 2>&1 || { echo "B7_FAILED manifest $1" >> $O; exit 1; }; }
until grep -aq "^B6_DONE" $O; do sleep 20; done
echo "B7 start $(date +%T) (in-session BP edit, no relaunch)" >> $O
mani revkeep --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching
printf 'import builtins
builtins.V234_SAVE = True
exec(open(r"C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V234_20261028/install_v234_revkeep.py", encoding="utf8").read())
' > $D/req/revkeep_install.py
step $D/req/revkeep_install.py revkeep "SHME_KIND=write SHME_MANIFEST=$MD/revkeep.json"
grep -a "REVKEEP234" $D/last_revkeep.out | tail -1 | grep -q '"ok": true' || { echo "B7_FAILED revkeep install" >> $O; exit 1; }
echo "B7_BUILT $(date +%T)" >> $O
export WARM=1 MEMPROBE=1
J="j30_rel_3200:K:1 j30_rel_3200:KR:1 j30_rel_3200:o:1 j30_rel_3450:K:1 j30_rel_3450:o:1 j30_slow:K:1 jstart:K:1 jback:K:1 e29_chain:K:1 e29_load:K:1 c29_combo:K:1 j34_chain1:K:1 s29_swl12:K:1 wstart:K:1"
ab b7 "$J" $D/vars234.sh
echo "B7_DONE $(date +%T)" >> $O
