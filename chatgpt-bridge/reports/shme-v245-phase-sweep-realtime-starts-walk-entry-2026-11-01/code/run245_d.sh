#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V245_20261101; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
for i in $(seq 1 360); do grep -q SWEEP2_DONE $D/chain.out && break; sleep 20; done
source $D/lib245.sh
"$PY" Tools/SHME_V233_20261027/manifest233.py v245_walk --assets /Game/GraceRanger/Animations/LocomotionBehavior/A_LB_Walk_Fwd /Game/GraceRanger/Animations/LocomotionBehavior/PSD_LB_WalkLoops --new /Game/GraceRanger/SHME/Animations/V245/SHM245_Walk_Fwd | tail -1 | cut -c1-160 >> $O
WARM=1 ab wb "w42_id:o gait:o taps:o"
echo "[walkgen] $(SHME_KIND=write SHME_OWNER=v245 SHME_MANIFEST=$M/v245_walk.json bash $RUN $REQ/walk245_out.py v245wgen 600 | grep -a 'G245W \|REFUSED\|Error\|Traceback' | grep -o '"after".*' | cut -c1-400)" >> $O
echo "[wentry] $(SHME_KIND=write SHME_OWNER=v245 SHME_MANIFEST=$M/v245_walk.json bash $RUN $REQ/wentry_req.py v245wentry 600 | grep -a 'WENTRY245\|REFUSED\|WRITE_GUARD\|Error\|Traceback' | cut -c1-700)" >> $O
relaunch wa 30
WARM=1 ab wa "w42_id:o gait:o taps:o w42_id:o:2"
relaunch wareal real; WARM=1 ab wareal "w42_id:o gait:o"
relaunch waend 30
CAP_START=1.9 CAP_SECS=7.0 ab wacap "w42_id:oS w42_id:oD" $D/vars245_cap.sh
echo WALK5_DONE >> $O
