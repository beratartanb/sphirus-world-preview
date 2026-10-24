# lib226.sh: V2.26 chain helpers (copy of lib225 with the V2.26 folder / log names)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V226_20261024; R=Tools/SHME_V2_20261014/run_v2.sh; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
: "${O:=$D/chain.out}"
relaunch() { export LR_LOG=$(basename "$(ls -t Saved/Logs/*.log | grep -v -i cef | head -1)"); if tasklist 2>/dev/null | grep -qi UnrealEditor.exe; then bash $R Tools/SHME_V21_20261014/revert_quit.py "rq_$1" 300 | grep -E "dirty after|QUIT|REFUSED" >> $O; else echo "no editor to quit" >> $O; fi
  for i in $(seq 1 90); do tasklist 2>/dev/null | grep -qi UnrealEditor.exe || break; sleep 2; done
  if [ "$2" = real ]; then unset V219_EDARGS; else export V219_EDARGS="-UseFixedTimeStep -FPS=$2"; fi
  bash Tools/SHME_V2_20261014/v2_editor_launch.sh "shmv226_$1" 2>&1 | tail -2 >> $O; export LR_LOG="shmv226_$1.log"; echo "RELAUNCH $1 $2 $(date +%T)" >> $O; }
ab() { export LR_LOG=$(basename "$(ls -t Saved/Logs/*.log | grep -v -i cef | head -1)"); TAG=$1 JOBS="$2" EXTRA_VARS="$(cat ${3:-$D/vars226.sh})" bash Tools/SHME_V226_20261024/ab_safe226.sh 2>&1 | grep -a " | rows\|REFUSED\|MEM\|GONE\|INVALID" >> $O; }
