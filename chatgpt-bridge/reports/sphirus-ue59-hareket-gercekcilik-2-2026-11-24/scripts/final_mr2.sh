#!/bin/bash
# final_mr2.sh : movement realism pass 2 verification on the SAVED + REOPENED state. Unique labels: r9_<plan>_<hz>_F2, mr2_F_*, m2_* (24 set), mr2F_*, mr2V_*.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; R=Saved/UE59Work/mr2/final; mkdir -p $R; LG=$R/log.txt; : > $LG
PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; P=Saved/UE59Work; HKF="$(cat Saved/UE59Work/r5/hk3_line.txt)"; T9=Saved/UE59Work/r9/t.sh
echo "start $(date +%H:%M) save $(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-12)" >> $LG
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh Saved/UE59Work/mr2/reopen_read.py reopen2 240 2>&1 | grep -E "REOPEN|RCHK" | cut -c1-700 > $R/reopen_read.txt; cat $R/reopen_read.txt >> $LG
# 1 steady gait, flat lane, 60 / 30 Hz
H=$R/hip.txt; : > $H
for hz in 60 30; do L=mr2_F_on$hz; DFPS=$hz.0 bash Tools/UE59_20261120/seqP.sh $L $P/planL8.txt "$HKF" > /dev/null 2>&1; "$PY" Tools/UE59_20261124/an_hip.py $L $P/planL8.txt >> $H 2>&1; "$PY" Tools/UE59_20261124/an_head2.py $L $P/planL8.txt >> $H 2>&1; "$PY" Tools/UE59_20261124/an_bob8.py $L >> $H 2>&1; "$PY" Tools/UE59_20261124/perf8.py $L >> $R/perf.txt 2>&1; done
echo "hip $(date +%H:%M)" >> $LG
# 2 acceptance plans + phase sweeps
N=$R/plans.txt; : > $N
bash $T9 F2 60 old_R1 old_U_A old_U_B old_K1 AD_run AD_sprint WAWD_run WAWD_sprint AD_taps brake_re AD_walk gait_chain gait_back gait_tempo starts_turn_run starts_turn_walk SWs1 SWs2 SWs3 SWr1 SWr2 SWt1 SWt2 SWw1 >> $N 2>&1
echo "plans60 $(date +%H:%M)" >> $LG
bash $T9 F2 30 old_R1 old_U_B old_K1 AD_run AD_sprint AD_taps brake_re gait_chain starts_turn_walk SWs1 SWr1 SWt2 >> $N 2>&1
bash $T9 F2 var old_R1 old_U_B AD_run AD_sprint AD_taps gait_chain starts_turn_walk SWs1 SWr1 SWt2 >> $N 2>&1
echo "plans $(date +%H:%M)" >> $LG
W=$R/weight.txt; : > $W
for p in gait_chain starts_turn_walk starts_turn_run brake_re AD_sprint; do "$PY" Tools/UE59_20261124/an_weight.py r9_${p}_60_F2 Saved/UE59Work/r9/plans/$p.txt >> $W 2>&1; done
"$PY" Tools/UE59_20261124/an_hipstab.py r9_AD_sprint_60_F2 r9_AD_sprint_30_F2 r9_AD_sprint_var_F2 r9_AD_taps_60_F2 r9_old_K1_60_F2 r9_gait_chain_60_F2 > $R/hipstab.txt 2>&1
# 3 fall (60 / 30 Hz)
F=$R/fall.txt; : > $F
for hz in 60 30; do CTHZ=$hz.0 bash Saved/UE59Work/r9/ct9.sh mr2F_log_sprint_$hz sprint "-6000 -4700 92 0" > /dev/null 2>&1; "$PY" Tools/UE59_20261124/an_ct7.py mr2F_log_sprint_$hz 2>&1 | cut -c1-200 >> $F; "$PY" Saved/UE59Work/r9/fallz.py mr2F_log_sprint_$hz | awk 'NR==1||NR%3==0' | cut -c1-130 >> $F; done
echo "fall $(date +%H:%M)" >> $LG
# 4 videos (after state): side / front three-quarter on the lane, rear + shoulder on the house map (same plans / cameras as the pass-1 videos)
export VSHOT=1; unset VKEEP; HK9="$(cat Saved/UE59Work/r9/hk9_line.txt)"; V=$R/videos.txt; : > $V
v9() { if [ -n "$3" ]; then export VSIDE="$3"; else unset VSIDE; fi; DFPS=60.0 bash Tools/UE59_20261120/seqP.sh $1 $2 "$HK9" 2>&1 | grep -E "VIDREC" >> $V; }
v9 mr2V_gait_chain_side Saved/UE59Work/r9/plans/gait_chain.txt "(520,-90,60,95,'pelvis')"; v9 mr2V_AD_sprint_side Saved/UE59Work/r9/plans/AD_sprint.txt "(520,-90,60,95,'pelvis')"
v9 mr2V_gait_chain_front34 Saved/UE59Work/r9/plans/gait_chain.txt "(520,35,60,95,'pelvis')"; v9 mr2V_idle_front2 Saved/UE59Work/mr2/planIdle.txt "(380,0,40,60,'pelvis')"
unset VSIDE VSHOT
bash Saved/UE59Work/mr1/vid.sh mr2V_walk_rear walk "(260,0,10,42)" >> $V 2>&1; bash Saved/UE59Work/mr1/vid.sh mr2V_run_rear run "(260,0,10,42)" >> $V 2>&1; bash Saved/UE59Work/mr1/vid.sh mr2V_walk_game walk "" >> $V 2>&1; bash Saved/UE59Work/mr1/vid.sh mr2V_run_game run "" >> $V 2>&1
echo "videos $(date +%H:%M)" >> $LG
# 5 the old 24 plan x time-step set
bash Saved/UE59Work/r6/final6.sh slide m2 > /dev/null 2>&1; cp Saved/UE59Work/r6/final6_slide.txt $R/slide24.txt; echo "slide24 $(date +%H:%M)" >> $LG
echo "save end $(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-12)" >> $LG; echo FINAL_MR2_DONE >> $LG
