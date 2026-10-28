#!/bin/bash
# run234_b5.sh : V2.34 B5 (same editor): straight steady sprint / jog upper-body attitude o vs calm candidate sc vs ablations (2 rep).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V234_20261028; export O=$D/chain.out; source $D/lib234.sh
until grep -aq "^B4_DONE" $O; do sleep 20; done
echo "B5 start $(date +%T)" >> $O
export WARM=0 MEMPROBE=1
ab b5 "s34_straight:o:1 s34_straight:sc:1 s34_straight:o:2 s34_straight:sc:2 s34_straight:scPBI:1 s34_straight:scFP:1 s34_straight:scSS:1 j34_straight:o:1 j34_straight:sc:1" $D/vars234.sh
echo "B5_DONE $(date +%T)" >> $O
