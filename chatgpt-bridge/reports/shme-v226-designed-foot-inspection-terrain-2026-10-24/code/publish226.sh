#!/bin/bash
# publish226.sh : copy pub/ into the sparse clone of the bridge repo and commit + push (author beratartanb).
set -e; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
SRC=Saved/Codex/SHME_V226_20261024/pub
G="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/ghpub225"
R=chatgpt-bridge/reports/shme-v226-designed-foot-inspection-terrain-2026-10-24
cd "$G"; git -c core.longpaths=true pull --ff-only -q || true
mkdir -p "$R"; cp -r "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/$SRC/." "$R/"
git -c core.longpaths=true add "$R"
git -c core.longpaths=true -c user.name=beratartanb -c user.email=beratartanb@gmail.com commit -q -F - <<'MSG'
SHME V2.26: designed-foot chain diagnosis (FootPlacement owner, world frame), inspection on real R05 masks (tag + probe contract), terrain lift half-convergence fix

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
MSG
git -c core.longpaths=true push -q origin HEAD
git -c core.longpaths=true log --oneline -1
