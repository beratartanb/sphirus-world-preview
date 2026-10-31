#!/bin/bash
# V2.41 N: the fixed side camera of j40_wall sits behind the wall (frames show only the wall) -> wall from the game camera
source Saved/Codex/SHME_V241_20261031/lib241.sh; O=$D/chain.out
export SHME_MANIFEST=$D/checkpoint/manifests/aopre.json
until grep -q "^M_DONE" $O; do sleep 20; done
echo "N start $(date +%T)" >> $O
WARM=0 ab cap2 "j40_wall:oG j40_wall:tkhaG" $D/vars241_cap.sh
echo "N_DONE $(date +%T)" >> $O
