#!/bin/bash
# vids_c3.sh <suffix>: effort A/B (EffortEnabled on/off applied every frame), 50 s idle, side + 3/4 body review of C.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; S=$1; CLS="/Game/Sphirus/Player/GASP/BP_Sph_GASP_B.BP_Sph_GASP_B_C"
SW="exec(open(u.Paths.project_dir()+'Tools/GASP_20261109/swap.py',encoding='utf8').read()); swap('$CLS'); import builtins; builtins.VID_SIDE=None; "
EF="[('',0.8,0),('W LeftShift',1.6,0),('S LeftShift',1.4,0),('W LeftShift',1.0,0),('S LeftShift',1.0,0),('W LeftShift',1.0,0),('',2.0,0),('S LeftShift',1.4,0),('',5.0,0),('W LeftShift',1.4,0),('S LeftShift',1.4,0),('',2.0,0)]"
PI="[('',50.0,0)]"
PS="[('',1.0,0),('W',4.0,0),('',2.0,0),('W LeftShift',3.0,0),('',2.5,0),('W',1.5,0),('S',2.0,0),('',2.0,0)]"
R(){ bash Tools/Embodied_20261105/relaunch.sh emb_d$S$1 2>&1 | tail -1; bash Tools/Day_20261107/ed.sh Tools/GASP_20261109/warm.py measure 600 | grep -c WARM; }
V(){ bash Tools/Day_20261107/v55.sh "$@" 2>&1 | grep -E "VIDREC|FRAMES|mp4"; }
R a; V EF_on_$S 2150 -700 190 180 "$EF" "${SW}builtins.VID_MOTION={}"
R b; V EF_off_$S 2150 -700 190 180 "$EF" "${SW}builtins.VID_MOTION={'EffortEnabled':False}"
R c; V I_idle50_$S 2200 -700 190 180 "$PI" "${SW}builtins.VID_MOTION={}"
R d; V SP_side_$S 2200 -700 190 180 "$PS" "${SW}builtins.VID_MOTION={}; builtins.VID_SIDE=(330,90,25)"
R e; V SQ_q34_$S 2200 -700 190 180 "$PS" "${SW}builtins.VID_MOTION={}; builtins.VID_SIDE=(300,140,35)"
