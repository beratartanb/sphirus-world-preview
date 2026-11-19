#!/bin/bash
# perf19.sh <suffix> "<label>=<console commands separated by ;>" ... : matched real-time GPU cost on the uphill trail (perf_cam.sh route,
# editor PIE, SphCamera on). Every run enables per-pass GPU stats in the CSV (r.GPUCsvStatsEnabled 1) and logs GPU clocks / power /
# temperature (nvidia-smi, 1 Hz) for the run. Candidates are console variables applied in PIE only (runtime, nothing saved).
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; S=$1; shift
O=Saved/Codex/Camera_20261112/perf; mkdir -p $O
for spec in "$@"; do
  lab=${spec%%=*}; cmds=${spec#*=}; py="cmd('r.GPUCsvStatsEnabled 1')"
  IFS=';' read -ra CC <<< "$cmds"; for c in "${CC[@]}"; do [ -n "$c" ] && py="$py; cmd('$c')"; done
  nvidia-smi --query-gpu=timestamp,clocks.gr,clocks.mem,power.draw,power.limit,temperature.gpu,utilization.gpu,clocks_throttle_reasons.active --format=csv,noheader -l 1 > $O/P19_${S}_$lab.smi.txt 2>/dev/null &
  SMI=$!
  bash Tools/Camera_20261112/perf_cam.sh P19_${S}_$lab True "$py" 2>&1 | tail -1
  kill $SMI 2>/dev/null
done
echo PERF19_DONE
