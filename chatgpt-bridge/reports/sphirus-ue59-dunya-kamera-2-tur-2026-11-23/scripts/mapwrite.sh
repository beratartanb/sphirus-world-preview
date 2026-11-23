#!/bin/bash
# mapwrite.sh <script.py> <label> [extra game assets to back up ...] [--new new packages ...]: reload the map from disk (drops in-memory candidates),
# verified backup of both house maps (+extras), gated write job. The script applies its change and saves (save_all_dirty_levels).
P="<PROJECT_ROOT>"; cd "$P"; export SHME_OWNER=emb
PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
SC="$P/Saved/UE59Work/rt/b2runner/jobs"; S="$1"; L="$2"; shift 2
[ -z "$NORELOAD" ] && SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$P/Tools/Embodied_20261105/reload_map.py" emb_reload 180 2>&1 | grep -E "AFTER" | cut -c1-160
M=r2g2_${L}_$(date +%H%M%S)
MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V233_20261027/manifest233.py $M --assets /Game/GraceRanger/Maps/L_GR_SphirusHouse /Game/GraceRanger/Maps/L_GR_CurrentHouseContent "$@" 2>&1 | tail -1 | cut -c1-300
SHME_KIND=write SHME_MANIFEST="Saved/Codex/SHME_V233_20261027/checkpoint/manifests/$M.json" bash Tools/SHME_V2_20261014/run_v2.sh "$P/$S" r2g2w_$L 600 >/dev/null 2>&1
f=$(ls -t "$SC"/r2g2w_$L-*.out | head -1); cut -c1-300 "$f" | tail -${TAILN:-14}
tail -2 Saved/Codex/SHME_V233_20261027/gate233.log | cut -c1-200; echo "MANIFEST $M"
