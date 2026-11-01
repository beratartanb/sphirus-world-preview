#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V244_20261101; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
for i in $(seq 1 120); do grep -q FPS244_DONE $D/chain.out && break; sleep 30; done
source $D/lib244.sh
"$PY" Tools/SHME_V233_20261027/manifest233.py v244_walkbk --assets /Game/GraceRanger/Animations/LocomotionBehavior/A_LB_Walk_Fwd | tail -1 | cut -c1-160 >> $O
export SHME_MANIFEST=$M/v244_walkbk.json
echo "[walkdry] $(SHME_KIND=measure SHME_OWNER=v244 bash $RUN $REQ/walk_dry.py v244walkdry 300 | grep -a 'G244W \|REFUSED\|Error\|Traceback' | cut -c1-900)" >> $O
WARM=1 ab walk "w42_id:walk4 gait:walk4 w42_id:o"
CAP_START=1.9 CAP_SECS=7.0 ab walkcap "w42_id:walk4S w42_id:oS w42_id:walk4D w42_id:oD" $D/vars244_cap.sh
echo WALK244_DONE >> $O
