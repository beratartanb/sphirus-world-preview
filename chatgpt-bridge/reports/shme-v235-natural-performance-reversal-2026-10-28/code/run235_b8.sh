#!/bin/bash
# run235_b8.sh : V2.35 B8 - stop re-plan REJECTED (out-of-phase stop entries lost their closing step: 36 cm drag) -> restore the V2.34 jog stop, then the reversal-content decision runs.
# re-target complete before the foot is low), continuing-pose bias -0.5 on the V235 reversal DBs, then the 30 FPS regression set and the
# 60 FPS release-repress set (frame-rate mode = editor launch argument).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V235_20261028; export O=$D/chain.out; source $D/lib235.sh; R=Tools/SHME_V2_20261014/run_v2.sh; T=Tools/SHME_V235_20261028; MD=$D/checkpoint/manifests
step() { echo "== $2 $(date +%T)" >> $O; out=$(env $3 bash $R "$1" "$2" 1500); echo "$out" > $D/last_$2.out; echo "$out" | head -1 >> $O; echo "$out" | grep -aE "REFUSED|Traceback|G235S|DBBIAS235" | head -3 | cut -c1-700 >> $O
  echo "$out" | head -1 | grep -qE "^OK" || { echo "B8_FAILED $2 $(date +%T)" >> $O; exit 1; }; }
mani() { MSYS_NO_PATHCONV=1 "$PY" $T/manifest235.py "$@" >> $O 2>&1 || { echo "B8_FAILED manifest $1" >> $O; exit 1; }; }
echo waitnone
echo "B8 start $(date +%T)" >> $O
export LR_LOG=$(basename "$(ls -t Saved/Logs/*.log | grep -v -i cef | head -1)")
bash $R Tools/SHME_V21_20261014/revert_quit.py rq_b8 300 | grep -E "dirty after|QUIT|REFUSED" >> $O
for i in $(seq 1 90); do tasklist 2>/dev/null | grep -qi UnrealEditor.exe || break; sleep 2; done
tasklist 2>/dev/null | grep -qi UnrealEditor.exe && { echo "B8_FAILED editor did not quit" >> $O; exit 1; }
BK=$D/checkpoint/manifests/stop1/Content/GraceRanger/SHME/Animations/Stops/SHM_A_CP2_Jog_Fwd_Stop.uasset; DST=Content/GraceRanger/SHME/Animations/Stops/SHM_A_CP2_Jog_Fwd_Stop.uasset
cp "$BK" "$DST" && [ "$(sha1sum < "$DST" | cut -c1-40)" = "1323d4cf743b401ea9a69a5377cb73f932197a01" ] && echo "RESTORED stop1 $(date +%T)" >> $O || { echo "B8_FAILED restore" >> $O; exit 1; }
relaunch b8 30
export WARM=1
ab b8 "j34_chain1:rvRG2 j34_chain1:rvRG2:2 j34_chain1:o j30_rel_3200:rvRG2 j30_rel_3200:o j35_relstop:rvRG2 jstart:rvRG2 jstart:o j35_rev:rvRG2 j30_slow:rvRG2 j30_slow:o" $D/vars235.sh
echo "B8_DONE $(date +%T)" >> $O
