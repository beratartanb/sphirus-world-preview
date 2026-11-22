#!/bin/bash
# job6.sh <script> <name> <timeout> [--assets ...] [--new ...] : per-job verified manifest + gated write job (round 6)
P="/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; cd "$P"
PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
S=$1; N=$2; TO=$3; shift 3; M="ue59_m27_$N_$(date +%H%M%S)"; M="ue59_m27_${N}_$(date +%H%M%S)"
MSYS_NO_PATHCONV=1 MSYS2_ARG_CONV_EXCL="*" "$PY" Tools/SHME_V233_20261027/manifest233.py $M "$@" 2>&1 | tail -1 | cut -c1-200
echo $M >> Saved/UE59Work/r7/manifests.txt
SHME_OWNER=emb SHME_KIND=write SHME_MANIFEST="Saved/Codex/SHME_V233_20261027/checkpoint/manifests/$M.json" bash Tools/SHME_V2_20261014/run_v2.sh "$P/$S" emb_$N $TO 2>&1 | tail -8 | cut -c1-1300
tail -1 Saved/Codex/SHME_V233_20261027/gate233.log | cut -c1-260
