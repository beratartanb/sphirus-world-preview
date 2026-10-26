#!/bin/bash
# run230_t3.sh : ONE fresh editor (measured): Routing funcs rebuild -> save -> re-author measure v3 -> loaded family dry run -> tests in the SAME
# session (no relaunch after the build: V2.30 tests whether the post-build relaunch is needed).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; T=Tools/SHME_V230_20261026; R="bash $V2/run_v2.sh"
D=Saved/Codex/SHME_V230_20261026; export O=$D/chain.out; source $D/lib230.sh
L=$D/t3_$(date +%H%M%S).log
step() { echo "== $2 $(date +%T)" | tee -a "$L"; out=$($R "$1" "$2" "${3:-900}"); echo "$out" | tail -c 3000 | tee -a "$L"; echo "$out" | grep -qE "^ERROR|FAIL |Traceback|TIMEOUT|REFUSED|AssertionError" && { echo "T3_FAILED $2 $(date +%T)" >> $O; exit 1; }; tasklist | grep -qi UnrealEditor.exe || { echo "T3_FAILED editor gone at $2" >> $O; exit 1; }; }
echo "T3 start $(date +%T)" >> $O
relaunch t3 30
step $V21/revert_noquit.py revert 300
step $V2/gc_job.py gc0 120
step $T/only_v230r.py only 60
step $V1/build_funcs.py funcs 1500
step $V2/save_comp.py save_comp 300
step $V2/only_all.py only_all 60
echo "T3 build done $(date +%T) mem $(powershell.exe -NoProfile -Command "[math]::Round((Get-Process UnrealEditor).PrivateMemorySize64/1GB,1)" | tr -d '\r') GB" >> $O
bash $R $D/req/ra_measure.py ra_measure3 900 > $D/ra_measure3.out 2>&1
bash $R $D/req/gen230L_dry.py gen230L_dry 1800 > $D/gen230L_dry.out 2>&1; grep -a "Traceback" $D/gen230L_dry.out | head -2 >> $O
export WARM=1 MEMPROBE=1
J=""; for s in e29_chain e29_load s29_swl12 s29_swl14 chain_sprint j30_slow s29_dg s29_sa j24_ad_ph0 c29_ad; do J="$J $s:lr2"; done
ab t3 "$J" $D/vars230.sh
echo "T3_DONE $(date +%T)" >> $O
