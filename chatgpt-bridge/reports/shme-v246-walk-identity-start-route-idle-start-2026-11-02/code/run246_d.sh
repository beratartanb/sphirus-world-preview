#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V246_20261101; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
for i in $(seq 1 540); do grep -q LR246_DONE $D/chain.out && break; sleep 20; done
source $D/lib246.sh
echo "[dcost dry] $(SHME_KIND=measure SHME_OWNER=v246 bash $RUN $REQ/dcost_dry.py v246dcdry 300 | grep -a 'DCOST246\|REFUSED\|Error' | cut -c1-600)" >> $O
"$PY" Tools/SHME_V233_20261027/manifest233.py v246_dc --from $D/data/dense_fwd_clips.json | tail -1 | cut -c1-160 >> $O
echo "[dcost] $(SHME_KIND=write SHME_OWNER=v246 SHME_MANIFEST=$M/v246_dc.json bash $RUN $REQ/dcost_req.py v246dcost 600 | grep -a 'DCOST246\|REFUSED\|WRITE_GUARD\|Error' | cut -c1-600)" >> $O
WARM=1 ab dc "w42_id:o taps:o gait:o wdiag:o wstart:o w43_idle:o w42_id:o:2"
relaunch dcreal real; WARM=1 ab dcreal "w42_id:o taps:o w42_id:o:2"
relaunch dcend 30
CAP_START=1.9 CAP_SECS=7.0 ab dccap "w42_id:oS w42_id:oD" $D/vars246_cap.sh
echo DC246_DONE >> $O
