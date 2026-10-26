#!/bin/bash
# run230_t1.sh : V2.30 fast dev tests on one fresh 30 FPS editor (memory sample per run). 1) low-speed reversal class: o vs lr on the
# failing cases + guards; 2) sway layer isolation (one layer off at a time); 3) 0.4 s stall inside the sprint RevTurn.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V230_20261026; export O=$D/chain.out; source $D/lib230.sh
echo "T1 start $(date +%T)" >> $O
relaunch t1 30; export WARM=1 MEMPROBE=1
bash Tools/SHME_V2_20261014/run_v2.sh $D/req/ra_measure.py ra_measure 900 > $D/ra_measure.out 2>&1; grep -a "RA230 {\|Error\|Traceback" $D/ra_measure.out | cut -c1-3000 >> $O
J=""; for s in e29_load s29_swl12 s29_swl14 j30_slow e29_chain chain_sprint e29_recov j24_dbl j24_rel w30_rev s29_ws c29_combo; do J="$J $s:o $s:lr"; done
ab t1 "$J" $D/vars230.sh
J=""; for v in oPBI oSCR oCLD oOW oSET; do J="$J s29_ws:$v e29_rest:$v"; done
ab t1 "$J" $D/vars230.sh
ab t1 "s29_camh:o s29_camh2:o" $D/vars230.sh
J=""; for s in j24_dbl j24_sw_ph2 j24_ph3 j24_rel e29_load s29_swl12; do J="$J $s:fg $s:lrfg"; done
ab t1 "$J ins_ws2:o ins_ws:o" $D/vars230.sh
echo "T1_DONE $(date +%T)" >> $O
