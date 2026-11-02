#!/bin/bash
# run249_n.sh : V2.49 chain N = rest gate for the turning-start owner (knob RM), verify, check at 30 / real / 60
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V249_20261102; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
source $D/lib249.sh
until grep -q TL249_DONE $O; do sleep 20; done
"$PY" Tools/SHME_V233_20261027/manifest233.py v249_restgate --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching | tail -1 | cut -c1-120 >> $O
SHME_KIND=write SHME_OWNER=v249 SHME_MANIFEST=$M/v249_restgate.json bash $RUN $REQ/restgate_req.py v249restgate 900 | grep -a 'RESTGATE249\|REFUSED\|WRITE_GUARD\|Error\|Traceback\|Assertion' > $D/data/restgate_install.out
echo "[restgate] $(cut -c1-500 $D/data/restgate_install.out)" >> $O
grep -q '"saved": true' $D/data/restgate_install.out || { echo "RG_ABORT" >> $O; exit 1; }
relaunch n30 30
echo "[verify] $(SHME_KIND=measure SHME_OWNER=v249 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v249verify9 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*\|\"bad\": \[[^]]*\]' | tr '\n' ' ' | cut -c1-400)" >> $O
WARM=1 ab n30 "j41_rl_p10:rmh j40_rlw:rmh j45_sl2:rmh jstart:rmh taps:rmh"
relaunch nreal real; WARM=1 ab nreal "j45_sl2:rmh j45_sl2:rmh:2 j45_sl2:rmh:3 j41_rl_p10:rmh jstart:rmh"
relaunch n60 60; WARM=1 ab n60 "j45_sl2:rmh jstart:rmh"
echo TN249_DONE >> $O
