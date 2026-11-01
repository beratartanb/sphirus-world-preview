#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V245_20261101; RUN=Tools/SHME_V2_20261014/run_v2.sh
for i in $(seq 1 360); do grep -q OWN_DONE $D/chain.out && break; sleep 20; done
source $D/lib245.sh
echo "[verify] $(SHME_KIND=measure SHME_OWNER=v245 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v245verify 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*')" >> $O
relaunch prod 30
echo "[probe] $(SHME_KIND=measure SHME_OWNER=v245 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v243/probe243_cdo.py v245probe 300 | grep -a 'PROBE243' | grep -o '"dirty".*' | cut -c1-200)" >> $O
WARM=1 ab prod "w42_id:o gait:o taps:o j41_rl_p10:o j42_lr_p10:o w43_idle:o jstart:o wdiag:o"
echo PROD245_DONE >> $O
