#!/bin/bash
# rec_r2g.sh <tag>: two player-camera recordings on the house map with injected key input (30 Hz fixed game step, 30 fps = real speed):
#   <tag>_out : shore path from the front landing: walk, jog, walk, stop, curve right/left, back-pedal, strafe, 180 turn, walk, sprint, stop
#   <tag>_in  : kitchen -> rear door -> garden path (GOTO steering: W held, look steered to waypoints), jog segment, 180 turns
# Keys are injected (Input.+key); look is written as control rotation by the harness. Not a human-played session, no gamepad.
cd "<proje>/sphirus_UE59"; export MAP=/Game/GraceRanger/Maps/L_GR_SphirusHouse VSHOT=1; unset VSIDE VKEEP
HKF="$(cat Saved/UE59Work/r5/hk3_line.txt)"; G=$1
OUT="[('',1.5,0,-6),('W',4.0,0,-6),('W LeftShift',3.0,0,-6),('W',2.0,0,-6),('',1.5,0,-6),('W',1.5,60,-6),('W',1.5,0,-6),('W',1.5,-60,-6),('',1.2,0,-6),('S',1.5,0,-6),('D',1.5,0,-6),('A',1.5,0,-6),('',1.0,0,-6),('W',0.3,600,-6),('W',3.0,0,-6),('W LeftShift LeftControl',2.0,0,-6),('',2.0,0,-6)]"
HOUSE="('',1.5,0,-12),('GOTO',1.5,0,-12,(1150,320,245)),('GOTOJ',1.6,0,-12,(1160,620,245)),('GOTO',2.0,0,-12,(1160,320,245)),('GOTO',2.0,0,-12,(1080,200,245))"
EXIT="('GOTO',2.5,0,-12,(1000,200,245)),('GOTO',2.5,0,-12,(840,60,240)),('GOTO',2.0,0,-12,(840,-40,220)),('GOTO',3.0,0,-12,(880,-150,210))"
PTH="('GOTO',3.0,0,-12,(1100,-200,205)),('GOTOJ',4.0,0,-12,(1300,-250,200)),('',1.5,0,-12),('W',0.3,600,-12),('W',1.5,0,-12),('',1.0,0,-12),('W',0.3,600,-12),('GOTOJ',4.0,0,-12,(1450,-480,150)),('GOTO',3.0,0,-14,(1540,-520,190)),('',2.0,0,-12)"
echo "$OUT" > Saved/UE59Work/r2g/plan_out.txt; echo "[$HOUSE,$EXIT,$PTH]" > Saved/UE59Work/r2g/plan_in.txt
POS="720 2330 71 43" bash Tools/UE59_20261120/seqP.sh ${G}_out Saved/UE59Work/r2g/plan_out.txt "$HKF" 2>&1 | grep -E "VIDREC|mp4|SLOT|FRAMES"
POS="1080 200 245 90" bash Tools/UE59_20261120/seqP.sh ${G}_in Saved/UE59Work/r2g/plan_in.txt "$HKF" 2>&1 | grep -E "VIDREC|mp4|SLOT|FRAMES"
