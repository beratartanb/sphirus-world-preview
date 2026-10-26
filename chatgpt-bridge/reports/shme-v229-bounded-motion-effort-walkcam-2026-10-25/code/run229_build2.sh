#!/bin/bash
# run229_build.sh : V2.29 build (run only when no qa chain runs). A) fresh editor: RevTurn wrapped-twist re-bake (content, saved) + SHME comp
# vars + profile fields (effort, walk framing) + save; B) fresh editor: SHM_UpdateState + SHM_UpdateCameraV21 rebuild + save;
# C) fresh editor: BP_GR_Player effort consumer + ABP resume window (graph patches, saved). Every new knob is installed OFF.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; T=Tools/SHME_V229_20261025; R="bash $V2/run_v2.sh"
D=Saved/Codex/SHME_V229_20261025; export O=$D/chain.out; source $D/lib229.sh
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; L=$D/build_$(date +%H%M%S).log
step() { echo "== $2 $(date +%T)" | tee -a "$L"; out=$($R "$1" "$2" "${3:-900}"); echo "$out" | tail -c 3000 | tee -a "$L"; echo "$out" | grep -qE "^ERROR|FAIL |Traceback|TIMEOUT|REFUSED|AssertionError" && { echo "STOP at $2" | tee -a "$L"; echo "BUILD229B_FAILED $2 $(date +%T)" >> $O; exit 1; }; }
echo "BUILD229B start $(date +%T)" >> $O
# (sources already patched)
"$PY" -I $V2/v2_check.py 2>&1 | tail -4 | tee -a "$L"; grep -q '"problems": \[\]' "$L" || { echo "STOP: DSL check" | tee -a "$L"; echo "BUILD229B_FAILED check" >> $O; exit 1; }
relaunch bA 30
step $V21/revert_noquit.py revert 300; grep -q "dirty after reload \[\]" "$L" || { echo "BUILD229B_FAILED dirty" >> $O; exit 1; }
step $V2/gc_job.py gc0 120
step $V1/build_comp_vars.py comp_vars 600
step $V1/build_profiles.py profiles 600
step $V2/save_comp.py save_comp 300
echo "BUILD229B A done $(date +%T)" >> $O
relaunch bB 30
step $V21/revert_noquit.py revertB 300; grep -q "dirty after reload \[\]" "$L" || { echo "BUILD229B_FAILED dirtyB" >> $O; exit 1; }
step $V2/gc_job.py gcB0 120
step $T/only_v229.py only_v229 60
step $V1/build_funcs.py funcs 1500
step $V2/gc_job.py gcB1 120
step $V2/save_comp.py save_compB 300
step $V2/only_all.py only_all 60
echo "BUILD229B B done $(date +%T)" >> $O
echo "BUILD229B_DONE $(date +%T)" >> $O
