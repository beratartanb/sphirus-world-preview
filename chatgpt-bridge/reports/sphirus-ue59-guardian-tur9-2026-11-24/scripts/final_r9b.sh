# final_r8.sh : round-8 verification on the SAVED + REOPENED state (w_save8, relaunch emb_r8fin). Labels f9_*.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; R=Saved/UE59Work/r9/final; mkdir -p $R; LG=$R/log.txt; echo "--- trimmed remainder" >> $LG
PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; P=Saved/UE59Work; HKF="$(cat Saved/UE59Work/r5/hk3_line.txt)"
V=$R/videos.txt; while ps -ef | grep -E "seqP.sh|ct6.sh|run2.sh" | grep -v grep > /dev/null; do sleep 10; done
# 7 house flows (house map); user save untouched check
H=$R/house.txt; : > $H; export MAP=/Game/GraceRanger/Maps/L_GR_SphirusHouse; export VSHOT=1
POS="1300 770 585 180" bash Tools/UE59_20261120/seqP.sh f9h_bed $P/planBed.txt "$HKF" 2>&1 | grep -E "VIDREC|mp4|SLOT" >> $H
POS="$(cat Saved/UE59Work/r4/maskpos.txt)" bash Tools/UE59_20261120/seqP.sh f9h_mask $P/planMask.txt "$HKF" 2>&1 | grep -E "VIDREC|mp4|SLOT" >> $H
POS="1330 760 585 0" bash Tools/UE59_20261120/seqP.sh f9h_ward $P/planWard.txt "$HKF" 2>&1 | grep -E "VIDREC|mp4|SLOT" >> $H
POS="1540 -480 190 0" bash Tools/UE59_20261120/seqP.sh f9h_tea $P/planTea.txt "$HKF" 2>&1 | grep -E "VIDREC|mp4|SLOT" >> $H
unset MAP VSHOT; bash Tools/UE59_20261119/fin19.sh R9 flow pieces loadfire 2>&1 | tail -3 >> $H; for t in flow loadfire; do "$PY" Tools/UE59_20261119/an_flow19.py F19_${t}_R9 2>&1 | grep -E "^==|CHECK" >> $H; done
echo "save after $(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-12)" >> $H; echo "house $(date +%H:%M)" >> $LG
# 8 round 9: acceptance plans with unique plan+Hz+tag labels (r9_<plan>_<hz>_F), fall with the round-9 hook, round-9 videos
T9=Saved/UE59Work/r9/t.sh; N=$R/r9.txt; : > $N
bash $T9 F 60 old_R1 old_U_A old_U_B old_K1 AD_run AD_sprint WAWD_run WAWD_sprint AD_taps brake_re AD_walk gait_chain gait_back gait_tempo starts_turn_run starts_turn_walk fatigue_chain >> $N 2>&1
bash $T9 F 30 old_R1 old_U_B AD_run AD_taps WAWD_run brake_re gait_chain >> $N 2>&1
bash $T9 F var old_R1 AD_run AD_taps gait_chain >> $N 2>&1
bash $T9 F2 60 AD_run AD_taps >> $N 2>&1; bash $T9 F2 30 AD_run >> $N 2>&1
"$PY" Tools/UE59_20261124/an_fat9.py r9_fatigue_chain_60_F Saved/UE59Work/r9/plans/fatigue_chain.txt 2>&1 | cut -c1-230 > $R/fatigue.txt
echo "r9 plans $(date +%H:%M)" >> $LG
F=$R/fall.txt; : > $F
for hz in 60 30; do for k in 1 2; do CTHZ=$hz.0 bash Saved/UE59Work/r9/ct9.sh r9F_log_sprint_${hz}_$k sprint "-6000 -4700 92 0" > /dev/null 2>&1; "$PY" Tools/UE59_20261124/an_ct7.py r9F_log_sprint_${hz}_$k 2>&1 | cut -c1-220 >> $F; "$PY" Saved/UE59Work/r9/fallz.py r9F_log_sprint_${hz}_$k | awk 'NR==1||NR%3==0' | cut -c1-130 >> $F; done; done
echo "r9 fall $(date +%H:%M)" >> $LG
export VSHOT=1; unset VKEEP; HK9="$(cat Saved/UE59Work/r9/hk9_line.txt)"; SDN="(520,-90,60,95,'pelvis')"; BKN="(520,180,60,95,'pelvis')"
v9() { if [ -n "$3" ]; then export VSIDE="$3"; else unset VSIDE; fi; DFPS=60.0 bash Tools/UE59_20261120/seqP.sh $1 Saved/UE59Work/r9/plans/$2.txt "$HK9" 2>&1 | grep -E "VIDREC|mp4" >> $V; }
v9 r9V_AD_run_side AD_run "$SDN"; v9 r9V_AD_run_sh AD_run ""; v9 r9V_AD_taps_side AD_taps "$SDN";
v9 r9V_AD_sprint_back AD_sprint "$BKN"
v9 r9V_gait_chain_side gait_chain "$SDN"; v9 r9V_gait_back_side gait_back "$SDN"
v9 r9V_starts_run_side starts_turn_run "$SDN"; v9 r9V_starts_walk_side starts_turn_walk "$SDN";
v9 r9V_fatigue_sh fatigue_chain ""
export VSIDE="(520,-90,110,95,'pelvis')"; bash Saved/UE59Work/r9/ct9.sh r9V_fall_side sprint "-6000 -4700 92 0" >> $V 2>&1
unset VSIDE; bash Saved/UE59Work/r9/ct9.sh r9V_fall_sh sprint "-6000 -4700 92 0" >> $V 2>&1
unset VSHOT; echo "r9 video $(date +%H:%M)" >> $LG
echo "save end $(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-12)" >> $LG; df -h /c | tail -1 | awk '{print "free",$4}' >> $LG; echo FINAL_R9_DONE >> $LG
