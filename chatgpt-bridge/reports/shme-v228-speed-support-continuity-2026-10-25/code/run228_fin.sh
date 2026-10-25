#!/bin/bash
# run228_fin.sh "<groups>" : V2.28 final chain. groups = python dict literal for promote228 (e.g. "{'motion': True, 'cancel': True, 'terrain': True}"; "{}" = no promotion = rollback proof).
# fresh editor -> promote228 (save) -> CLEAN reopen verify (verify_fin228 ALL_OK gate) -> PRODUCTION-mode evidence (no candidate overrides; movement, cancel paths,
# terrain, inspection, routes) -> real-time editor (cold start first) -> full-frame captures (production after the switch + the pre-switch reference labels exist from v227fin).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
G="${1:-{\}}"; D=Saved/Codex/SHME_V228_20261025; T=Tools/SHME_V228_20261025; R=Tools/SHME_V2_20261014/run_v2.sh; export O=$D/chain.out; source $D/lib228.sh
echo "FIN start groups=$G $(date +%T)" >> $O
relaunch pr 30
printf 'import builtins\nbuiltins.V228_PROMO = %s\nbuiltins.V228_SAVE = True\nexec(compile(open(r"C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V228_20261025/promote228.py", encoding="utf8").read(), "promote228.py", "exec"))\n' "$G" > $D/req/promo_fin.py
bash $R $D/req/promo_fin.py promo228 600 > $D/promo_fin.out 2>&1; grep -a "PROMO228" $D/promo_fin.out | cut -c1-1200 >> $O
grep -aq '"saved": true' $D/promo_fin.out || { echo "PROMO_FAILED" >> $O; exit 1; }
relaunch vf 30
printf 'import builtins\nbuiltins.V228_EXP = %s\nexec(open(r"C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V228_20261025/req/verify_fin228.py", encoding="utf8").read())\n' "$G" > $D/req/verify_fin_run.py
bash $R $D/req/verify_fin_run.py verify228 600 > $D/verify_fin.out 2>&1; grep -a "VERIFY228\|VERIFY226" $D/verify_fin.out | cut -c1-800 >> $O
grep -aq '"ALL_OK": true' $D/verify_fin.out || { echo "VERIFY_FAILED" >> $O; exit 1; }
relaunch fin 30; export WARM=1
ab fin "j24_sw_ph0:o j24_sw_ph2:o j24_ph0:o j24_ph3:o j24_rel:o j24_dbl:o j24_ad_ph0:o j24_m180w:o j23_m180:o r_cutrev_r:o s23_jstart:o taps:o ins_ws:o ins_ws2:o ter_drop_walk:o ter_drop_jog:o ter_step2:o ter_bump_jog:o map_r1:o map_r2:o" $D/vars228.sh
echo "FIN evidence done $(date +%T)" >> $O
relaunch finrt real; export WARM=0
ab finrt "j24_ph0:o" $D/vars228.sh
export WARM=1; ab finrt "j24_sw_ph2:o j24_dbl:o j24_rel:o ins_ws2:o map_r2:o" $D/vars228.sh
echo FIN_EVIDENCE_DONE >> $O
relaunch cap 30; export WARM=1 CAPV="o"
capf() { export LR_LOG=$(basename "$(ls -t Saved/Logs/*.log | grep -v -i cef | head -1)"); export CAP_START=$1 CAP_SECS=$2; TAG=$3 JOBS="$4" EXTRA_VARS="$(cat $D/vars228.sh; cat Saved/Codex/SHME_V227_20261024/req/cap227.sh)" bash Tools/SHME_V228_20261025/ab_safe228.sh 2>&1 | grep -a " | rows\|REFUSED\|MEM\|GONE" >> $O; }
capf 3.6 7.0 capfin "j24_sw_ph2:oS j24_sw_ph2:oG j24_ph0:oS j24_ph3:oS j24_dbl:oS j24_rel:oS"
capf 6.0 6.0 capter "ter_drop_jog:oS ter_drop_walk:oS"
capf 7.0 7.0 capins "ins_ws2:oG ins_ws2:oS"
echo CAP_DONE >> $O
echo "FIN_DONE $(date +%T)" >> $O
