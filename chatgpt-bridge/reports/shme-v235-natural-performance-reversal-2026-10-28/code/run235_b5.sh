#!/bin/bash
# run235_b5.sh : V2.35 B5 - restore the V2.34 jog stop, stop re-plan r6 (final landing planned on the BALL), stop / chain / restart tests at 30 and 60 FPS.
# re-target complete before the foot is low), continuing-pose bias -0.5 on the V235 reversal DBs, then the 30 FPS regression set and the
# 60 FPS release-repress set (frame-rate mode = editor launch argument).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V235_20261028; export O=$D/chain.out; source $D/lib235.sh; R=Tools/SHME_V2_20261014/run_v2.sh; T=Tools/SHME_V235_20261028; MD=$D/checkpoint/manifests
step() { echo "== $2 $(date +%T)" >> $O; out=$(env $3 bash $R "$1" "$2" 1500); echo "$out" > $D/last_$2.out; echo "$out" | head -1 >> $O; echo "$out" | grep -aE "REFUSED|Traceback|G235S|DBBIAS235" | head -3 | cut -c1-700 >> $O
  echo "$out" | head -1 | grep -qE "^OK" || { echo "B5_FAILED $2 $(date +%T)" >> $O; exit 1; }; }
mani() { MSYS_NO_PATHCONV=1 "$PY" $T/manifest235.py "$@" >> $O 2>&1 || { echo "B5_FAILED manifest $1" >> $O; exit 1; }; }
echo waitnone
echo "B5 start $(date +%T)" >> $O
export LR_LOG=$(basename "$(ls -t Saved/Logs/*.log | grep -v -i cef | head -1)")
bash $R Tools/SHME_V21_20261014/revert_quit.py rq_b5 300 | grep -E "dirty after|QUIT|REFUSED" >> $O
for i in $(seq 1 90); do tasklist 2>/dev/null | grep -qi UnrealEditor.exe || break; sleep 2; done
tasklist 2>/dev/null | grep -qi UnrealEditor.exe && { echo "B5_FAILED editor did not quit" >> $O; exit 1; }
BK=$D/checkpoint/manifests/stop1/Content/GraceRanger/SHME/Animations/Stops/SHM_A_CP2_Jog_Fwd_Stop.uasset; DST=Content/GraceRanger/SHME/Animations/Stops/SHM_A_CP2_Jog_Fwd_Stop.uasset
cp "$BK" "$DST" && [ "$(sha1sum < "$DST" | cut -c1-40)" = "1323d4cf743b401ea9a69a5377cb73f932197a01" ] && echo "RESTORED stop1 $(date +%T)" >> $O || { echo "B5_FAILED restore" >> $O; exit 1; }
relaunch b5 30
step Tools/SHME_V21_20261014/revert_noquit.py revert SHME_KIND=control
mani stop6 --assets /Game/GraceRanger/SHME/Animations/Stops/SHM_A_CP2_Jog_Fwd_Stop
step $D/req/g235swrite.py g235swrite6 "SHME_KIND=write SHME_MANIFEST=$MD/stop6.json"
export WARM=1
J="j34_chain1:rvR j34_chain1:o j35_rev:rvR j30_rel_3200:oR j30_rel_3200:rvR j30_slow:rvR j35_rev2:rvR e29_load:rvR jstart:rvR wdiag:rvR j34_chain1:rvRS j35_rev:rvRS"
ab b5 "$J" $D/vars235_cap.sh
echo "B5_30_DONE $(date +%T)" >> $O
relaunch b5f60 60
ab b5f60 "j34_chain1:rvR j35_rev:rvR j30_rel_3200:rvR j30_slow:rvR" $D/vars235.sh
echo "B5_DONE $(date +%T)" >> $O
