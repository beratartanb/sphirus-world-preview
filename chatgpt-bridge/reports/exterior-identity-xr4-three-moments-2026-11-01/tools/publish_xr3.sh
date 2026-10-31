#!/bin/bash
# publish_xr2.sh "<commit subject>" : copy pub/ into the sparse clone of the bridge repo (sparse-checkout add) and commit + push (author beratartanb).
set -e; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
SUBJ="${1:-Exterior XR4: three atmospheric moments on the route A slice (bedrock ledge, glade terrace, light A), before/after, clay, walks, restored}"
SRC=Saved/Codex/ExteriorIdentity_XR3_20261031/pub
G="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/ghpub241"
R=chatgpt-bridge/reports/exterior-identity-xr4-three-moments-2026-11-01
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
