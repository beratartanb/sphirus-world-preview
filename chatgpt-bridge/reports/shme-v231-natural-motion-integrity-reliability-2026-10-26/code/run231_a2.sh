#!/bin/bash
# run231_a2.sh : V2.31 A2 - same editor (fixed 30) after the slow family + route/exit patches: warm the new DBs, wait for index quiet, A/B.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V231_20261026; export O=$D/chain.out; source $D/lib231.sh
echo "A2 start $(date +%T)" >> $O
export WARM=1 MEMPROBE=1
ab a2w "s29_swl12:sx:0 j30_rel_3100:sx:0 e29_load:sx:0" $D/vars231.sh
LOG="Saved/Logs/$LR_LOG"; for i in $(seq 1 40); do n1=$(grep -a -c "BuildIndex" "$LOG"); sleep 15; n2=$(grep -a -c "BuildIndex" "$LOG"); [ "$n1" = "$n2" ] && break; done
export WARM=0
J=""; for v in o s1 x1 sx; do for s in s29_swl12 s29_swl14 j30_rel_3100 j30_rel_3200 e29_load e29_chain; do J="$J $s:$v"; done; done
J="$J s29_swl12:o:2 s29_swl12:sx:2 s29_swl12:sx:3 j24_ph0:o j24_ph0:s1 j24_ph0:sx j24_dbl:o j24_dbl:sx c30_calm:o c30_calm:sx j30_slow:o j30_slow:sx d_sprint:o d_sprint:sx e29_rest:o e29_rest:sx"
ab a2 "$J" $D/vars231.sh
echo "A2_DONE $(date +%T)" >> $O
