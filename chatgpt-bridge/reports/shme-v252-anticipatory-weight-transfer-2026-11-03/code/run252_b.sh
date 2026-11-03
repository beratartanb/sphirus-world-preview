#!/bin/bash
# run252_b.sh : V2.52 chain B = APA v2 (blend-compensated) rewrite of the 14 new clips, KeepRM installer, verify, A/B at 60 / 30 / real
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V252_20261103; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; source $D/lib252.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations; V=/Game/GraceRanger/SHME/Animations/V252
until grep -q TA252_DONE $O; do sleep 20; done
relaunch b0 60
echo "[apa2_dry] $(SHME_KIND=measure SHME_OWNER=v252 bash $R $REQ/apa2_dry_req.py v252apa2dry 900 2>&1 | grep -a 'APA252\|Traceback\|Error' | cut -c1-200)" >> $O
SHME_KIND=measure SHME_OWNER=v252 bash $R $REQ/apa2_dry_req.py v252apa2dry2 900 2>&1 | grep -a 'APA252' > $D/data/apa2_dry.out
NEW=""; for n in BL_Lfoot B_Rfoot FL_Lfoot FL_Rfoot FR_Lfoot FR_Rfoot F_Lfoot F_Rfoot LL_Lfoot LR_Rfoot RL_Lfoot RL_Rfoot RR_Lfoot RR_Rfoot; do NEW="$NEW $V/SHM252_StartTransfer_${n}_APA"; done
"$PY" Tools/SHME_V233_20261027/manifest233.py v252_apa2 --assets $V/PSD_SHM252_StartTransferAPA_L $V/PSD_SHM252_StartTransferAPA_R $NEW | tail -1 | cut -c1-100 >> $O
SHME_KIND=write SHME_OWNER=v252 SHME_MANIFEST=$M/v252_apa2.json bash $R $REQ/apa2_write_req.py v252apa2write 1500 2>&1 | grep -a 'APA252\|Traceback\|Error\|REFUSED' > $D/data/apa2_write.out
echo "[apa2] $(grep -o '"dbs": {"L": \[[^]]*\]' $D/data/apa2_write.out | cut -c1-200) $(grep -ao 'Traceback.*\|REFUSED.*' $D/data/apa2_write.out | head -2)" >> $O
"$PY" Tools/SHME_V233_20261027/manifest233.py v252_rmmode --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching | tail -1 | cut -c1-100 >> $O
echo "[rmmode] $(SHME_KIND=write SHME_OWNER=v252 SHME_MANIFEST=$M/v252_rmmode.json bash $R $REQ/rmmode_req.py v252rmmode 900 2>&1 | grep -a 'RMMODE252\|Traceback\|Error\|REFUSED' | cut -c1-400)" >> $O
echo "[verify] $(SHME_KIND=measure SHME_OWNER=v252 bash $R /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v252verify1 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*\|\"bad\": \[[^]]*\]' | tr '\n' ' ' | cut -c1-300)" >> $O
relaunch b60 60; WARM=1 ab b60 "wstart:apa w42_id:apa taps:apa gait:apa jstart:o jstart:rmk jstart:rmkyt j45_sl2:rmkyt"
relaunch b30 30; WARM=1 ab b30 "wstart:apa w42_id:apa taps:apa gait:apa jstart:rmkyt"
relaunch breal real; WARM=1 ab breal "wstart:apa wstart:apa:2 w42_id:apa jstart:rmkyt"
echo TB252_DONE >> $O
