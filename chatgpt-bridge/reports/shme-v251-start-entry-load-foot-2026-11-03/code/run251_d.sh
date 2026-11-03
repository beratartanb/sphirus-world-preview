#!/bin/bash
# run251_d.sh : V2.51 chain D = relaxed-leg support curve on the weighted idle + start latch step 2, verify, weighted idle A/B at 30 / 60
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V251_20261103; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; source $D/lib251.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
until grep -q TC251_DONE $O; do sleep 20; done
relaunch d0 60
echo "[idlesup_dry] $(SHME_KIND=measure SHME_OWNER=v251 bash $R $REQ/idlesup_dry_req.py v251isdry 600 2>&1 | grep -a 'IDLESUP251\|Traceback\|Error' | cut -c1-500)" >> $O
CL=$(grep -a "idlesup_dry\]" $O | tail -1 | grep -o '"SHM[A-Za-z0-9_]*": {"nf' | sed 's/": {"nf//; s/"//')
ARGS=""; for c in $CL; do P=$(find Content/GraceRanger -name "$c.uasset" | head -1 | sed 's#^Content#/Game#; s#\.uasset$##'); ARGS="$ARGS $P"; done
echo "[idlesup_assets] $ARGS" >> $O
"$PY" Tools/SHME_V233_20261027/manifest233.py v251_idlesup --assets $ARGS | tail -1 | cut -c1-100 >> $O
echo "[idlesup] $(SHME_KIND=write SHME_OWNER=v251 SHME_MANIFEST=$M/v251_idlesup.json bash $R $REQ/idlesup_write_req.py v251iswrite 900 2>&1 | grep -a 'IDLESUP251\|Traceback\|Error\|REFUSED' | cut -c1-500)" >> $O
"$PY" Tools/SHME_V233_20261027/manifest233.py v251_startload2 --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching | tail -1 | cut -c1-100 >> $O
echo "[startload2] $(SHME_KIND=write SHME_OWNER=v251 SHME_MANIFEST=$M/v251_startload2.json bash $R $REQ/startload2_req.py v251sl2 900 2>&1 | grep -a 'STARTLOAD2_251\|Traceback\|Error\|REFUSED' | cut -c1-500)" >> $O
echo "[verify] $(SHME_KIND=measure SHME_OWNER=v251 bash $R /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v251verify2 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*\|\"bad\": \[[^]]*\]' | tr '\n' ' ' | cut -c1-300)" >> $O
relaunch d30 30; WARM=1 ab d30 "w42_id:oiL gait:oiL wstart:oiL taps:oiL w43_idle:oiL j45_sl2:oiL jstart:oiL w42_id:eAYL"
relaunch d60 60; WARM=1 ab d60 "w42_id:oiL gait:oiL wstart:oiL taps:oiL"
echo TD251_DONE >> $O
