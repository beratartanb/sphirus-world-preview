#!/bin/bash
# run228_t2.sh : fresh editor -> GR fix (acceleration bypass + pre-compensated velocity) + ABP W threshold -> second clip-speed batch (fixed 30).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V228_20261025; export O=$D/chain.out; source $D/lib228.sh
echo "T2 start $(date +%T)" >> $O
taskkill //F //IM UnrealEditor.exe >/dev/null 2>&1; for i in $(seq 1 30); do tasklist 2>/dev/null | grep -qi UnrealEditor.exe || break; sleep 2; done
relaunch p4 30
bash Tools/SHME_V2_20261014/run_v2.sh $D/req/fix_gr2_save.py fixgr2d 900 | grep -a "GR228FIX\|Traceback\|Error" | cut -c1-1200 >> $O
grep -q 'GR228FIX {.*"saved": true' $O || { echo "T2 GR_FIX_FAILED $(date +%T)" >> $O; exit 1; }
bash Tools/SHME_V2_20261014/run_v2.sh $D/req/fix_abpw_save.py fixabpwd 600 | grep -a "ABPW228 {\|Traceback\|Error" | cut -c1-1200 >> $O
grep -q 'ABPW228 {.*"saved": true' $O || { echo "T2 ABPW_FIX_FAILED $(date +%T)" >> $O; exit 1; }
export WARM=1; relaunch t2 30
ab t2 "j24_ph3:rhC j24_ph0:rhC j24_sw_ph2:rhC j24_dbl:rhC j24_rel:rhC j24_sw_ph0:rhC j24_ph3:rhCF j24_ph0:rhCF j24_ph3:rhC0" $D/vars228.sh
echo "T2_DONE $(date +%T)" >> $O
