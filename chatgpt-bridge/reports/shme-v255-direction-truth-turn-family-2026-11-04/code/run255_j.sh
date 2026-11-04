#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V255_20261104; export O=$D/run255_j.out; source $D/lib255.sh
MD=Saved/Codex/SHME_V233_20261027/checkpoint/manifests
step() { echo "== $2 $(date +%T)" >> $O; out=$(env $3 bash $R "$1" "$2" 1500); echo "$out" > $D/data/last_$2.out; echo "$out" | head -1 | cut -c1-200 >> $O; echo "$out" | grep -aE "GUARD|REFUSED|Traceback|FAIL|DB255|V4255" | head -5 | cut -c1-400 >> $O
  echo "$out" | head -1 | grep -qE "^OK" || { echo "J_FAILED $2 $(date +%T)" >> $O; exit 1; }; }
step Tools/SHME_V21_20261014/revert_noquit.py revert SHME_KIND=control
step $D/req/v4_req.py v4 "SHME_KIND=write SHME_MANIFEST=$MD/v255_v4.json"
grep -a "V4255" $D/data/last_v4.out | grep -q '"ok": true' || { echo "J_FAILED v4" >> $O; exit 1; }
step $D/req/g3w_req.py g6a "SHME_KIND=write SHME_MANIFEST=$MD/v255_g6.json"
step $D/req/g4w_req.py g6b "SHME_KIND=write SHME_MANIFEST=$MD/v255_g6.json"
step $D/req/db5_req.py db6 "SHME_KIND=write SHME_MANIFEST=$MD/v255_g6.json"
echo J_BUILD_OK >> $O
WARM=1 ab j60w "s54_revR:c5 s54_revL:c5 s54_r90:c5 s54_l90:c5 j54_rev:c5 j54_r90:c5 j38_c90l:c5" $D/vars255.sh
ab j60 "s54_revR:c5 s54_revL:c5 s54_r90:c5 s54_l90:c5 j54_rev:c5 j54_r90:c5 j38_c90l:c5 s54_tap:c5 s54_mid:c5 s54_lr:c5 fz_sprint_a:c5 fz_sprint_m:c5 fz_jog_a:c5 fz_jog_m:c5" $D/vars255.sh
CAP_START=4.6 CAP_SECS=3.2 ab jcap "s54_revR:c5S s54_revL:c5S s54_r90:c5S j54_rev:c5S j54_r90:c5S s54_revR:c5G j54_rev:c5G" $D/vars255.sh
echo TJ255_DONE >> $O
