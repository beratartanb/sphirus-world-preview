#!/bin/bash
# seqC.sh: steady-walk shoulder/arm relaxation screening (runtime VI_ overrides on the body ABP, walk-only plan, 60 Hz data).
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"
echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
P="[('',2.0,0),('W',10.0,0),('',2.0,0)]"
W1="builtins.VID_BODY={'VI_ClavL':(0,-3,3),'VI_ClavR':(0,3,-3),'VI_ArmL':(9,-6,0),'VI_ArmR':(9,6,0)}"
W2="builtins.VID_BODY={'VI_ClavL':(0,-6,6),'VI_ClavR':(0,6,-6),'VI_ArmL':(9,-9,0),'VI_ArmR':(9,9,0)}"
W3="builtins.VID_BODY={'VI_ClavL':(0,-3,3),'VI_ClavR':(0,3,-3),'VI_ArmL':(9,-6,0),'VI_ArmR':(9,6,0),'VI_Spine5':(-8,0,0)}"
for c in W1 W2 W3; do eval X=\$$c; bash Tools/UE59_20261118/run2.sh C_walk_$c -6000 2000 92 0 "$P" "import builtins; $X"; done
echo "/Game/GraceRanger/Maps/L_GR_SphirusHouse" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
echo SEQC_DONE
