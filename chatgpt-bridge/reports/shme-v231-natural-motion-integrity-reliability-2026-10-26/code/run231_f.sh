#!/bin/bash
# run231_f.sh : V2.31 frame-rate / frame-time validation of the full candidate P vs production o. One fresh editor per mode (the FPS is a
# launch argument): fixed 60, 120, 20, then real time (variable frame time, t.MaxFPS uncapped by the harness) incl. a COLD first run.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V231_20261026; export O=$D/chain.out; source $D/lib231.sh
until grep -aq "L2_DONE" $O; do sleep 20; done
SC="e29_load e29_chain e29_recov s29_swl12 s29_swl14 j30_rel_3100 j30_rel_3450 j24_dbl j24_ph0 d_sprint c30_calm s29_cam e31_s2_4750 e31_s2_4900"
for F in 60 120 20; do
  echo "F$F start $(date +%T)" >> $O
  relaunch f$F $F
  export WARM=1 MEMPROBE=1
  ab f${F}w "s29_swl12:P:0 e29_load:P:0 d_sprint:o:0" $D/vars231.sh
  LOG="Saved/Logs/$LR_LOG"; for i in $(seq 1 40); do n1=$(grep -a -c "BuildIndex" "$LOG"); sleep 15; n2=$(grep -a -c "BuildIndex" "$LOG"); [ "$n1" = "$n2" ] && break; done
  export WARM=0
  J=""; for s in $SC; do for v in o P; do J="$J $s:$v"; done; done
  ab f$F "$J" $D/vars231.sh
done
echo "FRT start $(date +%T)" >> $O
relaunch frt real
export WARM=0 MEMPROBE=1
ab frt "s29_cam:P:1 s29_cam:o:1 e29_load:P e29_load:o s29_swl12:P s29_swl12:o j30_rel_3100:P j30_rel_3100:o c30_calm:P c30_calm:o d_sprint:P d_sprint:o" $D/vars231.sh
echo "F_DONE $(date +%T)" >> $O
