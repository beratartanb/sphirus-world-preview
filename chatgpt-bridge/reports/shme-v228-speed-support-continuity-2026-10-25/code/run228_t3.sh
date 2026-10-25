#!/bin/bash
# run228_t3.sh : FPS sweep of the clip-bound capsule speed candidate rhC (hold + clip speed, FP on): 60 / 120 / 20 FPS, then real time (cold first).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V228_20261025; export O=$D/chain.out; source $D/lib228.sh
echo "T3 start $(date +%T)" >> $O; export WARM=1
relaunch w60 60; ab w60 "j24_ph0:rhC j24_ph3:rhC j24_sw_ph2:rhC j24_ovl120:rhC j24_dbl:rhC j24_rel:rhC" $D/vars228.sh; echo "T3 60 done $(date +%T)" >> $O
relaunch w120 120; ab w120 "j24_ph3:rhC j24_ph0:rhC j24_sw_ph2:rhC j24_ovl120:rhC j24_rel:rhC" $D/vars228.sh; echo "T3 120 done $(date +%T)" >> $O
relaunch w20 20; ab w20 "j24_ph0:rhC j24_ph3:rhC j24_sw_ph2:rhC j24_ovl120:rhC j24_dbl:rhC j24_rel:rhC" $D/vars228.sh; echo "T3 20 done $(date +%T)" >> $O
relaunch rt real; export WARM=0; ab rt "j24_ph0:rhC" $D/vars228.sh; export WARM=1; ab rt "j24_sw_ph2:rhC j24_dbl:rhC j24_ph3:rhC" $D/vars228.sh; echo "T3 rt done $(date +%T)" >> $O
echo "T3_DONE $(date +%T)" >> $O
