#!/bin/bash
# vids_shme2.sh <suffix>: real-time acceptance videos, SHME turn 2. Same yard/hall/chop/idle/strafe set as vids_shme.sh
# plus PH (physics: run start/stop, 180 turns, walk reversal) on the yard lane, camera fixed. Relaunch between videos.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; S=$1
PA="[('',0.7,0),('W',2.0,0),('W LeftShift',1.1,0),('W LeftShift',1.2,150),('W LeftShift',1.3,0),('W',1.2,0),('',1.3,0),('W',1.2,0),('',1.0,0)]"
PB="[('',0.5,0),('W',1.5,0),('W',0.5,360),('W',1.5,0),('W',0.5,-360),('W',1.2,0),('W',0.3,150),('W',0.6,0),('W',0.3,-150),('W',0.8,0),('',1.2,0),('',0.8,180),('W',0.4,0),('',1.0,0),('W LeftShift',1.0,0),('W LeftShift',0.5,360),('W LeftShift',1.2,0),('',1.5,0)]"
PD="[('',0.5,0,-22),('W',1.15,0,-22),('',0.6,0,-22),('E',0.15,0,-22),('',3.2,0,-22),('LeftMouseButton',0.15,0,-22),('',4.0,0,-22),('',1.5,0,-22)]"
PH="[('',0.6,0),('W',2.5,0),('W LeftShift',1.5,0),('',1.2,0),('',0.6,300),('W',2.5,0),('',1.0,0)]"
PC="[('',0.8,0),('A',2.5,0),('',1.0,0),('D',2.5,0),('',1.0,0),('W A',2.0,0),('',0.8,0),('W D',2.0,0),('',0.8,0),('W',1.5,0),('S',2.0,0),('',1.2,0)]"
PI="[('',20.0,0)]"
PP="[('',0.8,0),('W LeftShift',1.7,0),('',1.8,0),('S',2.0,0),('',1.5,0),('W',1.5,0),('S',1.5,0),('',1.5,0)]"
R(){ bash Tools/Embodied_20261105/relaunch.sh emb_s$S$1 2>&1 | tail -1; }
V(){ bash Tools/Day_20261107/v55.sh "$@" 2>&1 | grep -E "VIDREC|FRAMES|VIDEO|mp4"; }
V PH_phys_$S 2200 -700 190 180 "$PP"
R a; V CL_strafe_$S 2200 -700 190 180 "$PC"
R b; V A_loco_$S 2200 -700 190 180 "$PA"
R c; V B_turns_$S 1400 -700 190 0 "$PB"
R d; V H_hall_$S 720 400 245 90 "$PH"
R e; V D_chop_$S 1640 -455 190 34 "$PD"
R f; V I_idle_$S 2200 -700 190 180 "$PI"
