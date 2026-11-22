# final6b.sh : round-6 verification chain on the SAVED + REOPENED state (tag f6). Output: Saved/UE59Work/r6/final6b.log + final6_<stage>.txt
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; LG=Saved/UE59Work/r6/final6b.log; : > $LG
PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; P=Saved/UE59Work; HKF="$(cat Saved/UE59Work/r5/hk3_line.txt)"
DFPS=60.0 bash Tools/UE59_20261120/seqP.sh f6_warm $P/planV1.txt "$HKF" > /dev/null 2>&1; echo "warm $(date +%H:%M)" >> $LG
bash Saved/UE59Work/r6/final6.sh slide f6; echo "slide $(date +%H:%M)" >> $LG
# contact subset
O=Saved/UE59Work/r6/final6_contact_f6.txt; : > $O; TIRED="builtins.CT_FAT=0.9"; CARRY="builtins.CT_CARRY=True"
run() { bash Saved/UE59Work/r6/ct6.sh f6_$1 $2 "$3" "$4" > /dev/null 2>&1; "$PY" Tools/UE59_20261123/an_ct6.py f6_$1 >> $O 2>&1; }
run wall_walk walk "-5500 -6000 92 0"; run wall_sprint sprint "-6000 -8000 92 0"; run knee_walk walk "-5500 -7000 92 0"; run knee_tempo tempo "-6000 -7000 92 0"; run knee_run runlong "-6000 -7000 92 0"
run knee_run_carry runlong "-6000 -7000 92 0" "$CARRY"; run knee_tempo_tired tempo "-6000 -7000 92 0" "$TIRED"; run side_graze graze "-6000 -7500 92 0"; run log_run runlong "-6000 -4700 92 0"; run log_sprint sprint "-6000 -4700 92 0"
run beam_walk walk "-5500 -3200 92 0"; run beam_run run "-6000 -3200 92 0"; run wall_run run "-6000 -6000 92 0"; run step_sprint sprint "-6000 -9000 92 0"; run tight_forced walk "-5805 -5200 92 0" "builtins.CT_SET={'CT_VRef':45.0,'CT_VMin':30.0}"; run stair_sprint sprint "-6000 -4000 92 0"; run knee_run_off runlong "-6000 -7000 92 0" "builtins.CT_SET={'CT_On':False}"
for sc in "knee_run runlong -6000 -7000" "log_sprint sprint -6000 -4700" "knee_walk walk -5500 -7000"; do set -- $sc
  CTHZ=30.0 bash Saved/UE59Work/r6/ct6.sh f6h30_$1 $2 "$3 $4 92 0" > /dev/null 2>&1; "$PY" Tools/UE59_20261123/an_ct6.py f6h30_$1 | sed 's/^/30Hz /' >> $O; done
for l in f6_wall_run f6_wall_sprint f6_wall_walk; do "$PY" Tools/UE59_20261123/an_palm6.py $l >> $O 2>&1; done; "$PY" Tools/UE59_20261123/an_palm6.py f6_side_graze 0 1 >> $O 2>&1
echo "contact $(date +%H:%M)" >> $LG
bash Saved/UE59Work/r6/final6.sh posture f6; echo "posture $(date +%H:%M)" >> $LG
bash Saved/UE59Work/r6/final6.sh terrain f6; echo "terrain $(date +%H:%M)" >> $LG
# videos (30 fps real time, no kept frames)
V=Saved/UE59Work/r6/final6_video.txt; : > $V; export VSHOT=1; unset VKEEP
v() { if [ -n "$4" ]; then export VSIDE="$4"; else unset VSIDE; fi
  if [ ${2#ct:} != $2 ]; then bash Saved/UE59Work/r6/ct6.sh $1 ${2#ct:} "$3" "$5" >> $V 2>&1; else POS="$3" bash Tools/UE59_20261120/seqP.sh $1 $P/$2.txt "$HKF" 2>&1 | grep -E "VIDREC|mp4" >> $V; fi; }
SD="(520,90,60,95,'pelvis')"; SD2="(520,-90,110,95,'pelvis')"; BK="(520,180,60,95,'pelvis')"
v f6v_loco_sh planV1 "-6000 2000 92 0"; v f6v_loco_side planV1 "-6000 2000 92 0" "$SD"; v f6v_start_side planStart6 "-6000 2000 92 0" "$SD"; v f6v_turn_sh planT1 "-6000 2000 92 0"; v f6v_rev_side planR1 "-6000 2000 92 0" "$SD"
v f6v_kneerun_side ct:runlong "-6000 -7000 92 0" "$SD"; v f6v_kneerun_sh ct:runlong "-6000 -7000 92 0" ""; v f6v_fall_side ct:sprint "-6000 -4700 92 0" "$SD2"; v f6v_fall_sh ct:sprint "-6000 -4700 92 0" ""
v f6v_wallsprint_sh ct:sprint "-6000 -8000 92 0" ""; v f6v_wallrun_side ct:run "-6000 -6000 92 0" "(300,125,45,95,'pelvis')"; v f6v_beam_side ct:run "-6000 -3200 92 0" "$SD"; v f6v_tight_side ct:walk "-5805 -5200 92 0" "$SD" "builtins.CT_SET={'CT_VRef':45.0,'CT_VMin':30.0}"
v f6v_graze_back ct:graze "-6000 -7500 92 0" "$BK"; v f6v_logrun_side ct:runlong "-6000 -4700 92 0" "$SD2"; v f6v_kneecarry_side ct:runlong "-6000 -7000 92 0" "$SD" "builtins.CT_CARRY=True"
v f6v_fat_sh planF1 "-6000 2000 92 0"; v f6v_fat_side planF1 "-6000 2000 92 0" "$SD"; v f6v_idle_side planIdle45 "-6000 2000 92 0" "(330,140,40,95,'pelvis')"
v f6v_stair_side ct:stair "-6000 -4000 92 0" "$SD"; v f6v_stairrun_side ct:stairrun "-6000 -4000 92 0" "$SD"
unset VSIDE; echo "video $(date +%H:%M)" >> $LG
# house flows
H=Saved/UE59Work/r6/final6_house.txt; : > $H; export MAP=/Game/GraceRanger/Maps/L_GR_SphirusHouse
POS="1300 770 585 180" bash Tools/UE59_20261120/seqP.sh f6h_bed $P/planBed.txt "$HKF" | grep -E "VIDREC|mp4|SLOT" >> $H
POS="$(cat Saved/UE59Work/r4/maskpos.txt)" bash Tools/UE59_20261120/seqP.sh f6h_mask $P/planMask.txt "$HKF" | grep -E "VIDREC|mp4|SLOT" >> $H
unset MAP; bash Tools/UE59_20261119/fin19.sh R6 flow 2>&1 | tail -3 >> $H; "$PY" Tools/UE59_20261119/an_flow19.py F19_flow_R6 2>&1 | grep -E "^==|CHECK" >> $H
sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-12 >> $H; echo "house $(date +%H:%M)" >> $LG
df -h /c | tail -1 | awk '{print "free",$4}' >> $LG; echo FINAL6B_DONE >> $LG
