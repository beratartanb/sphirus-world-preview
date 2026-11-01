#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V246_20261101; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests
for i in $(seq 1 540); do grep -q DC246_DONE $D/chain.out && break; sleep 20; done
source $D/lib246.sh
export SHME_MANIFEST=$M/v246_abpbk.json
WARM=1 ab in2 "taps:inrt jstart:inrt j40_rlw:inrt w43_idle:inrt taps:inrto jstart:inrto"
relaunch in2real real; WARM=1 ab in2real "taps:inrt jstart:inrt taps:inrt:2"
relaunch in2end 30
echo IN2_DONE >> $O
