# final8.sh : last verification on the saved + reopened state after the round-6b corrections (soft start latch, sprint-only friction relief)
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; LG=Saved/UE59Work/r6/final8.log; : > $LG
PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; P=Saved/UE59Work; HKF="$(cat Saved/UE59Work/r5/hk3_line.txt)"
DFPS=60.0 bash Tools/UE59_20261120/seqP.sh f8_warm $P/planV1.txt "$HKF" > /dev/null 2>&1; echo "warm $(date +%H:%M)" >> $LG
cp Saved/UE59Work/r6/final6_slide.txt Saved/UE59Work/r6/final7_slide.txt
bash Saved/UE59Work/r6/final6.sh slide f8; cp Saved/UE59Work/r6/final6_slide.txt Saved/UE59Work/r6/final8_slide.txt; echo "slide $(date +%H:%M)" >> $LG
O=Saved/UE59Work/r6/final8_contact.txt; : > $O
run() { bash Saved/UE59Work/r6/ct6.sh f8_$1 $2 "$3" "$4" > /dev/null 2>&1; "$PY" Tools/UE59_20261123/an_ct6.py f8_$1 >> $O 2>&1; }
run knee_run runlong "-6000 -7000 92 0"; run log_sprint sprint "-6000 -4700 92 0"; run wall_run run "-6000 -6000 92 0"; run beam_run run "-6000 -3200 92 0"; run knee_run_off runlong "-6000 -7000 92 0" "builtins.CT_SET={'CT_On':False}"
DFPS=60.0 bash Tools/UE59_20261120/seqP.sh f8_L_60 $P/planL1.txt "$HKF" > /dev/null 2>&1; "$PY" Tools/UE59_20261123/an_post6.py f8_L_60 2>&1 | cut -c1-330 > Saved/UE59Work/r6/final8_posture.txt
export VSHOT=1; unset VKEEP; export VSIDE="(520,90,60,95,'pelvis')"; POS="-6000 2000 92 0" bash Tools/UE59_20261120/seqP.sh f8v_start_side $P/planStart6.txt "$HKF" > /dev/null 2>&1; unset VSIDE VSHOT
sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-12 >> $LG; echo "FINAL8_DONE $(date +%H:%M)" >> $LG
