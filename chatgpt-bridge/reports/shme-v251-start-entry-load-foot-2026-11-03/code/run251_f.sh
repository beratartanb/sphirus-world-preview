#!/bin/bash
# run251_f.sh : V2.51 chain F = promotion, verify, clean-session production at 60 (+ before/after captures) / 30 / real / 20 / 120
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V251_20261103; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; source $D/lib251.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
relaunch f0 60
"$PY" Tools/SHME_V233_20261027/manifest233.py v251_prom --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching | tail -1 | cut -c1-100 >> $O
SHME_KIND=write SHME_OWNER=v251 SHME_MANIFEST=$M/v251_prom.json bash $R $REQ/prom_req.py v251prom 900 2>&1 | grep -a 'PROMOTE251\|Traceback\|Error\|REFUSED' > $D/data/promote.out
echo "[promote] $(cut -c1-400 $D/data/promote.out)" >> $O
grep -q '"saved": true' $D/data/promote.out || { echo PROM_ABORT >> $O; exit 1; }
echo "[verify] $(SHME_KIND=measure SHME_OWNER=v251 bash $R /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v251verify3 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*\|\"bad\": \[[^]]*\]' | tr '\n' ' ' | cut -c1-300)" >> $O
relaunch f60 60; WARM=1 ab f60 "j45_sl2:o jstart:o taps:o wstart:o w43_idle:o j41_rl_p10:o j40_rlw:o gait:o j45_sl:o w42_id:o jstart:pre"
CAP_START=4.85 CAP_SECS=1.6 ab fcap45 "jstart:preS jstart:oS jstart:preD jstart:oD" $D/vars251_cap.sh
CAP_START=10.85 CAP_SECS=1.6 ab fcapls "jstart:preS jstart:oS" $D/vars251_cap.sh
CAP_START=13.8 CAP_SECS=2.0 ab fcap180 "jstart:preD jstart:oD jstart:preS jstart:oS" $D/vars251_cap.sh
echo TF251_60 >> $O
relaunch f30 30; WARM=1 ab f30 "j45_sl2:o jstart:o taps:o wstart:o w43_idle:o j41_rl_p10:o j40_rlw:o gait:o j42_lr_p10:o w42_id:o"
relaunch freal real; WARM=1 ab freal "j45_sl2:o j45_sl2:o:2 j45_sl2:o:3 j45_sl2:o:4 jstart:o jstart:o:2 taps:o wstart:o"
relaunch f20 20; WARM=1 ab f20 "j45_sl2:o jstart:o w43_idle:o"
relaunch f120 120; WARM=1 ab f120 "j45_sl2:o jstart:o w43_idle:o"
echo TF251_DONE >> $O
