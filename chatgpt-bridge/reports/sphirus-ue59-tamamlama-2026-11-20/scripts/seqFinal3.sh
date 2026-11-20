#!/bin/bash
# seqFinal3.sh [tag]: saved-state verification, round 3. Plans: U_A (run direction changes), U_B (sprint/walk), St2 (starts incl.
# turn starts, real X toggle), Qt (tempo stops/turns, real X toggle). 60 Hz, 30 Hz, variable 22-60 Hz; slide from clip contacts.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; T=${1:-f3}; PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
HKF="$(cat Saved/UE59Work/hk_line.txt)"; O=Saved/UE59Work/final_$T.txt; : > $O
for m in 60 30 var; do
  if [ $m = var ]; then HZ=60.0; X="$HKF; builtins.VID_VARDT=(22.0,60.0)"; else HZ=$m.0; X="$HKF"; fi
  for p in A:planU_A B:planU_B S:planSt2 Q:planQt; do l=${T}_${p%%:*}_$m; f=Saved/UE59Work/${p##*:}.txt
    DFPS=$HZ bash Tools/UE59_20261120/seqP.sh $l $f "$X" | grep -E "VIDREC|SLOT_CH"
    echo "#### $l" >> $O; "$PY" Tools/UE59_20261120/an_slide2.py $l $f 8 >> $O; "$PY" Tools/UE59_20261120/an_start.py $l $f | tail -1 >> $O
    "$PY" Tools/UE59_20261119/an_stop3.py $l 2>&1 | grep seg | awk '{for(i=1;i<=NF;i++){if($i=="v_in")v=$(i+1); if($i=="stop")s=$(i+1); if($i=="path")p=$(i+1)}; printf "%s:%s/%s  ", v,s,p} END{print ""}' >> $O
    "$PY" Tools/UE59_20261120/an_pop.py $l | head -1 >> $O
  done
done
VSHOT=1 bash Tools/UE59_20261119/fin19.sh F22 flow 2>&1 | tail -3 >> $O; "$PY" Tools/UE59_20261119/an_flow19.py F19_flow_F22 2>&1 | grep -E "^==|CHECK" >> $O
echo SEQFINAL3_DONE
