#!/bin/bash
# vids_shme4.sh: re-shoot the seven acceptance videos with the corrected encoder (mkvid.py crop offset). The shme2/shme3
# mp4s were encoded with the crop rect off-centre (left ~200 px / top ~60 px of the game view missing); the raw PNGs
# were deleted after encoding, so the set is recorded again. Relaunch first (PIE ran since the last relaunch).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
PR=Saved/Codex/Day_20261107/vids4_progress.txt; : > $PR
log(){ echo "$(date +%H:%M:%S) $*" | tee -a $PR; }
RL(){ for i in 1 2 3; do R=$(bash Tools/Embodied_20261105/relaunch.sh emb_$1$i 2>&1 | tail -1); log "RELAUNCH $R"; [[ "$R" != STOP_* ]] && break; done; }
RL 458; log START
bash Tools/Day_20261107/vids_shme2.sh shme4 2>&1 | tee -a $PR
log END
