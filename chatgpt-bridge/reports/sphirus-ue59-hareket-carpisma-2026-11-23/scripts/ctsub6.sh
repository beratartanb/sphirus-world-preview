cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; T=$1; O=Saved/UE59Work/r6/ct_$T.txt; : > $O
PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
run() { bash Saved/UE59Work/r6/ct6.sh ${T}_$1 $2 "$3" "$4" > /dev/null 2>&1; "$PY" Tools/UE59_20261123/an_ct6.py ${T}_$1 >> $O 2>&1; }
CARRY="builtins.CT_CARRY=True"
run wall_walk walk "-5500 -6000 92 0"; run wall_run run "-6000 -6000 92 0"; run wall_sprint sprint "-6000 -8000 92 0"; run log_sprint_carry sprint "-6000 -4700 92 0" "$CARRY"; run knee_run_carry runlong "-6000 -7000 92 0" "$CARRY"
echo CT6_DONE >> $O
