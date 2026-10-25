#!/bin/bash
# run228_t1.sh : first clip-bound capsule speed batch (fixed 30): rhC (hold + clip speed, FP on), rhCF (+ FP off in clip), rhC0 (no look-ahead) on ph3 first.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V228_20261025; export O=$D/chain.out; source $D/lib228.sh
echo "T1 start $(date +%T)" >> $O; export WARM=1
relaunch t1 30
ab t1 "j24_ph3:rhC j24_ph3:rhC0 j24_ph3:rhCF j24_ph0:rhC j24_sw_ph2:rhC j24_dbl:rhC j24_rel:rhC j24_sw_ph0:rhC j24_ph0:rhCF j24_sw_ph2:rhCF" $D/vars228.sh
echo "T1_DONE $(date +%T)" >> $O
