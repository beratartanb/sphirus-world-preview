#!/bin/bash
# run232_iso.sh : V2.32 ISO (after FALL_DONE): owner of the two P regressions (c29_combo, j30_rel_3450) - fixed 30 fresh editor
# (reason: the FPS chain ends in a real-time editor), o / fg / bfxl / Pnf / P interleaved, 2 repeats.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V232_20261027; export O=$D/chain.out; source $D/lib232.sh
until grep -aq "FALL_DONE" $O; do sleep 30; done
echo "ISO start $(date +%T) (reason: fixed-30 editor for the regression owner isolation)" >> $O
relaunch iso 30
export WARM=1 MEMPROBE=1
J=""; for s in c29_combo j30_rel_3450 j30_slow a29_angb; do for rp in 1 2; do for v in o fg bfxl Pnf P; do J="$J $s:$v:$rp"; done; done; done
ab iso "$J" $D/vars232.sh
echo "ISO_DONE $(date +%T)" >> $O
