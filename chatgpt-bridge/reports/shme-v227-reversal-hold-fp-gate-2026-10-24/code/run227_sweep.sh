#!/bin/bash
# run227_sweep.sh <variant> : FPS sweep (20/60/120, fixed step, fresh editor each) of rv32 vs the V2.27 candidate on the reversal scenarios,
# then a real-time editor: cold start (first PIE after launch, WARM=0) + real-time set. Production 'o' per FPS = the V2.26 s20/s60/s120 runs.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
V=${1:-rh}; D=Saved/Codex/SHME_V227_20261024; export O=$D/chain.out; source $D/lib227.sh
echo "SWEEP $V start $(date +%T)" >> $O
for F in 20 60 120; do
  export WARM=1; relaunch s$F $F
  ab s$F "j24_ph0:rv32 j24_ph0:$V j24_sw_ph2:rv32 j24_sw_ph2:$V j24_ph3:rv32 j24_ph3:$V j24_ovl120:rv32 j24_ovl120:$V" $D/vars227.sh
  echo "SWEEP s$F done $(date +%T)" >> $O
done
relaunch rt real; export WARM=0
ab rt "j24_ph0:$V" $D/vars227.sh                       # cold start: first PIE of a fresh real-time editor
export WARM=1
ab rt "j24_sw_ph2:$V j24_ph3:$V j24_rel:$V j24_dbl:$V j24_ph0:rv32 j24_sw_ph2:rv32" $D/vars227.sh
echo "SWEEP_DONE $V $(date +%T)" >> $O
