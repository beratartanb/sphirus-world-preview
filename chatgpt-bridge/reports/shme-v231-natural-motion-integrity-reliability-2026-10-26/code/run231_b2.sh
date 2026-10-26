#!/bin/bash
# run231_b2.sh : V2.31 B2 (same editor as B1, fixed 30): curve rebake from the V2.30 sprint loop (RATE 1.0), loaded catch-step F_B family
# (32 bins, clean ones only), TIP-end hold patch, warm + index quiet, A3 tests.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V231_20261026; R="bash Tools/SHME_V2_20261014/run_v2.sh"; export O=$D/chain.out; source $D/lib231.sh
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
until grep -aq "B1D_DONE" $O; do sleep 20; done
echo "B2 start $(date +%T)" >> $O
# pending harness fix (qa.sh was locked during the B1 batch): fast failure of a qa_pie job that never starts PIE
[ -f $D/req/qa.sh.v231_pending ] && cp $D/req/qa.sh.v231_pending Tools/SHME_V1_20260925/qa.sh && rm $D/req/qa.sh.v231_pending && echo "QA_SH fast-fail installed" >> $O
$R $D/req/curves_rebake_dry.py cdry 900 > $D/curves_dry.out 2>&1; echo "CURVES_DRY $(grep -a -o '"foot_err_cm": [0-9.]*' $D/curves_dry.out | tr '\n' ' ')" >> $O
if [ "$(grep -a -o '"foot_err_cm": [0-9.]*' $D/curves_dry.out | awk '{ if ($2 >= 0.5) b++ } END { print b+0 }')" = "0" ] && [ "$(grep -a -c '"foot_err_cm"' $D/curves_dry.out)" -ge 6 ]; then
  $R $D/req/curves_rebake_write.py cwrite 900 > $D/curves_write.out 2>&1; echo "CURVES_WRITE saved=$(grep -a -o '"saved": true' $D/curves_write.out | wc -l)" >> $O
  $R $D/req/curves_rate1.py crate 300 > $D/curves_rate.out 2>&1; echo "CURVES_RATE $(tail -1 $D/curves_rate.out | cut -c1-300)" >> $O
else echo "CURVES_SKIPPED (dry foot error)" >> $O; fi
$R $D/req/gen_loaded_dry32.py gl32 1200 > $D/gload_dry32.out 2>&1
"$PY" $D/pick_loaded.py Saved/Codex/SHME_V231_20261026/gen231_loaded_dry.json $D/loaded_good.json >> $O
printf 'import builtins, json\nbuiltins.G231L = {"dry_run": False, "fam": ["F_B"], "nph": 32, "only": json.load(open(r"%s/loaded_good.json"))}\nexec(open(r"%s/gen231_loaded.py", encoding="utf8").read())\n' "C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/$D" "C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V231_20261026" > $D/req/gen_loaded_write.py
$R $D/req/gen_loaded_write.py glw 1200 > $D/gload_write.out 2>&1; echo "LOADED_WRITE saved=$(grep -a -o '"saved": true' $D/gload_write.out | wc -l)" >> $O
printf 'import builtins\nbuiltins.V231_CURVE = {"dry": False, "prefix": "SHM231L_LoadRev_", "nph": 32}\nexec(open(r"C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V231_20261026/curves231.py", encoding="utf8").read())\n' > $D/req/curves_loaded.py
$R $D/req/curves_loaded.py lcurves 900 > $D/curves_loaded.out 2>&1; echo "LOADED_CURVES $(grep -a -o 'SPEEDCURVE228 {"dry": false, "n": [0-9]*, "saved": [0-9]*' $D/curves_loaded.out)" >> $O
printf 'import builtins\nbuiltins.V231_DB = {"dry": False, "nph": 32, "fam": "LoadRev", "tag": "SHM231L"}\nexec(open(r"C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V231_20261026/build_v231_dbs.py", encoding="utf8").read())\n' > $D/req/db_loaded.py
$R $D/req/db_loaded.py ldb 900 > $D/db_loaded.out 2>&1; echo "LOADED_DB $(grep -a -o 'RDB226.\{0,300\}' $D/db_loaded.out)" >> $O
$R $D/req/tipend_save.py tipend 900 > $D/tipend.out 2>&1; grep -a -o "TIPEND231.*\|Traceback.*\|Error:.*" $D/tipend.out | cut -c1-600 >> $O
echo "B2_BUILT $(date +%T)" >> $O
export WARM=1 MEMPROBE=1
ab b2w "d_sprint:o:0 e29_load:ld:0 legs_slope_sprint:te:0" $D/vars231.sh
LOG="Saved/Logs/$LR_LOG"; for i in $(seq 1 40); do n1=$(grep -a -c "BuildIndex" "$LOG"); sleep 15; n2=$(grep -a -c "BuildIndex" "$LOG"); [ "$n1" = "$n2" ] && break; done
export WARM=0
J="d_sprint:o s29_cam:o s29_ws:o legs_slope_sprint:o legs_slope_sprint:te s29_cam:te"
for v in o ld sx sxld; do for s in e29_load e29_chain e29_recov; do J="$J $s:$v"; done; done
for ms in 4700 4750 4800 4850 4900 4950; do for v in o sxld; do J="$J e31_s2_$ms:$v"; done; done
ab b2 "$J" $D/vars231.sh
echo "B2_DONE $(date +%T)" >> $O
