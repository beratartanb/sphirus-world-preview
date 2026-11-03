#!/bin/bash
# run251_c.sh : V2.51 chain C = crop exit curve + TurnDone release (install), verify, 60 FPS A/B on the 135/180 turning starts
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V251_20261103; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; source $D/lib251.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; V=/Game/GraceRanger/SHME/Animations/V248; A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
until grep -q TB251_DONE $O; do sleep 20; done
relaunch c0 60
"$PY" Tools/SHME_V233_20261027/manifest233.py v251_exitcurve --assets $V/SHM248_Jog_Start_TurnL090_crop $V/SHM248_Jog_Start_TurnL135_crop $V/SHM248_Jog_Start_TurnL180_crop $V/SHM248_Jog_Start_TurnR090_crop $V/SHM248_Jog_Start_TurnR135_crop $V/SHM248_Jog_Start_TurnR180_crop | tail -1 | cut -c1-100 >> $O
echo "[exitcurve] $(SHME_KIND=write SHME_OWNER=v251 SHME_MANIFEST=$M/v251_exitcurve.json bash $R $REQ/exitcurve_req.py v251exitcurve 900 2>&1 | grep -a 'EXITCURVE251\|Traceback\|Error\|REFUSED' | cut -c1-500)" >> $O
"$PY" Tools/SHME_V233_20261027/manifest233.py v251_exitdone --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching | tail -1 | cut -c1-100 >> $O
echo "[exitdone] $(SHME_KIND=write SHME_OWNER=v251 SHME_MANIFEST=$M/v251_exitdone.json bash $R $REQ/exitdone_req.py v251exitdone 900 2>&1 | grep -a 'EXITDONE251\|Traceback\|Error\|REFUSED' | cut -c1-500)" >> $O
echo "[verify] $(SHME_KIND=measure SHME_OWNER=v251 bash $R /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v251verify1 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*\|\"bad\": \[[^]]*\]' | tr '\n' ' ' | cut -c1-300)" >> $O
relaunch c60 60; WARM=1 ab c60 "jstart:eAYLX j45_sl2:eAYLX jstart:eAYL"
echo TC251_DONE >> $O
