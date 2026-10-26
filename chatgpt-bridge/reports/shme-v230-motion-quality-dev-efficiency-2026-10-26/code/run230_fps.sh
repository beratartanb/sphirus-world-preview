#!/bin/bash
# run230_fps.sh : V2.30 production at fixed 20 / 60 / 120 FPS (same input times) on the low-speed reversal, effort chain, sprint 180 and jog
# reversal scenarios. Waits for CAP_DONE / CAP_FAILED (distinct markers, no stale marker in this chain.out).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V230_20261026; export O=$D/chain.out
until grep -aq "CAP_DONE\|CAP_FAILED" $O; do sleep 30; done
source $D/lib230.sh; echo "FPS start $(date +%T)" >> $O
for F in 20 60 120; do relaunch h$F $F; export WARM=1 MEMPROBE=1
  ab h$F "s29_swl14:o j30_slow:o e29_chain:o s29_cam:o j24_dbl:o e29_load:o" $D/vars230c.sh; done
echo "FPS_DONE $(date +%T)" >> $O
