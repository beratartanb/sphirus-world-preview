#!/bin/bash
# vids_shme.sh <suffix>: real-time acceptance videos for the SHME-quality report (window screenshots, per-frame time
# dilation so the game step is 1/30 s). Yard A loco, B turns, D chop, H hall, plus CL (camera fixed: A, D, W+A, W+D, W, S)
# and I (20 s idle). ~1.3 s wall per frame in the house map.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; S=$1
PA="[('',0.7,0),('W',2.0,0),('W LeftShift',1.1,0),('W LeftShift',1.2,150),('W LeftShift',1.3,0),('W',1.2,0),('',1.3,0),('W',1.2,0),('',1.0,0)]"
PB="[('',0.5,0),('W',1.5,0),('W',0.5,360),('W',1.5,0),('W',0.5,-360),('W',1.2,0),('W',0.3,150),('W',0.6,0),('W',0.3,-150),('W',0.8,0),('',1.2,0),('',0.8,180),('W',0.4,0),('',1.0,0),('W LeftShift',1.0,0),('W LeftShift',0.5,360),('W LeftShift',1.2,0),('',1.5,0)]"
PD="[('',0.5,0,-22),('W',1.15,0,-22),('',0.6,0,-22),('E',0.15,0,-22),('',3.2,0,-22),('LeftMouseButton',0.15,0,-22),('',4.0,0,-22),('',1.5,0,-22)]"
PH="[('',0.6,0),('W',2.5,0),('W LeftShift',1.5,0),('',1.2,0),('',0.6,300),('W',2.5,0),('',1.0,0)]"
PC="[('',0.8,0),('A',2.5,0),('',1.0,0),('D',2.5,0),('',1.0,0),('W A',2.0,0),('',0.8,0),('W D',2.0,0),('',0.8,0),('W',1.5,0),('S',2.0,0),('',1.2,0)]"
PI="[('',20.0,0)]"
R(){ bash Tools/Embodied_20261105/relaunch.sh emb_s$S$1 2>&1 | tail -1; }
bash Tools/Day_20261107/v55.sh CL_strafe_$S 2200 -700 190 180 "$PC" 2>&1 | grep -E "VIDREC|FRAMES|VIDEO|mp4"
R a; bash Tools/Day_20261107/v55.sh A_loco_$S 2200 -700 190 180 "$PA" 2>&1 | grep -E "VIDREC|FRAMES|VIDEO|mp4"
R b; bash Tools/Day_20261107/v55.sh B_turns_$S 1400 -700 190 0 "$PB" 2>&1 | grep -E "VIDREC|FRAMES|VIDEO|mp4"
R c; bash Tools/Day_20261107/v55.sh H_hall_$S 720 400 245 90 "$PH" 2>&1 | grep -E "VIDREC|FRAMES|VIDEO|mp4"
R d; bash Tools/Day_20261107/v55.sh D_chop_$S 1640 -455 190 34 "$PD" 2>&1 | grep -E "VIDREC|FRAMES|VIDEO|mp4"
R e; bash Tools/Day_20261107/v55.sh I_idle_$S 2200 -700 190 180 "$PI" 2>&1 | grep -E "VIDREC|FRAMES|VIDEO|mp4"
