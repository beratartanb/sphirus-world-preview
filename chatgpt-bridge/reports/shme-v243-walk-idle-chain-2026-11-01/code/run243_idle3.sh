#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V243_20261101; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
S=/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v243
source $D/lib243.sh
"$PY" Tools/SHME_V233_20261027/manifest233.py v243_idle3 --assets /Game/GraceRanger/SHME/Animations/V242/SHM243_Idle_Weighted2 /Game/GraceRanger/SHME/Animations/V242/PSD_SHM243_Idle --new /Game/GraceRanger/SHME/Animations/V242/PSD_SHM242_IdleB | tail -1 >> $O
SHME_KIND=write SHME_OWNER=v243 SHME_MANIFEST=$M/v243_idle3.json bash Tools/SHME_V2_20261014/run_v2.sh $S/idb3_req.py v243idb3 600 | grep -a 'IDB242 \|DEL243\|REFUSED\|WRITE_GUARD\|Error' | cut -c1-600 >> $O
WARM=1 ab idle3 "taps:idlg3 gait:idlg3 j40_rlw:idlg3 jstart:idlg3 jstart:og w43_idle:idlg3 w42_id:idlg3"
ab idle3cap "w43_idle:idlg3D w43_idle:idlg3S" $D/vars243_cap.sh
echo IDLE3_DONE >> $O
