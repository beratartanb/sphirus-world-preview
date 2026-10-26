#!/bin/bash
# V2.29 t2: isolate the owner of the sprint-reversal upper-body spin (s29_cam: spine_03 turns 360 deg against the pelvis in 6 frames)
source "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V229_20261025/lib229.sh"
until grep -q "T1 DONE" $O; do sleep 20; done
echo "T2 START $(date +%T)" >> $O
ab t2 "s29_cam:oOW s29_cam:oPBI s29_cam:oSCR s29_cam:oDR s29_cam:oRAW s29_cam:oSW s29_cam:o"
echo "T2 DONE $(date +%T)" >> $O
# read-only graph dumps (current GR / PBI / ABP) for the effort and spin owners
bash $R Tools/SHME_V229_20261025/dump_bp229.py dump_bp229 900 | grep -a "DIRDUMP\|Error" | tail -2 >> $O
bash $R Tools/SHME_V229_20261025/dump_abp229.py dump_abp229 900 | grep -a "DIRDUMP\|Error" | tail -2 >> $O
echo "T2 DUMPS_DONE $(date +%T)" >> $O
