---
name: sphirus-natural-motion
description: Procedure for making a SPHIRUS locomotion action read as one continuous human body - intent -> current speed/support -> motion plan -> source animation -> integration -> final visible-body check - for starts, stops, brakes, reversals, direction changes, catch / settle steps, re-push, release-repress, sprint attitude and terrain steps. Use before generating, re-authoring, routing or tuning any locomotion clip, database or runtime correction.
---

# SPHIRUS natural motion

Order of work for one *completed action* (not one clip). Engine contract / flags / equations: `sphirus-human-motion-engine`; feel target
and final acceptance: `sphirus-character-camera`; editor safety: `sphirus-safe-unreal-iteration` (manifest before any write).

## Target identity
A normal person with physical limits: measured effort, relaxed arms, controlled head, readable support and weight transfer. Not:
athletic / arcade bursts, big wind-ups, head / arm flailing, rubbery blends, slow motion, a capsule sliding under the feet, random stumbles.

## Procedure (mandatory order)
1. **Intent** - what the player asked (direction, gait, timing, cancel / re-press), from the input, not from the clip name.
2. **Current body** - real speed and acceleration, facing vs travel direction, support foot and contact / swing phase, pelvis and trunk
   motion, effort state. Read it from the run (LTP / cvars), never assume it. Three different bodies never share one entry:
   truly stopped (both feet planted, speed ~0, no brake left), braking (planted brake foot, decelerating), moving slowly.
3. **Plan** - write the action contract before content: entry speed range, facing / travel, support foot, phase window, pelvis / trunk
   motion, expected exit support, safe cancel point. One representative action first (one foot, one direction); widen to other feet /
   directions / speeds only after it is natural and reliable. Never multiply a failing choreography into 32 / 64 variants.
4. **Source** - is the source pose AND its continuing motion right? Same-looking poses can continue differently: match bone poses AND
   velocities / directions. Source wrong -> new content (generator, dry run first); runtime wrong -> fix the runtime owner.
5. **Integration** - route by the plan's entry conditions (support, phase, real motion; idle time alone never decides), own database or
   gate so other entries cannot pick it (a copy in a shared start DB is chosen by every matching pose - V2.32 IS copies), check notify /
   motion authority (BranchIn, Exclude, BlockTransition, root motion), inertialization / blend profile, cancel / re-entry from the current body.
6. **Final visible body** - measure on the final mesh: planted-ball slide / drag (contact231), one-frame selection blips (blip232), pose
   jumps, support continuity at entry and exit, trunk / head / arm envelope (upper232), terrain (terrain232); then normal-speed full-body and
   game-camera video. Hiding a slide (lifting the foot a few cm out of the classifier band, slowing the clip, freezing arms) is a failure.

## Rules from user review (V2.35, verified)
- **Weight feel is not an unexplained pose hold.** A body that waits in one pose while the request already changed is a defect until
  the first broken frame names its class: A clock held (clip rate ~0 / re-selection), B clip advances in one pose region (content),
  C family cannot switch (priority / minimum hold), D clip right but the final body stiff (blends, plant locks), E no linking motion at
  all. Show input, speed, support, family, clip + time + rate, root / pelvis and the visible body on the SAME frames (`diag235.py`).
- **A soft stop is not a lower brake coefficient.** Measure capsule decel, last plant, closing step, pelvis / trunk settle and idle entry
  separately; a correction step after the stop or a trunk that straightens in 0.15 s at the entry are content defects.
- **The female character's manner is not hip sway or one trunk angle.** Style = the same person in idle, start, loops, brake, stop:
  build transitions FROM the project loops (same arm carriage, lean, cadence); a vendor clip with another posture breaks the person.
- **A new natural motion is not a trigger list or a renamed clip.** It counts when new support / timing exists in the content and it
  is played in the final chain.
- **A designed slide is not a hidden drag.** A designed brake slide has start, direction, distance and end planned; it stays in the
  contact test as its own event. Anything else that moves a planted foot is a defect.
- **A candidate that does not work in final production is not a delivered feature.**
- Plan planted contacts on the part FootPlacement plants (the ball): an ankle target with the toes still up lands the ball short and
  the plant locks it there (stop r5 -> r6).
- A horizontal re-target must be complete before the foot gets low; measure the offset at the frame it gets low, never at the landing.

## Rules from user review (V2.36, verified)
- **A stop is one action per support phase at the release, not one clip.** A single stop clip entered at whatever time the search finds
  forces every phase into one choreography (the step that is redundant for one entry is the closing step of another). Build a family of
  release-phase bins (frame 0 = the loop pose at that phase, root = the MEASURED capsule stop), each planned from its own support:
  brake foot = the first foot that lands after the release. Two bins were not enough: the search re-entered the other bin's frame 0 one
  frame after entry (46 cm); 24 bins over the loop + continuing bias -3 held.
- **The brake foot lands at the loop's own landing reach** (A_CT_Jog_Fwd: 31-39 cm ahead of the root), never at the final spot (the
  vendor stop: 55-63 cm = the 'over-reaching' foot); when the remaining capsule distance is long, add a short step (step length cap)
  instead of a lunge; a trailing planted foot rolls onto its ball (heel up, ball pinned) before the pelvis is lowered.
- **The body rises as it slows.** Holding the jog pelvis height until the last landing read as a crouch (8-11 cm in game); rising with
  the deceleration (reach-limited) keeps the brake absorption without the squat.
- **The final stance of a stop decides the next start's DATABASE, not only its clip.** The start route searches the database of the
  UNLOADED foot; PSD_SHM_JogStartS_L (left foot first) had no straight jog start -> every straight request from a left-unloaded stance
  played TurnL045 (65-92 cm drag). Check that each side's database covers the straight case before tuning starts; the fix was content
  (SHM236_JogStart_F_L/R, stance -> jog loop, lean before the first step, arms rise into carriage with a growing swing).
- **Whole-body brake in a short action is easy to make invisible.** The V2.36 reversal arm change first moved the visible hand 3 cm (a
  0.4 s window, 40 % amplitude): compare the visible hand / trunk path of the old and new version on the SAME frames (vx_ / mx_) before
  calling the upper body changed.

## Rules from user review (V2.37, verified)
- **A start's root is the measured capsule, not a design acceleration.** The V2.36 straight start used 470 cm/s2 while the in-game jog
  start is 165 -> 245 cm/s2: MM played it at rate 0.70-0.84 (a slow-motion start). gen237_start.py plans the root from the measured
  capsule and every landing from the current speed (step 30 -> 65 -> 105 cm, the last landing IS a loop landing): rate 1.0.
- **A loaded foot never takes a swing pose.** The V2.36 stance foot was slerped toward the loop's AIRBORNE toe-off rotation with its ball
  pinned: pitch 39 -> 122 deg (folded over the toes) from 0.23 s, 16-17 cm slide in game. Cap the TOTAL pitch over flat (50 deg in the
  stance; the loop's own toe-off only in the last 0.16 s of push), lift by reach AND by the step clock's loop lift, fade offsets only in a swing.
- **A clip must exist in every database that can search it during its action.** The start family ends at StartTransferMaxTime (0.65 s),
  then the CP start route database searches; a start missing there was cut mid-step (vendor CP2 start @0.87). Put the start in both.
- **A re-press inside a stop continues from the stop pose, not from a start-from-rest.** Re-push links (frame 0 = the stop clip at the
  re-press time, its planted foot kept, the airborne foot lands with its own velocity, root from the stop's speed with the measured
  acceleration) in the CP route database: j36_rsm 19-38 -> 0-9 cm. A stop pose's trailing foot is already heel-up (55 deg): the cap is on
  the total pitch, and a foot planted before frame 0 gets no fresh stance minimum (else a 12-15 cm pelvis drop at frame 0).
- **Find both pelvis owners before moving the pelvis.** ac_SHM_HCi_pelvis_TZ (before FootPlacement) / ac_SHM_HCo_pelvis_TZ (after LegIK)
  give the FootPlacement pelvis change per frame: the V2.36 stop clip raised the pelvis to 94 cm (near-straight brake leg) and
  FootPlacement (AllLegs, spring) lowered it 6-9 cm -> the bent-knee crouch. The clip owns it now (curve SHM237_FPPelvisOff, ABP
  DisablePelvisCurveName): brake pelvis 84.5 -> 89.8 cm, knee 117 -> 144 deg. Lowering the source instead (5 cm knee margin) gave an
  80 cm source crouch - rejected before any run.
- **The release frame carries the loop's pelvis bob.** 'Lowest pelvis after the release' counts the jog loop's own low point; judge the
  brake on the window release +0.15 .. +0.8 s (tables237 brake pelvis + knee + FootPlacement share).
- **Judge the knee of the SUPPORT leg.** The minimum knee over both legs at the brake reads the swing knee (~87 deg, ball 13-21 cm up) as
  a squat; tables237 takes the leg with the lower ball (final stop: 142 deg).
- **A phase-binned entry must stick to its first bin.** The V2.37 stop re-picked a new bin at clip time 0 on consecutive searches in the
  first ~0.08 s (worse at 60/120 FPS: 15-20 cm). Stop database continuing bias -3 -> -25 held the first bin (120 FPS j36_stop 19.8 -> 5.0,
  rsm 19.8 -> 5.0; 30 FPS rse 14 -> 0) without changing content.

## Failed examples (real)
- V2.37 stop audit 'back' 12.8 cm (both the V2.36 and the V2.37 stop): the closing foot was still swinging FORWARD when the capsule
  stopped; the metric takes the first 3 samples' maximum as reference - read the ball path before calling a pull-back.
- V2.37 adding clips to a copied database changes its normalization: vendor clips are matched slightly differently even when no new clip
  plays (e29_chain SHM218_W2S entered at 0.88 instead of 0.84, 6.4 -> 11.1 cm) - compare owners frame by frame.
- V2.36 stop family ending in the idle frame (V2.8 walk-stop target): the stance read as left-unloaded -> left start database -> TurnL045
  for straight restarts (85 cm). Ending in the stance the paired straight start begins from (vendor stop end) fixed the side; the left
  straight start fixed the remaining cases.
- V2.36 re-press in the middle of a jog stop: adding the jog loop to the start-route database (resume) changed nothing (19 cm, the
  vendor start was still chosen mid-stride) - the owner is the start-from-rest route at 100 cm/s, not the database membership.
- V2.35 reversal freeze: SHM226_JogRev_F_B ran at clip rate 1.0 with BOTH feet planted 0.64 s (arms in jog carriage) - class E/B:
  the generator planned the first step of the new travel 0.40 s after the zero crossing on a capsule table that lingered < 40 cm/s.
  gen235_rev (push through zero, catch step at the zero crossing) removed the hold; tuning blend times would not have.
- V2.35 the new reversal content raised release-repress slides (13 -> 39-46 cm at 30 FPS): in the release gap the episode ended, the
  search left the clip that was already reversing and re-entered a full-speed bin's frame 0; the re-press blended two clip speed curves.
  New content changes which runtime rules are safe - rerun the whole chain set, not only the representative.
- V2.35 stop re-plan r2-r5: each fixed one symptom and moved the slide (hovering re-target, 50 cm jump at f_low, ankle-vs-ball landing,
  4.6 cm short stance -> the next start chose a turning start, 92 cm). The final stance of a stop decides the NEXT start's family.
- V2.33 "sprint calm candidate changed the arms 58 -> 56 only": a metric mismatch (hand vs shoulder incl. turns). Same metric, same window,
  same space at two observation points (stage234: MM mesh mx_ vs visible vx_) gave upper-arm swing 95 -> 76 deg at BOTH - the source change
  did arrive. Compare stages only with one metric / time window / reference space.
- V2.33 stand-back 38 -> 0 cm in the START clip while j30_slow stayed 22-28 cm (forward stop) and release-repress 51 cm: a zero at one
  start is not a zero in the chain - report the whole chain.
- V2.34 forward stop closing drag (22 cm in every chain) was in the SOURCE clip: the trailing toe slides 40-70 cm at <= 3 cm. A clearance
  rule on the ankle ('own lift' 5 cm) changed nothing; only the TOE clearance over the middle of the closing step (gen234_stopclear
  ball_mid, closing step only - strides untouched) gave 22 -> 12. Measure the part of the foot that actually drags.
- V2.34 release-repress: the component kept the reversal family but the ABP default chooser still searched the stand stop / start DBs ->
  find the stage that actually picks the database (Update_MotionMatching entry) before changing a family rule.
- V2.32 idle-stance start copies in the shared start DBs: true-idle back start 38 -> 22 cm but release-repress 35 -> 54 (MM chose the copy).
- V2.32 tick-order change: blips fewer, slides much worse (the system is tuned around the one-frame lag).
- V2.31 loaded family used at every entry: P21 / P30 double-landed the other foot; a "safe fallback" must itself pass control / support / style.
- Worst-slide deltas that were classifier segmentation (c29 48.8 -> 57.6 with <= 4 cm foot change) or MM branch divergence: compare ball
  paths frame by frame before calling a regression; repeat in one session.

## Acceptance test
Every target keeps an acceptance record: requested behaviour -> real change -> final production run -> visual / technical evidence ->
remaining blocker. A new natural motion counts only when it is PLAYED in the final production chain (routing hit, not a listed asset).
Same-session A/B decides a diagnosis; clean-reopen reliability is part of acceptance; "different selection between sessions" is not a
reason to ignore a regression. Node counts, compile and ALL_OK are build checks, never natural-performance acceptance.
Per action: same-session interleaved o / candidate, 2 repeats, one broken case + one sound counter-case; then entry phases / cancels; a
stable candidate also at 20 / 30 / 60 / 120 FPS + real time. No regression in input, family selection, large planted slide, pose jump,
camera visibility, normal walk, inspection. Technical PASS is not visual acceptance (user).

## Tools
`Tools/SHME_V232_20261027/` contact / blip / upper / terrain / tables tools, `Tools/SHME_V231_20261026/ltp231.py`, generators in
`Tools/SHME_V22x..V23x`, harness `Tools/SHME_V212_20261017/v212_run.sh` (scenarios), A/B `Tools/SHME_V232_20261027/v232_ab.sh`.

## Rollback
Content: manifest backups (safe-iteration); flags: the candidate stays a flag until promotion; promotion scripts carry `rollback`.
