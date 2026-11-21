# ctall.sh <tag> : contact scenario matrix on the MT_CT_* course (60 Hz data unless CTHZ is set). Results -> Saved/UE59Work/r5/ct_<tag>.txt
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; T=$1; O=Saved/UE59Work/r5/ct_$T.txt; : > $O
PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; P=Saved/UE59Work
echo "[('',1.0,0),('W',4.0,0),('',1.0,0),('S',1.2,0),('',1.0,0)]" > $P/plan_ct_walk.txt
echo "[('',1.0,0),('W LeftShift',4.0,0),('',1.0,0),('S',1.2,0),('',1.0,0)]" > $P/plan_ct_run.txt
echo "[('',1.0,0),('W LeftShift LeftControl',5.0,0),('',1.0,0),('S',1.2,0),('',1.0,0)]" > $P/plan_ct_sprint.txt
echo "[('',1.0,0),('X',0.15,0),('',0.4,0),('W',5.0,0),('',6.0,0)]" > $P/plan_ct_tempo.txt
echo "[('',1.0,0),('W LeftShift',2.2,0),('W D LeftShift',0.5,0),('W LeftShift',2.0,0),('',1.5,0)]" > $P/plan_ct_graze.txt
echo "[('',1.0,0),('W LeftShift',5.0,0),('',6.5,0)]" > $P/plan_ct_runlong.txt
run() { CTPOS="$3" bash Saved/UE59Work/r5/ct.sh ${T}_$1 None $P/plan_ct_$2.txt $4 > /dev/null 2>&1; "$PY" Tools/UE59_20261122/an_ct.py ${T}_$1 >> $O 2>&1; }
run wall_walk walk "-5500 -6000 92 0"
run wall_run run "-6000 -6000 92 0"
run wall_sprint sprint "-6000 -8000 92 0"
run waist_run run "-6000 -6500 92 0"
run knee_walk walk "-5500 -7000 92 0"
run knee_tempo tempo "-6000 -7000 92 0"
run knee_run runlong "-6000 -7000 92 0"
run knee_tempo_tired tempo "-6000 -7000 92 0" 0.9
run side_graze graze "-6000 -7500 92 0"
run wall45_run run "-6000 -8500 92 0"
run step_run run "-6000 -9000 92 0"
echo CT_DONE_$T >> $O
