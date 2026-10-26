#!/bin/bash
# run230_t7.sh : SAME editor as T6: remaining re-author (curves / push links / rear walk / lateral jog; per-clip guard fallback), loaded family
# (53 gated bins) -> DBs -> curves -> loaded-route patch, then after-tests (re-author families) + loaded-route A/B.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V230_20261026; R=Tools/SHME_V2_20261014/run_v2.sh; export O=$D/chain.out; source $D/lib230.sh; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
echo "T7 start $(date +%T)" >> $O
bash $R $D/req/ra_write2_inplace.py ra_write2 2400 > $D/ra_write7.out 2>&1; grep -a "Traceback" $D/ra_write7.out | head -2 >> $O
grep -a "RA230 {" $D/ra_write7.out | grep -q '"mode": "inplace"' && echo "T7 reauthor written $(date +%T)" >> $O || echo "T7 reauthor NOT written" >> $O
LOADED=0
bash $R $D/req/gen230L_write_good.py gen230L_wg 2400 > $D/gen230L_wg.out 2>&1; grep -a "Traceback" $D/gen230L_wg.out | head -2 >> $O
if grep -aq "G230L {" $D/gen230L_wg.out; then
  bash $R $D/req/db230L_write.py db230L 1800 > $D/db230L.out 2>&1; grep -a "RDB226\|Traceback" $D/db230L.out | cut -c1-500 >> $O
  bash $R $D/req/curves230L_write.py curves230L 1800 > $D/curves230L.out 2>&1; grep -a "CURVE\|Traceback" $D/curves230L.out | cut -c1-300 >> $O
  bash $R $D/req/loadroute_save.py loadroute 900 > $D/loadroute.out 2>&1; grep -a "LOADROUTE230 {\|Traceback" $D/loadroute.out | cut -c1-600 >> $O
  grep -aq '"ok": true' $D/loadroute.out && LOADED=1
fi
export WARM=1 MEMPROBE=1
J=""; for s in d_sprint s29_ws e29_rest chain_sscut s29_sa c29_combo a29_ang a29_angb j24_ad_ph0 c29_jlook j24_ph0 taps s23_jstart; do J="$J $s:lr2"; done
[ $LOADED = 1 ] && for s in e29_chain e29_load e29_recov chain_sscut e29_rest s29_ws j24_ph0 j24_dbl s29_dbl; do J="$J $s:lrL"; done
ab t7 "$J" $D/vars230.sh
echo "T7_DONE $(date +%T)" >> $O
