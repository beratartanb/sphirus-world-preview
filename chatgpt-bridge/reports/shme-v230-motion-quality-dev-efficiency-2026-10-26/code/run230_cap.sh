#!/bin/bash
# run230_cap.sh : V2.30 captures (fixed 30 = real speed, full frame 1728x972, unedited). o = V2.30 production; nolr = production with the
# low-speed reversal route off (V2.29 routing on the V2.30 content). Before = V2.29 published media (same scenarios) where content changed.
# First ONE short test capture; the batch only runs if its frames exist (maximized-window trap: captures refused silently).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V230_20261026; export O=$D/chain.out; source $D/lib230.sh; V=Saved/Codex/SHME_V138_20260927/Video
capf() { export LR_LOG=$(basename "$(ls -t Saved/Logs/*.log | grep -v -i cef | head -1)"); export CAP_START=$1 CAP_SECS=$2; TAG=$3 JOBS="$4" EXTRA_VARS="$(cat $D/vars230c.sh)" bash Tools/SHME_V230_20261026/ab_safe230.sh 2>&1 | grep -a " | rows\|REFUSED\|MEM\|GONE\|INVALID" >> $O; }
echo "CAP start $(date +%T)" >> $O
relaunch cap 30; export WARM=1 CAPV="o nolr"
capf 2.6 2.0 capt "j24_rel:oS"
n=$(ls $V/v230capt_j24_rel_oS_r1 2>/dev/null | wc -l); echo "CAPTEST frames $n" >> $O
[ "$n" -ge 50 ] || { echo "CAP_FAILED captest $(date +%T)" >> $O; exit 1; }
capf 1.6 10.6 cap "c30_calm:oS c30_calm:oG"
capf 3.6 6.0 cap "s29_swl14:oS s29_swl14:nolrS s29_swl14:oG"
capf 2.6 10.0 cap "e29_chain:oS e29_chain:oG s29_cam:oS s29_cam:oG"
capf 2.6 6.0 cap "j24_rel:oS j30_slow:oS j30_slow:nolrS j30_slow:oG"
capf 4.0 5.0 cap "d_sprint:oS d_sprint:oD"
capf 2.0 11.0 cap "legs_slope_sprint:oS"
echo "CAP_DONE $(date +%T)" >> $O
