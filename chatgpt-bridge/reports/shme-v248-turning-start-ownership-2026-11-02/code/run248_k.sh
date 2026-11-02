#!/bin/bash
# run248_k.sh : V2.48 chain K = revert turnbind4 + post-turn loop ownership (turnbind5), verify, A/B 60 / real time / 30 FPS, captures
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V248_20261102; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
source $D/lib248.sh
for i in $(seq 1 40); do tasklist 2>/dev/null | grep -qi UnrealEditor.exe && break; sleep 5; done
"$PY" Tools/SHME_V233_20261027/manifest233.py v248_abp8 --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching | tail -1 | cut -c1-120 >> $O
echo "[turnbind5] $(SHME_KIND=write SHME_OWNER=v248 SHME_MANIFEST=$M/v248_abp8.json bash $RUN $REQ/turnbind5_req.py v248turnbind5 900 | grep -a 'TURNBIND248E\|REFUSED\|WRITE_GUARD\|Error\|Traceback\|Assertion' | cut -c1-700)" >> $O
grep -a "turnbind5\]" $O | grep -q '"saved": true' || { echo "BIND5_ABORT" >> $O; exit 1; }
echo "[verify8] $(SHME_KIND=measure SHME_OWNER=v248 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v248verify8 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*\|\"bad\": \[[^]]*\]' | tr '\n' ' ' | cut -c1-400)" >> $O
relaunch tk60 60; WARM=1 ab tk60 "j45_sl2:ts j45_sl2:o"
CAP_START=9.3 CAP_SECS=3.4 ab tkcap "j45_sl2:tsS j45_sl2:tsD j45_sl2:oD" $D/vars248_cap.sh
relaunch tkreal real; WARM=1 ab tkreal "j45_sl2:ts j45_sl2:ts:2 j45_sl2:ts:3 j45_sl2:ts:4 j45_sl2:o j45_sl2:o:2 jstart:ts taps:ts wstart:ts"
relaunch tk30 30; WARM=1 ab tk30 "j45_sl2:ts taps:ts wstart:ts jstart:ts j41_rl_p10:ts j41_rl_p10:o jstart:o"
echo TK248_DONE >> $O
