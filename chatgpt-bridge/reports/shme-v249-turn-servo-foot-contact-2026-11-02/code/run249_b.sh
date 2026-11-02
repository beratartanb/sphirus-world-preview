#!/bin/bash
# run249_b.sh : V2.49 chain B = root position curves on the crops + capsule position servo (knob RM=1), verify, A/B 60 then real time
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V249_20261102; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
source $D/lib249.sh
tasklist 2>/dev/null | grep -qi UnrealEditor.exe || relaunch b0 60
V=/Game/GraceRanger/SHME/Animations/V248; CR=""; for s in L R; do for d in 090 135 180; do CR="$CR $V/SHM248_Jog_Start_Turn$s${d}_crop"; done; done
"$PY" Tools/SHME_V233_20261027/manifest233.py v249_rc --assets $CR | tail -1 | cut -c1-120 >> $O
SHME_KIND=write SHME_OWNER=v249 SHME_MANIFEST=$M/v249_rc.json bash $RUN $REQ/rootcurves_req.py v249rc 600 | grep -a 'ROOTCURVES249\|REFUSED\|WRITE_GUARD\|Error\|Traceback' > $D/data/rootcurves.out
echo "[rootcurves] $(cut -c1-700 $D/data/rootcurves.out)" >> $O
grep -q '"saved": 6' $D/data/rootcurves.out || { echo "RC_ABORT" >> $O; exit 1; }
"$PY" Tools/SHME_V233_20261027/manifest233.py v249_servo --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching | tail -1 | cut -c1-120 >> $O
SHME_KIND=write SHME_OWNER=v249 SHME_MANIFEST=$M/v249_servo.json bash $RUN $REQ/servo_req.py v249servo 1200 | grep -a 'SERVO249\|REFUSED\|WRITE_GUARD\|Error\|Traceback\|Assertion' > $D/data/servo_install.out
echo "[servo] $(cut -c1-900 $D/data/servo_install.out)" >> $O
grep -q '"saved": true' $D/data/servo_install.out || { echo "SERVO_ABORT" >> $O; exit 1; }
echo "[verify] $(SHME_KIND=measure SHME_OWNER=v249 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v249verify2 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*\|\"bad\": \[[^]]*\]' | tr '\n' ' ' | cut -c1-400)" >> $O
relaunch b60 60; WARM=1 ab b60 "j45_sl2:rm j45_sl2:o jstart:rm"
echo TB249_60 >> $O
relaunch breal real; WARM=1 ab breal "j45_sl2:rm j45_sl2:rm:2 j45_sl2:rm:3 j45_sl2:rm:4 j45_sl2:o j45_sl2:o:2"
echo TB249_DONE >> $O
