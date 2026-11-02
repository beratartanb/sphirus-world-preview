#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V247_20261102; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
source $D/lib247.sh
"$PY" Tools/SHME_V233_20261027/manifest233.py v247_rcrm --assets /Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/CharacterWorldFinal/WalkLoops/M_Ranger_Walk_Loop_F_PureForward_CWF | tail -1 | cut -c1-120 >> $O
echo "[rcost remove] $(SHME_KIND=write SHME_OWNER=v247 SHME_MANIFEST=$M/v247_rcrm.json bash $RUN $REQ/rcost_remove.py v247rcrm 300 | grep -a 'RCOST246\|REFUSED\|Error' | cut -c1-300)" >> $O
"$PY" Tools/SHME_V233_20261027/manifest233.py v247_dcrm --from Saved/Codex/SHME_V246_20261101/data/dense_fwd_clips.json | tail -1 | cut -c1-120 >> $O
echo "[dcost remove] $(SHME_KIND=write SHME_OWNER=v247 SHME_MANIFEST=$M/v247_dcrm.json bash $RUN $REQ/dcost_remove.py v247dcrm 600 | grep -a 'DCOST246\|REFUSED\|Error' | cut -c1-300)" >> $O
"$PY" Tools/SHME_V233_20261027/manifest233.py v247_abp --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching | tail -1 | cut -c1-120 >> $O
echo "[walkroute] $(SHME_KIND=write SHME_OWNER=v247 SHME_MANIFEST=$M/v247_abp.json bash $RUN $REQ/walkroute_req.py v247walkroute 900 | grep -a 'WALKROUTE247\|REFUSED\|WRITE_GUARD\|Error\|Traceback\|Assertion' | cut -c1-700)" >> $O
echo "[verify] $(SHME_KIND=measure SHME_OWNER=v247 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v247verify 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*')" >> $O
WARM=1 ab wr "w42_id:wr w42_id:o taps:wr gait:wr wdiag:wr wstart:wr w43_idle:wr w42_id:wr:2"
relaunch wrreal real; WARM=1 ab wrreal "w42_id:wr w42_id:wr:2 taps:wr wdiag:wr gait:wr"
relaunch wr60 60; WARM=1 ab wr60 "w42_id:wr taps:wr"
relaunch wrend 30
CAP_START=1.9 CAP_SECS=7.0 ab wrcap "w42_id:wrS w42_id:wrD w42_id:oS w42_id:oD" $D/vars247_cap.sh
echo WR247_DONE >> $O
