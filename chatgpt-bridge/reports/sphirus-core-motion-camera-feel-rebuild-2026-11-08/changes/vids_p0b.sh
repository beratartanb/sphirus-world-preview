#!/bin/bash
# vids_p0b.sh <suffix> [legacy]: acceptance videos at a real-time step - yard A loco, B turns, D chop (as vids_final.sh)
# plus H_hall: the lower hallway of the house (entry hall tree y=323 -> veranda door y=1140 along x~720, floor z=150),
# a real narrow passage for the camera: walk, jog, stop, 180, walk back. With "legacy" the driver uses the old database.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; S=$1
PRE="pass"; [ "$2" = "legacy" ] && PRE="PW.mesh.get_anim_instance().set_editor_property('ForceLegacy',True)"
PA="[('',0.7,0),('W',2.0,0),('W LeftShift',1.1,0),('W LeftShift',1.2,150),('W LeftShift',1.3,0),('W',1.2,0),('',1.3,0),('W',1.2,0),('',1.0,0)]"
PB="[('',0.5,0),('W',1.5,0),('W',0.5,360),('W',1.5,0),('W',0.5,-360),('W',1.2,0),('W',0.3,150),('W',0.6,0),('W',0.3,-150),('W',0.8,0),('',1.2,0),('',0.8,180),('W',0.4,0),('',1.0,0),('W LeftShift',1.0,0),('W LeftShift',0.5,360),('W LeftShift',1.2,0),('',1.5,0)]"
PD="[('',0.5,0,-22),('W',0.8,0,-22),('',0.6,0,-22),('E',0.15,0,-22),('',3.2,0,-22),('LeftMouseButton',0.15,0,-22),('',4.0,0,-22),('',1.5,0,-22)]"
PH="[('',0.6,0),('W',2.5,0),('W LeftShift',1.5,0),('',1.2,0),('',0.6,300),('W',2.5,0),('',1.0,0)]"
R(){ bash Tools/Embodied_20261105/relaunch.sh emb_v$S$1 2>&1 | tail -1; }
bash Tools/Day_20261107/v55.sh A_loco_$S 2200 -700 190 180 "$PA" "$PRE" 2>&1 | grep -E "VIDREC|FRAMES|VIDEO|mp4"
R a; bash Tools/Day_20261107/v55.sh B_turns_$S 1400 -700 190 0 "$PB" "$PRE" 2>&1 | grep -E "VIDREC|FRAMES|VIDEO|mp4"
R b; bash Tools/Day_20261107/v55.sh D_chop_$S 1640 -455 190 34 "$PD" "$PRE" 2>&1 | grep -E "VIDREC|FRAMES|VIDEO|mp4"
R c; bash Tools/Day_20261107/v55.sh H_hall_$S 720 400 245 90 "$PH" "$PRE" 2>&1 | grep -E "VIDREC|FRAMES|VIDEO|mp4"
