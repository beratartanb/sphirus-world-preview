#!/bin/bash
# final_mr1.sh : movement realism pass 1 regression on the SAVED + REOPENED state (test map). Unique labels: r9_<plan>_<hz>_M1, m1_<plan>_<hz> (24 set), mr1_L_*.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; R=Saved/UE59Work/mr1/final; mkdir -p $R; LG=$R/log.txt; : > $LG
PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; P=Saved/UE59Work; HKF="$(cat Saved/UE59Work/r5/hk3_line.txt)"; T9=Saved/UE59Work/r9/t.sh
SP(){ echo "$1" > Saved/UE59Work/r9/setp.json; SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh Saved/UE59Work/r9/setp.py setp9 120 >/dev/null 2>&1; grep -h SETP $(ls -t Saved/UE59Work/rt/b2runner/jobs/setp9-*.out | head -1) | cut -c1-30 >> $LG; }
echo "start $(date +%H:%M) save $(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-12)" >> $LG; cat Saved/UE59Work/mr1/reopen_read.txt >> $LG
# 1 long steady gait on the flat lane: layer ON (saved state), then OFF (in memory), then ON again
H=$R/hip.txt; : > $H
DFPS=60.0 bash Tools/UE59_20261120/seqP.sh mr1_L_on $P/planL8.txt "$HKF" > /dev/null 2>&1; "$PY" Tools/UE59_20261124/an_hip.py mr1_L_on $P/planL8.txt >> $H 2>&1; "$PY" Tools/UE59_20261124/an_bob8.py mr1_L_on >> $H 2>&1
SP '{"HIP_On":0.0}'; DFPS=60.0 bash Tools/UE59_20261120/seqP.sh mr1_L_off $P/planL8.txt "$HKF" > /dev/null 2>&1; "$PY" Tools/UE59_20261124/an_hip.py mr1_L_off $P/planL8.txt >> $H 2>&1; SP '{"HIP_On":1.0}'
DFPS=30.0 bash Tools/UE59_20261120/seqP.sh mr1_L_on30 $P/planL8.txt "$HKF" > /dev/null 2>&1; "$PY" Tools/UE59_20261124/an_hip.py mr1_L_on30 $P/planL8.txt >> $H 2>&1
echo "hip $(date +%H:%M)" >> $LG
# 2 round-9 acceptance plans
N=$R/r9plans.txt; : > $N
bash $T9 M1 60 old_R1 old_U_A old_U_B old_K1 AD_run AD_sprint WAWD_run WAWD_sprint AD_taps brake_re AD_walk gait_chain gait_back gait_tempo starts_turn_run starts_turn_walk >> $N 2>&1
bash $T9 M1 30 old_R1 old_U_B old_K1 AD_run AD_taps brake_re gait_chain >> $N 2>&1
bash $T9 M1 var old_R1 old_U_B AD_run AD_taps gait_chain >> $N 2>&1
echo "r9 plans $(date +%H:%M)" >> $LG
# 3 fall (60 / 30 Hz)
F=$R/fall.txt; : > $F
for hz in 60 30; do CTHZ=$hz.0 bash Saved/UE59Work/r9/ct9.sh mr1F_log_sprint_$hz sprint "-6000 -4700 92 0" > /dev/null 2>&1; "$PY" Tools/UE59_20261124/an_ct7.py mr1F_log_sprint_$hz 2>&1 | cut -c1-200 >> $F; "$PY" Saved/UE59Work/r9/fallz.py mr1F_log_sprint_$hz | awk 'NR==1||NR%3==0' | cut -c1-130 >> $F; done
echo "fall $(date +%H:%M)" >> $LG
# 4 the old 24 plan x time-step set
bash Saved/UE59Work/r6/final6.sh slide m1 > /dev/null 2>&1; cp Saved/UE59Work/r6/final6_slide.txt $R/slide24.txt; echo "slide24 $(date +%H:%M)" >> $LG
echo "save end $(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-12)" >> $LG; echo FINAL_MR1_DONE >> $LG
