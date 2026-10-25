#!/bin/bash
# run228_c3.sh : fresh editor -> cancel fix 3 (push-phase safety + family gate OR hold) -> cancel/regular batch at 30 and 120.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V228_20261025; R=Tools/SHME_V2_20261014/run_v2.sh; export O=$D/chain.out; source $D/lib228.sh
echo "C5 start $(date +%T)" >> $O
taskkill //F //IM UnrealEditor.exe >/dev/null 2>&1; for i in $(seq 1 30); do tasklist 2>/dev/null | grep -qi UnrealEditor.exe || break; sleep 2; done
relaunch r1 30
bash $R $D/req/fix_cancel3_save.py fixcancel3 900 | grep -a "CANCEL228C\|Traceback\|Error" | cut -c1-1200 >> $O
grep -q 'CANCEL228C {.*"saved": true' $O || { echo "C5 FIX_FAILED $(date +%T)" >> $O; exit 1; }
export WARM=1; relaunch r2 30
ab r2 "j24_dbl:rhCR j24_rel:rhCR j24_ph0:rhCR j24_ph3:rhCR j24_sw_ph2:rhCR j24_sw_ph0:rhCR" $D/vars228.sh
relaunch r120 120; ab r120 "j24_dbl:rhCR j24_sw_ph2:rhCR j24_ph0:rhCR" $D/vars228.sh
relaunch r60 60; ab r60 "j24_dbl:rhCR j24_rel:rhCR j24_ph3:rhCR" $D/vars228.sh
echo "C5_DONE $(date +%T)" >> $O
