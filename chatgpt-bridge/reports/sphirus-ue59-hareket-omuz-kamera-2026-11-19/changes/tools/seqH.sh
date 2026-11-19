#!/bin/bash
# seqH.sh <suffix> [prelude]: walk + jog exact-angle flicks (+-45/90/135/180) on the flat map, 60 Hz data.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; . Tools/UE59_20261116/plans.sh; S=$1; X=${2:-pass}
echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
for g in ${TS:-W J}; do case $g in
  W) bash Tools/UE59_20261118/run2.sh H_W_$S -6000 2000 92 0 "$PLAN_HIPW" "import builtins; $X";;
  J) bash Tools/UE59_20261118/run2.sh H_J_$S -6000 2000 92 0 "$PLAN_HIPJ" "import builtins; $X";;
esac; done
echo "/Game/GraceRanger/Maps/L_GR_SphirusHouse" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
echo SEQH_DONE
