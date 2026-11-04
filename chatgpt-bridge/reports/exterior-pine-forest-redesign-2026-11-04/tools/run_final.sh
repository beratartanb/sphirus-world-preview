#!/bin/bash
# run_final.sh <tag> : FINAL verification set in a freshly opened editor on the SAVED map (same poses / routes / settings as BEFORE):
#   top views -> 39 stations (lit) -> walks A and B (MediaCapture frames + csvprofile) -> engine memory report. Nothing is written to the map.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
TAG=${1:-final}
MY="/c/Users/berat/AppData/Local/Temp/claude/bbc6f8fdff1f8341/58bc34ab-b0fd-4574-9259-4850d781d32b/scratchpad"; D=Saved/Codex/PineForestRedesign_20261104; T=Tools/PineForestRedesign_20261104
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
echo "FINAL $TAG start $(date +%T)"
printf "import builtins\nbuiltins.PFR_TOP_TAG = '%s'\nexec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/PineForestRedesign_20261104/topview_pfr.py', encoding='utf-8').read(), 'topview_pfr.py', 'exec'), {'__name__': '__job__'})\n" "$TAG" > "$MY/top_$TAG.py"
rm -f "$D/cap/top_$TAG/done.json"; bash $T/pfr_chain.sh "job:measure:$MY/top_$TAG.py:120" | tail -1; for i in $(seq 1 60); do [ -f "$D/cap/top_$TAG/done.json" ] && break; sleep 3; done; echo "topview $TAG: $(ls $D/cap/top_$TAG | grep -c png) png"
bash $T/pfr_chain.sh "views:$TAG:lit:$D/data/stations_core.json" "walk:${TAG}A:A:lit:1" "walk:${TAG}B:B:lit:1" | tail -6
printf "import builtins\nbuiltins.PFR_VRAM_TAG = '%s'\nexec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/PineForestRedesign_20261104/probe_vram.py', encoding='utf-8').read(), 'probe_vram.py', 'exec'), {'__name__': '__job__'})\n" "$TAG" > "$MY/vram_$TAG.py"
rm -f "$D/perf/vram_probe_$TAG.json"; bash $T/pfr_chain.sh "job:control:$MY/vram_$TAG.py:120" | tail -1; for i in $(seq 1 30); do [ -f "$D/perf/vram_probe_$TAG.json" ] && break; sleep 3; done; cat "$D/perf/vram_probe_$TAG.json" 2>/dev/null | head -c 400; echo
ls -t Saved/Profiling/CSV/*.csv | head -2
echo "FINAL $TAG done $(date +%T)"
