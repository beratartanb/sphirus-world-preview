#!/bin/bash
# seqFinal.sh [tag]: saved-state verification, 4 plans x (60 Hz, 30 Hz, variable 22-60 Hz) data-only on simulated time.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; T=${1:-fin}; PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
ON="import builtins; builtins.VID_PAWN={'GR_TempoOn':True}"
for m in 60 30 var; do
  if [ $m = var ]; then HZ=60.0; X="import builtins; builtins.VID_VARDT=(22.0,60.0)"; XO="$ON; builtins.VID_VARDT=(22.0,60.0)"; else HZ=$m.0; X="pass"; XO="$ON"; fi
  DFPS=$HZ bash Tools/UE59_20261120/seqP.sh ${T}_A_$m Saved/UE59Work/planU_A.txt "$X" | grep -E "VIDREC|SLOT_CH"
  DFPS=$HZ bash Tools/UE59_20261120/seqP.sh ${T}_B_$m Saved/UE59Work/planU_B.txt "$X" | grep -E "VIDREC|SLOT_CH"
  DFPS=$HZ bash Tools/UE59_20261120/seqP.sh ${T}_C_$m Saved/UE59Work/planC.txt "$X" | grep -E "VIDREC|SLOT_CH"
  DFPS=$HZ bash Tools/UE59_20261120/seqP.sh ${T}_V_$m Saved/UE59Work/planV.txt "$XO" | grep -E "VIDREC|SLOT_CH"
done
O=Saved/UE59Work/final_$T.txt; : > $O
for m in 60 30 var; do
  for p in A:planU_A B:planU_B C:planC V:planV; do l=${T}_${p%%:*}_$m; f=Saved/UE59Work/${p##*:}.txt
    echo "#### $l" >> $O; "$PY" Tools/UE59_20261120/an_revslide.py $l $f | sed 's/ LeftShift/+Sh/g; s/ LeftControl/+Ct/g' >> $O
    "$PY" Tools/UE59_20261119/an_stop3.py $l 2>&1 | grep seg | sed 's/ LeftShift/+Sh/g; s/ LeftControl/+Ct/g; s/ | slide.*drift/ | drift/' | cut -c1-200 >> $O
    "$PY" Tools/UE59_20261120/an_pop.py $l | head -1 >> $O
  done
done
echo SEQFINAL_DONE
