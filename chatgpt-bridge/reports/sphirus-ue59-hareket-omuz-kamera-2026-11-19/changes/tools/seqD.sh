#!/bin/bash
# seqD.sh: relax-term screening on the saved p3 chain (runtime VID_BODY values), walk / jog 2 s->walk / jog 10 s->walk, 60 Hz data.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"
echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
VW="'VW_ClavL':(0,-3,3),'VW_ClavR':(0,3,-3),'VW_ArmL':(0,-3,0),'VW_ArmR':(0,3,0),'VW_Spine5':(4,0,0)"
R0="builtins.VID_BODY={}"; R1="builtins.VID_BODY={$VW}"
R2="builtins.VID_BODY={$VW,'VD_ClavL':(0,-3,2),'VD_ClavR':(0,3,-2),'VD_ArmL':(0,-5,0),'VD_ArmR':(0,5,0)}"
R3="builtins.VID_BODY={$VW,'VD_ClavL':(0,-5,3),'VD_ClavR':(0,5,-3),'VD_ArmL':(0,-9,0),'VD_ArmR':(0,9,0),'VD_Spine5':(3,0,0)}"
for c in ${CS:-R0 R1 R2 R3}; do eval X=\$$c
  bash Tools/UE59_20261118/run2.sh D_walk_$c -6000 2000 92 0 "[('',2.0,0),('W',8.0,0),('',2.0,0)]" "import builtins; $X"
  bash Tools/UE59_20261118/run2.sh D_jw2_$c -6000 2000 92 0 "[('',2.0,0),('W LeftShift',2.0,0),('W',8.0,0),('',2.0,0)]" "import builtins; $X"
  bash Tools/UE59_20261118/run2.sh D_jw10_$c -6000 2000 92 0 "[('',2.0,0),('W LeftShift',10.0,0),('W',8.0,0),('',2.0,0)]" "import builtins; $X"
done
echo "/Game/GraceRanger/Maps/L_GR_SphirusHouse" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
echo SEQD_DONE
