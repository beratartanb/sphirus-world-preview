#!/bin/bash
# run228_build.sh : V2.28 SHME component build in TWO fresh editors (funcs-build balloon trap): A) comp vars + profile fields + save;
# B) SHM_UpdateBodyTargets + SHM_UpdateCameraV21 rebuild + compile + save; then a clean verify (dirty after reload []). Run only when no qa chain runs.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; V28=Tools/SHME_V228_20261025; R="bash $V2/run_v2.sh"
D=Saved/Codex/SHME_V228_20261025; export O=$D/chain.out; source $D/lib228.sh
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; L=$D/build_$(date +%H%M%S).log
step() { echo "== $2 $(date +%T)" | tee -a "$L"; out=$($R "$1" "$2" "${3:-900}"); echo "$out" | tail -c 2500 | tee -a "$L"; echo "$out" | grep -qE "^ERROR|FAIL |Traceback|TIMEOUT|REFUSED" && { echo "STOP at $2" | tee -a "$L"; echo "BUILD228b_FAILED $2 $(date +%T)" >> $O; exit 1; }; }
echo "BUILD228b start $(date +%T)" >> $O
"$PY" -I $V2/v2_check.py 2>&1 | tail -4 | tee -a "$L"; grep -q '"problems": \[\]' "$L" || { echo "STOP: DSL check" | tee -a "$L"; echo "BUILD228b_FAILED check" >> $O; exit 1; }
relaunch cB 30
step $V21/revert_noquit.py revertB 300; grep -q "dirty after reload \[\]" "$L" || { echo "STOP: dirty packages remain (B)" | tee -a "$L"; echo "BUILD228b_FAILED dirtyB" >> $O; exit 1; }
step $V2/gc_job.py gcB0 120
step $V28/only_v228b.py only_v228b 60
step $V1/build_funcs.py funcs 1500
step $V2/gc_job.py gcB1 120
step $V2/save_comp.py save_compB 300
step $V2/only_all.py only_all 60
grep -q "saved" "$L" || { echo "BUILD228b_FAILED save" >> $O; exit 1; }
echo "BUILD228b_DONE $(date +%T)" >> $O
