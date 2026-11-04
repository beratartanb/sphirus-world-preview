#!/bin/bash
# run255_s.sh : V2.55 FPS sweep of the final candidate c7h against production o: 20, 30, 120 fixed and real time. Ends back on fixed 60.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V255_20261104; export O=$D/run255_s.out; source $D/lib255.sh
for F in 20 30 120 real; do
  relaunch s$F $F
  WARM=1 ab s${F}w "s54_revR:c7h s54_revL:c7h s54_r90:c7h s54_l90:c7h j54_rev:c7h j54_r90:c7h j38_c90l:c7h" $D/vars255.sh
  J=""; for s in s54_revR s54_revL s54_r90 j54_rev j54_r90 s54_tap fz_sprint_m fz_jog_m wstart taps; do J="$J $s:c7h"; done
  for s in s54_revR j54_rev fz_sprint_m fz_jog_m wstart; do J="$J $s:o"; done
  ab s$F "$J" $D/vars255.sh
  echo "S_DONE $F $(date +%T)" >> $O
done
relaunch end 60
echo TS255_DONE >> $O
