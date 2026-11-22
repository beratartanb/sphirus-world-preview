# final6.sh <stage> [tag=f6]: round-6 verification. Stages: slide | posture | contact | terrain | house | video
# Results: Saved/UE59Work/r6/final6_<stage>.txt (recordings under Saved/Codex/Grip_20261106/rec, videos under Saved/Codex/Day_20261107/videos)
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; S=$1; T=${2:-f6}; O=Saved/UE59Work/r6/final6_$S.txt; : > $O
PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; P=Saved/UE59Work; HKF="$(cat Saved/UE59Work/r5/hk3_line.txt)"
rec() { if [ $3 = var ]; then HZ=60.0; X="$HKF; builtins.VID_VARDT=(22.0,60.0)"; else HZ=$3.0; X="$HKF"; fi
  DFPS=$HZ bash Tools/UE59_20261120/seqP.sh $1 $P/$2.txt "$X" > /dev/null 2>&1; }
if [ $S = slide ]; then
  for m in 60 30 var; do
    if [ $m = 60 ]; then L="A:planU_A B:planU_B S:planSt2 Q:planQt K:planK1 T:planT1 C:planC1 W:planC2 D:planDm P:planSp R:planR1 Cv:planCv"; elif [ $m = 30 ]; then L="A:planU_A B:planU_B S:planSt2 K:planK1 C:planC1 W:planC2 Cv:planCv"; else L="A:planU_A B:planU_B K:planK1 C:planC1 W:planC2"; fi
    for p in $L; do l=${T}_${p%%:*}_$m; rec $l ${p##*:} $m
      echo "#### $l (${p##*:})" >> $O; "$PY" Tools/UE59_20261122/an_slide3.py $l $P/${p##*:}.txt 10 2>&1 | cut -c1-230 >> $O
      "$PY" Tools/UE59_20261121/an_popsum.py $l 2>&1 | tail -1 | cut -c1-230 >> $O; "$PY" Tools/UE59_20261123/an_snap6.py $l 2>&1 | cut -c1-230 >> $O
    done; done
  "$PY" Tools/UE59_20261122/an_turn5.py ${T}_T_60 >> $O 2>&1
fi
if [ $S = posture ]; then
  for m in 60 30 var; do l=${T}_L_$m; rec $l planL1 $m; "$PY" Tools/UE59_20261123/an_post6.py $l 2>&1 | cut -c1-330 >> $O; "$PY" Tools/UE59_20261122/an_carry5.py $l 2>&1 | cut -c1-330 >> $O; done
  rec ${T}_F_60 planF1 60; "$PY" Tools/UE59_20261123/an_post6.py ${T}_F_60 2>&1 | cut -c1-330 >> $O; "$PY" Tools/UE59_20261122/an_fat5.py ${T}_F_60 >> $O 2>&1
  rec ${T}_I_60 planIdle 60; "$PY" Tools/UE59_20261123/an_post6.py ${T}_I_60 2>&1 | cut -c1-330 >> $O
fi
if [ $S = contact ]; then
  bash Saved/UE59Work/r6/ctall6.sh $T > /dev/null 2>&1; cat Saved/UE59Work/r6/ct_$T.txt >> $O
  for sc in "wall_run run -6000 -6000" "knee_walk walk -5500 -7000" "knee_tempo tempo -6000 -7000" "knee_run runlong -6000 -7000" "log_sprint sprint -6000 -4700" "stair_sprint sprint -6000 -4000"; do set -- $sc
    CTHZ=30.0 bash Saved/UE59Work/r6/ct6.sh ${T}h30_$1 $2 "$3 $4 92 0" > /dev/null 2>&1; "$PY" Tools/UE59_20261123/an_ct6.py ${T}h30_$1 | sed 's/^/30Hz /' >> $O; done
fi
if [ $S = terrain ]; then
  run() { bash Saved/UE59Work/r6/ct6.sh ${T}_$1 x "$3" > /dev/null 2>&1; }
  for sc in "ramp_walk ramp -9500" "ramp_run ramprun -9500" "stair_walk stair -4000" "stair_run stairrun -4000"; do set -- $sc
    bash Saved/UE59Work/r6/ct6.sh ${T}_$1 $2 "-6000 $3 92 0" > /dev/null 2>&1; echo "#### ${T}_$1" >> $O
    "$PY" Tools/UE59_20261122/an_slide3.py ${T}_$1 $P/plan_ct_$2.txt 10 2>&1 | tail -3 | cut -c1-230 >> $O; "$PY" Tools/UE59_20261123/an_terr6.py ${T}_$1 >> $O 2>&1; done
  cp $P/planJ.txt $P/plan_ct_jump.txt; bash Saved/UE59Work/r6/ct6.sh ${T}_jump jump "-6000 2000 92 0" > /dev/null 2>&1; echo "#### ${T}_jump" >> $O; "$PY" Tools/UE59_20261123/an_terr6.py ${T}_jump >> $O 2>&1
fi
echo FINAL6_DONE_$S >> $O
