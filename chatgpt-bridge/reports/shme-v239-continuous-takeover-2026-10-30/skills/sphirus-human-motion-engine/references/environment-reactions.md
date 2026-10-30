# Terrain, balance loss and environment reactions (E)

Use when the ground or the world disturbs the gait: planned step-down / step-up, unexpected drop, slope, slip, bump / wall
brush, impact, landing, recovery. The rule is PROPORTION: small irregularities are absorbed by the legs, never by a stumble.
Physics supports a correct animation; it does not replace it. Owners stay as in architecture.md (CMC moves, FootPlacement / LegIK
correct contact, MM / CP choose poses, SHME plans and grades, PBI adds springs). Sources: research_sources.md M21, M22, E5.

## Data to request first
Live CMC values (MaxStepHeight, WalkableFloorAngle, PerchRadius / ledge settings, braking friction), FootPlacement / LegIK trace
and pelvis settings, SHME landing / perception values (LandingResponse, LandingSupport, severity Soft / Hard), the test geometry
(step heights, slope angles, wall angle, surface), the speed / gait / swing phase at the event, and player-camera video.

## Graded tiers (choose by measured cause, not by "something touched the capsule")
| Tier | Trigger (examples) | Expected body | Owner |
|---|---|---|---|
| 0 absorb | height change ≤ a fraction of MaxStepHeight, gentle slope, wall brush at walk / jog | no clip change; FootPlacement plants on the real surface, pelvis follows smoothly, stride rhythm kept | FootPlacement / LegIK |
| 1 adapt step | planned step-down / up, slope, uneven ground, lateral wall contact | shorter / higher step, knee-controlled descent downhill, hip-driven lift uphill [M21]; speed loss only if the geometry demands it | CMC + FootPlacement + clip choice |
| 2 recovery step | unexpected drop at speed, trip at a swing foot, strong bump | early swing: elevating step; late swing: lowering, quick short step [M22]; visible reaction 60–140 ms after the cause, not on the same frame | SHME foot plan → recovery DB |
| 3 stumble / fall | large unexpected drop, sprint into an obstacle | only with a qualified cause and a full recovery | dedicated clips (none owned, see below) |

## Coverage (2026-10-15, by FILE NAME only — not verified as suitable; classify before use, mm-coverage.md)
- Landing: 39 landing clips in databases (run light / heavy, walk, stand), `am_Jump_LandRecovery`, airborne / fall loops.
- Recovery steps: `/Game/GraceRanger/SHME/Animations/Recovery/` (PSD_SHM_Recovery_L / _R / _v131, SHM_Rec_* / SHM_RecS_* by
  direction and foot) — exist, selection by SHME foot plan; quality not re-verified in V2.8.
- Bumps: standing light bump reacts in 6 directions (`MC_Core_Motion/Animations/ReactBump`, `CoreMotion_Retargeted/AAMS/Walk`,
  `A_CP2_Bump_*`) — standing only; no moving (walk / jog) bump found.
- Idle repositioning steps: `am_Stand_Idle_Step_*` / `am_Ready_Idle_Step_*` (fwd / bwd / left / right).
- Not found by name: moving stumble / trip, slip, planned step-down / step-up while walking, slope-specific loops, wall brush.
  These are "no clip" candidates until a content search proves otherwise; brief or author them (contact-authoring.md).

## Rules
1. Never trigger tier 2–3 from contact alone; require a measured cause (vertical drop vs MaxStepHeight, capture-point error,
   traction excess, impact speed) and a speed / gait gate. Walk / jog wall contact = tier 0–1.
2. Planned vs unexpected: a visible step-down the player walks into is tier 1 (adapt), the same drop hidden in grass is tier 2.
3. Grade by speed: the same step at sprint is a bigger event than at walk; keep the family but not necessarily the speed.
4. Slope Warping is still in development in UE 5.8 [E5]: slopes stay with FootPlacement / IK and pelvis settings.

## Acceptance test (per tier, same as F: player camera + slowed review + fixed side view)
A step-height ladder (e.g. 2 / 5 / 10 / 20 / 30 cm, read MaxStepHeight first), slope set (5 / 10 / 15 / 20°), wall approach at
0 / 30 / 60° at walk / jog / sprint, an unexpected drop at walk and jog; both directions; measure planted-foot slip in the true
contact window, pelvis drop, speed loss, time to steady gait, and false positives (reactions on flat ground = FAIL).
V2.8 status: NOT_TESTED (no environment scenario was run in this task; coverage above is a file listing).

## V2.21 whole-body terrain answer (2026-10-21, SHME `SHM_UpdateBodyTargets`, production)
- Measured first: on an 8 deg hill the V2.20 trunk pitch was IDENTICAL on flat / uphill / downhill (14.0-14.2 deg walk, 22.1-22.7 jog):
  FootPlacement / LegIK moved the feet and pelvis height only. That is the "feet-only on terrain" defect.
- Source = the real collision (3 Visibility line traces, no tags / actor names): under the capsule, ahead along the TRAVEL (AheadTime
  0.45 s x speed, 35-140 cm; facing when slow) and 30 cm to the right. Feed filtered slope / cross slope into the existing body
  springs (LeanFwdTarget / LeanLatTarget / PelvisOffsetTarget) - no new layer, no second pelvis adaptation.
- Sizes that read without exaggeration (trunk pitch vs base): hill 8 deg walk +4.1 / -2.9, jog +3.2 / -2.2; real map +2.4..2.7 up;
  cross slope 10 deg: +2.3 deg toward the UPHILL side. The lean chain amplifies ~3.4x (LeanFwd deg -> trunk deg): start gains low.
- Gate the slope lean by travel speed (20 -> 80 cm/s): standing on split heights the ahead probe otherwise tilts the trunk.
- Step-down: a ground drop > 4 cm under the capsule in one frame = absorb dip (half when the drop was already seen ahead = planned).
- Verify on: ter_hill8 / hill15 / bump / dip / roots / drop / xslope / split courses (v212_run.sh, mvb + boxes), pilot route, real map
  lines map_r1..3 (probe_route.py). Tools terseg221.py (segment trunk pitch + slope signal), terrain221.py. Frame-rate check: identical
  at 20 / 30 / 60 / 120 FPS fixed step.
- Still open: no stepping change (shorter / higher steps uphill, controlled lowering step downhill, side-slope stance) - that needs
  clip content or a stride / step-height owner; no fall / jump hand-over change.

## V2.23 measured stepping gap (2026-10-22, fixed 30, win223.py = contact221 per foot)
- ter_bump_jog: right swing foot within 4 cm of the ground and > 60 cm/s for 580 cm of travel (skim) - the swing does not clear the
  bump; ter_bump_walk worst contact slip R 28.5 cm; ter_drop_walk L 32.5 cm; xslope walk L skim 225 cm. FootPlacement plants the
  stance foot; nothing owns swing clearance over a rise or a lowering step -> stepping (not trunk lean) is still open: needs a swing
  owner (ground probe ahead of the swing foot -> ik_foot lift) or clip content; not built in V2.23.

## V2.24 swing-foot clearance (2026-10-23, PARTIAL; SHME SwingLiftEnabled, FeetIK ik_foot lift before LegIK)
```
Owner split: FootPlacement plants the stance foot, the SHME component lifts only the SWING foot's IK target (SwingLiftL/R ->
  ABP SHM224_LiftL/R -> FeetIK 'Transform (Modify) Bone' ik_foot_l/r additive Z, inserted after FootPlacement, before the PBI pelvis and
  LegIK). Per swing foot: ground probe ahead (SwingLiftAhead x Speed), deficit = ground + margin - foot centre, only where the ground AHEAD
  RISES over the support plane FootZ (+1..+3 cm ramp), fast release in contact (0.03 s).
Lessons: FootCenter (foot/ball midpoint) is ~6.5 cm above the sole - a 4 cm margin never lifted; a sole-referenced margin without the
  rise gate lifted the swing feet on flat ground in half the walk frames (= a lift layer everywhere, rejected); a rise gate measured from
  baseZ (capsule centre - 86) opened too late (bump benefit lost). Final (FootZ gate): walk bump right plant slip 28.5 -> 3.7, drop left
  35 -> 14, jog drop clearance 0.9 -> 6.8 cm, flat ground untouched; left foot still catches the bump top 12 frames (open).
```

## V2.25 swing-lift gate + planted-foot guard (2026-10-24, production)

```
T1 gate: rise = MAX ground along the swing path (0.5 / 1.0 / 1.5 x ahead) - ground UNDER THE FOOT (per-foot trace), not the capsule plane.
T1b guard: lift only in a CONFIRMED swing - SwingAirTL/R (time out of contact) > 0.10 s; any contact frame resets it.
Why the guard: T1 alone lifted the PLANTED foot 2-10 cm on alternate frames before a bump (lift -> ContactL false + foot-speed spike ->
  'swing' -> more lift -> contact -> fast release -> repeat). Check planted-foot z second difference (V2.24 8.8, T1 12.6, T1b 6.2 cm).
Walk bump V2.24 -> V2.25: B1 right skim 51 -> 18 cm; B2 left swing min 0.9 -> 2.5 cm, skim 84 -> 35, plant slip 26 -> 7. Flat: lift 0.
Measurement fix: ter225 'catch' counted planted frames 1-2 cm under the trace on FLAT ground; now relative to the foot's own floor
  calibration (catch = h - floor < -1.5). The V2.24 'left foot catches the bump top 12 frames' was this artefact (0 after the fix).
Rejected: planned step preparation on the pelvis (StepPrep T2/T2b/T2c). V2.24 FootPlacement already moves the pelvis continuously on
  steps (89 -> 120 over ~0.9 s at a 28 cm step); the extra offset double-corrected (pelvis 90 -> 82 dip before rising).
Open: high step-up (22 / 28 cm) - the step foot lands inside the platform (6-18 frames) and then pops.
```

## V2.26 high step: lift target half-convergence + landing shift (2026-10-24; T3a-T3g `v226_patch_terrain5..10.py`, `step226.py`)
```
Root cause (since V2.24): the swing-lift target was computed from the ALREADY LIFTED foot (FootCenter includes the previous frame's lift),
  so the lift converged to half the deficit (28 cm step: 17 of 34 needed; bumps too). T3g: deficit from the un-lifted pose foot
  (fzL = FootCenter.z - SwingLiftL). Then the 28 cm step foot lands on top (z 31.8) instead of 18 cm inside the platform.
T3a gate: platform above the SUPPORT ground only (gL - guL vs guL - g0). T3d/T3e: a foot inside the platform is lifted out (no fast
  release), capped StepPenLiftMax 36. SwingLiftMargin 6 (was 10.5) with the full-deficit lift.
Landing shift (candidate StepEdgeOn): landing estimate = stance foot + Speed x StepEdgeStepTime, edge probes +-StepEdgeProbe; near an
  edge the ik_foot target is shifted StepEdgeShift(Far) along the travel (world-space ModifyBone SHM226_ShiftL/R, `install_v226_shift.py`),
  held while planted / over the platform. 28 cm step: plant 10 -> 22-23 cm onto the step; 20 cm step 7 -> 19 cm. Must stay silent on
  rolling ground (StepEdgeMin 10 cm): check SwingShiftTL/R on map_r1-r3 before promoting.
Jog 28 cm step (te6): the first foot hovers over the edge, dips 13 cm into the step for 0.1 s and never plants (the right foot lands
  112 cm in) - open. Capsule pre-rise is NOT a fix (hides the foot).
Regressions to read with every terrain candidate: bump walk lift (18-21 -> 14-15 ok), flat lift 0, map_r2 slip p90/max/pops.
```
