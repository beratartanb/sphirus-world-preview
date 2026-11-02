#!/bin/bash
# run248_h.sh : V2.48 chain H (consolidated) = both-direction turn DBs, signed Turn curves + lateral curve, V2.41 curve case restore,
# Delta sign patch, lateral velocity contract (component/ABP/pawn), verify, A/B 60 (+captures), real time, 30 FPS regressions
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V248_20261102; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
source $D/lib248.sh
J=/Game/GraceRanger/SHME/Animations/Starts/Jog; CL=""; for s in L R; do for d in 090 135 180; do CL="$CL $J/SHM_JogQ_af_Loco_Jog_Start_Turn$s${d}_${s}foot_AAMS"; done; done
"$PY" Tools/SHME_V233_20261027/manifest233.py v248_latvel3 --assets /Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching /Game/GraceRanger/BP_GR_Player /Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player | tail -1 | cut -c1-120 >> $O
echo "[latvel] $(SHME_KIND=write SHME_OWNER=v248 SHME_MANIFEST=$M/v248_latvel3.json bash $RUN $REQ/latvel_req.py v248latvel3 1200 | grep -a 'LATVEL248\|REFUSED\|WRITE_GUARD\|Error\|Traceback\|Assertion' | cut -c1-900)" >> $O
grep -a "latvel\]" $O | grep -q '"saved": true' || { echo "LATVEL_ABORT" >> $O; exit 1; }
echo "[verify5] $(SHME_KIND=measure SHME_OWNER=v248 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v248verify5c 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*\|\"bad\": \[[^]]*\]' | tr '\n' ' ' | cut -c1-400)" >> $O
relaunch th60 60; WARM=1 ab th60 "j45_sl:ts j45_sl2:ts j45_sl2:o j45_sl:o"
CAP_START=9.3 CAP_SECS=3.2 ab thcap "j45_sl:tsS j45_sl:tsD" $D/vars248_cap.sh
relaunch threal real; WARM=1 ab threal "j45_sl2:ts j45_sl2:ts:2 j45_sl2:ts:3 j45_sl2:ts:4 j45_sl2:o j45_sl2:o:2 j45_sl:ts j45_sl:ts:2 jstart:ts taps:ts wstart:ts"
relaunch th30 30; WARM=1 ab th30 "j45_sl:ts taps:ts wstart:ts jstart:ts w42_id:ts gait:ts j41_rl_p10:ts j45_sl2:ts"
echo TH248_DONE >> $O
