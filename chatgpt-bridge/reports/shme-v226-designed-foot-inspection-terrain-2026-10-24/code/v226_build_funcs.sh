#!/bin/bash
# v226_build_funcs.sh: funcs-only (BodyTargets + CameraV21) in a FRESH editor; vars + profiles were built and saved in the previous editor (balloon trap)
# v225_build4: SHM_UpdateCameraV21 only (I2 dwell cap); funcs-only in a fresh editor
# v225_build3: funcs-only rebuild (vars + profile fields already saved 20:38/20:39); the three earlier attempts ran comp_vars + profiles in the same editor right before funcs and ballooned
# v26_build.sh : V2.25 SHME build (terrain stepping chain + inspection camera) (settle / terrain body / living camera). revert harness state -> SHME patch (offline
# check) -> comp vars -> profiles -> SHM_UpdateBodyTargets + SHM_UpdateCameraV21 rebuild -> save -> verify. Run only when no qa chain runs.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; V26=Tools/SHME_V226_20261024; R="bash $V2/run_v2.sh"
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; L=Saved/Codex/SHME_V226_20261024/build_$(date +%H%M%S).log
step() { echo "== $2 $(date +%T)" | tee -a "$L"; out=$($R "$1" "$2" "${3:-900}"); echo "$out" | tail -c 2500 | tee -a "$L"; echo "$out" | grep -qE "^ERROR|FAIL |Traceback|TIMEOUT|REFUSED|\"ALL_OK\": false" && { echo "STOP at $2" | tee -a "$L"; exit 1; }; tasklist 2>/dev/null | grep -qi UnrealEditor.exe || { echo "STOP: editor gone after $2" | tee -a "$L"; exit 1; }; }
step $V21/revert_noquit.py revert 300; grep -q "dirty after reload \[\]" "$L" || { echo "STOP: dirty packages remain" | tee -a "$L"; exit 1; }
"$PY" $V2/v2_check.py 2>&1 | tail -4 | tee -a "$L"; grep -q '"problems": \[\]' "$L" || { echo "STOP: DSL check" | tee -a "$L"; exit 1; }
step $V2/gc_job.py gc0 120
step $V26/only_v226.py only_v226 60
step $V1/build_funcs.py funcs 1500
step $V2/gc_job.py gc1 120
step $V2/save_comp.py save_comp 300
step $V2/only_all.py only_all 60
step $V2/gc_job.py gc2 120
echo "BUILD_V226_DONE $(date +%T)" | tee -a "$L"
