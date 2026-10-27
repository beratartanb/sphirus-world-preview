#!/bin/bash
# run233_tel.sh : V2.33 telemetry to a side file. Editor A: component vars (TelemetryLine) + save; editor B (fresh, V2.30 OOM rule): only
# SHM_Telemetry rebuilt (PrintString -> set TelemetryLine) + save; smoke run: no SHM| lines in the log, rows in SHM/<label>.shm.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V233_20261027; export O=$D/chain.out; source $D/lib233.sh; R=Tools/SHME_V2_20261014/run_v2.sh
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; T=Tools/SHME_V233_20261027
M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests/telemetry_comp2.json
step() { echo "== $2 $(date +%T)" >> $O; out=$(env $3 bash $R "$1" "$2" 1500); echo "$out" | head -1 >> $O; echo "$out" | grep -E "GUARD|WRITE_GUARD|REFUSED|Traceback|FAIL|_lasthitby_patched|UP_TO_DATE|ERROR" | head -4 | cut -c1-300 >> $O
  echo "$out" | head -1 | grep -qE "^OK" || { echo "TEL2_FAILED $2 $(date +%T)" >> $O; exit 1; }; }
echo "TEL2 start $(date +%T) (reason: runner manifest-state fix; comp vars were saved by comp_vars at 12:55 under manifest telemetry_comp, original backup kept there)" >> $O
relaunch telB 30
step $V21/revert_noquit.py revert SHME_KIND=control
step $T/only_v233tel.py only SHME_KIND=control
step $V1/build_funcs.py funcs "SHME_KIND=write SHME_MANIFEST=$M"
step $V2/save_comp.py save_comp2 "SHME_KIND=write SHME_MANIFEST=$M"
step $V2/only_all.py only_all SHME_KIND=control
echo "TEL2_BUILT $(date +%T)" >> $O
( cd Tools/SHME_V212_20261017 && bash v212_run.sh v233tel_c30_calm c30_calm '{}' ',"state_mode":"production"' 2>&1 | tail -1 ) >> $O
echo "TEL2_SMOKE log_SHM_lines=$(grep -ac 'SHM|v233tel_c30_calm|' Saved/Logs/$LR_LOG) side_rows=$(wc -l < Saved/Codex/SHME_V1_20260925/SHM/v233tel_c30_calm.shm 2>/dev/null) $(grep -o '"bp_errors": [0-9]*' Saved/Codex/SHME_V1_20260925/v233tel_c30_calm_pie.json)" >> $O
echo "TEL2_DONE $(date +%T)" >> $O
