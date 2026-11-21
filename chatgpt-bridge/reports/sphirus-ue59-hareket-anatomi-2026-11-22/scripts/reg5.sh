# reg.sh <tag> [modes="60"] [plans]: slide + start + pop + continuity regression with the full-pose hook
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; T=$1; PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
HKF="$(cat Saved/UE59Work/r5/hk3_line.txt)"; O=Saved/UE59Work/r5/reg_$T.txt; : > $O
for m in ${2:-60}; do
  if [ $m = var ]; then HZ=60.0; X="$HKF; builtins.VID_VARDT=(22.0,60.0)"; else HZ=$m.0; X="$HKF"; fi
  for p in ${3:-A:planU_A B:planU_B S:planSt2 Q:planQt}; do l=${T}_${p%%:*}_$m; f=Saved/UE59Work/${p##*:}.txt
    DFPS=$HZ bash Tools/UE59_20261120/seqP.sh $l $f "$X" | grep -E "VIDREC|SLOT_CH"
    echo "#### $l" >> $O; "$PY" Tools/UE59_20261120/an_slide2.py $l $f 8 >> $O 2>&1; "$PY" Tools/UE59_20261120/an_start.py $l $f 2>&1 | tail -1 >> $O
    "$PY" Tools/UE59_20261121/an_contw.py $l 6 120 0 2>&1 | head -1 >> $O
  done
done
echo REG_DONE_$T >> $O
