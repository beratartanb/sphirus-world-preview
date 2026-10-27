#!/bin/bash
# run232_b1.sh : V2.32 build B1 (after S1_DONE). Editor A (b1a): DA fields CamOrbit* (build_profiles) + component vars CamOrbit* (build_comp_vars)
# -> save; BP_GR_Player GR_SHM_CamOrbit wiring (install_v232_camorbit, boom yaw only) -> save. Editor B (b1b, fresh: funcs alone rule):
# SHM_UpdateCameraV21 rebuilt ALONE -> save. Every relaunch reason logged.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; T=Tools/SHME_V232_20261027; R="bash $V2/run_v2.sh"
D=Saved/Codex/SHME_V232_20261027; export O=$D/chain.out; source $D/lib232.sh
L=$D/b1_$(date +%H%M%S).log
gb() { powershell.exe -NoProfile -Command "\$p = Get-Process UnrealEditor -ErrorAction SilentlyContinue | Select-Object -First 1; if (\$p) { [math]::Round(\$p.PrivateMemorySize64/1GB) } else { 0 }" 2>/dev/null | tr -d '\r'; }
step() { echo "== $2 $(date +%T) mem $(gb) GB" | tee -a "$L"; out=$($R "$1" "$2" "${3:-900}"); echo "$out" | tail -c 2500 | tee -a "$L"; echo "$out" | grep -a "ORBIT232 {" | cut -c1-900 >> $O; echo "$out" | grep -qE "^ERROR|FAIL |Traceback|TIMEOUT|REFUSED|AssertionError" && { echo "B1_FAILED $2 $(date +%T)" >> $O; kill $WD 2>/dev/null; exit 1; }; tasklist | grep -qi UnrealEditor.exe || { echo "B1_FAILED editor gone at $2 $(date +%T)" >> $O; kill $WD 2>/dev/null; exit 1; }; }
until grep -aq "S1_DONE" $O; do sleep 30; done
echo "B1 start $(date +%T) (reason: profile/var build needs a fresh editor; funcs build alone in a second fresh editor - V2.30 OOM rule)" >> $O
relaunch b1a 30
( while true; do g=$(gb); [ -n "$g" ] && [ "$g" -gt 55 ] && { echo "WATCHDOG kill at $g GB $(date +%T)" >> $O; taskkill //F //IM UnrealEditor.exe; break; }; sleep 3; done ) & WD=$!
step $V21/revert_noquit.py revert 300; grep -q "dirty after reload \[\]" "$L" || { echo "B1_FAILED dirty" >> $O; kill $WD; exit 1; }
step $V2/gc_job.py gc0 120
step $V1/build_profiles.py profiles 900
step $V1/build_comp_vars.py comp_vars 900
step $V2/save_comp.py save_comp 300
step $D/req/orbit_save.py orbit 900
kill $WD 2>/dev/null
relaunch b1b 30
( while true; do g=$(gb); [ -n "$g" ] && [ "$g" -gt 55 ] && { echo "WATCHDOG kill at $g GB $(date +%T)" >> $O; taskkill //F //IM UnrealEditor.exe; break; }; sleep 3; done ) & WD=$!
step $V21/revert_noquit.py revert 300
step $V2/gc_job.py gc1 120
step $T/only_v232c.py only 60
step $V1/build_funcs.py funcs 1500
step $V2/save_comp.py save_comp2 300
step $V2/only_all.py only_all 60
kill $WD 2>/dev/null
echo "B1_BUILT $(date +%T)" >> $O
export WARM=1 MEMPROBE=1
J=""; for v in o c1s c1 c1l; do for s in cam32_w45 cam32_j90 cam32_s90 cam32_s90l cam32_s180 cam32_brk2 cam32_wallturn cam32_look cam32_idlelook cam32_analog cam32_chain cam_corr; do J="$J $s:$v"; done; done
for v in o c1; do for s in s29_wall c29_combo ins_ws map_r1 legs_slope_sprint ter_drop_walk s29_cam; do J="$J $s:$v"; done; done
ab b1 "$J" $D/vars232.sh
echo "B1_DONE $(date +%T)" >> $O
