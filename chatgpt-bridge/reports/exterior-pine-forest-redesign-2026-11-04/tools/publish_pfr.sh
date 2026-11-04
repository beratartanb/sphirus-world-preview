#!/bin/bash
# publish_pfr.sh "<commit subject>" : copy Saved/Codex/PineForestRedesign_20261104/pub into the sparse clone of the PUBLIC bridge repo
# (beratartanb/sphirus-world-preview) under chatgpt-bridge/reports/exterior-pine-forest-redesign-2026-11-04 and commit + push (pattern of publish_xr5.sh).
set -e; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
SUBJ="${1:-Exterior PFR: first gameplay area redesigned on the Pine Forest Pack reference (saved map, before/after, reference pairs, walks, perf, report)}"
SRC=Saved/Codex/PineForestRedesign_20261104/pub
G="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/ghpub241"
R=chatgpt-bridge/reports/exterior-pine-forest-redesign-2026-11-04
mkdir -p "$SRC/tools"; cp Tools/PineForestRedesign_20261104/*.py Tools/PineForestRedesign_20261104/*.sh Tools/PineForestRedesign_20261104/*.ps1 "$SRC/tools/"
cd "$G"; git -c core.longpaths=true pull --ff-only -q || true
git -c core.longpaths=true sparse-checkout add "$R" 2>/dev/null || true
mkdir -p "$R"; cp -r "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/$SRC/." "$R/"
git -c core.longpaths=true add --sparse "$R"
git -c core.longpaths=true -c user.name=beratartanb -c user.email=beratartanb@gmail.com commit -q -F - <<MSG
$SUBJ

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
MSG
git -c core.longpaths=true push -q origin HEAD
git -c core.longpaths=true log --oneline -1
echo "PUBLISHED https://github.com/beratartanb/sphirus-world-preview/tree/main/$R"
