#!/bin/bash
# run231_s3.sh : slow family r2 (a support foot still landing at tau0 completes the loop landing instead of an air pin; 60 FPS swl12 drag 44 cm)
# fresh fixed-30 editor: dry -> write (all 32 when the dry metrics pass) -> rev/speed curves -> DB rebuild -> warm -> 30 FPS check; then a
# fixed-60 editor check of the same entries.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V231_20261026; R="bash Tools/SHME_V2_20261014/run_v2.sh"; export O=$D/chain.out; source $D/lib231.sh
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
until grep -aq "F_DONE" $O; do sleep 30; done
echo "S3 start $(date +%T)" >> $O
relaunch s3 30
$R $D/req/gen_slow_dry.py gslow2 900 > $D/gslow_dry2.out 2>&1
"$PY" $D/an_gslow.py $D/gslow_dry2.out G231S > $D/gslow_dry2.txt
BAD=$("$PY" -c "
import json; d=json.load(open('Saved/Codex/SHME_V231_20261026/gen231_slow_dry.json'))
print(sum(1 for v in d['clips'].values() if v.get('err') or v.get('planted_drift',99)>=3 or v.get('foot_err',99)>=8))")
echo "SLOW_R2_DRY bad=$BAD" >> $O
if [ "$BAD" -le 2 ]; then
  $R $D/req/gen_slow_write.py gslow_w2 900 > $D/gslow_write2.out 2>&1; echo "SLOW_R2_WRITE saved=$(grep -a -o '"saved": true' $D/gslow_write2.out | wc -l)" >> $O
  $R $D/req/curves_slow.py curves2 600 > $D/curves_slow2.out 2>&1; echo "SLOW_R2_CURVES $(grep -a -o 'SPEEDCURVE228 {"dry": false, "n": [0-9]*, "saved": [0-9]*' $D/curves_slow2.out)" >> $O
  $R $D/req/db_slow.py dbslow2 600 > $D/db_slow2.out 2>&1; echo "SLOW_R2_DB $(grep -a -c 'SHM231S_SlowRev_' $D/db_slow2.out)" >> $O
else echo "SLOW_R2 not written (dry bad $BAD)" >> $O; fi
export WARM=1 MEMPROBE=1
ab s3w "s29_swl12:P:0 j30_rel_3100:P:0" $D/vars231.sh
LOG="Saved/Logs/$LR_LOG"; for i in $(seq 1 40); do n1=$(grep -a -c "BuildIndex" "$LOG"); sleep 15; n2=$(grep -a -c "BuildIndex" "$LOG"); [ "$n1" = "$n2" ] && break; done
export WARM=0
ab s3 "s29_swl12:P:1 s29_swl12:P:2 s29_swl12:P:3 j30_rel_3100:P j30_rel_3200:P j30_slow:P e29_load:P j24_ph0:P c30_calm:P" $D/vars231.sh
relaunch s3b 60
export WARM=1; ab s3bw "s29_swl12:P:0" $D/vars231.sh; LOG="Saved/Logs/$LR_LOG"; for i in $(seq 1 40); do n1=$(grep -a -c "BuildIndex" "$LOG"); sleep 15; n2=$(grep -a -c "BuildIndex" "$LOG"); [ "$n1" = "$n2" ] && break; done
export WARM=0
ab s3b "s29_swl12:P:1 s29_swl12:P:2 j30_rel_3100:P e29_load:P e29_chain:P" $D/vars231.sh
echo "S3_DONE $(date +%T)" >> $O
