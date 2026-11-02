#!/bin/bash
# run248_i.sh : V2.48 chain I = contract ownership during the turning-start clip (turnbind4), verify, A/B 60 (+captures of j45_sl2), real time, 30 FPS
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V248_20261102; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
source $D/lib248.sh
until grep -q TH248_DONE $O; do sleep 20; done
"$PY" Tools/SHME_V233_20261027/manifest233.py v248_abp7 --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching | tail -1 | cut -c1-120 >> $O
echo "[turnbind4] $(SHME_KIND=write SHME_OWNER=v248 SHME_MANIFEST=$M/v248_abp7.json bash $RUN $REQ/turnbind4_req.py v248turnbind4 900 | grep -a 'TURNBIND248D\|REFUSED\|WRITE_GUARD\|Error\|Traceback\|Assertion' | cut -c1-600)" >> $O
grep -a "turnbind4\]" $O | grep -q '"saved": true' || { echo "BIND4_ABORT" >> $O; exit 1; }
echo "[verify6] $(SHME_KIND=measure SHME_OWNER=v248 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v248verify6 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*\|\"bad\": \[[^]]*\]' | tr '\n' ' ' | cut -c1-400)" >> $O
relaunch ti60 60; WARM=1 ab ti60 "j45_sl2:ts j45_sl:ts"
CAP_START=9.3 CAP_SECS=3.4 ab ticap "j45_sl2:tsS j45_sl2:tsD j45_sl2:oD" $D/vars248_cap.sh
relaunch tireal real; WARM=1 ab tireal "j45_sl2:ts j45_sl2:ts:2 j45_sl2:ts:3 j45_sl2:ts:4 j45_sl2:o j45_sl2:o:2 j45_sl:ts j45_sl:ts:2 jstart:ts taps:ts wstart:ts"
relaunch ti30 30; WARM=1 ab ti30 "j45_sl:ts taps:ts wstart:ts jstart:ts w42_id:ts gait:ts j41_rl_p10:ts j45_sl2:ts"
echo TI248_DONE >> $O
