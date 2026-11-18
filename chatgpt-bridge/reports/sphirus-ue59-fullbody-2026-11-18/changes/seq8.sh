#!/bin/bash
# seq8.sh: redo after restoring the vegetation show flags: matched perf, bridge export, interaction-flow video
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"
bash Tools/UE59_20261118/perf18.sh M18v
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/UE59_20261118/export_standard18.py" emb_bridge3 300 2>&1 | tail -1
sleep 90
VSHOT=1 bash Tools/UE59_20261118/wood18.sh C flow
echo SEQ8_DONE
