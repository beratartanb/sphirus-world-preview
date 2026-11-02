#!/bin/bash
# run248_n.sh : V2.48 chain N = trigger threshold 130 deg (SHM248_BackCos -0.64), verify, real-time + 30 FPS production confirmation
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V248_20261102; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
source $D/lib248.sh
until grep -q TJ248_DONE $O; do sleep 20; done
"$PY" Tools/SHME_V233_20261027/manifest233.py v248_backcos --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching | tail -1 | cut -c1-120 >> $O
echo "[backcos] $(SHME_KIND=write SHME_OWNER=v248 SHME_MANIFEST=$M/v248_backcos.json bash $RUN $REQ/backcos_req.py v248backcos 600 | grep -a 'BACKCOS248\|REFUSED\|WRITE_GUARD\|Error\|Traceback' | cut -c1-400)" >> $O
grep -a "backcos\]" $O | grep -q '"saved": true' || { echo "BACKCOS_ABORT" >> $O; exit 1; }
echo "[verify11] $(SHME_KIND=measure SHME_OWNER=v248 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v248verify11 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*\|\"bad\": \[[^]]*\]' | tr '\n' ' ' | cut -c1-400)" >> $O
relaunch prod2real real; WARM=1 ab prod2real "j45_sl2:o j45_sl2:o:2 j45_sl2:o:3 j45_sl2:o:4 j45_sl:o wstart:o"
relaunch prod2end 30; WARM=1 ab prod2 "j45_sl2:o j45_sl:o"
echo TN248_DONE >> $O
