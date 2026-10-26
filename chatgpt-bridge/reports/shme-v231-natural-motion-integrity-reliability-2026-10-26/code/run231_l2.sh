#!/bin/bash
# run231_l2.sh : loaded catch-step family r2 (reach-limited support pin, pinned early landing) in the same editor after A3: dry -> pick ->
# write the clean bins -> speed/rev curves -> DB rebuild (BranchIn tracks are removed by write) -> warm.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V231_20261026; R="bash Tools/SHME_V2_20261014/run_v2.sh"; export O=$D/chain.out; source $D/lib231.sh
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
until grep -aq "A3_DONE" $O; do sleep 20; done
echo "L2 start $(date +%T)" >> $O
$R $D/req/gen_loaded_dry32.py gl32b 1200 > $D/gload_dry32b.out 2>&1
cp Saved/Codex/SHME_V231_20261026/gen231_loaded_dry.json $D/gen231_loaded_dry_r2.json
"$PY" $D/pick_loaded.py $D/gen231_loaded_dry_r2.json $D/loaded_good2.json >> $O
N2=$("$PY" -c "import json;print(len(json.load(open('$D/loaded_good2.json'))))"); N1=$("$PY" -c "import json;print(len(json.load(open('$D/loaded_good.json'))))")
if [ "$N2" -gt "$N1" ]; then
  sed "s#loaded_good.json#loaded_good2.json#" $D/req/gen_loaded_write.py > $D/req/gen_loaded_write2.py
  $R $D/req/gen_loaded_write2.py glw2 1200 > $D/gload_write2.out 2>&1; echo "LOADED_WRITE2 saved=$(grep -a -o '"saved": true' $D/gload_write2.out | wc -l)" >> $O
  $R $D/req/curves_loaded.py lcurves2 900 > $D/curves_loaded2.out 2>&1; echo "LOADED_CURVES2 $(grep -a -o 'SPEEDCURVE228 {"dry": false, "n": [0-9]*, "saved": [0-9]*' $D/curves_loaded2.out)" >> $O
  $R $D/req/db_loaded.py ldb2 900 > $D/db_loaded2.out 2>&1; echo "LOADED_DB2 $(grep -a -o '"PSD_SHM231L_LoadRevFwd": \[[^]]*\]' $D/db_loaded2.out | tr -cd 'P' | wc -c) bins" >> $O
else echo "LOADED_R2 not better ($N2 vs $N1) - keep r1" >> $O; fi
echo "L2_DONE $(date +%T)" >> $O
