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

## Failed examples (real)
- V2.32 idle-stance start copies in the shared start DBs: true-idle back start 38 -> 22 cm but release-repress 35 -> 54 (MM chose the copy).
- V2.32 tick-order change: blips fewer, slides much worse (the system is tuned around the one-frame lag).
- V2.31 loaded family used at every entry: P21 / P30 double-landed the other foot; a "safe fallback" must itself pass control / support / style.
- Worst-slide deltas that were classifier segmentation (c29 48.8 -> 57.6 with <= 4 cm foot change) or MM branch divergence: compare ball
  paths frame by frame before calling a regression; repeat in one session.

## Acceptance test
Per action: same-session interleaved o / candidate, 2 repeats, one broken case + one sound counter-case; then entry phases / cancels; a
stable candidate also at 20 / 30 / 60 / 120 FPS + real time. No regression in input, family selection, large planted slide, pose jump,
camera visibility, normal walk, inspection. Technical PASS is not visual acceptance (user).

## Tools
`Tools/SHME_V232_20261027/` contact / blip / upper / terrain / tables tools, `Tools/SHME_V231_20261026/ltp231.py`, generators in
`Tools/SHME_V22x..V23x`, harness `Tools/SHME_V212_20261017/v212_run.sh` (scenarios), A/B `Tools/SHME_V232_20261027/v232_ab.sh`.

## Rollback
Content: manifest backups (safe-iteration); flags: the candidate stays a flag until promotion; promotion scripts carry `rollback`.
