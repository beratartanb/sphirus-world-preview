#!/bin/bash
# gd14_eval.sh <face tag (SKM_GD14_Face_<tag> with existing GD14 bindings)> <capture label> <sets> [light=front] : re-compose the qa scene for that
# face (NOBIND) and capture - so every candidate is captured on ITS OWN face (a cycle leaves the composition on the last rigged face)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; W=Saved/Codex/GD14_Identity_20261009
NOBIND=1 bash $W/tools/gd14_bind_comp.sh $1 | grep -E "GD14_COMP|READY" | cut -c1-120; LIGHT=${4:-front} bash $W/tools/gd14_caps.sh $2 $3 | grep -E "DONE|ERROR"
