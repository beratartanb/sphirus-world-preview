#!/bin/bash
# seqB.sh <tag> [prelude]: upper-body review videos (30 Hz fixed step, 30 fps encode = real speed) of walk start + jog 2 s -> walk
# from front 3/4 (35), side (90), back 3/4 (150). Camera aims at spine_05, FOV 40, 200 cm.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; T=$1; X=${2:-pass}
echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
P="[('',1.5,0),('W',4.0,0),('W LeftShift',2.5,0),('W',5.0,0),('',1.5,0)]"
for a in ${ANG:-35 90 150}; do VSHOT=1 VSIDE="(200,$a,0,0,'spine_05')" bash Tools/UE59_20261118/run2.sh B_${T}_a$a -6000 2000 92 0 "$P" "$X"; done
echo "/Game/GraceRanger/Maps/L_GR_SphirusHouse" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
echo SEQB_DONE
