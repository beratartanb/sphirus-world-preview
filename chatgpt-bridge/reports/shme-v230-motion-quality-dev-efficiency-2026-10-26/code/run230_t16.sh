#!/bin/bash
# run230_t16.sh : same editor as T15 (idle guard installed, knob 0): release-time sweep of the jog reversal release -> re-press (S released
# 3.10..3.45 s after the move start, re-pressed 0.15 s later), production vs SHM230_IdleGuard 1.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V230_20261026; export O=$D/chain.out; source $D/lib230.sh
echo "T16 start $(date +%T)" >> $O; export WARM=0 MEMPROBE=1
J=""; for m in 3100 3150 3200 3250 3300 3350 3400 3450; do J="$J j30_rel_$m:o j30_rel_$m:ig"; done
ab t16 "$J" $D/vars230c.sh
echo "T16_DONE $(date +%T)" >> $O
