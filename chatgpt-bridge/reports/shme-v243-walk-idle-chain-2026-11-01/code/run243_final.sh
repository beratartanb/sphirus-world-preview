#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V243_20261101; S=/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v243
for i in $(seq 1 60); do grep -q PROD3_DONE $D/chain.out && break; sleep 20; done
source $D/lib243.sh
echo "[final probe] $(SHME_KIND=measure SHME_OWNER=v243 bash Tools/SHME_V2_20261014/run_v2.sh $S/probe243_cdo.py v243probe2 300 | grep -a 'PROBE243\|REFUSED\|Error' | cut -c1-700)" >> $O
echo FINAL_DONE >> $O
