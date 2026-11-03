#!/bin/bash
# run251_e.sh : V2.51 chain E = crop entry block (only enterable in the first 0.25 s), verify, 60 FPS check of the 180/135 turning starts
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V251_20261103; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; source $D/lib251.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; V=/Game/GraceRanger/SHME/Animations/V248
until grep -q TD251_DONE $O; do sleep 20; done
relaunch e0 60
"$PY" Tools/SHME_V233_20261027/manifest233.py v251_cropblock --assets $V/SHM248_Jog_Start_TurnL090_crop $V/SHM248_Jog_Start_TurnL135_crop $V/SHM248_Jog_Start_TurnL180_crop $V/SHM248_Jog_Start_TurnR090_crop $V/SHM248_Jog_Start_TurnR135_crop $V/SHM248_Jog_Start_TurnR180_crop | tail -1 | cut -c1-100 >> $O
echo "[cropblock] $(SHME_KIND=write SHME_OWNER=v251 SHME_MANIFEST=$M/v251_cropblock.json bash $R $REQ/cropblock_req.py v251cropblock 900 2>&1 | grep -a 'CROPBLOCK251\|Traceback\|Error\|REFUSED' | cut -c1-400)" >> $O
relaunch e60 60; WARM=1 ab e60 "jstart:eAY j45_sl2:eAY jstart:o"
echo TE251_DONE >> $O
