#!/bin/bash
# vids_side.sh <suffix> <pawn class or ''> [extra prelude]: full-body review videos with the side / 3-4 tracking camera
# (vid.py VID_SIDE): profile (90 deg) and front 3-4 (140 deg). Same input as the player-camera protocol PS below.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; S=$1; CLS=$2; EX=$3
SW="exec(open(u.Paths.project_dir()+'Tools/GASP_20261109/swap.py',encoding='utf8').read()); swap('$CLS'); "; [ -z "$CLS" ] && SW=""
PS="[('',1.0,0),('W',4.0,0),('',2.0,0),('W LeftShift',3.0,0),('',2.5,0),('W',1.5,0),('S',2.0,0),('',2.0,0)]"
R(){ bash Tools/Embodied_20261105/relaunch.sh emb_s$S$1 2>&1 | tail -1; [ -n "$CLS" ] && bash Tools/Day_20261107/ed.sh Tools/GASP_20261109/warm.py measure 600 | grep -c WARM; }
V(){ bash Tools/Day_20261107/v55.sh "$@" 2>&1 | grep -E "VIDREC|FRAMES|mp4"; }
R a; V SP_side_$S 2200 -700 190 180 "$PS" "${SW}import builtins; builtins.VID_SIDE=(330,90,25); $EX"
R b; V SQ_q34_$S 2200 -700 190 180 "$PS" "${SW}import builtins; builtins.VID_SIDE=(300,140,35); $EX"
