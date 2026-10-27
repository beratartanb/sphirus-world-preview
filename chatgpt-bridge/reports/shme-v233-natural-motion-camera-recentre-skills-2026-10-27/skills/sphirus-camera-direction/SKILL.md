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

## Failed examples (real)
- V2.32 orbit read the control yaw through Pawn.LastHitBy (None): the orbit was relative to world X for 9 hours of tests (harness yaw0 = 0).
- V2.32 orbit = speed x sin(angle): max 13.7 deg but the right-turn 3/4 time did not grow and a 180 turn gave 0; CamOrbitYaw -> 0 does NOT
  mean the camera sits behind the new direction (the boom still follows the control yaw).

## Acceptance test
Measure the FINAL camera (position, yaw vs body / travel), not the orbit variable: 3/4 view time inside the brake / push window,
time to settle behind the new travel, player input path, movement path, framing and obstacle clearance; compare jerk in real time units.
Mandatory: walk -> right / left turn -> behind follow with no right stick; jog / sprint -> brake -> diagonal view -> behind follow;
real 180 vs backward travel; manual look in the middle of the reaction / recentre; new request, narrow space, mask inspection, slope.
Body x camera A/B/C/D (old/new body x old/new camera). Gamepad tested on PC only unless PS hardware was used.

## Tools / rollback
`Tools/SHME_V232_20261027/cam232.py`, `camcmp232.py`; camera DA knobs (CamOrbit*, follow knobs) switch each layer off -> previous stable
camera returns; BP changes behind manifests (safe-iteration).
