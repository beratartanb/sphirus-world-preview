#!/bin/bash
# publish243.sh "<commit subject>" : copy pub/ into the sparse clone of the bridge repo (sparse-checkout add) and commit + push (author beratartanb).
set -e; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
SUBJ="${1:-SHME V2.43: idle owner fixed (stance hold off + weighted MM idle), standing-turn needs-look rule, lateral family closing step; promotion per regression}"
SRC=Saved/Codex/SHME_V243_20261101/pub
G="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/ghpub241"
R=chatgpt-bridge/reports/shme-v243-walk-idle-chain-2026-11-01
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
