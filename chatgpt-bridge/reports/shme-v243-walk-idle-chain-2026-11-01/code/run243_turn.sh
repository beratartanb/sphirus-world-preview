#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V243_20261101; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests
for i in $(seq 1 60); do n=$(ls Saved/Codex/SHME_V212_20261017/Reports/ | grep -c v243i4); [ "$n" -ge 2 ] && break; sleep 30; done; sleep 20
source $D/lib243.sh
"$PY" Tools/SHME_V233_20261027/manifest233.py v243_pawn1 --assets /Game/GraceRanger/BP_GR_Player /Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player | tail -1 >> $O
echo "[turnlook] $(SHME_KIND=write SHME_OWNER=v243 SHME_MANIFEST=$M/v243_pawn1.json bash Tools/SHME_V2_20261014/run_v2.sh /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v243/turnlook_req.py v243turnlook 600 | grep -a 'TURNLOOK243\|Error' | cut -c1-500)" >> $O
echo "[verify] $(SHME_KIND=measure SHME_OWNER=v243 bash Tools/SHME_V2_20261014/run_v2.sh /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v243verify1 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*')" >> $O
WARM=1 ab t1 "j41_rl_p04:latgl j41_rl_p10:latgl j42_lr_p10:latgl j41_rl_p04:o"
echo T1_DONE >> $O
