#!/bin/bash
# final5.sh: stop foot hold OFF (release slides) -> save, relaunch, reopen read, slide regression + starts video on the reopened state
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; export MSYS_NO_PATHCONV=1; PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
P=Saved/UE59Work/p4; F=$P/final; LG=$F/log5.txt; echo "start $(date +%H:%M)" > $LG
bash Saved/UE59Work/r9/job9.sh Tools/UE59_20261125/w_save_p4.py p4save2 400 --assets /Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player /Game/Sphirus/Player/Motion/AC_Sph_Motion 2>&1 | grep -a "SAVEP4\|DIRTY\|WRITE_END" >> $LG
bash Tools/Embodied_20261105/relaunch.sh p4_reopen2.log 2>&1 | tail -1 >> $LG
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/UE59_20261125/reopen_p4.py" p4reopen2 200 2>&1 | grep -a REOPENP4 > $F/reopen_read.txt
R9=Saved/UE59Work/r9/plans; DBG="builtins.MOV5=None; builtins.CT_EXTRA=('SH_T','SH_AR'); builtins.CT_EXS=('CS_Clear',)"
for p in accel AD_sprint gait_tempo; do bash $P/rec.sh p4G_$p $R9/$p.txt - "" 60 "$DBG" >> $LG 2>&1; "$PY" Tools/UE59_20261122/an_slide3.py p4G_$p $R9/$p.txt 8 2>&1 | grep TOTAL | sed "s/^/p4G_$p /" >> $F/slide5.txt; done
bash $P/rec.sh p4G_starts $P/plans/starts.txt - "" 60 "$DBG" >> $LG 2>&1; "$PY" Tools/UE59_20261125/an_loco4.py p4G_starts $P/plans/starts.txt > $F/loco5.txt 2>&1
VSHOT=1 VSIDE="(560,90,0,55,'pelvis')" bash $P/rec.sh p4VID_starts_side2 $P/plans/starts.txt - "" 30 "$DBG" >> $F/videos.txt 2>&1
echo "save end $(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-12)" >> $LG; echo FINAL5_DONE >> $LG
