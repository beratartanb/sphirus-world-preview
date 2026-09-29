#!/bin/bash
# usage: run_of.sh <script.py> <seq_name> [timeout_s]  -- queue into the scratchpad B2 runner (editor launched with -ExecCmds) and wait
J="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/53df87b2-1800-4b0d-8cb5-35bc735c40a0/scratchpad/b2runner/jobs"
src="$1"; name="$2"; to="${3:-300}"
cp "$src" "$J/$name.py.tmp" && mv "$J/$name.py.tmp" "$J/$name.py"
for i in $(seq 1 $to); do
  if [ -f "$J/$name.out" ]; then cat "$J/$name.out"; exit 0; fi
  sleep 1
done
echo "TIMEOUT waiting for $name"; exit 1
