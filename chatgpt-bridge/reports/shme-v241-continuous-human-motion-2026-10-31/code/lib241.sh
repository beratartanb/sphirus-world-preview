# lib236.sh: V2.38 chain helpers (lib236 with the V2.37 folder, owner v238)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V241_20261031; R=Tools/SHME_V2_20261014/run_v2.sh; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
# V2.31: a relaunch from any chain shell keeps the editor mode (fixed 30 by default); A1 lost the fixed step after a crash relaunch
export V219_EDARGS="${V219_EDARGS--UseFixedTimeStep -FPS=30}"
: "${O:=$D/chain.out}"
relaunch() { export LR_LOG=$(basename "$(ls -t Saved/Logs/*.log | grep -v -i cef | head -1)"); if tasklist 2>/dev/null | grep -qi UnrealEditor.exe; then bash $R Tools/SHME_V21_20261014/revert_quit.py "rq_$1" 300 | grep -E "dirty after|QUIT|REFUSED" >> $O; else echo "no editor to quit" >> $O; fi
  for i in $(seq 1 90); do tasklist 2>/dev/null | grep -qi UnrealEditor.exe || break; sleep 2; done
  if tasklist 2>/dev/null | grep -qi UnrealEditor.exe; then echo "RELAUNCH_FAILED $1: the old editor did not quit (refused / dirty) - no second editor (V2.33 gate) $(date +%T)" >> $O; exit 1; fi
  if [ "$2" = real ]; then unset V219_EDARGS; else export V219_EDARGS="-UseFixedTimeStep -FPS=$2"; fi
  bash Tools/SHME_V230_20261026/editor_launch230.sh "shmv241_$1" 2>&1 | tail -2 >> $O; export LR_LOG="shmv241_$1.log"; echo "RELAUNCH $1 $2 $(date +%T)" >> $O; }
ab() { export LR_LOG=$(basename "$(ls -t Saved/Logs/*.log | grep -v -i cef | head -1)"); TAG=$1 JOBS="$2" EXTRA_VARS="$(cat ${3:-$D/vars241.sh})" bash Tools/SHME_V241_20261031/ab_safe241.sh 2>&1 | grep -a " | rows\|REFUSED\|MEM\|GONE\|INVALID" >> $O; }
# V2.29: a relaunch whose runner never becomes ready (ZenServer wait) is killed (editor + zenserver) and retried; never run a batch on it
relaunch0() { relaunch "$@"; }
eval "$(declare -f relaunch | sed '1s/relaunch/relaunch_base/')"
relaunch() { for a in 1 2; do relaunch_base "$1" "$2"; tail -4 $O | grep -q "RUNNER_NOT_READY" || return 0
  # V2.30: record WHY the runner was not ready before any kill (last editor log lines, zen process state)
  echo "RUNNER_NOT_READY_CAUSE $(tail -c 4000 "Saved/Logs/$LR_LOG" 2>/dev/null | grep -a -o -E 'Waiting for ZenServer.{0,60}|Fatal error.{0,80}|Assertion failed.{0,80}' | tail -2 | tr -d '\r' | tr '\n' '|') zen=$(tasklist | grep -ci zenserver)" >> $O
  echo "RELAUNCH_RETRY $a $(date +%T)" >> $O; powershell.exe -NoProfile -Command "Stop-Process -Name UnrealEditor -Force -ErrorAction SilentlyContinue; Start-Sleep 3; Stop-Process -Name zenserver -Force -ErrorAction SilentlyContinue" >/dev/null 2>&1; sleep 5; done
  echo "RELAUNCH_FAILED $1 $(date +%T)" >> $O; exit 1; }
export SHME_OWNER=v241
