#!/bin/bash
# run230_t2.sh : one fresh 30 FPS editor: EarlyRev graph patch (saved, knob off) -> re-author measure v2 (read-only) -> A/B o vs lr2 / er on the
# low-speed reversal family + guards.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V230_20261026; R=Tools/SHME_V2_20261014/run_v2.sh; export O=$D/chain.out; source $D/lib230.sh
echo "T2 start $(date +%T)" >> $O
relaunch t2 30
bash $R Tools/SHME_V21_20261014/revert_noquit.py revert_t2 300 | grep -a "dirty after" >> $O
bash $R $D/req/install_earlyrev_save.py earlyrev230 900 > $D/earlyrev230.out 2>&1; grep -a "EARLYREV230 {\|Traceback\|Error" $D/earlyrev230.out | cut -c1-700 >> $O
grep -aq '"ok": true' $D/earlyrev230.out || { echo "T2_FAILED earlyrev" >> $O; exit 1; }
bash $R $D/req/ra_measure.py ra_measure2 900 > $D/ra_measure2.out 2>&1; grep -a "Traceback\|Error" $D/ra_measure2.out | head -3 >> $O
export WARM=1 MEMPROBE=1
J=""; for s in e29_load s29_swl12 s29_swl14 s29_swl16 e29_recov j30_slow e29_chain chain_sprint; do J="$J $s:lr2 $s:er"; done
ab t2 "$J" $D/vars230.sh
J=""; for s in s29_ws s29_dbl s29_rel j24_ph0 j24_dbl j24_rel j24_sw_ph2 w30_rev c29_combo s23_jstart taps; do J="$J $s:lr2"; done
ab t2 "$J" $D/vars230.sh
echo "T2_DONE $(date +%T)" >> $O
