#!/bin/bash
# run248_d.sh : V2.48 chain D = V2.41 curve check/restore on the turn copies, hold-release patch, verify, A/B at 60 (deterministic turn case) +
# captures, real time x4, 30 FPS regressions
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V248_20261102; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
"$PY" Tools/SHME_V233_20261027/manifest233.py v248_abp4 --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching | tail -1 | cut -c1-120 >> $O
echo "[turnbind2] $(SHME_KIND=write SHME_OWNER=v248 SHME_MANIFEST=$M/v248_abp4.json bash $RUN $REQ/turnbind2_req.py v248turnbind2b 900 | grep -a 'TURNBIND248B\|REFUSED\|WRITE_GUARD\|Error\|Traceback\|Assertion' | cut -c1-700)" >> $O
grep -a "turnbind2\]" $O | grep -q '"saved": true' || { echo "BIND2_ABORT install not saved" >> $O; exit 1; }
echo "[verify3] $(SHME_KIND=measure SHME_OWNER=v248 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v248verify3b 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*\|\"bad\": \[[^]]*\]' | tr '\n' ' ' | cut -c1-500)" >> $O
relaunch tc60 60; WARM=1 ab tc60 "j45_sl:ts j45_sl:ts:2 j45_sl:o jstart:o"
CAP_START=9.3 CAP_SECS=3.2 ab tccap "j45_sl:tsS j45_sl:tsD j45_sl:oS j45_sl:oD" $D/vars248_cap.sh
relaunch tcreal real; WARM=1 ab tcreal "j45_sl:ts j45_sl:ts:2 j45_sl:ts:3 j45_sl:ts:4 j45_sl:o j45_sl:o:2 jstart:ts taps:ts wstart:ts"
relaunch tc30 30; WARM=1 ab tc30 "j45_sl:ts taps:ts wstart:ts jstart:ts w42_id:ts gait:ts j41_rl_p10:ts"
echo TC248_DONE >> $O
