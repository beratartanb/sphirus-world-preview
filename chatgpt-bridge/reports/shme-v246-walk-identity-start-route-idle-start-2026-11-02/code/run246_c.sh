#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V246_20261101; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; S2=/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad
for i in $(seq 1 360); do grep -q IN246_DONE $D/chain.out && break; sleep 20; done
source $D/lib246.sh
"$PY" Tools/SHME_V233_20261027/manifest233.py v246_abp --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching | tail -1 | cut -c1-120 >> $O
"$PY" Tools/SHME_V233_20261027/manifest233.py v246_pawn --assets /Game/GraceRanger/BP_GR_Player /Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player | tail -1 | cut -c1-120 >> $O
echo "[lookroute] $(SHME_KIND=write SHME_OWNER=v246 SHME_MANIFEST=$M/v246_abp.json bash $RUN $REQ/lookroute_req.py v246lookroute 900 | grep -a 'LOOKROUTE246\|REFUSED\|WRITE_GUARD\|Error\|Traceback' | cut -c1-700)" >> $O
echo "[lookyaw] $(SHME_KIND=write SHME_OWNER=v246 SHME_MANIFEST=$M/v246_pawn.json bash $RUN $REQ/lookyaw_req.py v246lookyaw 900 | grep -a 'LOOKYAW246\|REFUSED\|WRITE_GUARD\|Error\|Traceback' | cut -c1-700)" >> $O
echo "[verify] $(SHME_KIND=measure SHME_OWNER=v246 bash $RUN $S2/v242/verify241_req.py v246verify 300 | tail -1 | grep -o '"ALL_OK": [a-z]*')" >> $O
WARM=1 ab lr "j45_sl:lr j45_sl:o jstart:lr wstart:lr j41_rl_p04:lr j42_lr_p10:lr taps:lr"
relaunch lrreal real; WARM=1 ab lrreal "j45_sl:lr j45_sl:lr:2 j45_sl:lr:3 j45_sl:o j45_sl:o:2"
relaunch lrend 30
echo LR246_DONE >> $O
