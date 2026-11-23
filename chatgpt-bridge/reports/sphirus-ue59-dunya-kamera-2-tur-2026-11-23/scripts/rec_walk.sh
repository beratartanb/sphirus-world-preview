#!/bin/bash
# rec_walk.sh <tag>: one player-camera recording with injected input (GOTO steering): front yard -> veranda -> front door -> hall ->
# stair hall -> workshop -> back through the hall -> rear door -> stones along the wall -> chopping yard. Not a human-played session.
cd "<PROJECT_ROOT>"; export MAP=/Game/GraceRanger/Maps/L_GR_SphirusHouse VSHOT=1; unset VSIDE VKEEP
HKF="$(cat Saved/UE59Work/r5/hk3_line.txt)"
PLAN="[('',1.0,0,-6),('GOTO',2.5,0,-6,(860,1480,200)),('GOTO',2.4,0,-6,(845,1250,245)),('GOTO',2.2,0,-6,(845,1030,245)),('GOTO',3.4,0,-8,(800,640,245)),('GOTO',2.4,0,-8,(560,570,245)),('GOTO',2.4,0,-8,(540,330,245)),('',1.2,0,-8),('W',0.3,600,-8),('GOTO',2.4,0,-8,(560,560,245)),('GOTO',2.4,0,-8,(800,480,245)),('GOTO',3.2,0,-8,(830,120,245)),('GOTO',2.0,0,-8,(835,-60,225)),('GOTO',1.6,0,-8,(900,-160,210)),('GOTO',2.2,0,-8,(1108,-212,200)),('GOTO',3.0,0,-8,(1424,-186,200)),('GOTO',1.4,0,-8,(1528,-206,200)),('GOTO',1.4,0,-8,(1610,-290,200)),('GOTO',1.4,0,-8,(1692,-372,200)),('GOTO',1.2,0,-8,(1772,-352,200)),('',1.5,0,-8)]"
echo "$PLAN" > Saved/UE59Work/r2g2/plan_walk.txt
POS="850 1750 138 -90" bash Tools/UE59_20261120/seqP.sh $1 Saved/UE59Work/r2g2/plan_walk.txt "$HKF" 2>&1 | grep -E "VIDREC|mp4|SLOT|FRAMES|STALL|ERR" | cut -c1-200
