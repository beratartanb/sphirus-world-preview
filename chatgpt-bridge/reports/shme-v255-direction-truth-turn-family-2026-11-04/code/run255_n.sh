#!/bin/bash
# run255_n.sh : V2.55 FPS sweep of candidate c5 (20 / 30 / 120 fixed + real time) after run255_m; warm pass per editor session (a new DB indexes asynchronously at first use); AO head candidate c5h at 60 and 120
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V255_20261104; export O=$D/run255_n.out; source $D/lib255.sh
until grep -q "TM255_DONE\|M_FAILED\|RELAUNCH_FAILED\|TOO_MANY" $D/run255_m.out 2>/dev/null; do sleep 30; done
grep -q "TM255_DONE" $D/run255_m.out || { echo "N_SKIPPED chain m did not finish" >> $O; exit 1; }
ab m60h "s54_revR:c5h s54_revR:c5h fz_sprint_m:c5h" $D/vars255.sh
W="s54_revR:c5 s54_revL:c5 s54_r90:c5 s54_l90:c5 j54_rev:c5 j54_r90:c5 j38_c90l:c5"
T="s54_revR:c5 s54_revL:c5 s54_r90:c5 j54_rev:c5 j54_r90:c5 s54_tap:c5 fz_sprint_m:c5 fz_jog_m:c5 fz_sprint_m:o fz_jog_m:o"
for F in 20 30 120 real; do
  relaunch n$F $F
  WARM=1 ab n${F}w "$W" $D/vars255.sh
  ab n$F "$T" $D/vars255.sh
  [ "$F" = 120 ] && ab n120h "s54_revR:c5h s54_revR:c5h" $D/vars255.sh
  echo "N_FPS_DONE $F $(date +%T)" >> $O
done
relaunch nend 60
echo TN255_DONE >> $O
