#!/bin/bash
# publish227.sh "<commit subject>" : copy pub/ into the sparse clone of the bridge repo (sparse-checkout add) and commit + push (author beratartanb).
set -e; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
SUBJ="${1:-SHME V2.28: speed, support and animation continuity}"
SRC=Saved/Codex/SHME_V228_20261025/pub
G="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/ghpub225"
R=chatgpt-bridge/reports/shme-v228-speed-support-continuity-2026-10-25
cd "$G"; git -c core.longpaths=true pull --ff-only -q || true
git -c core.longpaths=true sparse-checkout add "$R" 2>/dev/null || true
mkdir -p "$R"; cp -r "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/$SRC/." "$R/"
rm -f "$R/CHANGES_V228.md.tpl"
git -c core.longpaths=true add --sparse "$R"
git -c core.longpaths=true -c user.name=beratartanb -c user.email=beratartanb@gmail.com commit -q -F - <<MSG
$SUBJ

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
MSG
git -c core.longpaths=true push -q origin HEAD
git -c core.longpaths=true log --oneline -1
