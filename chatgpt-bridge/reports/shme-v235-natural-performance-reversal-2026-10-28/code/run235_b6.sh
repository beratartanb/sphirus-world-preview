#!/bin/bash
# run235_b6.sh : V2.35 B6 - DA field RevGapKeep (editor A, fresh: new profile field) + SHM_UpdateRouting (editor B, fresh, functions alone,
# census before save), then the release-repress / release-stop / chain tests at 30 and 60 FPS.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V235_20261028; export O=$D/chain.out; source $D/lib235.sh; R=Tools/SHME_V2_20261014/run_v2.sh
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; T=Tools/SHME_V235_20261028; T3=Tools/SHME_V233_20261027; MD=$D/checkpoint/manifests
step() { echo "== $2 $(date +%T)" >> $O; out=$(env $3 bash $R "$1" "$2" 1500); echo "$out" > $D/last_$2.out; echo "$out" | head -1 >> $O; echo "$out" | grep -aE "GUARD|REFUSED|Traceback|FAIL|ROUTE235" | head -5 | cut -c1-600 >> $O
  echo "$out" | head -1 | grep -qE "^OK" || { echo "B6_FAILED $2 $(date +%T)" >> $O; exit 1; }
  echo "$out" | grep -q "FAIL DSL\|BUILD_FUNCS_FAILED" && { echo "B6_FAILED $2 (build fail)" >> $O; exit 1; }; }
mani() { MSYS_NO_PATHCONV=1 "$PY" $T/manifest235.py "$@" >> $O 2>&1 || { echo "B6_FAILED manifest $1" >> $O; exit 1; }; }
until grep -aqE "^B5_DONE|^B5_FAILED" $O; do sleep 20; done
echo "B6 start $(date +%T) (reason: new DA field RevGapKeep -> fresh profile classes; routing function alone in a fresh editor)" >> $O
relaunch b6A 30
step $V21/revert_noquit.py revert SHME_KIND=control
mani route2 --assets /Game/GraceRanger/BP_GR_Player /Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player /Game/GraceRanger/SHME/BP_SHM_AnthropometryProfile /Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent /Game/GraceRanger/SHME/BP_SHM_ResponseProfile /Game/GraceRanger/SHME/DA_SHM_Anthropometry_Default /Game/GraceRanger/SHME/DA_SHM_Response_Default
step $V1/build_profiles.py profiles "SHME_KIND=write SHME_MANIFEST=$MD/route2.json"
step $T3/save_manifest_dirty.py smd "SHME_KIND=write SHME_MANIFEST=$MD/route2.json"
relaunch b6B 30
step $V21/revert_noquit.py revert SHME_KIND=control
step $T/only235_route.py only SHME_KIND=control
step $V1/build_funcs.py funcs "SHME_KIND=write SHME_MANIFEST=$MD/route2.json"
step $T/probe235_route.py census SHME_KIND=measure
grep -a "ROUTE235" $D/last_census.out | tail -1 | grep -q '"ok": true' || { echo "B6_FAILED census (nothing saved)" >> $O; exit 1; }
step $V2/save_comp.py save_comp "SHME_KIND=write SHME_MANIFEST=$MD/route2.json"
step $V2/only_all.py only_all SHME_KIND=control
step $T3/save_manifest_dirty.py smd2 "SHME_KIND=write SHME_MANIFEST=$MD/route2.json"
echo "B6_BUILT $(date +%T)" >> $O
export WARM=1
J="j30_rel_3200:rvRG2 j30_rel_3200:rvR j30_rel_3450:rvRG2 j35_relstop:rvRG2 j35_relstop:rvR j35_relstop:o j35_rev:rvRG2 j35_rev2:rvRG2 j30_slow:rvRG2 j34_chain1:rvRG2 e29_chain:rvRG2 e29_load:rvRG2 s29_swl12:rvRG2 jback:rvRG2 j30_rel_3200:rvRG2S j35_relstop:rvRG2S"
ab b6 "$J" $D/vars235_cap.sh
echo "B6_30_DONE $(date +%T)" >> $O
relaunch b6f60 60
ab b6f60 "j30_rel_3200:rvRG2 j30_rel_3200:oR j35_relstop:rvRG2 j35_rev:rvRG2 j34_chain1:rvRG2" $D/vars235.sh
echo "B6_DONE $(date +%T)" >> $O
