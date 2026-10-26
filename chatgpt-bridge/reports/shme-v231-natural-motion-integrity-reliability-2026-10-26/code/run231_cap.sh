#!/bin/bash
# run231_cap.sh : V2.31 captures in the finv editor (fixed 30 = real speed, full frame 1728x972, unedited). o = V2.31 production, pre = the
# same production with every V2.31 knob at its V2.30 value. One short test capture first; the batch only runs if its frames exist.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V231_20261026; export O=$D/chain.out; source $D/lib231.sh; V=Saved/Codex/SHME_V138_20260927/Video
capf() { export LR_LOG=$(basename "$(ls -t Saved/Logs/*.log | grep -v -i cef | head -1)"); export CAP_START=$1 CAP_SECS=$2; TAG=$3 JOBS="$4" EXTRA_VARS="$(cat $D/vars231.sh)" bash Tools/SHME_V231_20261026/ab_safe231.sh 2>&1 | grep -a " | rows\|REFUSED\|MEM\|GONE\|INVALID" >> $O; }
echo "CAP start $(date +%T)" >> $O
export WARM=0 CAPV="o" CAPV2="pre"
capf 2.6 2.0 capt "j24_rel:oS"
n=$(ls $V/v231capt_j24_rel_oS_r1 2>/dev/null | wc -l); echo "CAPTEST frames $n" >> $O
[ "$n" -ge 50 ] || { echo "CAP_FAILED captest $(date +%T)" >> $O; exit 1; }
capf 1.6 10.6 cap "c30_calm:oS c30_calm:oG"
capf 3.6 4.4 cap "s29_swl12:oS s29_swl12:preS s29_swl12:oG"
capf 2.6 10.0 cap "e29_chain:oS e29_chain:oG"
capf 2.4 9.0 cap "e29_load:oS e29_load:preS e29_rest:oS"
capf 2.6 4.0 cap "j30_rel_3100:oS j30_rel_3100:preS"
capf 2.0 11.0 cap "legs_slope_sprint:oS legs_slope_sprint:preS"
capf 2.6 10.0 cap "s29_cam:oG d_sprint:oS"
capf 12.0 8.0 cap "a29_angb:oS"
capf 9.0 9.0 cap "ter_drop_walk:oS ter_drop_walk:preS"
capf 1.4 9.0 cap "ins_ws:oG ins_ws:preG"
capf 1.0 18.0 cap "map_r1:oG"
echo "CAP_DONE $(date +%T)" >> $O
