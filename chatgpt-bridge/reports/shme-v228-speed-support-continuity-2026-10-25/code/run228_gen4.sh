#!/bin/bash
# run228_gen.sh : regenerate the ten floor-shuffle bins (gen228), rebuild the two reversal databases with full BranchIn windows, re-add the
# three curves, then test the bins that were hit (sw_ph2 picks B_F P6 at 120 FPS / real time) plus the regular set at fixed 30.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V228_20261025; R=Tools/SHME_V2_20261014/run_v2.sh; export O=$D/chain.out; source $D/lib228.sh
echo "GEN4 start $(date +%T)" >> $O
taskkill //F //IM UnrealEditor.exe >/dev/null 2>&1; for i in $(seq 1 30); do tasklist 2>/dev/null | grep -qi UnrealEditor.exe || break; sleep 2; done
relaunch m1 30
bash $R $D/req/fix_cancel2_save.py fixcancel2 900 | grep -a "CANCEL228B\|Traceback\|Error" | cut -c1-1200 >> $O
grep -q 'CANCEL228B {.*"saved": true' $O || { echo "GEN4 CANCEL2_FAILED $(date +%T)" >> $O; exit 1; }
bash $R $D/req/gen228_dry.py gen228dry 900 | grep -a "G228\|Traceback" | cut -c1-1600 >> $O
grep -q 'G228 {"dry": true' $O || { echo "GEN4 DRY_FAILED $(date +%T)" >> $O; exit 1; }
bash $R $D/req/gen228_write.py gen228write 1500 | grep -a "G228\|Traceback" | cut -c1-1600 >> $O
grep -q 'G228 {"dry": false' $O || { echo "GEN4 WRITE_FAILED $(date +%T)" >> $O; exit 1; }
bash $R $D/req/revdbs_full.py revdbs 900 | grep -a "RDB226\|Traceback" | cut -c1-600 >> $O
bash $R $D/req/revcurve_save.py revcurve 900 | grep -a "REVCURVE227\|Traceback" | cut -c1-300 >> $O
bash $R $D/req/speedcurve_save.py speedcurve2 900 | grep -a "SPEEDCURVE228\|Traceback" | cut -c1-300 >> $O
echo "GEN4 assets done $(date +%T)" >> $O
export WARM=1; relaunch m2 30
ab m2 "j24_dbl:rhCR j24_rel:rhCR j24_sw_ph2:rhCR j24_ph0:rhCR j24_ph3:rhCR j24_sw_ph0:rhCR j24_dbl:rhC" $D/vars228.sh
relaunch m120 120; ab m120 "j24_sw_ph2:rhCR j24_ph3:rhCR j24_ph0:rhCR j24_dbl:rhCR" $D/vars228.sh
echo "GEN4_DONE $(date +%T)" >> $O
