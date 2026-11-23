cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; O=Saved/UE59Work/r8/bis8.txt; : > $O
M0="{}"
t() { bash Saved/UE59Work/r8/ab8.sh $1 "$2" "$3" planB8s 30 > /dev/null 2>&1; echo "#### $1 $2 $3" >> $O; "$PY" Tools/UE59_20261122/an_slide3.py $1 Saved/UE59Work/planB8s.txt 5 2>&1 | cut -c1-230 >> $O; }
t b8_base "{}" "$M0"
t b8_ftoff "{'FT_On':False}" "$M0"
t b8_boboff "{'FT_On':True,'BOB_On':False}" "$M0"
t b8_kfat0 "{'BOB_On':True,'GR_KFat':0.0}" "$M0"
t b8_rk0 "{'GR_KFat':0.12,'PS_RK':0.0}" "$M0"
t b8_rcmin150 "{'PS_RK':0.6}" "{'RcMin':150.0}"
t b8_restore "{'FT_On':True,'BOB_On':True,'PS_RK':0.6,'GR_KFat':0.12}" "{'RcMin':750.0}"
echo BIS_DONE >> $O
