#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V243_20261101; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests
for i in $(seq 1 120); do grep -q T4_DONE $D/chain.out 2>/dev/null && break; sleep 30; done; sleep 10
source $D/lib243.sh
echo "[idle2] $(SHME_KIND=write SHME_OWNER=v243 SHME_MANIFEST=$M/v243_idle2.json bash Tools/SHME_V2_20261014/run_v2.sh /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v243/gidle2.py v243gidle2 600 | grep -a 'G242I' | grep -o '\"saved\": [a-z]*\|\"frames\": [0-9]*' | tr '\n' ' ')" >> $O
echo "[idle2 DB] $(SHME_KIND=write SHME_OWNER=v243 SHME_MANIFEST=$M/v243_idle2.json bash Tools/SHME_V2_20261014/run_v2.sh /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v243/idb2_req.py v243idb2 600 | grep -a -c 'IDB242 ')" >> $O
WARM=1 ab attr "taps:latgl gait:latgl j40_rlw:latgl taps:og gait:og j40_rlw:og taps:idlg2 gait:idlg2 j40_rlw:idlg2 jstart:idlg2 w43_idle:idlg2"
echo ATTR243_DONE >> $O
