#!/bin/bash
# run248_m.sh : V2.48 chain M = locomotion frame follows the turn (install248_loco), verify, A/B 60 (+captures), real time, 30 FPS (+ production pairs)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V248_20261102; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
JD="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/b2runner/jobs"
source $D/lib248.sh
for i in $(seq 1 30); do [ "$(ls $JD/*.py 2>/dev/null | wc -l)" = "0" ] && break; sleep 10; done; sleep 30
tasklist 2>/dev/null | grep -qi UnrealEditor.exe || relaunch tm0 60
"$PY" Tools/SHME_V233_20261027/manifest233.py v248_abp14 --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching | tail -1 | cut -c1-120 >> $O
echo "[loco] $(SHME_KIND=write SHME_OWNER=v248 SHME_MANIFEST=$M/v248_abp14.json bash $RUN $REQ/loco_req.py v248loco 900 | grep -a 'LOCO248\|REFUSED\|WRITE_GUARD\|Error\|Traceback\|Assertion' | cut -c1-600)" >> $O
grep -a "loco\]" $O | grep -q '"saved": true' || { echo "LOCO_ABORT" >> $O; exit 1; }
echo "[verify10] $(SHME_KIND=measure SHME_OWNER=v248 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v248verify10 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*\|\"bad\": \[[^]]*\]' | tr '\n' ' ' | cut -c1-400)" >> $O
relaunch tm60 60; WARM=1 ab tm60 "j45_sl2:ts j45_sl2:o j45_sl:ts"
CAP_START=9.3 CAP_SECS=3.4 ab tmcap "j45_sl2:tsS j45_sl2:tsD j45_sl2:oD" $D/vars248_cap.sh
relaunch tmreal real; WARM=1 ab tmreal "j45_sl2:ts j45_sl2:ts:2 j45_sl2:ts:3 j45_sl2:ts:4 j45_sl2:o j45_sl2:o:2 j45_sl:ts j45_sl:ts:2 jstart:ts taps:ts wstart:ts"
relaunch tm30 30; WARM=1 ab tm30 "j45_sl2:ts taps:ts wstart:ts jstart:ts jstart:o j41_rl_p10:ts j41_rl_p10:o w42_id:ts gait:ts"
echo TM248_DONE >> $O
