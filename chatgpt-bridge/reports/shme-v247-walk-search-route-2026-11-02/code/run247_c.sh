#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V247_20261102; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
sleep 40
source $D/lib247.sh
"$PY" Tools/SHME_V233_20261027/manifest233.py v247_abp4 --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching | tail -1 | cut -c1-120 >> $O
echo "[walkroute2] $(SHME_KIND=write SHME_OWNER=v247 SHME_MANIFEST=$M/v247_abp4.json bash $RUN $REQ/walkroute2_req.py v247walkroute2 900 | grep -a 'WALKROUTE247B\|REFUSED\|WRITE_GUARD\|Error\|Traceback\|Assertion' | cut -c1-600)" >> $O
echo "[verify] $(SHME_KIND=measure SHME_OWNER=v247 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v247verifyb 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*')" >> $O
WARM=1 ab wr2 "w42_id:wr w42_id:wr:2 taps:wr gait:wr wdiag:wr w43_idle:wr wstart:wr"
relaunch wr2real real; WARM=1 ab wr2real "w42_id:wr w42_id:wr:2 w42_id:wr:3 taps:wr gait:wr wdiag:wr"
relaunch wr260 60; WARM=1 ab wr260 "w42_id:wr taps:wr"
relaunch wr2end 30
CAP_START=1.9 CAP_SECS=7.0 ab wr2cap "w42_id:wrS w42_id:wrD w42_id:oS w42_id:oD" $D/vars247_cap.sh
echo WR2_DONE >> $O
