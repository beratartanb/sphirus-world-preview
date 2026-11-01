#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V246_20261101; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
source $D/lib246.sh
: wb done
: manifest done
echo "[rcost] $(SHME_KIND=write SHME_OWNER=v246 SHME_MANIFEST=$M/v246_rc.json bash $RUN $REQ/rcost_req.py v246rcost 300 | grep -a 'RCOST246\|REFUSED\|WRITE_GUARD\|Error' | cut -c1-500)" >> $O
WARM=1 ab wa "w42_id:o gait:o taps:o wdiag:o wstart:o w43_idle:o"
relaunch rcreal real; WARM=1 ab rcreal "w42_id:o w42_id:o:2 wdiag:o gait:o"
relaunch rcend 30
CAP_START=1.9 CAP_SECS=7.0 ab rccap "w42_id:oS w42_id:oD" $D/vars246_cap.sh
echo RC246_DONE >> $O
