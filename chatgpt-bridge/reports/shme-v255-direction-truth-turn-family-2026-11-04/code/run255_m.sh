#!/bin/bash
# run255_m.sh : V2.55 final candidate c5 (walk unchanged): rebuild content, same-session A/B against production: scripted, fuzz, direction matrix, regression, captures; then FPS sweep
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V255_20261104; export O=$D/run255_m.out; source $D/lib255.sh
MD=Saved/Codex/SHME_V233_20261027/checkpoint/manifests
step() { echo "== $2 $(date +%T)" >> $O; out=$(env $3 bash $R "$1" "$2" 1500); echo "$out" > $D/data/last_$2.out; echo "$out" | head -1 | cut -c1-200 >> $O; echo "$out" | grep -aE "GUARD|REFUSED|Traceback|FAIL|DB255|LEG_GUARD|write_error" | head -5 | cut -c1-320 >> $O
  echo "$out" | head -1 | grep -qE "^OK" || { echo "M_FAILED $2 $(date +%T)" >> $O; exit 1; }; }
step Tools/SHME_V21_20261014/revert_noquit.py revert SHME_KIND=control
step $D/req/g3w_req.py g9a "SHME_KIND=write SHME_MANIFEST=$MD/v255_g9.json"
step $D/req/g4w_req.py g9b "SHME_KIND=write SHME_MANIFEST=$MD/v255_g9.json"
grep -aq "write_error\|\"error\"" $D/data/last_g9a.out $D/data/last_g9b.out && { echo "M_FAILED clip write" >> $O; exit 1; }
step $D/req/db5_req.py db9 "SHME_KIND=write SHME_MANIFEST=$MD/v255_g9.json"
echo M_BUILD_OK >> $O
SC="s54_revR s54_revL s54_r90 s54_l90 s54_r135 j54_rev j54_r90 j38_c90l j54_r135 w54_rev s54_tap s54_mid s54_lr"
FZ="fz_sprint_a fz_sprint_m fz_jog_a fz_jog_m fz_walk_a fz_walk_m"
DM="fz_dm_walk_0 fz_dm_walk_60 fz_dm_walk_m120 fz_dm_jog_0 fz_dm_jog_60 fz_dm_jog_m120 fz_dm_sprint_0 fz_dm_sprint_60 fz_dm_sprint_m120"
RG="wstart w42_id taps jstart j36_stop j45_sl2 gait w43_idle j40_rlw"
J=""; for s in $SC; do J="$J $s:c5"; done
WARM=1 ab m60w "s54_revR:c5 s54_revL:c5 s54_r90:c5 s54_l90:c5 j54_rev:c5 j54_r90:c5 j38_c90l:c5" $D/vars255.sh
J=""; for s in $SC $FZ $DM $RG; do J="$J $s:c5 $s:o"; done
ab m60 "$J" $D/vars255.sh
echo M_AB_DONE >> $O
CAP_START=4.6 CAP_SECS=3.2 ab mcap "s54_revR:oS s54_revR:c5S s54_revR:oG s54_revR:c5G s54_r90:oS s54_r90:c5S j54_rev:oS j54_rev:c5S j54_rev:oG j54_rev:c5G j54_r90:oS j54_r90:c5S" $D/vars255.sh
echo TM255_DONE >> $O
