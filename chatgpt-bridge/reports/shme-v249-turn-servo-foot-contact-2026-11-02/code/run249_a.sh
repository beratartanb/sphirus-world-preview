#!/bin/bash
# run249_a.sh : V2.49 chain A = engine root motion owner for the turning start (install249_rm, knob off), verify, A/B 60 (+warp diagnostics), real time, 30/20/120 FPS
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V249_20261102; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
source $D/lib249.sh
"$PY" Tools/SHME_V233_20261027/manifest233.py v249_rm --assets /Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching /Game/GraceRanger/BP_GR_Player /Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player | tail -1 | cut -c1-120 >> $O
SHME_KIND=write SHME_OWNER=v249 SHME_MANIFEST=$M/v249_rm.json bash $RUN $REQ/rm_req.py v249rm 1200 | grep -a 'RM249\|REFUSED\|WRITE_GUARD\|Error\|Traceback\|Assertion' > $D/data/rm_install.out
echo "[rm] $(cut -c1-900 $D/data/rm_install.out)" >> $O
grep -q '"saved": true' $D/data/rm_install.out || { echo "RM_ABORT" >> $O; exit 1; }
echo "[verify] $(SHME_KIND=measure SHME_OWNER=v249 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v249verify 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*\|\"bad\": \[[^]]*\]' | tr '\n' ' ' | cut -c1-400)" >> $O
relaunch a60 60; WARM=1 ab a60 "j45_sl2:rm j45_sl2:o j45_sl2:rmOW j45_sl2:rmFP j45_sl2:rmSW jstart:rm"
CAP_START=9.3 CAP_SECS=3.4 ab acap "j45_sl2:rmS j45_sl2:rmD" $D/vars249_cap.sh
relaunch areal real; WARM=1 ab areal "j45_sl2:rm j45_sl2:rm:2 j45_sl2:rm:3 j45_sl2:rm:4 j45_sl2:o j45_sl2:o:2 j45_sl:rm jstart:rm taps:rm wstart:rm"
relaunch a30 30; WARM=1 ab a30 "j45_sl2:rm j45_sl2:o jstart:rm taps:rm wstart:rm w42_id:rm gait:rm j41_rl_p10:rm"
relaunch a20 20; WARM=1 ab a20 "j45_sl2:rm j45_sl2:o"
relaunch a120 120; WARM=1 ab a120 "j45_sl2:rm j45_sl2:o"
echo TA249_DONE >> $O
