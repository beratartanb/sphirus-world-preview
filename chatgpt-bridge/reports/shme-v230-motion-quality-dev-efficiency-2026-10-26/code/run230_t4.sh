#!/bin/bash
# run230_t4.sh : SAME editor as T3 (no relaunch): loaded family dry v2 (measured-table tempo) -> gate (no errors, planted drift <= 3 cm, foot error
# like production r4) -> write 64 clips, DBs, curves -> ABP loaded-route patch (knob off) -> A/B production vs loaded route on the effort chains.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V230_20261026; R=Tools/SHME_V2_20261014/run_v2.sh; export O=$D/chain.out; source $D/lib230.sh
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
echo "T4 start $(date +%T)" >> $O
bash $R $D/req/gen230L_dry.py gen230L_dry2 1800 > $D/gen230L_dry2.out 2>&1
"$PY" $D/gate230L.py $D/gen230L_dry2.out >> $O || { echo "T4_STOP gate" >> $O; exit 1; }
bash $R $D/req/gen230L_write.py gen230L_write 2400 > $D/gen230L_write.out 2>&1; "$PY" $D/gate230L.py $D/gen230L_write.out >> $O || { echo "T4_STOP write" >> $O; exit 1; }
bash $R $D/req/db230L_write.py db230L 1800 > $D/db230L.out 2>&1; grep -a "RDB226\|Traceback" $D/db230L.out | cut -c1-600 >> $O
bash $R $D/req/curves230L_write.py curves230L 1800 > $D/curves230L.out 2>&1; grep -a "CURVE\|Traceback" $D/curves230L.out | cut -c1-300 >> $O
bash $R $D/req/loadroute_save.py loadroute 900 > $D/loadroute.out 2>&1; grep -a "LOADROUTE230 {\|Traceback" $D/loadroute.out | cut -c1-600 >> $O
grep -aq '"ok": true' $D/loadroute.out || { echo "T4_STOP loadroute" >> $O; exit 1; }
export WARM=1 MEMPROBE=1
J=""; for s in e29_chain e29_load e29_recov chain_sscut e29_rest s29_ws s29_dbl j24_ph0 j24_dbl; do J="$J $s:lr2 $s:lrL"; done
ab t4 "$J" $D/vars230.sh
echo "T4_DONE $(date +%T)" >> $O
