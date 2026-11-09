#!/bin/bash
# cam_sym2.sh <suffix>: fixed-camera framing labs on the open test corridor (no obstacles): run A / D / W+A / W+D and
# walk A / D, plus mouse sweeps at walk and run. Data-only, real time.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; S=$1
PR="[('',0.8,0),('A LeftShift',3.0,0),('',1.2,0),('D LeftShift',3.0,0),('',1.2,0),('W A LeftShift',2.5,0),('',1.0,0),('W D LeftShift',2.5,0),('',1.0,0),('A',2.5,0),('',1.0,0),('D',2.5,0),('',1.0,0)]"
PM="[('',0.6,0),('W',1.5,0),('W',1.0,90),('W',1.5,0),('W',1.0,-90),('W',1.5,0),('W',0.5,360),('W',1.5,0),('W LeftShift',2.0,0),('W LeftShift',1.0,90),('W LeftShift',1.5,0),('W LeftShift',1.0,-90),('W LeftShift',1.5,0),('',1.0,0)]"
bash Tools/Day_20261107/lab.sh CS_run_$S test -2000 0 92 0 "$PR" 2>&1 | tail -1
bash Tools/Day_20261107/lab.sh CS_mouse_$S test -2000 0 92 0 "$PM" 2>&1 | tail -1
