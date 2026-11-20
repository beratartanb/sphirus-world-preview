#!/bin/bash
# seqP.sh <label> <planfile> [prelude]: one recording on the move test map (DFPS, VSHOT, VSIDE honoured), saved+in-memory state.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"
echo "${MAP:-/Game/Sphirus/Test/L_Sph_MoveTest}" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
bash Tools/UE59_20261118/run2.sh "$1" ${POS:--6000 2000 92 0} "$(cat "$2")" "${3:-pass}"
