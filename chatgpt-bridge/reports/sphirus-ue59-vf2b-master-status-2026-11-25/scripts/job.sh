#!/bin/bash
# vf2b_job.sh (no folder guard; manifest gate applies) <script.py> <name> <timeout> <kind:write|measure> [--assets ...] [--new ...]
# Gated runner submit for the AI asset pipeline (owner "aip"). write jobs get a fresh verified manifest first.
# Sandbox only: every --new / --assets path must be under /Game/Sandbox/AIPipeline_TEST/.
P="<PROJECT>"; cd "$P"
PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
S=$1; N=$2; TO=$3; K=$4; shift 4

if [ "$K" = "write" ]; then
  M="vf2_$N$(date +%H%M%S)"
  MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V233_20261027/manifest233.py $M "$@" 2>&1 | tail -1 | cut -c1-160
  SHME_OWNER=aip SHME_KIND=write SHME_MANIFEST="Saved/Codex/SHME_V233_20261027/checkpoint/manifests/$M.json" bash Tools/SHME_V2_20261014/run_v2.sh "$P/$S" vf2_$N $TO 2>&1 | tail -12 | cut -c1-600
else
  SHME_OWNER=aip SHME_KIND=measure bash Tools/SHME_V2_20261014/run_v2.sh "$P/$S" vf2_$N $TO 2>&1 | tail -12 | cut -c1-600
fi
tail -1 Saved/Codex/SHME_V233_20261027/gate233.log | cut -c1-300
