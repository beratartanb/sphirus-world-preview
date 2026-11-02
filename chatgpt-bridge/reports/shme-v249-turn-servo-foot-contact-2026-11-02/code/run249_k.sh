#!/bin/bash
# run249_k.sh : V2.49 chain K = turn-end latch + |T| hold fix (knob RM), verify, candidate check at 60 / real / 30
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V249_20261102; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
source $D/lib249.sh
until grep -q TJ249_DONE $O; do sleep 20; done
"$PY" Tools/SHME_V233_20261027/manifest233.py v249_turndone --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching | tail -1 | cut -c1-120 >> $O
SHME_KIND=write SHME_OWNER=v249 SHME_MANIFEST=$M/v249_turndone.json bash $RUN $REQ/turndone_req.py v249turndone 900 | grep -a 'TURNDONE249\|REFUSED\|WRITE_GUARD\|Error\|Traceback\|Assertion' > $D/data/turndone_install.out
echo "[turndone] $(cut -c1-500 $D/data/turndone_install.out)" >> $O
grep -q '"saved": true' $D/data/turndone_install.out || { echo "TD_ABORT" >> $O; exit 1; }
echo "[verify] $(SHME_KIND=measure SHME_OWNER=v249 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v249verify7 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*\|\"bad\": \[[^]]*\]' | tr '\n' ' ' | cut -c1-400)" >> $O
relaunch k60 60; WARM=1 ab k60 "j45_sl2:rm jstart:rm j40_rlw:rmi"
relaunch kreal real; WARM=1 ab kreal "j45_sl2:rm j45_sl2:rm:2 j45_sl2:rm:3 jstart:rm j40_rlw:rmi"
relaunch k30 30; WARM=1 ab k30 "j45_sl2:rm jstart:rm j40_rlw:rmi j41_rl_p10:rm"
echo TK249_DONE >> $O
