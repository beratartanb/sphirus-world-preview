#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V244_20261101; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; S2=/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad
for i in $(seq 1 360); do grep -q WALK2_DONE $D/chain.out && break; sleep 30; done
source $D/lib244.sh
echo "[promote lat4] $(date +%T)" >> $O
"$PY" Tools/SHME_V233_20261027/manifest233.py v244_prom --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching | tail -1 | cut -c1-160 >> $O
SHME_KIND=write SHME_OWNER=v244 SHME_MANIFEST=$M/v244_prom.json bash $RUN $REQ/promote_lat_req.py v244prom 600 | grep -a 'PROMOTE244\|REFUSED\|WRITE_GUARD\|Error' | cut -c1-700 >> $O
echo "[verify] $(SHME_KIND=measure SHME_OWNER=v244 bash $RUN $S2/v242/verify241_req.py v244verify 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*')" >> $O
relaunch fprod 30
echo "[probe] $(SHME_KIND=measure SHME_OWNER=v244 bash $RUN $S2/v243/probe243_cdo.py v244probe 300 | grep -a 'PROBE243' | cut -c1-400)" >> $O
WARM=1 ab prod "j41_rl_p04:o j41_rl_p10:o j42_lr_p10:o taps:o gait:o w42_id:o jstart:o wdiag:o j40_rlw:o w43_idle:o"
echo PROMOTE244_DONE >> $O
