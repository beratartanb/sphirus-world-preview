---
name: sphirus-camera-direction
description: Procedure for the SPHIRUS third-person camera's behaviour states - player look priority -> base follow -> transient physical (cinematic) reaction -> settle back to the follow angle -> collision and input audit - including automatic recentre behind the new travel direction without the right stick, gamepad vs mouse profiles and the input-frame handover. Use before changing camera follow, orbit, recentre, framing, look handling or camera-relative movement.
---

# SPHIRUS camera direction

One coordinator in the existing camera owner (BP_GR_Player GR_UpdateRig + the SHME camera layer) - no new framework, no second system
pulling the camera the other way. Feel target / acceptance: `sphirus-character-camera`; signals: `sphirus-human-motion-engine`.

## Behaviour states (mandatory order of priority)
1. **Player look** - mouse / right stick / gyro above the real dead zone wins at once; hand-over keeps the currently SEEN angle (no jump
   to an old centre). Stick drift is not a look.
2. **Base follow** - during stable travel the view sits behind / over the shoulder of the travel direction.
3. **Transient reaction** - brake onset, turn direction, support hand-over, re-push and the body settling into the new direction drive
   a bounded extra view angle that is built early when needed, shows the important body motion, and resolves at the end of the action.
   A camera that swings out after the turn has finished is a failure. 180 deg: a real turn keeps a stable side (support / previous turn /
   room); backward stepping does not orbit.
4. **Settle -> auto recentre** - after the reaction, if the travel direction is stable, the critical brake / settle phase is over, the
   player is not looking elsewhere, no inspection / aim / interaction priority and the space is safe: ease (accelerate / decelerate, no
   snap, no constant-rate sweep, no overshoot) to the follow angle behind the new travel direction. Not a fixed timer; a new reverse
   request re-evaluates from the current state. Standing look-around and inspection are never pulled back. Pitch untouched first.
5. **Collision / input audit** - the WHOLE orbit and recentre path is collision-safe (not only the end point); near walls the angle
   narrows, the shoulder side does not flip, no spring-back when the obstacle clears; character visibility, route and control readability
   before cinematics.

## Input frame (architecture rule)
The transient orbit never feeds ControlRotation. Auto recentre may move the base view reference, but only through ONE owner, and must
never create a movement direction the player did not ask for: while the same move input is held, keep its world direction (hand the
reference over smoothly on a new deliberate input) - no circles / zig-zag. Walk exploration orientation and deliberate strafe / back
steps stay distinct. Gamepad: assisted follow default; mouse: less intrusive profile; auto follow and cinematic reaction separately switchable.
**The camera changes neither direction NOR speed** (V2.34): every locomotion reader that classified the move against the control yaw
(BP_GR_Player CalculateMaxSpeed / MaxAcceleration / GroundFriction / GetDesiredGait / CR_UpdateBackwardIntent / CP_PhysicalRedirect /
UpdateIdleTurn) reads the SHME body frame `LocoYaw` instead - the auto recentre turned a held right sprint from side (417) into forward
(490) and rotated the walking body. A body re-orientation (walk exploration, a real turn) is the BODY's decision (`LocoExplore*`), the
camera follows the body. Hand-over of the held input: by the stick's NET deviation from where it was when the auto turn began (small
corrections steer, never re-interpret; no single angle threshold), at once on release, by the player's own look.

## Failed examples (real)
- V2.33 recentre rotated the control yaw that the speed / facing functions read: same input, camera on vs off = 73 cm/s, 297 cm path, 92 deg
  body yaw difference (camab234). "A visual preference" was a dependency bug.
- V2.33 walk recentre was switched off (MinSpeed 170) after a slide - a disabled walk follow is not a delivered walk follow.
- V2.34 first manual-look test: the look happened BEFORE the recentre started (it then waited LookHold) - the test never exercised "look
  during the recentre": check the target state is active at the event (CamRecDelta != 0 at the look start) or report NOT_TRIGGERED.
- V2.34 first hand-over (accumulated stick change): +-5 deg corrections slowly re-interpreted the held stick in the new view = a drift the
  player did not ask for.
- V2.32 orbit read the control yaw through Pawn.LastHitBy (None): the orbit was relative to world X for 9 hours of tests (harness yaw0 = 0).
- V2.34 "the camera makes MM pick another lower-body clip" (sprint cut, mouse) was not proven: V2.35 same body, camera on / off, 2 repeats
  each - 3 of 4 runs had identical clip + time; the one divergent run was a camera-OFF repeat (off1 vs off2 differ too). Compare selection
  between repeats of the SAME variant before blaming the camera; the camera only moved the head <= 1-11 cm (aim offset).
- V2.34 mouse walk follow (scale 0.35 -> 16 deg/s) never settled in 5.5 s: "less intrusive" is not acceptance; 0.7 settles in 2.4 s.
- "body234 = new body + old camera" is not a camera-off test; a camera-off variant switches the follow off (CamRecEnabled false) and the
  report names the active settings.
- V2.32 orbit = speed x sin(angle): max 13.7 deg but the right-turn 3/4 time did not grow and a 180 turn gave 0; CamOrbitYaw -> 0 does NOT
  mean the camera sits behind the new direction (the boom still follows the control yaw).

## Acceptance test
Measure the FINAL camera (position, yaw vs body / travel), not the orbit variable: 3/4 view time inside the brake / push window,
time to settle behind the new travel, player input path, movement path, framing and obstacle clearance; compare jerk in real time units.
Mandatory: walk -> right / left turn -> behind follow with no right stick; jog / sprint -> brake -> diagonal view -> behind follow;
real 180 vs backward travel; manual look in the middle of the reaction / recentre; new request, narrow space, mask inspection, slope.
Body x camera A/B/C/D (old/new body x old/new camera). Gamepad tested on PC only unless PS hardware was used.
Camera on / off with the SAME body version: speed, travel yaw, actor yaw, acceleration, gait class and planar path must be identical while
the input is held (`Tools/SHME_V234_20261028/camab234.py`, 0.0 = decoupled). A stick that moved after the view turned is camera-relative
by design - judge it by continuity (no jump, no stuck direction), not by equality.

## Tools / rollback
`Tools/SHME_V232_20261027/cam232.py`, `camcmp232.py`, `Tools/SHME_V233_20261027/rec233.py`, `Tools/SHME_V234_20261028/camab234.py`, `check234.py`; camera DA knobs (CamOrbit*, follow knobs) switch each layer off -> previous stable
camera returns; BP changes behind manifests (safe-iteration).
