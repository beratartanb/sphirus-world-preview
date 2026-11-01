#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V242_20261101; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests
source $D/lib242.sh
"$PY" Tools/SHME_V233_20261027/manifest233.py v242_abp6 --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching | tail -1 >> $O
echo "[idle hook v2] $(SHME_KIND=write SHME_OWNER=v242 SHME_MANIFEST=$M/v242_abp6.json bash Tools/SHME_V2_20261014/run_v2.sh /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/idledb2_req.py v242idlehook4 600 | grep -a 'IDLEDB242B\|Error' | cut -c1-600)" >> $O
echo "[verify] $(SHME_KIND=measure SHME_OWNER=v242 bash Tools/SHME_V2_20261014/run_v2.sh /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v242verify8 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*')" >> $O
WARM=1 ab r5 "w42_id:idl"
CAP_START=5.2 CAP_SECS=9.0 ab r5cap "w42_id:idlS w42_id:idlG w42_id:oS w42_id:oG" $D/vars242_cap.sh
CAP_START=10.8 CAP_SECS=3.2 ab r5lat "j41_rl_p04:latgS j41_rl_p04:latgG j41_rl_p04:oG" $D/vars242_cap.sh
echo POST3_242_DONE >> $O
