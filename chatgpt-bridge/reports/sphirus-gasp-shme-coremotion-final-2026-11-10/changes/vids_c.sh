#!/bin/bash
# vids_c.sh <suffix>: C candidate (GASP + Sphirus motion layer) protocol + effort A/B (same input, EffortEnabled on/off).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; S=$1; CLS="/Game/Sphirus/Player/GASP/BP_Sph_GASP_B.BP_Sph_GASP_B_C"
SW="exec(open(u.Paths.project_dir()+'Tools/GASP_20261109/swap.py',encoding='utf8').read()); swap('$CLS')"
EOFF="; import builtins; builtins.VID_MOTION={'EffortEnabled':False}"
EON="; import builtins; builtins.VID_MOTION={}"
PP="[('',0.8,0),('W LeftShift',1.7,0),('',1.8,0),('S',2.0,0),('',1.5,0),('W',1.5,0),('S',1.5,0),('',1.5,0)]"
PB="[('',0.5,0),('W',1.5,0),('W',0.5,360),('W',1.5,0),('W',0.5,-360),('W',1.2,0),('W',0.3,150),('W',0.6,0),('W',0.3,-150),('W',0.8,0),('',1.2,0),('',0.8,180),('W',0.4,0),('',1.0,0),('W LeftShift',1.0,0),('W LeftShift',0.5,360),('W LeftShift',1.2,0),('',1.5,0)]"
PA="[('',0.7,0),('W',2.0,0),('W LeftShift',1.1,0),('W LeftShift',1.2,150),('W LeftShift',1.3,0),('W',1.2,0),('',1.3,0),('W',1.2,0),('',1.0,0)]"
PH="[('',0.6,0),('W',2.5,0),('W LeftShift',1.5,0),('',1.2,0),('',0.6,300),('W',2.5,0),('',1.0,0)]"
EF="[('',0.8,0),('W LeftShift',1.6,0),('S LeftShift',1.4,0),('W LeftShift',1.0,0),('S LeftShift',1.0,0),('W LeftShift',1.0,0),('',2.0,0),('S LeftShift',1.4,0),('',5.0,0),('W LeftShift',1.4,0),('S LeftShift',1.4,0),('',2.0,0)]"
R(){ bash Tools/Embodied_20261105/relaunch.sh emb_c$S$1 2>&1 | tail -1; bash Tools/Day_20261107/ed.sh Tools/GASP_20261109/warm.py measure 600 | grep -c WARM; }
V(){ bash Tools/Day_20261107/v55.sh "$@" 2>&1 | grep -E "VIDREC|FRAMES|mp4"; }
R a; V PH_phys_$S 2200 -700 190 180 "$PP" "$SW"
R b; V B_turns_$S 1400 -700 190 0 "$PB" "$SW"
R c; V EF_on_$S 2150 -700 190 180 "$EF" "$SW$EON"
R d; V EF_off_$S 2150 -700 190 180 "$EF" "$SW$EOFF"
R e; V A_loco_$S 2200 -700 190 180 "$PA" "$SW"
R f; V H_hall_$S 720 400 245 90 "$PH" "$SW"
