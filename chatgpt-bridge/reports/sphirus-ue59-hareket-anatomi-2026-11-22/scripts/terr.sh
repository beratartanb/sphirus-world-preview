# terr.sh <tag> : ramp / stairs / jump / crouch runs with the contact log (60 Hz data). Results -> Saved/UE59Work/r5/terr_<tag>.txt
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; T=$1; O=Saved/UE59Work/r5/terr_$T.txt; : > $O
PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; P=Saved/UE59Work
echo "[('',1.0,0),('W',6.5,0),('',1.2,0),('S',3.0,0),('',1.0,0)]" > $P/plan_ct_ramp.txt
echo "[('',1.0,0),('W LeftShift',3.0,0),('',1.5,0)]" > $P/plan_ct_ramprun.txt
echo "[('',1.0,0),('W',6.5,0),('',1.5,0)]" > $P/plan_ct_stair.txt
echo "[('',1.0,0),('W LeftShift',3.2,0),('',1.5,0)]" > $P/plan_ct_stairrun.txt
run() { CTPOS="$3" bash Saved/UE59Work/r5/ct.sh ${T}_$1 None $P/$2.txt > /dev/null 2>&1
  echo "#### ${T}_$1" >> $O; "$PY" Tools/UE59_20261122/an_ct.py ${T}_$1 2>&1 | grep -v approach >> $O
  "$PY" Tools/UE59_20261122/an_slide3.py ${T}_$1 $P/$2.txt 10 2>&1 | tail -4 | cut -c1-230 >> $O
  "$PY" Tools/UE59_20261121/an_contw.py ${T}_$1 6 120 0 2>&1 | head -1 >> $O
  "$PY" Tools/UE59_20261122/an_terr.py ${T}_$1 >> $O 2>&1; }
run ramp_walk plan_ct_ramp "-6000 -9500 92 0"
run ramp_run plan_ct_ramprun "-6000 -9500 92 0"
run stair_walk plan_ct_stair "-6000 -4000 92 0"
run stair_run plan_ct_stairrun "-6000 -4000 92 0"
run jump_crouch planJ "-6000 2000 92 0"
echo TERR_DONE_$T >> $O
