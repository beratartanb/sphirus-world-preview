#!/bin/bash
# seqW.sh: jog->walk with forward input held (2 s and 10 s jog, 6 s walk), flat test map, 60 Hz data, variants in VS (prelude per variant).
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"
echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
vda="import builtins; builtins.VID_BODY={'VD_ArmL':(0,-2,0),'VD_ArmR':(0,2,0)}"
vdb="import builtins; builtins.VID_BODY={'VD_ArmL':(0,0,0),'VD_ArmR':(0,0,0),'VD_ClavL':(0,-1.5,1),'VD_ClavR':(0,1.5,-1)}"
base="pass"; vd0="import builtins; builtins.VID_BODY={'VD_ArmL':(0,0,0),'VD_ArmR':(0,0,0)}"
for v in ${VS:-vda vdb}; do eval X=\$$v
  for d in ${DS:-2 10}; do bash Tools/UE59_20261118/run2.sh A_jw${d}_$v -6000 2000 92 0 "[('',2.0,0),('W LeftShift',$d.0,0),('W',6.0,0),('',2.0,0)]" "$X" | grep -c SLOT_OK; done
done
echo SEQW_DONE
