#!/bin/bash
# run227_fin.sh <PROMO 1|0> : V2.27 final chain. PROMO=1: production switch (promote227: 32-bin reversal DBs + SHM227_RevHold/FPOff 1) in a fresh
# editor, then a CLEAN reopen verify (verify_fin227 ALL_OK gate), then PRODUCTION-mode evidence (no candidate overrides), a real-time editor
# (cold start first), full-frame captures. PROMO=0: verify the unchanged production (knobs 0) and run the same evidence (rollback proof).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
PROMO=${1:-1}; D=Saved/Codex/SHME_V227_20261024; T=Tools/SHME_V227_20261024; R=Tools/SHME_V2_20261014/run_v2.sh; export O=$D/chain.out; source $D/lib227.sh
echo "FIN start PROMO=$PROMO $(date +%T)" >> $O
if [ "$PROMO" = 1 ]; then
  relaunch pr 30
  printf 'import builtins\nbuiltins.V227_REV = True\nbuiltins.V227_SAVE = True\nexec(compile(open(r"C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V227_20261024/promote227.py", encoding="utf8").read(), "promote227.py", "exec"))\n' > $D/req/promo_fin.py
  bash $R $D/req/promo_fin.py promo227 600 > $D/promo_fin.out 2>&1; grep -a "PROMO227" $D/promo_fin.out | cut -c1-900 >> $O
  grep -aq '"saved": true' $D/promo_fin.out || { echo "PROMO_FAILED" >> $O; exit 1; }
fi
relaunch vf 30
printf 'import builtins\nbuiltins.V227_EXP_REV = %s\nexec(open(r"C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V227_20261024/req/verify_fin227.py", encoding="utf8").read())\n' "$([ "$PROMO" = 1 ] && echo True || echo False)" > $D/req/verify_fin_run.py
bash $R $D/req/verify_fin_run.py verify227 600 > $D/verify_fin.out 2>&1; grep -a "VERIFY227\|VERIFY226" $D/verify_fin.out | cut -c1-600 >> $O
grep -aq '"ALL_OK": true' $D/verify_fin.out || { echo "VERIFY_FAILED" >> $O; exit 1; }
relaunch fin 30; export WARM=1
ab fin "j24_sw_ph0:o j24_sw_ph2:o j24_ph0:o j24_ph3:o j24_rel:o j24_dbl:o j24_ad_ph0:o j24_m180w:o j23_m180:o r_cutrev_r:o s23_jstart:o taps:o ins_ws:o ter_drop_walk:o ter_step2:o map_r2:o" $D/vars227.sh
echo "FIN evidence done $(date +%T)" >> $O
relaunch finrt real; export WARM=0
ab finrt "j24_ph0:o" $D/vars227.sh
export WARM=1; ab finrt "j24_sw_ph2:o j24_dbl:o map_r2:o" $D/vars227.sh
echo FIN_EVIDENCE_DONE >> $O
relaunch cap 30; export WARM=1 CAPV="o rh"
capf() { export LR_LOG=$(basename "$(ls -t Saved/Logs/*.log | grep -v -i cef | head -1)"); export CAP_START=$1 CAP_SECS=$2; TAG=$3 JOBS="$4" EXTRA_VARS="$(cat $D/vars227.sh; cat $D/req/cap227.sh)" bash $T/ab_safe227.sh 2>&1 | grep -a " | rows\|REFUSED\|MEM\|GONE" >> $O; }
capf 3.6 7.0 capfin "j24_sw_ph2:oS j24_sw_ph2:rhS j24_ph0:oS j24_ph0:rhS j24_dbl:oS j24_dbl:rhS j24_sw_ph2:rhG"
echo CAP_DONE >> $O
echo "FIN_DONE $(date +%T)" >> $O
