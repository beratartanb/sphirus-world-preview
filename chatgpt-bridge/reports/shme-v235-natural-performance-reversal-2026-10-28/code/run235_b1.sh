#!/bin/bash
# run235_b1.sh : V2.35 B1 - (1) quit the editor and restore the V2.34 jog stop clip from the stop1 manifest backup (the stop generator must
# start from the V2.34 content; a loaded .uasset cannot be replaced) ; (2) editor A (fresh; reason: new DA field RevOverHard -> fresh profile
# classes): profiles + save ; (3) editor B (fresh; reason: V2.30 rule, functions alone): SHM_UpdateRouting only, census before save ;
# (4) same editor: stop re-plan r2 (trunk remap, apex 15) under manifest stop2 ; (5) tests: release-repress + stop + chain.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V235_20261028; export O=$D/chain.out; source $D/lib235.sh; R=Tools/SHME_V2_20261014/run_v2.sh
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; T=Tools/SHME_V235_20261028; T3=Tools/SHME_V233_20261027; MD=$D/checkpoint/manifests
step() { echo "== $2 $(date +%T)" >> $O; out=$(env $3 bash $R "$1" "$2" 1500); echo "$out" > $D/last_$2.out; echo "$out" | head -1 >> $O; echo "$out" | grep -aE "GUARD|REFUSED|Traceback|FAIL|ROUTE235|G235S" | head -5 | cut -c1-600 >> $O
  echo "$out" | head -1 | grep -qE "^OK" || { echo "B1_FAILED $2 $(date +%T)" >> $O; exit 1; }
  echo "$out" | grep -q "FAIL DSL\|BUILD_FUNCS_FAILED" && { echo "B1_FAILED $2 (build fail)" >> $O; exit 1; }; }
mani() { MSYS_NO_PATHCONV=1 "$PY" $T/manifest235.py "$@" >> $O 2>&1 || { echo "B1_FAILED manifest $1" >> $O; exit 1; }; }
echo "B1 start $(date +%T)" >> $O
export LR_LOG=$(basename "$(ls -t Saved/Logs/*.log | grep -v -i cef | head -1)")
bash $R Tools/SHME_V21_20261014/revert_quit.py rq_b1 300 | grep -E "dirty after|QUIT|REFUSED" >> $O
for i in $(seq 1 90); do tasklist 2>/dev/null | grep -qi UnrealEditor.exe || break; sleep 2; done
tasklist 2>/dev/null | grep -qi UnrealEditor.exe && { echo "B1_FAILED editor did not quit" >> $O; exit 1; }
BK=$D/checkpoint/manifests/stop1/Content/GraceRanger/SHME/Animations/Stops/SHM_A_CP2_Jog_Fwd_Stop.uasset; DST=Content/GraceRanger/SHME/Animations/Stops/SHM_A_CP2_Jog_Fwd_Stop.uasset
cp "$BK" "$DST" && [ "$(sha1sum < "$DST" | cut -c1-40)" = "1323d4cf743b401ea9a69a5377cb73f932197a01" ] && echo "RESTORED stop1 $(date +%T)" >> $O || { echo "B1_FAILED restore" >> $O; exit 1; }
relaunch b1A 30
step $V21/revert_noquit.py revert SHME_KIND=control
mani route1 --assets /Game/GraceRanger/BP_GR_Player /Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player /Game/GraceRanger/SHME/BP_SHM_AnthropometryProfile /Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent /Game/GraceRanger/SHME/BP_SHM_ResponseProfile /Game/GraceRanger/SHME/DA_SHM_Anthropometry_Default /Game/GraceRanger/SHME/DA_SHM_Response_Default
step $V1/build_profiles.py profiles "SHME_KIND=write SHME_MANIFEST=$MD/route1.json"
step $T3/save_manifest_dirty.py smd "SHME_KIND=write SHME_MANIFEST=$MD/route1.json"
relaunch b1B 30
step $V21/revert_noquit.py revert SHME_KIND=control
step $T/only235_route.py only SHME_KIND=control
step $V1/build_funcs.py funcs "SHME_KIND=write SHME_MANIFEST=$MD/route1.json"
step $T/probe235_route.py census SHME_KIND=measure
grep -a "ROUTE235" $D/last_census.out | tail -1 | grep -q '"ok": true' || { echo "B1_FAILED census (nothing saved)" >> $O; exit 1; }
step $V2/save_comp.py save_comp "SHME_KIND=write SHME_MANIFEST=$MD/route1.json"
step $V2/only_all.py only_all SHME_KIND=control
step $T3/save_manifest_dirty.py smd2 "SHME_KIND=write SHME_MANIFEST=$MD/route1.json"
echo "B1_BUILT $(date +%T)" >> $O
mani stop2 --assets /Game/GraceRanger/SHME/Animations/Stops/SHM_A_CP2_Jog_Fwd_Stop
printf 'import builtins\nbuiltins.G235S = {"dry_run": False}\nexec(open(r"C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V235_20261028/gen235_stop.py", encoding="utf8").read())\n' > $D/req/g235swrite.py
step $D/req/g235swrite.py g235swrite2 "SHME_KIND=write SHME_MANIFEST=$MD/stop2.json"
export WARM=1
J="j30_rel_3200:rv j30_rel_3200:rvR j30_rel_3450:rvR j35_rev:rvR j35_rev2:rvR j30_slow:rvR e29_chain:rvR s29_swl12:rvR j35_rev:rvRS"
ab b1 "$J" $D/vars235_cap.sh
echo "B1_DONE $(date +%T)" >> $O
