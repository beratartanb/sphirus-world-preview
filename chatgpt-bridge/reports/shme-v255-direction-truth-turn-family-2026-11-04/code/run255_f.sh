#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V255_20261104; export O=$D/run255_f.out; source $D/lib255.sh
MD=Saved/Codex/SHME_V233_20261027/checkpoint/manifests
step() { echo "== $2 $(date +%T)" >> $O; out=$(env $3 bash $R "$1" "$2" 1500); echo "$out" > $D/data/last_$2.out; echo "$out" | head -1 | cut -c1-200 >> $O; echo "$out" | grep -aE "GUARD|REFUSED|Traceback|FAIL|PAWN255|ABP255|G255|DB255" | head -5 | cut -c1-1200 >> $O
  echo "$out" | head -1 | grep -qE "^OK" || { echo "F_FAILED $2 $(date +%T)" >> $O; exit 1; }; }
step $D/req/abp_req.py abp "SHME_KIND=write SHME_MANIFEST=$MD/v255_ctl.json"
grep -a "ABP255" $D/data/last_abp.out | grep -q '"ok": true' || { echo "F_FAILED abp" >> $O; exit 1; }
step $D/req/g2w_req.py g2w "SHME_KIND=write SHME_MANIFEST=$MD/v255_g2.json"
step $D/req/db2_req.py db2 "SHME_KIND=write SHME_MANIFEST=$MD/v255_g2.json"
WARM=1 ab e60 "s54_revR:c1 s54_revR:c1 s54_revL:c1 s54_r135:c1 fz_sprint_a:c1 fz_sprint_m:c1" $D/vars255.sh
echo TF255_DONE >> $O
