#!/bin/bash
# run230_build2.sh : V2.30 build B. Fresh editor: SHM_UpdateRouting + SHM_UpdateCameraV21 rebuild ALONE (profiles already saved in build A),
# save; then in the SAME editor the ABP family-gate graph patch (measured: V2.29 used a third editor for graph patches). Watchdog 3 s,
# kill above 55 GB. Memory samples between steps.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; T=Tools/SHME_V230_20261026; R="bash $V2/run_v2.sh"
D=Saved/Codex/SHME_V230_20261026; export O=$D/chain.out; source $D/lib230.sh
L=$D/build2_$(date +%H%M%S).log
gb() { powershell.exe -NoProfile -Command "\$p = Get-Process UnrealEditor -ErrorAction SilentlyContinue | Select-Object -First 1; if (\$p) { [math]::Round(\$p.PrivateMemorySize64/1GB) } else { 0 }" 2>/dev/null | tr -d '\r'; }
step() { echo "== $2 $(date +%T)" | tee -a "$L"; out=$($R "$1" "$2" "${3:-900}"); echo "$out" | tail -c 2500 | tee -a "$L"; echo "$out" | grep -a "MEM230\|FAMGATE230 {" | cut -c1-400 >> $O; echo "$out" | grep -qE "^ERROR|FAIL |Traceback|TIMEOUT|REFUSED|AssertionError" && { echo "STOP at $2" | tee -a "$L"; echo "BUILD230B_FAILED $2 $(date +%T)" >> $O; kill $WD 2>/dev/null; exit 1; }; tasklist | grep -qi UnrealEditor.exe || { echo "BUILD230B_FAILED editor gone at $2 $(date +%T)" >> $O; kill $WD 2>/dev/null; exit 1; }; }
echo "BUILD230B start $(date +%T)" >> $O
relaunch bB 30
( while true; do g=$(gb); echo "$(date +%T) $g" >> $D/build2_mem.log; [ -n "$g" ] && [ "$g" -gt 55 ] && { echo "WATCHDOG kill at $g GB $(date +%T)" >> $O; taskkill //F //IM UnrealEditor.exe; break; }; sleep 3; done ) & WD=$!
step $V21/revert_noquit.py revert 300; grep -q "dirty after reload \[\]" "$L" || { echo "BUILD230B_FAILED dirty" >> $O; kill $WD; exit 1; }
step $V2/gc_job.py gc0 120
step $D/req/mp_c0.py mp_c0 300
step $T/only_v230.py only_v230 60
step $V1/build_funcs.py funcs 1500
step $D/req/mp_c_funcs.py mp_c_funcs 300
step $V2/save_comp.py save_comp 300
step $V2/only_all.py only_all 60
step $D/req/mp_c_save.py mp_c_save 300
step $D/req/install_famgate_save.py famgate230 900
step $D/req/mp_c_patch.py mp_c_patch 300
kill $WD 2>/dev/null
echo "BUILD230B_DONE $(date +%T)" >> $O
