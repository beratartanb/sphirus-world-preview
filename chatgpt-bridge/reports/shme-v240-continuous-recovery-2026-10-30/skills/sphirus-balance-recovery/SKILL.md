---
name: sphirus-balance-recovery
description: How SPHIRUS decides, from the body's real state, whether a locomotion request is met with normal support, a braking / transfer contact, an extra recovery step or (rarely) a measured loss of balance - centre of mass, base of support, momentum, extrapolated CoM / capture point, per-contact impulse budget, which foot is available at the request, foot placement from the force direction, and the anti-dither rules. Use before designing, routing or judging any hard direction change (45/90/135/180), brake, re-push, catch step or recovery, and whenever someone proposes "make it harder" by delaying, freezing or slowing the character.
---

# SPHIRUS balance & recovery

Decision owner for "what does the body physically need to do now". Equations already implemented live in
`sphirus-human-motion-engine/references/biomechanics.md` (segment CoM, support, LIP capture point, demands) - do NOT build a second
physics engine; read those values or the same LTP frames. Action procedure (intent -> support -> plan -> source -> integration -> body):
`sphirus-natural-motion`. Content generation: `sphirus-motion-synthesis`. Editor gates: `sphirus-safe-unreal-iteration`.

## What this model is (and is not)
- An explainable, calibrated approximation for choosing a motion. CoM from Dempster segment fractions on the visible mesh, level ground,
  rigid segments. It explains WHY a plan has 2 or 3 contacts; it does not measure forces and does not guarantee balance.
- Running is not an inverted pendulum: use the LIP capture point only for the "can one step catch it?" question; use the per-contact
  impulse budget below for "how many contacts does the redirect need?". State which one a number comes from.

## Quantities (all from data the game already logs)
| Quantity | Source / formula | Kind |
|---|---|---|
| v, heading, a | capsule `ax` finite differences (3-frame) | measured |
| intent | input vector `lix/liy`, component `DesiredVelocity`; event = first frame the input direction changes > 30 deg | measured |
| CoM, v_CoM | Dempster/Winter fractions on `vb_*`/`vx_*` (`Tools/SHME_V238_20261030/balance238.py`) or component `SHM_UpdateBody` | approximation |
| XCoM / capture point | CoM + v_CoM / w, w = sqrt(g / h_CoM) (~3.2 1/s at h 95 cm) | approximation (LIP) |
| support / BoS | per foot: ball within 3 cm of its floor and < 40 cm/s; heel-ball segment +5 cm | heuristic |
| contact impulse | capsule dv between a touchdown and the next touchdown | measured |
| required redirect dv | |v_new - v_old| (90 deg at equal speed = 1.41 v) | kinematics |

## The decision (jog 90 deg, the verified case - extend by the same rules)
1. The request is acknowledged at once by the body (head / trunk start turning in the first frames); the CAPSULE keeps its momentum until a
   foot can push - nothing can change the velocity before a contact. That is not a delay; freezing the body or the input is.
2. Which foot lands next, and how much time is left before it lands, decides the plan (the support state, not the angle alone):
   - OUTSIDE foot next with time to re-aim it (>= ~0.26 s full, nothing below ~0.06 s): PLANT (brake + push toward the turn) ->
     TRANSFER (inside foot, first step on the new line) -> PUSH.  = normal support (level 1).
   - INSIDE foot next: it cannot push toward the turn from its own side -> in-line BRAKE step with a small spin-turn share (lands slightly
     across), then PLANT, TRANSFER, PUSH. = one extra contact (level 2, "elverissiz destek").
   - Outside foot landing too soon to re-aim: WEAK plant (brakes, little turn), then TRANSFER. Also level 2.
3. Impulse budget per contact (calibrated in this project): a deliberate cut ~0.55 g (540 cm/s2) per contact period; the project's
   relaxed jog stop brakes at 410 cm/s2 (0.42 g); re-acceleration 300 cm/s2 (jog start range 165-245, push slightly more). Production
   V2.37 turned a jog 90 at 0.9 g (881 cm/s2) with no braking contact - that was the "mechanical / athletic" read.
4. Force direction = from the foot to the CoM. A plant that must brake AND push right goes ahead-left of the CoM (for a right cut), wider
   than the jog track; a brake step goes ahead in line; transfer / push steps land on the current velocity line.
5. Number of contacts EMERGES from simulating the velocity through these contacts (never a table of angles): jog 90 = 4 (normal) or 5
   (extra step) contacts to the new line, ~1.1-1.5 s, speed dipping to ~130-170 cm/s at the plant/transfer.
6. Level 3 (measured loss of balance) only when the required dv exceeds the plan + one extra step, or an external push / bad ground: rare,
   deterministic for the same state, never random. Not implemented as content yet (V2.38).

## Verified in game (V2.38 jog 90, fixed 30, same session vs production)
- Planned cut in game: MM enters the matching phase bin on the request frame (clip time 0.03-0.07) and plays it through; the capsule follows
  the plan exactly (actor yaw = commanded yaw every frame, speed within ~10 cm/s): heading 80 % at 0.67-0.83 s (production 0.5), speed dips
  300 -> 115-176 (production 206), peak a after the request frame 0.53-0.57 g (production 0.65 g), worst planted slide 0-5 cm
  (production 6-13). The chest leads the pelvis and the head leads into the turn during the action (head 41-47 deg at 0.2-0.6 s,
  production 12-25).
- Final clean-reopen evidence (fin4, 2026-10-30): slide c90r / rb / l / lb 9.6 / 0 / 0 / 6.0 cm vs V2.37 12.5 / 11.2 / 12.8 / 6.6; peak a
  0.53-0.67 g; favourable phase (outside foot next: P05, P13) = plant first, min speed 162-169; unfavourable (inside foot / too early:
  P20, P21) = brake or weak plant first, min speed 115-176. 120 FPS / real time pass; 60 FPS left cut leaves its clip early (class-0
  re-latch breaks the hold) - open. In-game contact detection double-counts a foot within 0.1-0.2 s: judge support by the plan roles +
  measured speed / heading, not by a raw contact count.
- The SHME push detector is not a balance judge for authored motion: a clip-bound speed restore / re-acceleration reads as an external
  push (PerturbState -> family 6 shove recovery over the planned brake). An authored, physically planned redirect owns its recovery;
  guard the recovery family while it plays (+1.6 s for the push memory). Component-level fix still open (ignore pushes while the clip owns
  the speed).

## A second request during a plan (V2.39, verified)
- Ownership: the running plan owns the database and the capsule contracts while its own clip weight (curve `SHM238_W`) runs - not the
  component's episode class. A class re-latch with NO new input (60 FPS left cut, V2.38) or with one (cc90) used to re-route the database
  mid-brake (JogSteady / V2.16 RevTurn), and a one-frame V2.28 dropout re-latched the yaw contract to the new input (1400 deg/s snap).
- The new intent is latched at once (intent vs the plan target > 35 deg; dropped < 20 deg or on release); the takeover is served from the
  INHERITED state: actual velocity / heading / support foot / loop phase at the next planned touchdown (planned contact clock curve
  `SHM239_Step`, exact - the component heel-strike flags lag ~0.1 s). Back (toward the old travel) vs Opp (the opposite side) is the
  intent's angle in the plan frame; how many supports it costs EMERGES from the inherited velocity (Opp from 180 cm/s at heading 58 =
  brake to ~20 cm/s, plant, pivot; Back = plant, transfer, push).
- Real external effect vs planned velocity change: with the clip-speed contract the plan DEFINES the capsule velocity, so the residual
  |measured - commanded| explains it: planned motion <= 9 cm/s, a 300 cm/s shove 282 cm/s. Above 80 cm/s the plan YIELDS (contracts,
  owner and the recovery guard release; the existing pushRaw recovery acts: families 6 then 3 on the shove frame). Compute it FIRST in the
  frame, or the clip contract erases the shove before anything sees it (it did once). V2.38 production erased real shoves during plans.
- Live read (`SHM239_Bal`, telemetry): need = |dv| / per-contact budget from live velocity and intent - explains the class (Stable /
  Controlled Redirect / Recovery Step / Loss-of-balance candidate); the motion itself comes from the inherited-state plans. Not a controller.

## Takeover reliability, third request, obstacle, head (V2.40, measured)
- The first cause of the 120 FPS takeover slides was the switch itself, not the content: a latch that closes on a BLENDED curve and
  re-forces by frame count re-searches every 2nd frame at 120 FPS (selection hops between sources for 0.35 s). Decide the switch from
  what motion matching ACTUALLY selected (CurrentSelectedDatabase) and retry only by time.
- The entry is a lookup, not a search: the playing source bin (curve), the latched target and the next planned contact name the one
  clip; a per-(source, target) entry database whose windows cover only [t_(K-1), t_K + 0.05] makes the entry frame identical to the
  playing cut at every frame rate (rw 116 -> 7.6 cm, cc90 112 -> 9.6 cm at 120 FPS).
- When a plan ends, its final heading must be HANDED to the body frame (V2.34 LocoYaw / exploration state) in the same frame, or the
  facing writer turns the body back to the old frame and the next stop is lateral (lr 36 -> 7 cm).
- Third request: a running takeover plan does not take over again (no source content); at its momentum low (|v| < 80 cm/s) with an
  intent > 35 deg from its target it YIELDS to the normal start / push routing - the remaining momentum is negligible, the old re-push
  would be a detour (rlw 21.9 -> 5-10 cm, no -90 detour). Above that speed the plan finishes (content/architecture limit).
- Obstacle: a wall during a plan shows as residual (commanded plan speed vs blocked capsule). Production kept writing the plan velocity
  into the wall (residual 298 cm/s) and the cut ran on the spot; on a blocked residual the plan yields and ONE forced stand search ends
  the clip (needs the throttle release). No wall-reaction content exists - the stand blend is the honest limit.
- Head: the vendor aim offset (Delta(ControlRotation, Root)) turns head AND chest / pelvis toward the camera although the player did
  not look - the first layer that diverges from the travel. Manual look owns it (IA_Look pulse clock TW_LastLookTime); while moving and
  not looking it fades (FInterpTo, frame-rate independent) - but only after the plan curve: inside an authored cut the AO's pelvis part
  removed moved a planted foot 3 cm in one frame.

## Anti-dither
- Decide once per contact, at the touchdown, from the latched request; never re-classify every frame (the V1.3.x traction/recovery
  branch produced 35 / 84 cm false steps by re-deciding).
- A plan's contact count may only grow by one per contact (late request), never flip back and forth; release / new opposite request is
  a new action (cancel path), not an oscillation of the same one.
- Never "make it harder" by delaying the input, freezing a pose or slowing the clip clock: the extra effort is an extra contact, a slower
  speed through the plant and a longer re-push, all visible.

## Check list before accepting a redirect
- Same frames, same space: contacts after the event (foot, time, along / side vs the CoM), dv per contact, peak a (mu_eff), heading 80 %
  time, pelvis vs chest yaw separation, head yaw (not locked to the camera), clip / database per frame (`balance238.py <label>`).
- The two support states (outside-next vs inside-next) must look different at normal speed (fixed side + game camera sheets).
- Technical numbers fine but the body looks stiff, waiting or athletic -> not PASS.

## Failed examples (real)
- V2.37 production jog 90: one 0.43 s contact placed on the old line, loop variants, 0.9 g, head stayed on the camera direction
  (AAMS LookAtAimOffset: 12-25 deg while the pelvis had turned 80-85) - "mechanical", "locked".
- V2.10: vendor run turns for jog = 512 cm/s source speed, 26-33 cm pelvis dip - an athletic cut on a relaxed character.
- V2.38 first dry run: the frame-0 stance foot held 0.12 s past its natural lift -> leg overstretch -> 18-22 cm pelvis drop. A foot in
  stance at the request leaves where the loop lifts it.
