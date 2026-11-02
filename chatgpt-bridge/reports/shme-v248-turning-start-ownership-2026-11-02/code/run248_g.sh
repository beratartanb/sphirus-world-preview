#!/bin/bash
# run248_g.sh : V2.48 chain G = lateral clip-bound velocity (curve + component var + ABP + pawn), verify, A/B 60 / real time, captures
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V248_20261102; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
source $D/lib248.sh
until grep -q TF248_DONE $O; do sleep 20; done
J=/Game/GraceRanger/SHME/Animations/Starts/Jog; CL=""; for s in L R; do for d in 090 135 180; do CL="$CL $J/SHM_JogQ_af_Loco_Jog_Start_Turn$s${d}_${s}foot_AAMS"; done; done
"$PY" Tools/SHME_V233_20261027/manifest233.py v248_lat --assets $CL | tail -1 | cut -c1-120 >> $O
echo "[latcurve] $(SHME_KIND=write SHME_OWNER=v248 SHME_MANIFEST=$M/v248_lat.json bash $RUN $REQ/latcurve_req.py v248latcurve 600 | grep -a 'LATCURVE248\|REFUSED\|WRITE_GUARD\|Error\|Traceback' | grep -o '"saved": [0-9]*\|"vl_samples": \[[^]]*\]\|REFUSED.*\|WRITE_GUARD.*\|Error.*\|Traceback.*' | head -8 | tr '\n' ' ' | cut -c1-600)" >> $O
grep -a "latcurve\]" $O | grep -q '"saved": 6' || { echo "LAT_ABORT curves not saved" >> $O; exit 1; }
"$PY" Tools/SHME_V233_20261027/manifest233.py v248_latvel --assets /Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching /Game/GraceRanger/BP_GR_Player /Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player | tail -1 | cut -c1-120 >> $O
echo "[latvel] $(SHME_KIND=write SHME_OWNER=v248 SHME_MANIFEST=$M/v248_latvel.json bash $RUN $REQ/latvel_req.py v248latvel 1200 | grep -a 'LATVEL248\|REFUSED\|WRITE_GUARD\|Error\|Traceback\|Assertion' | cut -c1-900)" >> $O
grep -a "latvel\]" $O | grep -q '"saved": true' || { echo "LATVEL_ABORT install not saved" >> $O; exit 1; }
echo "[verify4] $(SHME_KIND=measure SHME_OWNER=v248 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v248verify4 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*\|\"bad\": \[[^]]*\]' | tr '\n' ' ' | cut -c1-400)" >> $O
relaunch tg60 60; WARM=1 ab tg60 "j45_sl:ts j45_sl2:ts j45_sl2:o"
CAP_START=9.3 CAP_SECS=3.2 ab tgcap "j45_sl:tsS j45_sl:tsD" $D/vars248_cap.sh
relaunch tgreal real; WARM=1 ab tgreal "j45_sl2:ts j45_sl2:ts:2 j45_sl2:ts:3 j45_sl:ts j45_sl:ts:2 jstart:ts taps:ts wstart:ts"
relaunch tg30 30; WARM=1 ab tg30 "j45_sl:ts taps:ts wstart:ts jstart:ts w42_id:ts gait:ts j41_rl_p10:ts j45_sl2:ts"
echo TG248_DONE >> $O
