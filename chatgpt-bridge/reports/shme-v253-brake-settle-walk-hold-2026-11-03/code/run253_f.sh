#!/bin/bash
# run253_f.sh : V2.53 chain F = promotion (walk hold + post-brake settle; crop kink content already in), verify, clean-session production +
# same-session before/after at 60 with captures, then 30 / real / 20 / 120
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V253_20261104; O=$D/run253_f.out; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; source $D/lib253.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
relaunch f0 60
"$PY" Tools/SHME_V233_20261027/manifest233.py v253_prom --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching | tail -1 | cut -c1-100 >> $O
SHME_KIND=write SHME_OWNER=v253 SHME_MANIFEST=$M/v253_prom.json bash $R $REQ/prom_req.py v253prom 900 2>&1 | grep -a 'PROMOTE253\|Traceback\|Error\|REFUSED' > $D/data/promote.out
echo "[promote] $(cut -c1-700 $D/data/promote.out)" >> $O
grep -q '"saved": true' $D/data/promote.out || { echo PROM_ABORT >> $O; exit 1; }
echo "[verify] $(SHME_KIND=measure SHME_OWNER=v253 bash $R /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v253verify 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*\|\"bad\": \[[^]]*\]' | tr '\n' ' ' | cut -c1-300)" >> $O
relaunch f60 60; WARM=1 ab f60 "w42_id:o w42_id:pre wstart:o wstart:pre taps:o taps:pre jstart:o j36_stop:o j36_stop:pre j36_stopb:o j36_stopb:pre j45_sl2:o gait:o w43_idle:o j40_rlw:o j41_rl_p10:o"
CAP_START=4.9 CAP_SECS=2.0 ab fcaps "j36_stop:preS j36_stop:oS j36_stop:preD j36_stop:oD j36_stop:preG j36_stop:oG" $D/vars253_cap.sh
CAP_START=4.85 CAP_SECS=1.5 ab fcapw "wstart:preS wstart:oS wstart:preD wstart:oD" $D/vars253_cap.sh
CAP_START=13.8 CAP_SECS=2.0 ab fcap180 "jstart:oD" $D/vars253_cap.sh
echo TF253_60 >> $O
relaunch f30 30; WARM=1 ab f30 "w42_id:o wstart:o taps:o jstart:o j36_stop:o j45_sl2:o gait:o w43_idle:o"
relaunch freal real; WARM=1 ab freal "w42_id:o w42_id:o:2 wstart:o wstart:o:2 taps:o jstart:o j36_stop:o j36_stop:o:2 j40_rlw:o"
relaunch f20 20; WARM=1 ab f20 "w42_id:o wstart:o jstart:o j36_stop:o"
relaunch f120 120; WARM=1 ab f120 "w42_id:o wstart:o jstart:o j36_stop:o"
bash $R Tools/SHME_V21_20261014/revert_quit.py rq_fend 300 | grep -E "dirty after|QUIT|REFUSED" >> $O
echo TF253_DONE >> $O
