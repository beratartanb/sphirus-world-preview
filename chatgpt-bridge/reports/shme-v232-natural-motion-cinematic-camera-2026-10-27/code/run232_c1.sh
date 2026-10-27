#!/bin/bash
# run232_c1.sh : V2.32 build C1 (after B12_DONE; reason: a DA field + component vars + SHM_UpdateBodyTargets rebuild need fresh editors:
# vars / profiles in one editor, funcs ALONE in a second - V2.30 OOM rule), then T6 tests in the second editor.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; T=Tools/SHME_V232_20261027; R="bash $V2/run_v2.sh"
D=Saved/Codex/SHME_V232_20261027; export O=$D/chain.out; source $D/lib232.sh
L=$D/c1_$(date +%H%M%S).log
gb() { powershell.exe -NoProfile -Command "\$p = Get-Process UnrealEditor -ErrorAction SilentlyContinue | Select-Object -First 1; if (\$p) { [math]::Round(\$p.PrivateMemorySize64/1GB) } else { 0 }" 2>/dev/null | tr -d '\r'; }
step() { echo "== $2 $(date +%T) mem $(gb) GB" | tee -a "$L"; out=$($R "$1" "$2" "${3:-900}"); echo "$out" | tail -c 2500 | tee -a "$L"; echo "$out" | grep -qE "^ERROR|FAIL |Traceback|TIMEOUT|REFUSED|AssertionError" && { echo "C1_FAILED $2 $(date +%T)" >> $O; kill $WD 2>/dev/null; exit 1; }; tasklist | grep -qi UnrealEditor.exe || { echo "C1_FAILED editor gone at $2 $(date +%T)" >> $O; kill $WD 2>/dev/null; exit 1; }; }
until grep -aq "SOAK_FIN" $O; do sleep 30; done  # (restarted after the dirty-package fix; the IsUnique soak took the editor first)
echo "C1 start $(date +%T) (reason: T6/T7 DA fields + component vars + SHM_UpdateBodyTargets build; C idle-stance copies; content restores)" >> $O
# C (second form): duplicate the pinned straight JogQ starts as SHM232_IS_* (same start databases), then restore the originals (and the
# stopfix-written stop clips: no measurable effect = unverified change) from the checkpoint with the editor CLOSED
grep -aq "^DPW DP232" $O || bash $R $D/req/dp_write.py dpw 900 > $D/dp_write.out 2>&1; grep -aq "^DPW DP232" $O || echo "DPW $(grep -a -o 'DP232 {.\{0,900\}' $D/dp_write.out | head -1)" >> $O
export LR_LOG=$(basename "$(ls -t Saved/Logs/*.log | grep -v -i cef | head -1)"); bash $R Tools/SHME_V21_20261014/revert_quit.py rq_c1 300 | grep -E "dirty after|QUIT|REFUSED" >> $O
for i in $(seq 1 90); do tasklist 2>/dev/null | grep -qi UnrealEditor.exe || break; sleep 2; done
tasklist 2>/dev/null | grep -qi UnrealEditor.exe && { echo "C1_FAILED editor still open before the restore" >> $O; exit 1; }
CK=$D/checkpoint/pre_v232/content/GraceRanger/SHME/Animations
cp -f $CK/Starts/Jog/SHM_JogQ_*.uasset Content/GraceRanger/SHME/Animations/Starts/Jog/ && cp -f $CK/Stops/*.uasset Content/GraceRanger/SHME/Animations/Stops/ && echo "RESTORED JogQ starts $(ls $CK/Starts/Jog/SHM_JogQ_*.uasset | wc -l) + stops $(ls $CK/Stops/*.uasset | wc -l) $(date +%T)" >> $O
relaunch c1a 30
( while true; do g=$(gb); [ -n "$g" ] && [ "$g" -gt 55 ] && { echo "WATCHDOG kill at $g GB $(date +%T)" >> $O; taskkill //F //IM UnrealEditor.exe; break; }; sleep 3; done ) & WD=$!
step $V21/revert_noquit.py revert 300; grep -q "dirty after reload \[\]" "$L" || { echo "C1_FAILED dirty" >> $O; kill $WD; exit 1; }
step $V2/gc_job.py gc0 120
step $V1/build_profiles.py profiles 900
step $V1/build_comp_vars.py comp_vars 900
step $V2/save_comp.py save_comp 300
kill $WD 2>/dev/null
relaunch c1b 30
( while true; do g=$(gb); [ -n "$g" ] && [ "$g" -gt 55 ] && { echo "WATCHDOG kill at $g GB $(date +%T)" >> $O; taskkill //F //IM UnrealEditor.exe; break; }; sleep 3; done ) & WD=$!
step $V21/revert_noquit.py revert 300
step $V2/gc_job.py gc1 120
step $T/only_v232t.py only 60
step $V1/build_funcs.py funcs 1500
step $V2/save_comp.py save_comp2 300
step $V2/only_all.py only_all 60
kill $WD 2>/dev/null
echo "C1_BUILT $(date +%T)" >> $O
export WARM=1 MEMPROBE=1
J="c30_calm:oPBI c30_calm:oBRK c30_calm:oPB wstart:oPBI wstart:oBRK"; for v in o sb; do for s in j30_slow jback d_back j30_rel_3200 j30_rel_3400 jstart k_jogback; do J="$J $s:$v"; done; done; for v in o fg; do for s in c30_calm wstart wdiag cam32_w45 jstart j30_slow stopphase taps; do J="$J $s:$v"; done; done; for v in o t6a t6b t6fg; do for s in ter_drop_walk ter_step2 ter_drop_jog legs_steps_walk legs_steps_jog map_r1 c30_calm d_sprint; do J="$J $s:$v"; done; done
ab c1 "$J" $D/vars232.sh
echo "C1_DONE $(date +%T)" >> $O
