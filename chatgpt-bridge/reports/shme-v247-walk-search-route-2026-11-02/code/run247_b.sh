#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V247_20261102; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
for i in $(seq 1 540); do grep -q WR247_DONE $D/chain.out && break; sleep 20; done
source $D/lib247.sh
"$PY" Tools/SHME_V233_20261027/manifest233.py v247_prom --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching | tail -1 | cut -c1-120 >> $O
echo "[promote] $(SHME_KIND=write SHME_OWNER=v247 SHME_MANIFEST=$M/v247_prom.json bash $RUN $REQ/promote_req.py v247prom 600 | grep -a 'PROMOTE247\|REFUSED\|Error' | cut -c1-500)" >> $O
echo "[verify] $(SHME_KIND=measure SHME_OWNER=v247 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v247verify2 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*')" >> $O
relaunch prod 30
echo "[probe] $(SHME_KIND=measure SHME_OWNER=v247 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v243/probe243_cdo.py v247probe 300 | grep -a 'PROBE243' | grep -o '"dirty".*' | cut -c1-120)" >> $O
WARM=1 ab prod "w42_id:o taps:o gait:o wdiag:o wstart:o w43_idle:o j41_rl_p10:o j42_lr_p10:o jstart:o j40_rlw:o"
relaunch prodreal real; WARM=1 ab prodreal "w42_id:o w42_id:o:2 taps:o wdiag:o"
relaunch prodend 30
echo "[verify3] $(SHME_KIND=measure SHME_OWNER=v247 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v247verify3 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*')" >> $O
echo PROD247_DONE >> $O
