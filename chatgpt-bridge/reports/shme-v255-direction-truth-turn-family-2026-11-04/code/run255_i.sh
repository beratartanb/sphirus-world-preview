#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V255_20261104; export O=$D/run255_i.out; source $D/lib255.sh
MD=Saved/Codex/SHME_V233_20261027/checkpoint/manifests
step() { echo "== $2 $(date +%T)" >> $O; out=$(env $3 bash $R "$1" "$2" 1500); echo "$out" > $D/data/last_$2.out; echo "$out" | head -1 | cut -c1-200 >> $O; echo "$out" | grep -aE "GUARD|REFUSED|Traceback|FAIL|V3255|DB255" | head -5 | cut -c1-500 >> $O
  echo "$out" | head -1 | grep -qE "^OK" || { echo "I_FAILED $2 $(date +%T)" >> $O; exit 1; }; }
step Tools/SHME_V21_20261014/revert_noquit.py revert SHME_KIND=control
step $D/req/v3_req.py v3 "SHME_KIND=write SHME_MANIFEST=$MD/v255_v3.json"
grep -a "V3255" $D/data/last_v3.out | grep -q '"ok": true' || { echo "I_FAILED v3" >> $O; exit 1; }
step $D/req/g3w_req.py g5a "SHME_KIND=write SHME_MANIFEST=$MD/v255_g5.json"
step $D/req/g4w_req.py g5b "SHME_KIND=write SHME_MANIFEST=$MD/v255_g5.json"
step $D/req/db5_req.py db5 "SHME_KIND=write SHME_MANIFEST=$MD/v255_g5.json"
echo I_BUILD_OK >> $O
WARM=1 ab i60w "s54_revR:c4 s54_revL:c4 s54_r90:c4 s54_l90:c4 j54_rev:c4 j54_r90:c4 j38_c90l:c4" $D/vars255.sh
ab i60 "s54_revR:c4 s54_revL:c4 s54_r90:c4 s54_l90:c4 j54_rev:c4 j54_r90:c4 j38_c90l:c4 j54_r135:c4 s54_r135:c4 s54_tap:c4 s54_mid:c4 s54_lr:c4 fz_sprint_a:c4 fz_sprint_m:c4 fz_jog_a:c4 fz_jog_m:c4 fz_walk_a:c4 fz_walk_m:c4" $D/vars255.sh
echo TI255_DONE >> $O
