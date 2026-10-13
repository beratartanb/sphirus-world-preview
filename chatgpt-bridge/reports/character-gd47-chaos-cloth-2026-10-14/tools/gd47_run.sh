#!/bin/bash
# gd47_run.sh <job.py> <name> [timeout] [prefix-lines...] : run a GD47 job through the B2 runner (builtins prefix from GD47_PRE env), print marker lines
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; N=Saved/Codex/GD47_ChaosCloth_20261014; R=Tools/OutfitHome_20260929/run_of.sh
JOB=$1; NAME=$2; TO=${3:-900}; T=$N/jobs/_run_$NAME.py
{ echo "import builtins"; echo "${GD47_PRE:-}"; cat "$JOB"; } > "$T"
MSYS_NO_PATHCONV=1 bash $R "$(cygpath -w "$(pwd)/$T")" gd47-$NAME $TO | grep -oE 'GD47_[A-Z_]+.{0,1500}|Traceback.*|[A-Za-z]*Error.*|TIMEOUT.*' | head -6
