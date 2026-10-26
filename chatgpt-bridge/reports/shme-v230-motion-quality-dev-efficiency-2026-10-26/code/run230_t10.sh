#!/bin/bash
# run230_t10.sh : fresh editor: Routing funcs (low-speed class: recent run = peak OR effort) + EarlyRev widening patch + sprint-curve upper-body
# re-author (stride 1.0) -> warm-ups -> index quiet -> tests (lr2 / lrL, walk safety after sprint).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; T=Tools/SHME_V230_20261026; R="bash $V2/run_v2.sh"
D=Saved/Codex/SHME_V230_20261026; export O=$D/chain.out; source $D/lib230.sh
L=$D/t10_$(date +%H%M%S).log
step() { echo "== $2 $(date +%T)" | tee -a "$L"; out=$($R "$1" "$2" "${3:-900}"); echo "$out" | tail -c 3000 | tee -a "$L"; echo "$out" | grep -a "EARLYREV2_230 {" | cut -c1-500 >> $O; echo "$out" | grep -qE "^ERROR|FAIL |Traceback|TIMEOUT|REFUSED|AssertionError" && { echo "T10_FAILED $2 $(date +%T)" >> $O; exit 1; }; }
echo "T10 start $(date +%T)" >> $O
relaunch t10 30
step $V21/revert_noquit.py revert 300
step $V2/gc_job.py gc0 120
step $T/only_v230r.py only 60
step $V1/build_funcs.py funcs 1500
step $V2/save_comp.py save_comp 300
step $V2/only_all.py only_all 60
step $D/req/install_earlyrev2_save.py earlyrev2 900
bash $R $D/req/ra_curves.py ra_curves 2400 > $D/ra_curves.out 2>&1; grep -a '"saved"' -o $D/ra_curves.out | wc -l | sed 's/^/T10 curves saved count /' >> $O
export WARM=1 MEMPROBE=1
ab t10w "d_sprint:lr2 e29_chain:lrL j24_ph0:lr2 s29_dg:lr2" $D/vars230.sh
LOG="Saved/Logs/$LR_LOG"; for i in $(seq 1 40); do n1=$(grep -a -c "BuildIndex" "$LOG"); sleep 15; n2=$(grep -a -c "BuildIndex" "$LOG"); [ "$n1" = "$n2" ] && break; done
echo "T10 index quiet $(date +%T)" >> $O
J=""; for s in e29_load e29_chain e29_recov s29_swl12 s29_swl14 j30_slow w30_rev w30_postsprint c29_combo s29_ws j24_ph0 d_sprint s29_dg s29_sa chain_sscut; do J="$J $s:lr2 $s:lrL"; done
ab t10 "$J" $D/vars230.sh
echo "T10_DONE $(date +%T)" >> $O
