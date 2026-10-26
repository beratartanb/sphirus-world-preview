#!/bin/bash
# run231_b1.sh : V2.31 build B1 (after A2B_DONE). Editor A: DA field SwingLiftBaseComp (build_profiles) + component variables (build_comp_vars)
# -> save. Editor B (fresh): SHM_UpdateBodyTargets + SHM_UpdateCameraV21 rebuilt ALONE -> save; inspection tick link fix; warm; B1 tests.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; T=Tools/SHME_V231_20261026; R="bash $V2/run_v2.sh"
D=Saved/Codex/SHME_V231_20261026; export O=$D/chain.out; source $D/lib231.sh
L=$D/b1_$(date +%H%M%S).log
gb() { powershell.exe -NoProfile -Command "\$p = Get-Process UnrealEditor -ErrorAction SilentlyContinue | Select-Object -First 1; if (\$p) { [math]::Round(\$p.PrivateMemorySize64/1GB) } else { 0 }" 2>/dev/null | tr -d '\r'; }
step() { echo "== $2 $(date +%T) mem $(gb) GB" | tee -a "$L"; out=$($R "$1" "$2" "${3:-900}"); echo "$out" | tail -c 2500 | tee -a "$L"; echo "$out" | grep -a "INSPECTTICK231 {" | cut -c1-600 >> $O; echo "$out" | grep -qE "^ERROR|FAIL |Traceback|TIMEOUT|REFUSED|AssertionError" && { echo "B1_FAILED $2 $(date +%T)" >> $O; kill $WD 2>/dev/null; exit 1; }; tasklist | grep -qi UnrealEditor.exe || { echo "B1_FAILED editor gone at $2 $(date +%T)" >> $O; kill $WD 2>/dev/null; exit 1; }; }
until grep -aq "A2B_DONE" $O; do sleep 30; done
echo "B1 start $(date +%T)" >> $O
relaunch b1a 30
( while true; do g=$(gb); [ -n "$g" ] && [ "$g" -gt 55 ] && { echo "WATCHDOG kill at $g GB $(date +%T)" >> $O; taskkill //F //IM UnrealEditor.exe; break; }; sleep 3; done ) & WD=$!
step $V21/revert_noquit.py revert 300; grep -q "dirty after reload \[\]" "$L" || { echo "B1_FAILED dirty" >> $O; kill $WD; exit 1; }
step $V2/gc_job.py gc0 120
step $V1/build_profiles.py profiles 900
step $V1/build_comp_vars.py comp_vars 900
step $V2/save_comp.py save_comp 300
kill $WD 2>/dev/null
relaunch b1b 30
( while true; do g=$(gb); [ -n "$g" ] && [ "$g" -gt 55 ] && { echo "WATCHDOG kill at $g GB $(date +%T)" >> $O; taskkill //F //IM UnrealEditor.exe; break; }; sleep 3; done ) & WD=$!
step $V21/revert_noquit.py revert 300
step $V2/gc_job.py gc1 120
step $T/only_v231.py only 60
step $V1/build_funcs.py funcs 1500
step $V2/save_comp.py save_comp2 300
step $V2/only_all.py only_all 60
step $D/req/inspect_tick_fix.py tickfix 600
bash $R $D/req/gen_loaded_dry.py gload 900 > $D/gload_dry.out 2>&1; echo "GLOAD_DRY $(grep -a -c "G231L " $D/gload_dry.out)" >> $O
bash $R $D/req/slide_audit.py slide 900 > $D/slide_audit.out 2>&1; echo "SLIDE_AUDIT $(grep -a -c "SLIDE231 " $D/slide_audit.out)" >> $O
kill $WD 2>/dev/null
echo "B1_BUILT $(date +%T)" >> $O
export WARM=1 MEMPROBE=1
ab b1w "ins_ws:ins2:0 ter_drop_walk:sl1:0" $D/vars231.sh
LOG="Saved/Logs/$LR_LOG"; for i in $(seq 1 40); do n1=$(grep -a -c "BuildIndex" "$LOG"); sleep 15; n2=$(grep -a -c "BuildIndex" "$LOG"); [ "$n1" = "$n2" ] && break; done
export WARM=0
J=""; for v in o ins2; do for s in ins_ws ins_ws2 ins_qa; do J="$J $s:$v"; done; done
for v in o sl1 pr1 slpr; do for s in ter_drop_walk ter_step2 ter_drop_jog; do J="$J $s:$v"; done; done
J="$J map_r1:o map_r1:slpr c30_calm:slpr d_sprint:slpr j24_ph0:slpr"
for v in o slf; do for s in j30_rel_3100 j30_rel_3200 j30_rel_3250 j30_rel_3350 j30_rel_3450 s29_swl12 j24_ph0 j24_dbl w30_rev c30_calm; do J="$J $s:$v"; done; done
ab b1 "$J" $D/vars231.sh
echo "B1_DONE $(date +%T)" >> $O
