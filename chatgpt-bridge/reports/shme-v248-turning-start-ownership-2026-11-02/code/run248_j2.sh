#!/bin/bash
# run248_j.sh : V2.48 chain J = PROMOTION (SHM248_On := 1.0 on the ABP CDO), verify, relaunch, clean-session production batches (30 / real / 60 FPS) + captures
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V248_20261102; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
source $D/lib248.sh
until grep -q TM248_DONE $O; do sleep 20; done
"$PY" Tools/SHME_V233_20261027/manifest233.py v248_prom --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching | tail -1 | cut -c1-120 >> $O
echo "[promote] $(SHME_KIND=write SHME_OWNER=v248 SHME_MANIFEST=$M/v248_prom.json bash $RUN $REQ/promote_req.py v248promote 600 | grep -a 'PROMOTE248\|REFUSED\|WRITE_GUARD\|Error\|Traceback' | cut -c1-400)" >> $O
grep -a "promote\]" $O | grep -q '"saved": true' || { echo "PROM_ABORT" >> $O; exit 1; }
echo "[verify7] $(SHME_KIND=measure SHME_OWNER=v248 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v248verify7 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*\|\"bad\": \[[^]]*\]' | tr '\n' ' ' | cut -c1-400)" >> $O
relaunch prod30 30; WARM=1 ab prod "j45_sl:o j45_sl2:o taps:o wstart:o jstart:o w42_id:o gait:o j41_rl_p10:o j42_lr_p10:o w43_idle:o"
relaunch prodreal real; WARM=1 ab prodreal "j45_sl2:o j45_sl2:o:2 j45_sl2:o:3 j45_sl:o j45_sl:o:2 jstart:o taps:o wstart:o w42_id:o"
relaunch prod60 60; WARM=1 ab prod60 "j45_sl2:o j45_sl:o jstart:o"
CAP_START=9.3 CAP_SECS=3.4 ab prodcap "j45_sl2:oS j45_sl2:oD" $D/vars248_cap.sh
echo TJ248_DONE >> $O
