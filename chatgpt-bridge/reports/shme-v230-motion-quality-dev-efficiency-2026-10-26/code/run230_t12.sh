#!/bin/bash
# run230_t12.sh : fresh editor: Routing funcs (low-speed class gated by the requested gait) + EarlyRev v3 (same gate) -> warm -> index quiet ->
# low-speed + walk-safety tests (lr2).  Then run230_t13.sh: real-time editor (no fixed step) cold-start + 0.4 s stall inside the sprint RevTurn.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; T=Tools/SHME_V230_20261026; R="bash $V2/run_v2.sh"
D=Saved/Codex/SHME_V230_20261026; export O=$D/chain.out; source $D/lib230.sh
L=$D/t12_$(date +%H%M%S).log
step() { echo "== $2 $(date +%T)" | tee -a "$L"; out=$($R "$1" "$2" "${3:-900}"); echo "$out" | tail -c 3000 | tee -a "$L"; echo "$out" | grep -a "EARLYREV3_230 {" | cut -c1-500 >> $O; echo "$out" | grep -qE "^ERROR|FAIL |Traceback|TIMEOUT|REFUSED|AssertionError" && { echo "T12_FAILED $2 $(date +%T)" >> $O; exit 1; }; }
echo "T12 start $(date +%T)" >> $O
relaunch t12 30
step $V21/revert_noquit.py revert 300
step $V2/gc_job.py gc0 120
step $T/only_v230r.py only 60
step $V1/build_funcs.py funcs 1500
step $V2/save_comp.py save_comp 300
step $V2/only_all.py only_all 60
step $D/req/install_earlyrev3_save.py earlyrev3 900
export WARM=1 MEMPROBE=1
ab t12w "j24_ph0:lr2 e29_chain:lr2 d_sprint:lr2" $D/vars230.sh
LOG="Saved/Logs/$LR_LOG"; for i in $(seq 1 40); do n1=$(grep -a -c "BuildIndex" "$LOG"); sleep 15; n2=$(grep -a -c "BuildIndex" "$LOG"); [ "$n1" = "$n2" ] && break; done
J=""; for s in w30_postsprint w30_rev e29_load e29_chain e29_recov s29_swl12 s29_swl14 s29_swl16 j30_slow c29_combo j24_ph0 j24_dbl s29_ws s29_dg; do J="$J $s:lr2"; done
ab t12 "$J" $D/vars230.sh
echo "T12_DONE $(date +%T)" >> $O
