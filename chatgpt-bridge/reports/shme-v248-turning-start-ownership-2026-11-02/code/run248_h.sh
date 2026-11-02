#!/bin/bash
# run248_h.sh : V2.48 chain H (consolidated) = both-direction turn DBs, signed Turn curves + lateral curve, V2.41 curve case restore,
# Delta sign patch, lateral velocity contract (component/ABP/pawn), verify, A/B 60 (+captures), real time, 30 FPS regressions
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V248_20261102; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
source $D/lib248.sh
J=/Game/GraceRanger/SHME/Animations/Starts/Jog; CL=""; for s in L R; do for d in 090 135 180; do CL="$CL $J/SHM_JogQ_af_Loco_Jog_Start_Turn$s${d}_${s}foot_AAMS"; done; done
"$PY" Tools/SHME_V233_20261027/manifest233.py v248_tdb2 --from $D/data/turnstart_clips.json --assets $CL /Game/GraceRanger/SHME/Animations/V248/PSD_SHM248_JogStartT_L /Game/GraceRanger/SHME/Animations/V248/PSD_SHM248_JogStartT_R | tail -1 | cut -c1-120 >> $O
echo "[tdb v2] $(SHME_KIND=write SHME_OWNER=v248 SHME_MANIFEST=$M/v248_tdb2.json bash $RUN $REQ/tdb_build_req.py v248tdb2 900 | grep -a 'DB248\|REFUSED\|WRITE_GUARD\|Error\|Traceback\|Assertion' | grep -o '"entries": \[[^]]*\]\|REFUSED.*\|WRITE_GUARD.*\|Error.*\|Traceback.*' | tr '\n' ' ' | cut -c1-1200)" >> $O
"$PY" Tools/SHME_V233_20261027/manifest233.py v248_curves2 --assets $CL | tail -1 | cut -c1-120 >> $O
echo "[curves v2] $(SHME_KIND=write SHME_OWNER=v248 SHME_MANIFEST=$M/v248_curves2.json bash $RUN $REQ/curves_write_req.py v248curves2 600 | grep -a 'TURNCURVES248\|REFUSED\|WRITE_GUARD\|Error\|Traceback' | grep -o '"saved": [0-9]*\|"turn_samples": \[[^]]*\]\|REFUSED.*\|WRITE_GUARD.*\|Error.*\|Traceback.*' | head -7 | tr '\n' ' ' | cut -c1-600)" >> $O
echo "[latcurve] $(SHME_KIND=write SHME_OWNER=v248 SHME_MANIFEST=$M/v248_curves2.json bash $RUN $REQ/latcurve_req.py v248latcurve 600 | grep -a 'LATCURVE248\|REFUSED\|WRITE_GUARD\|Error\|Traceback' | grep -o '"saved": [0-9]*\|"vl_samples": \[[^]]*\]\|REFUSED.*\|WRITE_GUARD.*\|Error.*\|Traceback.*' | head -7 | tr '\n' ' ' | cut -c1-600)" >> $O
echo "[syaw restore2] $(SHME_KIND=write SHME_OWNER=v248 SHME_MANIFEST=$M/v248_curves2.json bash $RUN $REQ/syaw_req.py v248syaw2 600 | grep -a 'SY241\|REFUSED\|WRITE_GUARD\|Error\|Traceback' | cut -c1-200)" >> $O
"$PY" Tools/SHME_V233_20261027/manifest233.py v248_abp6 --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching | tail -1 | cut -c1-120 >> $O
echo "[turnbind3] $(SHME_KIND=write SHME_OWNER=v248 SHME_MANIFEST=$M/v248_abp6.json bash $RUN $REQ/turnbind3_req.py v248turnbind3 900 | grep -a 'TURNBIND248C\|REFUSED\|WRITE_GUARD\|Error\|Traceback\|Assertion' | cut -c1-600)" >> $O
grep -a "turnbind3\]" $O | grep -q '"saved": true' || { echo "BIND3_ABORT" >> $O; exit 1; }
"$PY" Tools/SHME_V233_20261027/manifest233.py v248_latvel --assets /Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching /Game/GraceRanger/BP_GR_Player /Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player | tail -1 | cut -c1-120 >> $O
echo "[latvel] $(SHME_KIND=write SHME_OWNER=v248 SHME_MANIFEST=$M/v248_latvel.json bash $RUN $REQ/latvel_req.py v248latvel 1200 | grep -a 'LATVEL248\|REFUSED\|WRITE_GUARD\|Error\|Traceback\|Assertion' | cut -c1-900)" >> $O
grep -a "latvel\]" $O | grep -q '"saved": true' || { echo "LATVEL_ABORT" >> $O; exit 1; }
echo "[verify5] $(SHME_KIND=measure SHME_OWNER=v248 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v248verify5 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*\|\"bad\": \[[^]]*\]' | tr '\n' ' ' | cut -c1-400)" >> $O
relaunch th60 60; WARM=1 ab th60 "j45_sl:ts j45_sl2:ts j45_sl2:o j45_sl:o"
CAP_START=9.3 CAP_SECS=3.2 ab thcap "j45_sl:tsS j45_sl:tsD" $D/vars248_cap.sh
relaunch threal real; WARM=1 ab threal "j45_sl2:ts j45_sl2:ts:2 j45_sl2:ts:3 j45_sl2:ts:4 j45_sl2:o j45_sl2:o:2 j45_sl:ts j45_sl:ts:2 jstart:ts taps:ts wstart:ts"
relaunch th30 30; WARM=1 ab th30 "j45_sl:ts taps:ts wstart:ts jstart:ts w42_id:ts gait:ts j41_rl_p10:ts j45_sl2:ts"
echo TH248_DONE >> $O
