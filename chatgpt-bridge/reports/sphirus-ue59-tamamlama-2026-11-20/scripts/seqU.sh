#!/bin/bash
# seqU.sh: real W/A/S/D direction-change set (camera yaw fixed), saved state, move test map. TAG=label suffix, PRE=prelude python.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"
echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
J="W LeftShift"; SP="W LeftShift LeftControl"
PA="[('',1.5,0),('$J',3.0,0),('S LeftShift',2.2,0),('$J',2.2,0),('',2.0,0),('$J',3.0,0),('S',2.2,0),('',2.0,0),('$J',3.0,0),('A LeftShift',2.0,0),('D LeftShift',2.0,0),('A LeftShift',2.0,0),('',2.0,0),('$J',2.5,0),('W A LeftShift',1.5,0),('W D LeftShift',1.5,0),('',2.0,0),('$J',2.5,0),('D LeftShift',2.0,0),('',2.0,0)]"
PB="[('',1.5,0),('$SP',3.5,0),('S LeftShift LeftControl',2.2,0),('',2.5,0),('$SP',3.5,0),('D LeftShift LeftControl',2.0,0),('A LeftShift LeftControl',2.0,0),('',2.5,0),('W',3.0,0),('S',2.2,0),('W',2.2,0),('A',2.0,0),('D',2.0,0),('',2.0,0),('W',0.15,0),('',1.2,0),('$J',0.2,0),('',1.2,0),('$J',0.5,0),('',1.5,0),('$J',3.0,0),('W',2.5,0),('$J',2.0,0),('',2.0,0)]"
echo "$PA" > Saved/UE59Work/planU_A.txt; echo "$PB" > Saved/UE59Work/planU_B.txt
for hz in ${HZ:-60}; do
  [ -z "$ONLY" -o "$ONLY" = A ] && DFPS=$hz.0 bash Tools/UE59_20261118/run2.sh U_A_$hz${TAG} -6000 2000 92 0 "$PA" "${PRE:-pass}"
  [ -z "$ONLY" -o "$ONLY" = B ] && DFPS=$hz.0 bash Tools/UE59_20261118/run2.sh U_B_$hz${TAG} -6000 2000 92 0 "$PB" "${PRE:-pass}"
done
echo SEQU_DONE
