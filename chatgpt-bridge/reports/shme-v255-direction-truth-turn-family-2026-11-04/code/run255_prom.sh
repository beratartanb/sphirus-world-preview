#!/bin/bash
# run255_prom.sh : V2.55 promotion of c7h (head + frame) and clean-reopen verification with the plain production variant o
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V255_20261104; export O=$D/run255_prom.out; : > $O; source $D/lib255.sh
V21=Tools/SHME_V21_20261014; MD=Saved/Codex/SHME_V233_20261027/checkpoint/manifests
step() { echo "== $2 $(date +%T)" >> $O; out=$(env $3 bash $R "$1" "$2" 1500); echo "$out" > $D/data/last_$2.out; echo "$out" | head -1 | cut -c1-200 >> $O; echo "$out" | grep -aE "GUARD|REFUSED|Traceback|FAIL|PROMOTE255|write_error" | head -8 | cut -c1-1500 >> $O
  echo "$out" | head -1 | grep -qE "^OK" || { echo "P_FAILED $2 $(date +%T)" >> $O; exit 1; }; }
step $V21/revert_noquit.py revert SHME_KIND=control
step $D/req/prom_req.py prom "SHME_KIND=write SHME_MANIFEST=$MD/v255_prom.json"
grep -q '"saved": true' $D/data/last_prom.out || { echo "P_FAILED not saved" >> $O; exit 1; }
echo PROM_SAVED >> $O
relaunch pv 60
WARM=1 ab pvw "s54_revR:o s54_revL:o s54_r90:o s54_l90:o j54_rev:o j54_r90:o j38_c90l:o" $D/vars255.sh
ab pv "s54_revR:o s54_revL:o s54_r135:o s54_r90:o s54_l90:o j54_rev:o j54_r135:o j54_r90:o j38_c90l:o w54_rev:o wstart:o s54_tap:o fz_sprint_m:o fz_jog_m:o" $D/vars255.sh
echo TP255_DONE >> $O
