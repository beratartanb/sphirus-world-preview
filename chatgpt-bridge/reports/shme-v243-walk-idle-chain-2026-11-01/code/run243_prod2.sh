#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V243_20261101; S=/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v243
for i in $(seq 1 60); do grep -q PROMOTE_DONE $D/chain.out && break; sleep 20; done
source $D/lib243.sh
echo "[probe] $(SHME_KIND=measure SHME_OWNER=v243 bash Tools/SHME_V2_20261014/run_v2.sh $S/probe243_cdo.py v243probe 300 | grep -a 'PROBE243\|REFUSED\|Error' | cut -c1-700)" >> $O
WARM=1 ab prod2 "j41_rl_p04:o j41_rl_p10:o j42_lr_p10:o wdiag:o wstart:o jstart:o taps:o w42_id:o"
echo PROD2_DONE >> $O
