#!/bin/bash
# vids_final.sh <suffix> [legacy]: the acceptance videos at a real-time 30 fps step. With "legacy" the driver is forced to
# the old single database (same build) so the gait selection can be compared on identical routes.
# Yard: A loco (walk/jog/180 reversal into run/walk/stop/restart), B turns (180 x2, 45 zig-zag, stop, turn in place, jog
# reversal), D chop action. Corridor: CA loco straight, CB turns, CC doorway + wall pass.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; S=$1
PRE="pass"; [ "$2" = "legacy" ] && PRE="PW.mesh.get_anim_instance().set_editor_property('ForceLegacy',True)"
PA="[('',0.7,0),('W',2.0,0),('W LeftShift',1.1,0),('W LeftShift',1.2,150),('W LeftShift',1.3,0),('W',1.2,0),('',1.3,0),('W',1.2,0),('',1.0,0)]"
PB="[('',0.5,0),('W',1.5,0),('W',0.5,360),('W',1.5,0),('W',0.5,-360),('W',1.2,0),('W',0.3,150),('W',0.6,0),('W',0.3,-150),('W',0.8,0),('',1.2,0),('',0.8,180),('W',0.4,0),('',1.0,0),('W LeftShift',1.0,0),('W LeftShift',0.5,360),('W LeftShift',1.2,0),('',1.5,0)]"
PD="[('',0.5,0,-22),('W',0.8,0,-22),('',0.6,0,-22),('E',0.15,0,-22),('',3.2,0,-22),('LeftMouseButton',0.15,0,-22),('',4.0,0,-22),('',1.5,0,-22)]"
CA="[('',0.7,0),('W',3.0,0),('W LeftShift',3.5,0),('W',2.0,0),('',1.5,0),('W',1.5,0),('',1.2,0)]"
CB="[('',0.5,0),('W',1.5,0),('W',0.3,150),('W',1.5,0),('W',0.3,300),('W',1.5,0),('W',0.5,360),('W',1.8,0),('W LeftShift',1.2,0),('W LeftShift',0.5,360),('W LeftShift',1.5,0),('',1.5,0),('',0.8,180),('W',0.4,0),('',1.2,0)]"
CC="[('',0.5,0),('W',4.0,0),('W LeftShift',4.0,0),('',1.5,0)]"
R(){ bash Tools/Embodied_20261105/relaunch.sh emb_v$S$1 2>&1 | tail -1; }
bash Tools/Day_20261107/v55.sh A_loco_$S 2200 -700 190 180 "$PA" "$PRE" 2>&1 | grep -E "VIDREC|FRAMES|VIDEO|mp4"
R a; bash Tools/Day_20261107/v55.sh B_turns_$S 1400 -700 190 0 "$PB" "$PRE" 2>&1 | grep -E "VIDREC|FRAMES|VIDEO|mp4"
R b; bash Tools/Day_20261107/v55.sh D_chop_$S 1640 -455 190 34 "$PD" "$PRE" 2>&1 | grep -E "VIDREC|FRAMES|VIDEO|mp4"
[ -n "$SKIPCORR" ] && exit 0
R c; bash Tools/Day_20261107/v56.sh CA_loco_$S "$CA" -200 0 0 "$PRE" 2>&1 | grep -E "VIDREC|FRAMES|VIDEO|mp4"
R d; bash Tools/Day_20261107/v56.sh CB_turns_$S "$CB" -200 0 0 "$PRE" 2>&1 | grep -E "VIDREC|FRAMES|VIDEO|mp4"
R e; bash Tools/Day_20261107/v56.sh CC_door_$S "$CC" 1000 0 0 "$PRE" 2>&1 | grep -E "VIDREC|FRAMES|VIDEO|mp4"
