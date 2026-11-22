# ctall6.sh <tag> : round-6 contact matrix (60 Hz data; CTHZ=30.0 for 30 Hz). Results -> Saved/UE59Work/r6/ct_<tag>.txt
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; T=$1; O=Saved/UE59Work/r6/ct_$T.txt; : > $O
PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
run() { bash Saved/UE59Work/r6/ct6.sh ${T}_$1 $2 "$3" "$4" > /dev/null 2>&1; "$PY" Tools/UE59_20261123/an_ct6.py ${T}_$1 >> $O 2>&1; }
TIRED="builtins.CT_FAT=0.9"; CARRY="builtins.CT_CARRY=True"
run wall_walk walk "-5500 -6000 92 0"; run wall_run run "-6000 -6000 92 0"; run wall_sprint sprint "-6000 -8000 92 0"; run waist_run run "-6000 -6500 92 0"
run knee_walk walk "-5500 -7000 92 0"; run knee_tempo tempo "-6000 -7000 92 0"; run knee_run runlong "-6000 -7000 92 0"
run knee_run_tired runlong "-6000 -7000 92 0" "$TIRED"; run knee_run_carry runlong "-6000 -7000 92 0" "$CARRY"; run knee_tempo_tired tempo "-6000 -7000 92 0" "$TIRED"
run side_graze graze "-6000 -7500 92 0"; run wall45_run run "-6000 -8500 92 0"; run step_run run "-6000 -9000 92 0"; run step_sprint sprint "-6000 -9000 92 0"
run log_walk walk "-5500 -4700 92 0"; run log_run runlong "-6000 -4700 92 0"; run log_run_tired runlong "-6000 -4700 92 0" "$TIRED"; run log_sprint sprint "-6000 -4700 92 0"; run log_sprint_carry sprint "-6000 -4700 92 0" "$CARRY"
run tight_forced walk "-5805 -5200 92 0" "builtins.CT_SET={'CT_VRef':45.0,'CT_VMin':30.0}"
run beam_run run "-6000 -3200 92 0"; run push_run run "-6000 -2700 92 0"
run stair_run stairrun "-6000 -4000 92 0"; run ramp_run ramprun "-6000 -9500 92 0"; run stair_sprint sprint "-6000 -4000 92 0"
echo CT6_DONE >> $O
