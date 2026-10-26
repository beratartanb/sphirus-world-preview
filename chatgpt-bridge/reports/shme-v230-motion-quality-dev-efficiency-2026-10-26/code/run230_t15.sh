#!/bin/bash
# run230_t15.sh : after FPS_DONE. Fresh editor (fixed 30): idle-entry guard patch (knob default 0, saved), warm + index quiet, then a
# same-content A/B: production (route 30) vs route off (nolr) vs route floor 70 (lr70) vs idle guard (ig) vs lr70ig, repeated scenarios.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
V2=Tools/SHME_V2_20261014; R="bash $V2/run_v2.sh"; D=Saved/Codex/SHME_V230_20261026; export O=$D/chain.out
until grep -aq "FPS_DONE" $O; do sleep 30; done
source $D/lib230.sh; echo "T15 start $(date +%T)" >> $O
relaunch t15 30
$R $D/req/install_idleguard_save.py idleguard 900 | grep -a "IDLEGUARD230\|Traceback\|Error" | cut -c1-900 >> $O
grep -a "IDLEGUARD230 {" $O | tail -1 | grep -q '"saved": true' || { echo "T15_FAILED idleguard $(date +%T)" >> $O; exit 1; }
export WARM=1 MEMPROBE=1
ab t15w "j24_rel:ig j24_ph0:o e29_chain:o" $D/vars230c.sh
LOG="Saved/Logs/$LR_LOG"; for i in $(seq 1 40); do n1=$(grep -a -c "BuildIndex" "$LOG"); sleep 15; n2=$(grep -a -c "BuildIndex" "$LOG"); [ "$n1" = "$n2" ] && break; done
J=""; for v in o ig; do for s in j24_rel j24_dbl j24_ph0 c30_calm c29_combo w30_rev j30_slow; do J="$J $s:$v"; done; done
for v in o nolr lr70 lr70ig; do for s in s29_swl12 s29_swl14 s29_swl16 e29_load e29_recov; do J="$J $s:$v"; done; done
J="$J j24_rel:o:2 j24_rel:ig:2 s29_swl12:o:2 s29_swl12:lr70:2"
ab t15 "$J" $D/vars230c.sh
echo "T15_DONE $(date +%T)" >> $O
