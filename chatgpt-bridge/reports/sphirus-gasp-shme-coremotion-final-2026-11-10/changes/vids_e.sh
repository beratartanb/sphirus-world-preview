#!/bin/bash
# vids_e.sh <suffix>: effort A/B with the PRODUCTION player on the flat test stage (EffortEnabled switched without
# edit notification, vid.py VID_MOTION). Same input both runs.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; P="$PWD"; S=$1
EF="[('',0.8,0),('W LeftShift',1.6,0),('S LeftShift',1.4,0),('W LeftShift',1.0,0),('S LeftShift',1.0,0),('W LeftShift',1.0,0),('',2.0,0),('S LeftShift',1.4,0),('',5.0,0),('W LeftShift',1.4,0),('S LeftShift',1.4,0),('',2.0,0)]"
R(){ for i in 1 2 3; do X=$(bash Tools/Embodied_20261105/relaunch.sh emb_e$S$1$i 2>&1 | tail -1); [[ "$X" == RUNNER_READY* ]] && break; done; echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt; SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$P/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED; }
V(){ bash Tools/Day_20261107/v55.sh "$@" 2>&1 | grep -E "VIDREC|FRAMES|mp4"; }
R a; V EP_on_$S -6000 2000 92 0 "$EF" "import builtins; builtins.VID_MOTION={}; builtins.VID_SIDE=None"
R b; V EP_off_$S -6000 2000 92 0 "$EF" "import builtins; builtins.VID_MOTION={'EffortEnabled':False}; builtins.VID_SIDE=None"
for i in 1 2 3; do X=$(bash Tools/Embodied_20261105/relaunch.sh emb_e${S}z$i 2>&1 | tail -1); [[ "$X" == RUNNER_READY* ]] && break; done; echo "$X"
