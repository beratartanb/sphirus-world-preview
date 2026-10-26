# lib227.sh: V2.26 chain helpers (copy of lib225 with the V2.26 folder / log names)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V229_20261025; R=Tools/SHME_V2_20261014/run_v2.sh; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
: "${O:=$D/chain.out}"
relaunch() { export LR_LOG=$(basename "$(ls -t Saved/Logs/*.log | grep -v -i cef | head -1)"); if tasklist 2>/dev/null | grep -qi UnrealEditor.exe; then bash $R Tools/SHME_V21_20261014/revert_quit.py "rq_$1" 300 | grep -E "dirty after|QUIT|REFUSED" >> $O; else echo "no editor to quit" >> $O; fi
  for i in $(seq 1 90); do tasklist 2>/dev/null | grep -qi UnrealEditor.exe || break; sleep 2; done
  if [ "$2" = real ]; then unset V219_EDARGS; else export V219_EDARGS="-UseFixedTimeStep -FPS=$2"; fi
  bash Tools/SHME_V2_20261014/v2_editor_launch.sh "shmv229_$1" 2>&1 | tail -2 >> $O; export LR_LOG="shmv229_$1.log"; echo "RELAUNCH $1 $2 $(date +%T)" >> $O; }
ab() { export LR_LOG=$(basename "$(ls -t Saved/Logs/*.log | grep -v -i cef | head -1)"); TAG=$1 JOBS="$2" EXTRA_VARS="$(cat ${3:-$D/vars229.sh})" bash Tools/SHME_V229_20261025/ab_safe229.sh 2>&1 | grep -a " | rows\|REFUSED\|MEM\|GONE\|INVALID" >> $O; }
# V2.29: a relaunch whose runner never becomes ready (ZenServer wait) is killed (editor + zenserver) and retried; never run a batch on it
relaunch0() { relaunch "$@"; }
eval "$(declare -f relaunch | sed '1s/relaunch/relaunch_base/')"
relaunch() { for a in 1 2 3; do relaunch_base "$1" "$2"; tail -4 $O | grep -q "RUNNER_NOT_READY" || return 0
  echo "RELAUNCH_RETRY $a $(date +%T)" >> $O; powershell.exe -NoProfile -Command "Stop-Process -Name UnrealEditor -Force -ErrorAction SilentlyContinue; Start-Sleep 3; Stop-Process -Name zenserver -Force -ErrorAction SilentlyContinue" >/dev/null 2>&1; sleep 5; done
  echo "RELAUNCH_FAILED $1 $(date +%T)" >> $O; exit 1; }
