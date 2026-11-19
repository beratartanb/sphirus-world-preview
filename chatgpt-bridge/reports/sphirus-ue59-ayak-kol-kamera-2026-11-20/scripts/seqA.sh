#!/bin/bash
# seqA.sh: shoulder/arm baseline on the flat test map (saved state, 60 Hz data step, no video). W held throughout in R*.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"
echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
X=${X:-pass}; S=${S:-base}
bash Tools/UE59_20261118/run2.sh A_walk_$S -6000 2000 92 0 "[('',2.0,0),('W',10.0,0),('',2.0,0)]" "$X"
bash Tools/UE59_20261118/run2.sh A_jw2_$S -6000 2000 92 0 "[('',2.0,0),('W LeftShift',2.0,0),('W',10.0,0),('',2.0,0)]" "$X"
bash Tools/UE59_20261118/run2.sh A_jw10_$S -6000 2000 92 0 "[('',2.0,0),('W LeftShift',10.0,0),('W',10.0,0),('',2.0,0)]" "$X"
echo "/Game/GraceRanger/Maps/L_GR_SphirusHouse" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
echo SEQA_DONE
