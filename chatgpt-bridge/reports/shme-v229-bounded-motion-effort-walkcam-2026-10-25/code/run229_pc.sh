#!/bin/bash
# run229_pc.sh : V2.29 push-phase cancel. A) fresh editor: install SHM229_PushCancel (knob OFF, ABPs saved); B) fresh editor 30 FPS:
# production (o) vs candidate (pc) on the push-phase reversal sweep + the V2.28 reversal regressions.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; R="bash $V2/run_v2.sh"
D=Saved/Codex/SHME_V229_20261025; export O=$D/chain.out; source $D/lib229.sh
L=$D/build_pc_$(date +%H%M%S).log
step() { echo "== $2 $(date +%T)" | tee -a "$L"; out=$($R "$1" "$2" "${3:-900}"); echo "$out" | tail -c 3000 | tee -a "$L"; echo "$out" | grep -qE "^ERROR|FAIL |Traceback|TIMEOUT|REFUSED|AssertionError" && { echo "STOP at $2" | tee -a "$L"; echo "PC229_FAILED $2 $(date +%T)" >> $O; exit 1; }; }
echo "PC229 start $(date +%T)" >> $O
relaunch pcA 30
step $V21/revert_noquit.py revert 300; grep -q "dirty after reload \[\]" "$L" || { echo "PC229_FAILED dirty" >> $O; exit 1; }
step $D/req/install_pushcancel_save.py pushcancel229 900; grep -a "PUSHCANCEL229 {" "$L" | cut -c1-600 >> $O
grep -a "PUSHCANCEL229 {" "$L" | grep -q '"ok": true' || { echo "PC229_FAILED install" >> $O; exit 1; }
echo "PC229 installed $(date +%T)" >> $O
relaunch pcB 30; export WARM=1
J=""; for s in e29_load s29_swl08 s29_swl10 s29_swl12 s29_swl14 s29_swl16 s29_swl20 j29_swl10 j29_swl14 j29_swl20; do J="$J $s:o $s:pc"; done
ab v229pc "$J" $D/vars229f.sh
J=""; for s in j24_dbl j24_rel j24_ph0 j24_ph3 j24_sw_ph0 j24_sw_ph2 j24_ad_ph0 s29_dbl s29_ws e29_chain chain_sscut s29_cam; do J="$J $s:o $s:pc"; done
ab v229pc "$J" $D/vars229f.sh
echo "PC229_DONE $(date +%T)" >> $O
