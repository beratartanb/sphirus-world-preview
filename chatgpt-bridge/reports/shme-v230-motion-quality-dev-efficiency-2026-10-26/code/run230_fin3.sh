#!/bin/bash
# run230_fin3.sh : second V2.30 switch (idle guard on top of lowrev) in a fresh editor, save, clean reopen verify, production evidence for
# the affected flows (release sweep, jog reversals, calm / walk / low-speed guards) at fixed 30.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
V2=Tools/SHME_V2_20261014; R="bash $V2/run_v2.sh"; D=Saved/Codex/SHME_V230_20261026; export O=$D/chain.out; source $D/lib230.sh
echo "FIN3 start $(date +%T)" >> $O
relaunch fin3 30
$R $D/req/promo_save2.py promo 600 | grep -a "PROMO230\|Traceback\|Error" | cut -c1-1500 | tee $D/promo_fin3.out >> $O
grep -q '"ok": true' $D/promo_fin3.out && grep -q '"saved": true' $D/promo_fin3.out || { echo "FIN3_FAILED promo $(date +%T)" >> $O; exit 1; }
relaunch fin3v 30
$R $D/req/verify_fin3.py verify 600 | grep -a "VERIFY229\|VERIFY230\|Traceback\|Error" | cut -c1-2500 | tee $D/verify_fin3.out >> $O
grep -q '"ALL_OK": true}' $D/verify_fin3.out || { echo "FIN3_FAILED verify $(date +%T)" >> $O; exit 1; }
export WARM=1 MEMPROBE=1
ab f3w "j24_rel:o e29_chain:o" $D/vars230c.sh
LOG="Saved/Logs/$LR_LOG"; for i in $(seq 1 40); do n1=$(grep -a -c "BuildIndex" "$LOG"); sleep 15; n2=$(grep -a -c "BuildIndex" "$LOG"); [ "$n1" = "$n2" ] && break; done
J=""; for m in 3100 3200 3250 3300 3350 3400 3450; do J="$J j30_rel_$m:o"; done
for s in j24_rel j24_dbl j24_ph0 c30_calm c29_combo w30_rev j30_slow e29_chain e29_load e29_recov e29_rest s29_swl12 s29_swl14 s29_cam s29_ws d_sprint wdiag; do J="$J $s:o"; done
ab fin3 "$J" $D/vars230c.sh
echo "FIN3_DONE $(date +%T)" >> $O
