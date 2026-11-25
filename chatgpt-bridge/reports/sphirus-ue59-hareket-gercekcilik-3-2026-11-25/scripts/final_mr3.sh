#!/bin/bash
# final_mr3.sh : movement realism pass 3 verification on the SAVED + REOPENED state. Labels: mr3V_*, mr3_F_*, r9_<plan>_<hz>_F5, mr3F_*.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; R=Saved/UE59Work/mr3/final; mkdir -p $R; LG=$R/log.txt; : > $LG
PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; P=Saved/UE59Work; HKF="$(cat Saved/UE59Work/r5/hk3_line.txt)"; T9=Saved/UE59Work/r9/t.sh; PL=Saved/UE59Work/r9/plans
echo "start $(date +%H:%M) save $(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-12)" >> $LG
# 0 house map videos first (editor opens on the house map)
V=$R/videos.txt; : > $V
bash Saved/UE59Work/mr1/vid.sh mr3V_house_walk_rear walk "(260,0,10,42)" >> $V 2>&1; bash Saved/UE59Work/mr1/vid.sh mr3V_house_run_rear run "(260,0,10,42)" >> $V 2>&1; bash Saved/UE59Work/mr1/vid.sh mr3V_house_walk_game walk "" >> $V 2>&1; bash Saved/UE59Work/mr1/vid.sh mr3V_house_run_game run "" >> $V 2>&1
echo "house $(date +%H:%M)" >> $LG
# 1 steady gait 60 / 30
H=$R/hip.txt; : > $H; : > $R/perf.txt
for hz in 60 30; do L=mr3_F_on$hz; DFPS=$hz.0 bash Tools/UE59_20261120/seqP.sh $L $P/planL8.txt "$HKF" > /dev/null 2>&1; "$PY" Tools/UE59_20261124/an_hip.py $L $P/planL8.txt >> $H 2>&1; "$PY" Tools/UE59_20261124/an_head2.py $L $P/planL8.txt >> $H 2>&1; "$PY" Tools/UE59_20261124/perf8.py $L >> $R/perf.txt 2>&1; done
echo "hip $(date +%H:%M)" >> $LG
# 2 plans
N=$R/plans.txt; : > $N
bash $T9 F5 60 old_R1 old_U_A old_U_B old_K1 AD_run AD_sprint WAWD_run WAWD_sprint AD_taps brake_re AD_walk gait_chain gait_back gait_tempo starts_turn_run starts_turn_walk SWs1 SWs2 SWr1 SWt1 SWt2 SWw1 accel tempo_toggle crouchjump exert >> $N 2>&1
echo "plans60 $(date +%H:%M)" >> $LG
bash $T9 F5 30 old_U_B old_K1 AD_run AD_sprint AD_taps brake_re gait_chain starts_turn_walk SWs1 SWr1 SWt2 accel crouchjump >> $N 2>&1
bash $T9 F5 var AD_sprint AD_taps gait_chain starts_turn_walk SWs1 SWt2 accel >> $N 2>&1
echo "plans $(date +%H:%M)" >> $LG
grep -h EXISTS $N >> $LG
A=$R/trans.txt; : > $A; for hz in 60 30 var; do for p in accel gait_chain; do "$PY" Tools/UE59_20261124/an_trans.py r9_${p}_${hz}_F5 $PL/$p.txt >> $A 2>&1; done; done
for p in tempo_toggle gait_tempo starts_turn_walk starts_turn_run; do "$PY" Tools/UE59_20261124/an_trans.py r9_${p}_60_F5 $PL/$p.txt >> $A 2>&1; done
B=$R/arm.txt; : > $B; for p in accel gait_tempo gait_back; do "$PY" Tools/UE59_20261124/an_arm.py r9_${p}_60_F5 $PL/$p.txt | cut -c1-340 >> $B 2>&1; done
C=$R/turn.txt; : > $C; for hz in 60 30; do for p in WAWD_run WAWD_sprint AD_run AD_sprint; do [ -f Saved/Codex/Grip_20261106/rec/r9_${p}_${hz}_F5.json ] && "$PY" Tools/UE59_20261124/an_turn.py r9_${p}_${hz}_F5 $PL/$p.txt | tail -1 >> $C 2>&1; done; done
for hz in 60 30; do "$PY" Saved/UE59Work/mr3/an_cj.py r9_crouchjump_${hz}_F5 $PL/crouchjump.txt >> $R/crouchjump.txt 2>&1; done
"$PY" Saved/UE59Work/mr3/an_ex.py r9_exert_60_F5 > $R/exert.txt 2>&1
"$PY" Tools/UE59_20261124/an_hipstab.py r9_AD_sprint_60_F5 r9_AD_sprint_30_F5 r9_gait_chain_60_F5 > $R/hipstab.txt 2>&1
# 3 fall 60 / 30
F=$R/fall.txt; : > $F
for hz in 60 30; do CTHZ=$hz.0 bash Saved/UE59Work/r9/ct9.sh mr3F_log_sprint_$hz sprint "-6000 -4700 92 0" > /dev/null 2>&1; "$PY" Tools/UE59_20261124/an_ct7.py mr3F_log_sprint_$hz 2>&1 | cut -c1-200 >> $F; "$PY" Saved/UE59Work/r9/fallz.py mr3F_log_sprint_$hz | awk 'NR==1||NR%3==0' | cut -c1-130 >> $F; done
echo "fall $(date +%H:%M)" >> $LG
# 4 lane videos
export VSHOT=1; unset VKEEP; HK9="$(cat Saved/UE59Work/r9/hk9_line.txt)"
v9() { if [ -n "$3" ]; then export VSIDE="$3"; else unset VSIDE; fi; DFPS=60.0 bash Tools/UE59_20261120/seqP.sh $1 $2 "$HK9" 2>&1 | grep -E "VIDREC" >> $V; }
v9 mr3V_gait_chain_side $PL/gait_chain.txt "(520,-90,60,95,'pelvis')"; v9 mr3V_accel_side $PL/accel.txt "(520,-90,60,95,'pelvis')"; v9 mr3V_accel_front34 $PL/accel.txt "(520,35,60,95,'pelvis')"
v9 mr3V_AD_sprint_side $PL/AD_sprint.txt "(520,-90,60,95,'pelvis')"; v9 mr3V_WAWD_sprint_rear $PL/WAWD_sprint.txt "(520,180,60,95,'pelvis')"; v9 mr3V_gait_tempo_side $PL/gait_tempo.txt "(520,-90,60,95,'pelvis')"; v9 mr3V_gait_tempo_front $PL/gait_tempo.txt "(520,0,60,95,'pelvis')"
v9 mr3V_exert_front34 $PL/exert.txt "(420,25,50,70,'pelvis')"; v9 mr3V_accel_game $PL/accel.txt ""
echo "videos $(date +%H:%M)" >> $LG
# 5 'before-equivalent' videos: pass-3 parameters switched off IN MEMORY (not saved; the editor is relaunched afterwards)
unset VSIDE VSHOT
bash Saved/UE59Work/mr2/sp.sh '{"CS_On":0.0,"GU_Run":0.8,"GU_Tempo":0.8,"CA_On":0.0,"PS_AbdBack":0.0,"TLM_On":0.0,"PS_S2":0.0,"PS_S3":0.0,"PS_S4":0.0,"BR_Sh":0.0,"BR_FatK":0.0,"PS_BrEff":1.6}' >> $LG 2>&1
bash Saved/UE59Work/mr2/sm.sh '{"StBoostMaxSt":1400.0,"StBoostDur":0.9}' >> $LG 2>&1
echo "import builtins; builtins.MR3C={'SpeedArm':4.0,'SprArm':0.0,'FovSpr':0.0}; builtins.MR3P={'CS_On':0.0,'GU_Run':0.8,'GU_Tempo':0.8,'CA_On':0.0,'PS_AbdBack':0.0,'TLM_On':0.0,'PS_S2':0.0,'PS_S3':0.0,'PS_S4':0.0,'BR_Sh':0.0,'BR_FatK':0.0,'PS_BrEff':1.6}; builtins.MR3M={'StBoostMaxSt':1400.0,'StBoostDur':0.9}" > Saved/UE59Work/mr3/off.py; cat Tools/UE59_20261124/c_mr3_defaults.py >> Saved/UE59Work/mr3/off.py
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh Saved/UE59Work/mr3/off.py mr3off 120 2>&1 | grep -a MR3DEF | cut -c1-300 >> $LG
export VSHOT=1
v9 mr3V_OFF_accel_side $PL/accel.txt "(520,-90,60,95,'pelvis')"; v9 mr3V_OFF_WAWD_sprint_rear $PL/WAWD_sprint.txt "(520,180,60,95,'pelvis')"; v9 mr3V_OFF_gait_tempo_front $PL/gait_tempo.txt "(520,0,60,95,'pelvis')"; v9 mr3V_OFF_accel_game $PL/accel.txt ""
unset VSIDE VSHOT
bash $T9 OFF5 60 accel WAWD_sprint gait_tempo >> $R/plans_off.txt 2>&1
"$PY" Tools/UE59_20261124/an_trans.py r9_accel_60_OFF5 $PL/accel.txt > $R/trans_off.txt 2>&1; "$PY" Tools/UE59_20261124/an_arm.py r9_accel_60_OFF5 $PL/accel.txt | cut -c1-340 > $R/arm_off.txt 2>&1; "$PY" Tools/UE59_20261124/an_arm.py r9_gait_tempo_60_OFF5 $PL/gait_tempo.txt | cut -c1-340 >> $R/arm_off.txt 2>&1; "$PY" Tools/UE59_20261124/an_turn.py r9_WAWD_sprint_60_OFF5 $PL/WAWD_sprint.txt | tail -1 > $R/turn_off.txt 2>&1
echo "off $(date +%H:%M)" >> $LG
bash Tools/Embodied_20261105/relaunch.sh mr3_reopen5 >> $LG 2>&1
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh Saved/UE59Work/mr3/reopen_read3.py mr3reopen 120 2>&1 | grep -a REOPEN3 | cut -c1-700 > $R/reopen_read_end.txt
echo "save end $(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-12)" >> $LG; echo FINAL_MR3_DONE >> $LG
