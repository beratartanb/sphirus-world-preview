# shared test plans (keys, seconds, yawRate deg/s)
PLAN_TURN="[('',2.0,0),('W',3.0,0),('W',6.0,60),('W',2.0,0),('W',1.0,90),('W',2.0,0),('W',1.0,-135),('W',2.0,0),('W',1.0,180),('W',2.0,0),('',2.0,0)]"
PLAN_JOGTURN="[('',2.0,0),('W LeftShift',4.0,0),('W LeftShift',4.0,60),('W LeftShift',2.0,0),('W LeftShift',1.0,90),('W LeftShift',2.0,0),('W LeftShift',1.0,180),('W LeftShift',2.0,0),('',3.0,0)]"
PLAN_CROUCH="[('',2.0,0),('C',0.2,0),('',2.0,0),('W',6.0,0),('',2.0,0),('S',4.0,0),('A',3.0,0),('',1.0,0),('C',0.2,0),('',3.0,0)]"
PLAN_STOP="[('',2.0,0),('W LeftShift LeftControl',7.0,0),('',3.0,0),('W LeftShift LeftControl',5.0,0),('',3.0,0),('W LeftShift',5.0,0),('',3.0,0),('W',5.0,0),('',3.0,0)]"
# hip-swing turn plans: mouse flicks of 45/90/135/180 deg in 0.25 s, both directions, 3 s straight after each (walk / jog)
HT(){ echo "('$1',4.0,0),('$1',0.25,180),('$1',3.0,0),('$1',0.25,-180),('$1',3.0,0),('$1',0.25,360),('$1',3.0,0),('$1',0.25,-360),('$1',3.0,0),('$1',0.25,540),('$1',3.0,0),('$1',0.25,-540),('$1',3.0,0),('$1',0.25,720),('$1',3.0,0),('$1',0.25,-720),('$1',3.0,0)"; }
PLAN_HIPW="[('',2.0,0),$(HT 'W'),('',2.0,0)]"
PLAN_HIPJ="[('',2.0,0),$(HT 'W LeftShift'),('',2.0,0)]"
PLAN_JUMP="[('',2.0,0),('SpaceBar',0.2,0),('',2.5,0),('W',3.0,0),('W SpaceBar',0.2,0),('W',3.0,0),('W LeftShift',3.0,0),('W LeftShift SpaceBar',0.2,0),('W LeftShift',3.0,0),('W LeftShift LeftControl',3.0,0),('W LeftShift LeftControl SpaceBar',0.2,0),('W LeftShift LeftControl',2.0,0),('',3.0,0)]"
PLAN_HIPS="[('',2.0,0),$(HT 'W LeftShift LeftControl'),('',2.0,0)]"
# brake + re-push, S backstep out of a walk / jog, quick W taps (2026-11-17)
PLAN_BRAKE="[('',2.0,0),('W LeftShift',4.0,0),('',0.35,0),('W LeftShift',3.0,0),('',0.35,0),('W',3.0,0),('',0.3,0),('W',3.0,0),('S',2.5,0),('W',3.0,0),('W LeftShift',3.0,0),('S',2.5,0),('',2.0,0),('W',0.15,0),('',1.5,0),('W',0.3,0),('',1.5,0),('W',0.6,0),('',2.5,0)]"
