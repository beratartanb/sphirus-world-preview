#!/bin/bash
# seqI.sh: slope behaviour on the house map (saved state): walk up, stop on the slope, 180 reverse, walk down, re-walk up, jump,
# jog down to the flat (slope layer carry-over + downhill brake). 60 Hz data + one player-camera video (30 Hz, real speed).
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"
echo "/Game/GraceRanger/Maps/L_GR_SphirusHouse" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
P="[('',1.5,0),('W',6.0,0),('',1.5,0),('W',0.3,180),('W',3.0,0),('',1.2,0),('W',0.3,-180),('W',3.0,0),('W SpaceBar',0.2,0),('W',2.0,0),('W',0.3,180),('W LeftShift',4.0,0),('',2.0,0)]"
bash Tools/UE59_20261118/run2.sh I_slope${SL:-} ${X0:-2640} ${Y0:-420} ${Z0:-322} ${YAW0:--83} "$P" "pass"
[ -n "$VID" ] && VSHOT=1 bash Tools/UE59_20261118/run2.sh I_slope_pc${SL:-} ${X0:-2640} ${Y0:-420} ${Z0:-322} ${YAW0:--83} "$P" "pass"
echo SEQI_DONE
