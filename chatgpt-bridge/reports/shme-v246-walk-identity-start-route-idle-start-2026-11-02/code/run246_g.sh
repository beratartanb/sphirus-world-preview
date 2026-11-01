#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V246_20261101; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
for i in $(seq 1 540); do grep -q DC2_DONE $D/chain.out && break; sleep 20; done
source $D/lib246.sh
"$PY" Tools/SHME_V233_20261027/manifest233.py v246_abpbk2 --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching | tail -1 | cut -c1-120 >> $O
export SHME_MANIFEST=$M/v246_abpbk2.json
WARM=1 ab in3 "taps:inrt jstart:inrt j40_rlw:inrt w43_idle:inrt taps:inrto"
relaunch in3real real; WARM=1 ab in3real "taps:inrt jstart:inrt"
relaunch in3end 30
echo "[verify3] $(SHME_KIND=measure SHME_OWNER=v246 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v246verify3 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*')" >> $O
echo IN3_DONE >> $O
