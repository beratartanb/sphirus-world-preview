#!/bin/bash
# editor_launch230.sh <log_name> : v2_editor_launch.sh + V2.30 ZenServer guards. (1) before launch wait up to 20 s for a zenserver left by the
# previous editor to exit (the new editor otherwise found no data-dir owner, started a second instance and hung at "Waiting for ZenServer
# to be ready" for the full 15 min wait, 2026-10-26 finv). (2) while waiting: if the log ends on that line and has not grown for 90 s,
# stop waiting (RUNNER_NOT_READY ZEN_STALL) so the caller's limited retry runs at once.
# V2.19: optional extra editor arguments from env V219_EDARGS (e.g. -UseFixedTimeStep -FPS=60 for the frame-rate study); unset = unchanged.
# Refuses when an UnrealEditor process already exists (another session may own it). Quarantines this runner's stale
# jobs, sets aside (never deletes) crash-restore data, waits for SPH_V2_RUNNER_READY, then switches editor throttling off.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
SC="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad"
if tasklist 2>/dev/null | grep -qi "UnrealEditor.exe"; then echo "REFUSED: an UnrealEditor process is already running (another session may own it)"; exit 2; fi
mkdir -p "$SC/b2runner/stale" "$SC/b2runner/jobs"
for f in "$SC"/b2runner/jobs/*.py "$SC"/b2runner/jobs/*.done "$SC"/b2runner/jobs/*.out; do [ -f "$f" ] && mv -f "$f" "$SC/b2runner/stale/"; done
[ -f Saved/Autosaves/PackageRestoreData.json ] && mv Saved/Autosaves/PackageRestoreData.json "Saved/Autosaves/PackageRestoreData_$(date +%H%M%S).json.aside"
for z in $(seq 1 10); do tasklist 2>/dev/null | grep -qi zenserver.exe || break; sleep 2; done
W="$(cygpath -w "$SC")"; L="${1:-shmv2_$(date +%H%M%S)}"
powershell.exe -NoProfile -Command "Start-Process -FilePath 'C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe' -ArgumentList '\"$(cygpath -w "$(pwd)/sphirus.uproject")\" -ExecCmds=\"py $W\b2runner\runner.py\" -nosound -log=$L.log $V219_EDARGS'"
zs=-1; zn=0
for i in $(seq 1 450); do grep -q "SPH_V2_RUNNER_READY" "Saved/Logs/$L.log" 2>/dev/null && break; sleep 2
  s=$(stat -c %s "Saved/Logs/$L.log" 2>/dev/null || echo 0); if [ "$s" = "$zs" ] && tail -c 300 "Saved/Logs/$L.log" 2>/dev/null | grep -q "Waiting for ZenServer to be ready"; then zn=$((zn+1)); else zn=0; fi; zs=$s
  [ $zn -ge 45 ] && { echo "ZEN_STALL $L.log after $((i*2)) s"; break; }; done
grep -q "SPH_V2_RUNNER_READY" "Saved/Logs/$L.log" && echo "RUNNER_READY $L.log" || { echo "RUNNER_NOT_READY $L.log"; exit 1; }
bash Tools/SHME_V2_20261014/run_v2.sh "$SC/throttle.py" throttle 300 | tail -1
