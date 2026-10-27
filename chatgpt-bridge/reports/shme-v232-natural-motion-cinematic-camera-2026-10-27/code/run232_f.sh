#!/bin/bash
# run232_f.sh : V2.32 FPS sessions (after P1_DONE). The FPS is an editor launch argument -> one relaunch per mode (reason logged):
# fixed 60, fixed 120, fixed 20, real time (unlocked). Per mode: o vs P on the FPS-sensitive set (same real-time input).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V232_20261027; export O=$D/chain.out; source $D/lib232.sh
until grep -aq "P2_DONE" $O; do sleep 30; done
J=""; for s in e29_chain e29_load e31_s2_4750 e31_s2_4900 s29_swl12 j30_rel_3200 j30_rel_3450 cam32_s90 cam32_chain c30_calm; do J="$J $s:o $s:P"; done
for m in 60 120 20 real; do
  echo "F start $m $(date +%T) (reason: frame-rate mode is an editor launch argument)" >> $O
  relaunch f$m $m
  export WARM=1 MEMPROBE=1
  ab f$m "$J" $D/vars232.sh
  echo "F_DONE $m $(date +%T)" >> $O
done
echo "FALL_DONE $(date +%T)" >> $O
