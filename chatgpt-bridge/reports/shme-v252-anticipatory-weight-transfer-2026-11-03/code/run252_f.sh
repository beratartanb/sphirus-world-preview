#!/bin/bash
# run252_f.sh : V2.52 chain F = promotion (APA walk-start databases + smooth yaw), verify, clean-session production + same-session
# before/after captures at 60, then 30 / real / 20 / 120
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V252_20261103; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; source $D/lib252.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
relaunch f0 60
"$PY" Tools/SHME_V233_20261027/manifest233.py v252_prom --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching | tail -1 | cut -c1-100 >> $O
SHME_KIND=write SHME_OWNER=v252 SHME_MANIFEST=$M/v252_prom.json bash $R $REQ/prom_req.py v252prom 900 2>&1 | grep -a 'PROMOTE252\|Traceback\|Error\|REFUSED' > $D/data/promote.out
echo "[promote] $(cut -c1-500 $D/data/promote.out)" >> $O
grep -q '"saved": true' $D/data/promote.out || { echo PROM_ABORT >> $O; exit 1; }
echo "[verify] $(SHME_KIND=measure SHME_OWNER=v252 bash $R /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v252verify2 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*\|\"bad\": \[[^]]*\]' | tr '\n' ' ' | cut -c1-300)" >> $O
relaunch f60 60; WARM=1 ab f60 "w42_id:o w42_id:pre wstart:o wstart:pre taps:o taps:pre gait:o jstart:o jstart:pre j45_sl2:o w43_idle:o j41_rl_p10:o j40_rlw:o j45_sl:o"
CAP_START=13.85 CAP_SECS=1.5 ab fcapw "w42_id:preS w42_id:oS w42_id:preG w42_id:oG w42_id:preD w42_id:oD" $D/vars252_cap.sh
CAP_START=4.85 CAP_SECS=1.5 ab fcapws "wstart:preS wstart:oS" $D/vars252_cap.sh
CAP_START=13.8 CAP_SECS=2.0 ab fcap180 "jstart:preD jstart:oD" $D/vars252_cap.sh
echo TF252_60 >> $O
relaunch f30 30; WARM=1 ab f30 "w42_id:o wstart:o taps:o gait:o jstart:o j45_sl2:o w43_idle:o j41_rl_p10:o j40_rlw:o j42_lr_p10:o"
relaunch freal real; WARM=1 ab freal "w42_id:o w42_id:o:2 wstart:o wstart:o:2 taps:o jstart:o j45_sl2:o j40_rlw:o"
relaunch f20 20; WARM=1 ab f20 "w42_id:o wstart:o jstart:o w43_idle:o"
relaunch f120 120; WARM=1 ab f120 "w42_id:o wstart:o jstart:o w43_idle:o"
echo TF252_DONE >> $O
