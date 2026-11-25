#!/bin/bash
# final4.sh: pass-4 verification on the saved + reopened state (data, then videos). Results -> p4/final/
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; export MSYS_NO_PATHCONV=1; PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
P=Saved/UE59Work/p4; F=$P/final; mkdir -p $F; LG=$F/log.txt; echo "start $(date +%H:%M) save $(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-12)" > $LG
DBG="builtins.MOV5=None; builtins.CT_EXTRA=('SH_T','SH_AR','ATH_Y','AW_SL','AW_SR','AW_CL','AW_CR','AW_TY','AW_HY','PS_AbdClipA','TR_Kind','GT_H','GT_D','GT_Dist'); builtins.CT_EXS=('SH_Lat','GT_Ok','GT_Room','GT_Done','GT_FlOk')"
R9=Saved/UE59Work/r9/plans
for x in "starts 60" "repress 60"; do set -- $x; bash $P/rec.sh p4F_$1 $P/plans/$1.txt - "" $2 "$DBG" >> $LG 2>&1; "$PY" Tools/UE59_20261125/an_loco4.py p4F_$1 $P/plans/$1.txt >> $F/loco.txt 2>&1; done
for hz in 60 30 var; do bash $P/rec.sh p4F_accel_$hz $R9/accel.txt - "" $hz "$DBG" >> $LG 2>&1; "$PY" Tools/UE59_20261125/an_loco4.py p4F_accel_$hz $R9/accel.txt >> $F/loco.txt 2>&1; "$PY" Tools/UE59_20261122/an_slide3.py p4F_accel_$hz $R9/accel.txt 8 2>&1 | grep TOTAL | sed "s/^/p4F_accel_$hz /" >> $F/slide.txt; done
for p in AD_sprint AD_taps gait_tempo; do bash $P/rec.sh p4F_$p $R9/$p.txt - "" 60 "$DBG" >> $LG 2>&1; "$PY" Tools/UE59_20261122/an_slide3.py p4F_$p $R9/$p.txt 8 2>&1 | grep TOTAL | sed "s/^/p4F_$p /" >> $F/slide.txt; done
"$PY" Tools/UE59_20261124/an_air.py p4F_AD_sprint $R9/AD_sprint.txt >> $F/turn.txt 2>&1; "$PY" Tools/UE59_20261124/an_turn.py p4F_AD_sprint $R9/AD_sprint.txt 2>&1 | grep MEAN >> $F/turn.txt
R=-4793; SP=Saved/UE59Work/b4/plan_sprel.txt
br() { bash $P/rec.sh p4FK_$1 $SP "$2" "$3" 60 "$DBG" >> $LG 2>&1; "$PY" Tools/UE59_20261125/an_coast5.py p4FK_$1 "$2" >> $F/brake.txt 2>&1; }
br open "[]"; br wall260 "[[$((R+290)),2000,150,30,400,300]]"; br corner "[[$((R+200)),2060,150,30,400,300,45]]"; br lowbox "[[$((R+215)),2000,17,30,300,35]]"
br cliff "[[$((R-600)),2000,30,1520,400,60]]" "-6000 2000 152 0"; br stairs "[[$((R+135)),2000,9,30,300,18],[$((R+165)),2000,18,30,300,36],[$((R+195)),2000,27,30,300,54],[$((R+225)),2000,36,30,300,72],[$((R+255)),2000,45,30,300,90]]"
T=-5740
for x in "h60:[[$T,2000,30,40,400,60]]:trav" "h150:[[$((T+90)),2000,75,220,400,150]]:trav" "h240:[[$((T+90)),2000,120,220,400,240]]:trav" "h330:[[$T,2000,165,40,400,330]]:trav" "w90:[[$((T-80)),2000,45,40,400,90]]:travwalk"; do
  IFS=: read n s pl <<< "$x"; bash $P/rec.sh p4FV_$n $P/plans/$pl.txt "$s" "" 60 "$DBG" >> $LG 2>&1; "$PY" Tools/UE59_20261125/an_trav4.py p4FV_$n >> $F/trav.txt 2>&1; done
bash $P/rec.sh p4FW_aware $P/plans/aware.txt "[[-5200,2058,150,1400,20,300],[-4300,1930,150,40,40,300]]" "" 60 "$DBG" >> $LG 2>&1; "$PY" Tools/UE59_20261125/an_aware4.py p4FW_aware >> $F/aware.txt 2>&1
bash $P/rec.sh p4FV_ceil $P/plans/ceiling.txt "[[-6000,2000,140,300,300,20]]" "" 60 "$DBG" >> $LG 2>&1
echo "data $(date +%H:%M)" >> $LG
# videos (normal speed, uncut, 30 fps screenshots)
vid() { VSHOT=1 VSIDE="$4" bash $P/rec.sh $1 $2 "$3" "" 30 "$DBG" >> $F/videos.txt 2>&1; }
vid p4VID_starts_side $P/plans/starts.txt - "(560,90,0,55,'pelvis')"
vid p4VID_tempo_front $R9/gait_tempo.txt - "(430,0,0,55,'pelvis')"
vid p4VID_ADsprint_side $R9/AD_sprint.txt - "(620,90,0,55,'pelvis')"
vid p4VID_trav_h60 $P/plans/trav.txt "[[$T,2000,30,40,400,60]]" "(520,90,40,60,'pelvis')"
vid p4VID_trav_h150 $P/plans/trav.txt "[[$((T+90)),2000,75,220,400,150]]" "(560,90,80,60,'pelvis')"
vid p4VID_trav_h240 $P/plans/trav.txt "[[$((T+90)),2000,120,220,400,240]]" "(620,90,120,60,'pelvis')"
vid p4VID_aware_game $P/plans/aware.txt "[[-5200,2058,150,1400,20,300],[-4300,1930,150,40,40,300]]" ""
vid p4VID_brake_wall $SP "[[$((R+290)),2000,150,30,400,300]]" "(620,90,0,55,'pelvis')"
vid p4VID_ceil $P/plans/ceiling.txt "[[-6000,2000,140,300,300,20]]" "(430,60,0,55,'pelvis')"
bash $P/rec.sh p4F_cleanup Saved/UE59Work/b4/plan_idle4.txt - >> $LG 2>&1
echo "save end $(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-12)" >> $LG; echo FINAL4_DONE >> $LG
