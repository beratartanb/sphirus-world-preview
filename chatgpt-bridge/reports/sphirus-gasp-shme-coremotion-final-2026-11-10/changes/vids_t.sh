#!/bin/bash
# vids_t.sh <suffix>: full-body review + effort A/B + long walk/idle on the flat test stage (L_Sph_MoveTest, house light).
# A = current Sphirus player (no swap), B = GASP pawn with the Sphirus motion layer OFF, C = layer ON.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; P="$PWD"; S=$1; CLS="/Game/Sphirus/Player/GASP/BP_Sph_GASP_B.BP_Sph_GASP_B_C"
SW="exec(open(u.Paths.project_dir()+'Tools/GASP_20261109/swap.py',encoding='utf8').read()); swap('$CLS'); import builtins; "
NS="import builtins; "
PS="[('',1.0,0),('W',4.0,0),('',2.0,0),('W LeftShift',3.0,0),('',2.5,0),('W',1.5,0),('S',2.0,0),('',2.0,0)]"
EF="[('',0.8,0),('W LeftShift',1.6,0),('S LeftShift',1.4,0),('W LeftShift',1.0,0),('S LeftShift',1.0,0),('W LeftShift',1.0,0),('',2.0,0),('S LeftShift',1.4,0),('',5.0,0),('W LeftShift',1.4,0),('S LeftShift',1.4,0),('',2.0,0)]"
WL="[('',1.0,0),('W',30.0,0),('',2.0,0)]"
PI="[('',50.0,0)]"
R(){ bash Tools/Embodied_20261105/relaunch.sh emb_t$S$1 2>&1 | tail -1; echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt; SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$P/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED; bash Tools/Day_20261107/ed.sh Tools/GASP_20261109/warm.py measure 600 | grep -c WARM; }
V(){ bash Tools/Day_20261107/v55.sh "$@" 2>&1 | grep -E "VIDREC|FRAMES|mp4"; }
OFF="builtins.VID_MOTION={'Enabled':False,'EffortEnabled':False}"; ON="builtins.VID_MOTION={}"
R a; V TS_side_A_$S -6000 2000 92 0 "$PS" "${NS}builtins.VID_SIDE=(330,90,25)"
R b; V TS_side_B_$S -6000 2000 92 0 "$PS" "${SW}$OFF; builtins.VID_SIDE=(330,90,25)"
R c; V TS_side_C_$S -6000 2000 92 0 "$PS" "${SW}$ON; builtins.VID_SIDE=(330,90,25)"
R d; V TQ_q34_A_$S -6000 2000 92 0 "$PS" "${NS}builtins.VID_SIDE=(300,140,35)"
R e; V TQ_q34_C_$S -6000 2000 92 0 "$PS" "${SW}$ON; builtins.VID_SIDE=(300,140,35)"
R f; V TE_on_C_$S -6000 2000 92 0 "$EF" "${SW}$ON; builtins.VID_SIDE=None"
R g; V TE_off_C_$S -6000 2000 92 0 "$EF" "${SW}builtins.VID_MOTION={'EffortEnabled':False}; builtins.VID_SIDE=None"
R h; V TW_walk30_C_$S -6000 2000 92 0 "$WL" "${SW}$ON; builtins.VID_SIDE=None"
R i; V TI_idle50_C_$S -6000 2000 92 0 "$PI" "${SW}$ON; builtins.VID_SIDE=None"
bash Tools/Embodied_20261105/relaunch.sh emb_t${S}z 2>&1 | tail -1
