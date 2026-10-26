#!/bin/bash
# run230_t6.sh : fresh editor: Routing funcs rebuild (low-speed class = backpedal only) -> loaded family dry k 0.5 -> gate -> write, DBs, curves,
# loaded-route patch -> tests in the same session (lr2 recheck on the chains + loaded route A/B).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; T=Tools/SHME_V230_20261026; R="bash $V2/run_v2.sh"
D=Saved/Codex/SHME_V230_20261026; export O=$D/chain.out; source $D/lib230.sh; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
L=$D/t6_$(date +%H%M%S).log
step() { echo "== $2 $(date +%T)" | tee -a "$L"; out=$($R "$1" "$2" "${3:-900}"); echo "$out" | tail -c 3000 | tee -a "$L"; echo "$out" | grep -qE "^ERROR|FAIL |Traceback|TIMEOUT|REFUSED|AssertionError" && { echo "T6_FAILED $2 $(date +%T)" >> $O; exit 1; }; }
echo "T6 start $(date +%T)" >> $O
relaunch t6 30
step $V21/revert_noquit.py revert 300
step $V2/gc_job.py gc0 120
step $T/only_v230r.py only 60
step $V1/build_funcs.py funcs 1500
step $V2/save_comp.py save_comp 300
step $V2/only_all.py only_all 60
bash $R $D/req/ra_write_inplace.py ra_write 2400 > $D/ra_write6.out 2>&1; grep -a "Traceback\|LEG_GUARD_FAIL" $D/ra_write6.out | head -3 | cut -c1-400 >> $O
grep -a "RA230 {" $D/ra_write6.out | grep -q '"mode": "inplace"' && echo "T6 reauthor written $(date +%T)" >> $O || echo "T6 reauthor NOT written" >> $O
LOADED=0
bash $R $D/req/gen230L_dry5.py gen230L_dry5 1800 > $D/gen230L_dry5.out 2>&1
if "$PY" $D/gate230L.py $D/gen230L_dry5.out >> $O; then
  bash $R $D/req/gen230L_write5.py gen230L_write5 2400 > $D/gen230L_write5.out 2>&1; "$PY" $D/gate230L.py $D/gen230L_write5.out >> $O && {
  bash $R $D/req/db230L_write.py db230L 1800 > $D/db230L.out 2>&1; grep -a "RDB226\|Traceback" $D/db230L.out | cut -c1-600 >> $O
  bash $R $D/req/curves230L_write.py curves230L 1800 > $D/curves230L.out 2>&1; grep -a "CURVE\|Traceback" $D/curves230L.out | cut -c1-300 >> $O
  bash $R $D/req/loadroute_save.py loadroute 900 > $D/loadroute.out 2>&1; grep -a "LOADROUTE230 {\|Traceback" $D/loadroute.out | cut -c1-600 >> $O
  grep -aq '"ok": true' $D/loadroute.out && LOADED=1; }
else echo "T6 loaded gate failed (k 0.5)" >> $O; fi
export WARM=1 MEMPROBE=1
J=""; for s in e29_chain e29_load s29_swl12 s29_swl14 e29_recov j30_slow chain_sprint s29_dg; do J="$J $s:lr2"; done
for s in d_sprint s29_ws e29_rest chain_sscut s29_sa c29_combo a29_ang a29_angb j24_ad_ph0 c29_jlook j24_ph0 taps s23_jstart; do J="$J $s:lr2"; done
[ $LOADED = 1 ] && for s in e29_chain e29_load e29_recov chain_sscut e29_rest s29_ws j24_ph0 j24_dbl; do J="$J $s:lrL"; done
ab t6 "$J" $D/vars230.sh
echo "T6_DONE $(date +%T)" >> $O
