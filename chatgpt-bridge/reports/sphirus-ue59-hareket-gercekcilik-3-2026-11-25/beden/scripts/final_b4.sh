#!/bin/bash
# final_b4.sh : B4 body + pass-3 follow-up verification on the SAVED + REOPENED state. Labels b4F_*, r9_<plan>_<hz>_F6, b4V_F_*, b4V_OFF_*.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; R=Saved/UE59Work/b4/final; mkdir -p $R; LG=$R/log.txt; : > $LG
PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; T9=Saved/UE59Work/r9/t.sh; PL=Saved/UE59Work/r9/plans; W="C:/Users/berat/Documents/Unreal Projects/sphirus_UE59/Saved/UE59Work/b4"
echo "start $(date +%H:%M) save $(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-12)" >> $LG
V=$R/videos.txt; : > $V
bash Saved/UE59Work/mr1/vid.sh b4V_F_house_walk_game walk "" >> $V 2>&1; bash Saved/UE59Work/mr1/vid.sh b4V_F_house_run_game run "" >> $V 2>&1; bash Saved/UE59Work/mr1/vid.sh b4V_F_house_run_rear run "(260,0,10,42)" >> $V 2>&1
echo "house $(date +%H:%M)" >> $LG
N=$R/plans.txt; : > $N
bash $T9 F6 60 accel gait_chain gait_tempo tempo_toggle AD_sprint AD_run AD_taps WAWD_sprint starts_turn_walk starts_turn_run SWs1 brake_re old_K1 gait_back crouchjump >> $N 2>&1
bash $T9 F6 30 accel AD_sprint SWs1 starts_turn_walk AD_taps >> $N 2>&1
bash $T9 F6 var accel AD_sprint starts_turn_walk >> $N 2>&1
grep -h EXISTS $N >> $LG; echo "plans $(date +%H:%M)" >> $LG
A=$R/trans.txt; : > $A; for hz in 60 30 var; do "$PY" Tools/UE59_20261124/an_trans.py r9_accel_${hz}_F6 $PL/accel.txt >> $A 2>&1; done; for p in gait_chain tempo_toggle gait_tempo; do "$PY" Tools/UE59_20261124/an_trans.py r9_${p}_60_F6 $PL/$p.txt >> $A 2>&1; done
"$PY" Tools/UE59_20261124/an_turn.py r9_WAWD_sprint_60_F6 $PL/WAWD_sprint.txt | tail -1 > $R/turn.txt; "$PY" Tools/UE59_20261124/an_turn.py r9_AD_sprint_60_F6 $PL/AD_sprint.txt | tail -1 >> $R/turn.txt
"$PY" Tools/UE59_20261124/an_air.py r9_AD_sprint_60_F6 $PL/AD_sprint.txt > $R/air.txt 2>&1
"$PY" Saved/UE59Work/mr3/an_cj.py r9_crouchjump_60_F6 $PL/crouchjump.txt > $R/crouchjump.txt 2>&1
for p in accel gait_tempo gait_back; do "$PY" Tools/UE59_20261124/an_arm.py r9_${p}_60_F6 $PL/$p.txt | cut -c1-300 >> $R/arm_proxy.txt 2>&1; done
# real-surface arm clearance
bash Saved/UE59Work/b4/arm_rec.sh b4F_arm_accel $PL/accel.txt >> $LG 2>&1; bash Saved/UE59Work/b4/arm_rec.sh b4F_arm_tempo $PL/gait_tempo.txt >> $LG 2>&1
sed -e 's/b4A_accel/b4F_arm_accel/; s/b4A_tempo/b4F_arm_tempo/; s#arm/armsurf_1.txt#final/armsurf.txt#' Saved/UE59Work/b4/p_arm1.json > Saved/UE59Work/b4/p_armF.json
BLWAIT=900 bash Tools/Bio_20261115/bl.sh $R/armsurf.txt.done -b --python "C:/Users/berat/Documents/Unreal Projects/sphirus_UE59/Tools/UE59_20261124/b4_armsurf.py" -- "$W/p_armF.json" >> $LG 2>&1
echo "arm $(date +%H:%M)" >> $LG
# fall
CTHZ=60.0 bash Saved/UE59Work/r9/ct9.sh b4F_fall_sprint_60 sprint "-6000 -4700 92 0" > /dev/null 2>&1; "$PY" Tools/UE59_20261124/an_ct7.py b4F_fall_sprint_60 2>&1 | cut -c1-200 > $R/fall.txt
echo "fall $(date +%H:%M)" >> $LG
# lane videos (new body)
export VSHOT=1; unset VKEEP; HK9="$(cat Saved/UE59Work/r9/hk9_line.txt)"
v9() { if [ -n "$3" ]; then export VSIDE="$3"; else unset VSIDE; fi; DFPS=60.0 bash Tools/UE59_20261120/seqP.sh $1 $2 "$HK9" 2>&1 | grep -E "VIDREC" >> $V; }
for a in "front 0" "side -90" "back 180" "f34 35"; do set -- $a; v9 b4V_F_idle_$1 Saved/UE59Work/b4/plan_idle4.txt "(430,$2,0,60,'pelvis')"; done
v9 b4V_F_gait_chain_side $PL/gait_chain.txt "(520,-90,60,95,'pelvis')"; v9 b4V_F_accel_side $PL/accel.txt "(520,-90,60,95,'pelvis')"; v9 b4V_F_accel_front34 $PL/accel.txt "(520,35,60,95,'pelvis')"
v9 b4V_F_gait_tempo_front $PL/gait_tempo.txt "(520,0,60,95,'pelvis')"; v9 b4V_F_WAWD_sprint_rear $PL/WAWD_sprint.txt "(520,180,60,95,'pelvis')"; v9 b4V_F_AD_sprint_side $PL/AD_sprint.txt "(520,-90,60,95,'pelvis')"
v9 b4V_F_accel_game $PL/accel.txt ""
R0=-4793; export VSIDE="(520,-90,60,95,'pelvis')"; bash Saved/UE59Work/b4/sc.sh b4V_F_brake_wall Saved/UE59Work/b4/plan_sprel.txt "[[$((R0+275)),2000,150,30,600,300]]" >> $V 2>&1; bash Saved/UE59Work/b4/sc.sh b4V_F_brake_open Saved/UE59Work/b4/plan_sprel.txt "[]" >> $V 2>&1
"$PY" Saved/UE59Work/b4/an_coast.py b4V_F_brake_wall 1467 > $R/coast.txt 2>&1; "$PY" Saved/UE59Work/b4/an_coast.py b4V_F_brake_open >> $R/coast.txt 2>&1
echo "videos $(date +%H:%M)" >> $LG
# before-body comparison: old body + VF2 garments IN MEMORY only (not saved; relaunch afterwards)
unset VSIDE
echo "import builtins; builtins.B4_OFF=True" > Saved/UE59Work/b4/off.py; cat Tools/UE59_20261124/c_b4_wire.py >> Saved/UE59Work/b4/off.py
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh Saved/UE59Work/b4/off.py b4off 120 2>&1 | grep -a B4WIRE | cut -c1-300 >> $LG
for a in "front 0" "side -90" "back 180" "f34 35"; do set -- $a; v9 b4V_OFF_idle_$1 Saved/UE59Work/b4/plan_idle4.txt "(430,$2,0,60,'pelvis')"; done
v9 b4V_OFF_accel_game $PL/accel.txt ""; v9 b4V_OFF_gait_tempo_front $PL/gait_tempo.txt "(520,0,60,95,'pelvis')"
unset VSIDE VSHOT
echo "off $(date +%H:%M)" >> $LG
bash Tools/Embodied_20261105/relaunch.sh b4_reopen3 >> $LG 2>&1
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh Saved/UE59Work/b4/reopen_b4.py b4reopen 120 2>&1 | grep -a REOPENB4 | cut -c1-500 > $R/reopen_read_end.txt
echo "save end $(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-12)" >> $LG; echo FINAL_B4_DONE >> $LG
