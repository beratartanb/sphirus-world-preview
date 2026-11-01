#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V245_20261101; RUN=Tools/SHME_V2_20261014/run_v2.sh
for i in $(seq 1 360); do grep -q PROD245_DONE $D/chain.out && break; sleep 20; done
source $D/lib245.sh
echo "[verify2] $(SHME_KIND=measure SHME_OWNER=v245 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v245verify2 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*')" >> $O
echo VERIFY245_DONE >> $O
