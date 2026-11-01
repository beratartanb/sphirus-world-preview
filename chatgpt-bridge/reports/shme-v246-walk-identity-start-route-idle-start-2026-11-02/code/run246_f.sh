#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V246_20261101; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
for i in $(seq 1 540); do grep -q IN2_DONE $D/chain.out && break; sleep 20; done
source $D/lib246.sh
"$PY" Tools/SHME_V233_20261027/manifest233.py v246_ddb --assets /Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/PSD_Dense_Stand_Walk_Loops | tail -1 | cut -c1-120 >> $O
echo "[saveddb] $(SHME_KIND=write SHME_OWNER=v246 SHME_MANIFEST=$M/v246_ddb.json bash $RUN $REQ/save_densedb.py v246saveddb 300 | grep -a 'SAVEDDB246\|REFUSED\|WRITE_GUARD\|Error' | cut -c1-300)" >> $O
relaunch dc2 30
WARM=1 ab dc2 "w42_id:o taps:o gait:o wdiag:o w43_idle:o w42_id:o:2"
relaunch dc2real real; WARM=1 ab dc2real "w42_id:o taps:o w42_id:o:2"
relaunch dc2end 30
CAP_START=1.9 CAP_SECS=7.0 ab dc2cap "w42_id:oS w42_id:oD" $D/vars246_cap.sh
echo DC2_DONE >> $O
