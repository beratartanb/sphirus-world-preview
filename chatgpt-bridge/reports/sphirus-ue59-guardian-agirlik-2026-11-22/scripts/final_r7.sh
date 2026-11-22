# final_r7.sh : round-7 verification on the SAVED + REOPENED state (editor relaunched 2026-11-22 after w_save7). All labels g7_*.
# Stages: slide (60/30/var), reversals + starts + gait bob, contact matrix (phase-split penetration), terrain, posture, house, videos.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; R=Saved/UE59Work/r7/final; mkdir -p $R; LG=$R/log.txt; : > $LG
PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; P=Saved/UE59Work; HKF="$(cat Saved/UE59Work/r5/hk3_line.txt)"
echo "start $(date +%H:%M) save $(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-12)" >> $LG
DFPS=60.0 bash Tools/UE59_20261120/seqP.sh g7_warm $P/planV1.txt "$HKF" > /dev/null 2>&1
# 1 slide / pops: general set (planU_A, planU_B) at 60, 30, variable Hz
bash Saved/UE59Work/r6/base.sh g7s "A:planU_A:60 B:planU_B:60 A:planU_A:30 B:planU_B:30 A:planU_A:var B:planU_B:var" > /dev/null 2>&1; cp Saved/UE59Work/r6/slide_g7s.txt $R/slide.txt; echo "slide $(date +%H:%M)" >> $LG
# 2 reversals / turning starts / quick A-D, straight starts, gait ladder bob + transitions
for hz in 60 30; do DFPS=$hz.0 bash Tools/UE59_20261120/seqP.sh g7_R_$hz $P/planR7.txt "$HKF" > /dev/null 2>&1
  "$PY" Tools/UE59_20261124/an_rev7.py g7_R_$hz $P/planR7.txt >> $R/rev.txt 2>&1; "$PY" Tools/UE59_20261122/an_slide3.py g7_R_$hz $P/planR7.txt 10 2>&1 | tail -6 | cut -c1-230 >> $R/rev.txt; done
DFPS=60.0 bash Tools/UE59_20261120/seqP.sh g7_S $P/planS7.txt "$HKF" > /dev/null 2>&1; "$PY" Tools/UE59_20261124/an_trans7.py g7_S $P/planS7.txt >> $R/starts.txt 2>&1
DFPS=60.0 bash Tools/UE59_20261120/seqP.sh g7_G $P/planG7.txt "$HKF" > /dev/null 2>&1; "$PY" Tools/UE59_20261124/an_bob7.py g7_G >> $R/bob.txt 2>&1; "$PY" Tools/UE59_20261124/an_trans7.py g7_G $P/planG7.txt >> $R/bob.txt 2>&1
echo "rev/starts/bob $(date +%H:%M)" >> $LG
# 3 contact matrix (an_ct7 phase-split penetration)
O=$R/contact.txt; : > $O
run() { bash Saved/UE59Work/r6/ct6.sh g7_$1 $2 "$3" "$4" > /dev/null 2>&1; "$PY" Tools/UE59_20261124/an_ct7.py g7_$1 >> $O 2>&1; }
TIRED="builtins.CT_FAT=0.9"; CARRY="builtins.CT_CARRY=True"
run wall_walk walk "-5500 -6000 92 0"; run wall_run run "-6000 -6000 92 0"; run wall_sprint sprint "-6000 -8000 92 0"; run waist_run run "-6000 -6500 92 0"
run knee_walk walk "-5500 -7000 92 0"; run knee_tempo tempo "-6000 -7000 92 0"; run knee_run runlong "-6000 -7000 92 0"; run knee_run_tired runlong "-6000 -7000 92 0" "$TIRED"
run knee_run_carry runlong "-6000 -7000 92 0" "$CARRY"; run side_graze graze "-6000 -7500 92 0"; run side_graze_propR graze "-6000 -7500 92 0" "builtins.CT_PROP='r'"
run wall_walk_propR walk "-5500 -6000 92 0" "builtins.CT_PROP='r'"; run wall45_run run "-6000 -8500 92 0"; run step_run run "-6000 -9000 92 0"
run log_walk walk "-5500 -4700 92 0"; run log_tempo tempo "-6000 -4700 92 0"; run log_run runlong "-6000 -4700 92 0"; run log_sprint sprint "-6000 -4700 92 0"; run log_sprint_tired sprint "-6000 -4700 92 0" "$TIRED"
run tight_forced walk "-5805 -5200 92 0" "builtins.CT_SET={'CT_VRef':45.0,'CT_VMin':30.0}"; run beam_run run "-6000 -3200 92 0"; run push_run run "-6000 -2700 92 0"
run corr_walk walk "-6300 -10500 92 0"; run corrk_tempo tempo "-6600 -10500 92 0"; run corrk_run runlong "-6900 -10500 92 0"; run corrk_sprint sprint "-7000 -10500 92 0"
run back_walk back "-5500 -6000 92 180"; run back_tempo backrun "-5600 -6000 92 180"
for k in 1 2 3; do CTHZ=30.0 bash Saved/UE59Work/r6/ct6.sh g7h30_log_sprint$k sprint "-6000 -4700 92 0" > /dev/null 2>&1; "$PY" Tools/UE59_20261124/an_ct7.py g7h30_log_sprint$k | sed 's/^/30Hz /' >> $O; done
for y in -4690 -4710; do run log_sprint_ph$y sprint "-6000 $y 92 0"; done
echo "contact $(date +%H:%M)" >> $LG
# 4 terrain
T=$R/terrain.txt; : > $T
tr7() { bash Saved/UE59Work/r6/ct6.sh g7_$1 $2 "$3" > /dev/null 2>&1; echo "#### g7_$1" >> $T; "$PY" Tools/UE59_20261123/an_terr6.py g7_$1 >> $T 2>&1; "$PY" Tools/UE59_20261122/an_slide3.py g7_$1 $P/plan_ct_$2.txt 10 2>&1 | tail -2 | cut -c1-200 >> $T; }
tr7 stair_walk stair "-6000 -4000 92 0"; tr7 stair_run stairrun "-6000 -4000 92 0"; tr7 stair_walk_down stairdown "-4650 -4000 240 180"; tr7 stair_run_down stairdownrun "-4650 -4000 240 180"
tr7 ramp_walk ramp "-6000 -9500 92 0"; tr7 ramp_run ramprun "-6000 -9500 92 0"; tr7 jump jump "-6000 2000 92 0"
bash Saved/UE59Work/r6/ct6.sh g7_fresh G7 "-6000 2000 92 0" "builtins.CT_FAT=0.0" > /dev/null 2>&1; bash Saved/UE59Work/r6/ct6.sh g7_tired G7 "-6000 2000 92 0" "builtins.CT_FAT=0.9" > /dev/null 2>&1
for l in g7_fresh g7_tired; do "$PY" Tools/UE59_20261124/an_bob7.py $l >> $T 2>&1; done
echo "terrain $(date +%H:%M)" >> $LG
# 5 posture
DFPS=60.0 bash Tools/UE59_20261120/seqP.sh g7_L_60 $P/planL1.txt "$HKF" > /dev/null 2>&1; "$PY" Tools/UE59_20261123/an_post6.py g7_L_60 2>&1 | cut -c1-330 > $R/posture.txt
echo "posture $(date +%H:%M)" >> $LG
# 6 videos (shoulder camera + fixed side camera), same version
V=$R/videos.txt; : > $V; export VSHOT=1; unset VKEEP
v() { if [ -n "$4" ]; then export VSIDE="$4"; else unset VSIDE; fi
  if [ ${2#ct:} != $2 ]; then bash Saved/UE59Work/r6/ct6.sh $1 ${2#ct:} "$3" "$5" >> $V 2>&1; else POS="$3" bash Tools/UE59_20261120/seqP.sh $1 $P/$2.txt "$HKF" 2>&1 | grep -E "VIDREC|mp4" >> $V; fi; }
SD="(520,90,60,95,'pelvis')"; SD2="(520,-90,110,95,'pelvis')"; BK="(520,180,60,95,'pelvis')"
v g7v_gait_sh planG7 "-6000 2000 92 0"; v g7v_gait_side planG7 "-6000 2000 92 0" "$SD"; v g7v_start_side planS7 "-6000 2000 92 0" "$SD"
v g7v_rev_sh planR7 "-6000 2000 92 0"; v g7v_rev_side planR7 "-6000 2000 92 0" "$SD"
v g7v_kneetempo_side ct:tempo "-6000 -7000 92 0" "$SD"; v g7v_kneerun_side ct:runlong "-6000 -7000 92 0" "$SD"; v g7v_kneerun_sh ct:runlong "-6000 -7000 92 0" ""
v g7v_logsprint_side ct:sprint "-6000 -4700 92 0" "$SD2"; v g7v_logsprint_sh ct:sprint "-6000 -4700 92 0" ""; v g7v_logwalk_side ct:walk "-5500 -4700 92 0" "$SD2"
v g7v_corrk_run_sh ct:runlong "-6900 -10500 92 0" ""; v g7v_corrk_tempo_sh ct:tempo "-6600 -10500 92 0" ""; v g7v_back_tempo_side ct:backrun "-5600 -6000 92 180" "$SD"
v g7v_graze_back ct:graze "-6000 -7500 92 0" "$BK"; v g7v_carry_prop_sh ct:walk "-5500 -6000 92 0" "" "builtins.CT_PROP='r'"; v g7v_kneecarry_side ct:runlong "-6000 -7000 92 0" "$SD" "builtins.CT_CARRY=True"
v g7v_stair_side ct:stair "-6000 -4000 92 0" "$SD"; v g7v_stairdown_side ct:stairdown "-4650 -4000 240 180" "$SD"; v g7v_jump_side ct:jump "-6000 2000 92 0" "$SD"
v g7v_tired_side ct:G7 "-6000 2000 92 0" "$SD" "builtins.CT_FAT=0.9"
unset VSIDE VSHOT; echo "video $(date +%H:%M)" >> $LG
# 7 house flows (house map), user save untouched check
H=$R/house.txt; : > $H; export MAP=/Game/GraceRanger/Maps/L_GR_SphirusHouse; export VSHOT=1
POS="1300 770 585 180" bash Tools/UE59_20261120/seqP.sh g7h_bed $P/planBed.txt "$HKF" 2>&1 | grep -E "VIDREC|mp4|SLOT" >> $H
POS="$(cat Saved/UE59Work/r4/maskpos.txt)" bash Tools/UE59_20261120/seqP.sh g7h_mask $P/planMask.txt "$HKF" 2>&1 | grep -E "VIDREC|mp4|SLOT" >> $H
POS="1330 760 585 0" bash Tools/UE59_20261120/seqP.sh g7h_ward $P/planWard.txt "$HKF" 2>&1 | grep -E "VIDREC|mp4|SLOT" >> $H
POS="1540 -480 190 0" bash Tools/UE59_20261120/seqP.sh g7h_tea $P/planTea.txt "$HKF" 2>&1 | grep -E "VIDREC|mp4|SLOT" >> $H
unset MAP VSHOT; bash Tools/UE59_20261119/fin19.sh R7 flow pieces loadfire 2>&1 | tail -3 >> $H; "$PY" Tools/UE59_20261119/an_flow19.py F19_flow_R7 2>&1 | grep -E "^==|CHECK" >> $H
echo "save after $(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-12)" >> $H; echo "house $(date +%H:%M)" >> $LG
df -h /c | tail -1 | awk '{print "free",$4}' >> $LG; echo FINAL_R7_DONE >> $LG
