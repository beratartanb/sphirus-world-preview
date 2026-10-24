#!/bin/bash
# run227_t4.sh : fourth-pass candidate (hold + FP gate + restart + re-entry latch + search throttle) at fixed 30, then 60 / 120 / 20 FPS.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V227_20261024; export O=$D/chain.out; source $D/lib227.sh
echo "T4 start $(date +%T)" >> $O
export WARM=1; relaunch t4 30
ab t4 "j24_ph0:rh j24_ph3:rh j24_sw_ph0:rh j24_sw_ph2:rh j24_rel:rh j24_dbl:rh j24_ph0:rv32" $D/vars227.sh
echo "T4 30 done $(date +%T)" >> $O
relaunch u60 60; ab u60 "j24_ph0:rh j24_sw_ph2:rh j24_ph3:rh j24_ovl120:rh j24_ph0:rv32" $D/vars227.sh; echo "T4 60 done $(date +%T)" >> $O
relaunch u120 120; ab u120 "j24_ph3:rh j24_ph0:rh j24_sw_ph2:rh j24_ovl120:rh" $D/vars227.sh; echo "T4 120 done $(date +%T)" >> $O
relaunch u20 20; ab u20 "j24_ph0:rh j24_ph3:rh j24_sw_ph2:rh j24_ovl120:rh" $D/vars227.sh; echo "T4 20 done $(date +%T)" >> $O
echo "T4_DONE $(date +%T)" >> $O
