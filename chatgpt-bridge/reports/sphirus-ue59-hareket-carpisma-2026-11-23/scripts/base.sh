# base.sh <tag> "<list label:plan:mode ...>" : slide baseline batch -> Saved/UE59Work/r6/slide_<tag>.txt
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; T=$1; O=Saved/UE59Work/r6/slide_$T.txt; : > $O
PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; P=Saved/UE59Work; HKF="$(cat Saved/UE59Work/r5/hk3_line.txt)"
for e in $2; do IFS=: read lb pl m <<< "$e"; l=${T}_${lb}_$m
  if [ $m = var ]; then HZ=60.0; X="$HKF; builtins.VID_VARDT=(22.0,60.0)"; else HZ=$m.0; X="$HKF"; fi
  DFPS=$HZ bash Tools/UE59_20261120/seqP.sh $l $P/$pl.txt "$X" > /dev/null 2>&1
  echo "#### $l ($pl)" >> $O; "$PY" Tools/UE59_20261122/an_slide3.py $l $P/$pl.txt 10 2>&1 | cut -c1-260 >> $O
  "$PY" Tools/UE59_20261121/an_popsum.py $l 2>&1 | tail -2 | cut -c1-230 >> $O
done; echo BASE_DONE >> $O
