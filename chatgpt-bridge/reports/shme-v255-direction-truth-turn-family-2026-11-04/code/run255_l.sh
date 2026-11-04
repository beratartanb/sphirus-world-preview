#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V255_20261104; export O=$D/run255_l.out; source $D/lib255.sh
MD=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; AB=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
step() { echo "== $2 $(date +%T)" >> $O; out=$(env $3 bash $R "$1" "$2" 1500); echo "$out" > $D/data/last_$2.out; echo "$out" | head -1 | cut -c1-200 >> $O; echo "$out" | grep -aE "GUARD|REFUSED|Traceback|FAIL|DB255|V6255|V7255" | head -5 | cut -c1-320 >> $O
  echo "$out" | head -1 | grep -qE "^OK" || { echo "L_FAILED $2 $(date +%T)" >> $O; exit 1; }; }
step Tools/SHME_V21_20261014/revert_noquit.py revert SHME_KIND=control
step $D/req/v6_req.py v6 "SHME_KIND=write SHME_MANIFEST=$MD/v255_v6.json"
grep -a "V6255" $D/data/last_v6.out | grep -q '"ok": true' || { echo "L_FAILED v6" >> $O; exit 1; }
MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V233_20261027/manifest233.py v255_v7 --assets $AB/ABP_GR_MotionMatchingBase $AB/ABP_GR_MotionMatching | tail -1 | cut -c1-120 >> $O
step $D/req/v7_req.py v7 "SHME_KIND=write SHME_MANIFEST=$MD/v255_v7.json"
grep -a "V7255" $D/data/last_v7.out | grep -q '"ok": true' || { echo "L_FAILED v7" >> $O; exit 1; }
step $D/req/g8w_req.py g8w "SHME_KIND=write SHME_MANIFEST=$MD/v255_g8.json"
step $D/req/db8_req.py db8 "SHME_KIND=write SHME_MANIFEST=$MD/v255_g8.json"
echo L_BUILD_OK >> $O
WARM=1 ab l60w "s54_revR:c6 s54_revL:c6 w54_rev:c6 j54_rev:c6" $D/vars255.sh
ab l60 "s54_revR:c6 s54_revL:c6 s54_r90:c6 s54_l90:c6 j54_rev:c6 j54_r90:c6 j38_c90l:c6 w54_rev:c6 s54_tap:c6 s54_mid:c6 s54_lr:c6 fz_sprint_a:c6 fz_sprint_m:c6 fz_jog_a:c6 fz_jog_m:c6 fz_walk_a:c6 fz_walk_m:c6" $D/vars255.sh
CAP_START=4.6 CAP_SECS=3.2 ab lcap "s54_revR:c6S s54_revL:c6S s54_r90:c6S j54_rev:c6S j54_r90:c6S w54_rev:c6S s54_revR:c6G j54_rev:c6G" $D/vars255.sh
echo TL255_DONE >> $O
