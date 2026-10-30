---
name: sphirus-motion-synthesis
description: How SPHIRUS produces NEW locomotion animation for physically planned actions (hard-turn brake / plant / transfer / re-push, catch and recovery steps, rested vs effortful variants) - the source -> skeleton -> contact -> root/capsule -> in-game selection -> visible-body order, the procedural footstep generator path that works on the MetaHuman skeleton today, and when (not) to use NVIDIA MotionBricks / Kimodo / ARDY / ProtoMotions or UE Physics Control. Use before generating, importing or evaluating any new locomotion clip family or any AI motion model.
---

# SPHIRUS motion synthesis

Owner of HOW new motion content is made. WHAT the body must do comes from `sphirus-balance-recovery` (plan) and
`sphirus-natural-motion` (procedure); editor safety from `sphirus-safe-unreal-iteration`; DB / MM mechanics from
`sphirus-human-motion-engine/references/mm-coverage.md`.

## Order (never skip a step; each has its own check)
1. **Plan** - contacts (foot, time, place), velocity / heading per frame from the balance plan. Check: contact count, speed dip, peak a.
2. **Source pose** - the loop at the request phase (entry pose = what is in the game), loop swing shapes, the loop's landing rotations.
3. **Skeleton** - MetaHuman/UE skeleton directly (component space: forward +Y, left +X, up +Z; `v137_animedit.py`). Any other skeleton
   (SOMA, SMPL) needs a retarget whose foot contacts are re-verified AFTER retargeting.
4. **Contact** - planted balls pinned in the world (drift <= 2 cm), heel-toe roll capped (50 deg in stance), swing never beyond the leg,
   a swing already in the air follows its own loop path + an offset to the plan.
5. **Root / capsule** - the clip root IS the planned path; in game the capsule must follow it: speed via the V2.28 contract (`SHM226_V/W`),
   heading via the V2.38 contract (`SHM238_Turn/W` -> ABP `SHM238_*` -> component `ClipYaw/On` -> GR SetActorRotation in the clip-speed
   branch). A clip whose root differs from the capsule path slides, whatever the selection.
6. **Selection** - phase bins (24 per loop cycle) in their own database, full-window BranchIn (entry-window trap), continuing bias -25
   (stop-entry bin hopping fix), routed by an existing route (jog lateral: `SHM210_JogCutMode` + `SHM_RedirectDB_JL`); first run after a
   DB edit is a warm run.
7. **Visible body** - pelvis / chest / head yaw, trunk lean, arm damping, pelvis height on the VISIBLE mesh at normal speed, fixed side +
   game camera.

## The working generator path (verified on this project)
- `Tools/SHME_V238_20261030/gen238_cut.py` (jog 90 cut, both sides, 24 bins): balance plan -> loop-clock body -> planned contacts ->
  two-bone leg solve -> pelvis from reach -> whole-body layers (gaze lead, chest lead, pelvis follow, lean from a/g, arm damping by
  braking share) -> curves (`SHM226_V/W`, `SHM238_Turn/W`, `SHM237_FPPelvisOff`, loop curves) -> new assets only (manifest).
- Earlier family generators to reuse: `gen237_start.py` (starts / re-push), `gen237_stop.py` (stops), `gen225_rev.py` / V2.36 reversal.
- Review without the game: stick JSON + `stick238.ps1` (side / front in the travel frame + top view of contacts and facing).

## AI motion models (research 2026-10-30, `Saved/Codex/SHME_V238_20261030/research/research_v238.md`)
| Model | Verdict | Why |
|---|---|---|
| MotionBricks (SOMA weights) | adaptation needed - offline candidate only | commercial weights, Windows, target/context interface fits; but SOMA skeleton + our own SOMA->MetaHuman retarget + exporter; kinematic (no balance), foot skating admitted |
| Kimodo (SOMA-SEED) | adaptation needed | same retarget need; SMPL-X weights are NON-commercial - never use those |
| ARDY | experimental only | Linux-tested, gated Llama-3-8B text encoder, kinematic, no recovery examples |
| ProtoMotions | unnecessary cost (ideas only) | IsaacLab/Linux, multi-A100 training, policies cannot run in UE |
| UE Physics Control / Physical Animation | experimental / unnecessary for the plan | secondary body reaction only; no balance; jitter and owner conflicts |
Rule: an AI clip enters the comparison only after steps 3-5 pass on OUR skeleton; it is promoted only if it beats the procedural clip on
the same contacts / root / visible-body checks at normal speed. No model download or training without a measured need, licence and VRAM check.

## Integration traps (V2.38, real)
- A contract curve pair read as value / weight (`SHM238_Turn / SHM238_W`, like `SHM226_V / W`) must drop TOGETHER: W stepping 1 -> 0
  between two keys with the value held reads up to 2x in the interpolated frame (yaw 90 -> 145 in one frame, 93 cm slide).
- Body layers driven by the plan's acceleration must be smoothed (centred +-0.13 s): the plan's acceleration jumps at each touchdown and
  stepped the trunk lean / arm damping in one frame (head pop 58 m/s2 -> 26 after smoothing).
- The route hold ends on the old alignment rule (velocity within 8 deg of the input) before a slower, physically planned turn is done:
  keep the episode / database hold alive while the clip's own weight says the turn is not finished.
- A reused route switch can leak to other gaits: `SHM210_JogCutMode` also un-skipped WALK lateral episodes (walk 90 slide 0 -> 10.5 cm);
  gate by the episode's START speed (the cut itself dips below jog speed mid-turn) - AND by its class and start only: the first
  speed-only guard also skipped the backpedal -> forward reversal (class 2, 206 cm/s: j35_rev 6 -> 34 cm) and a re-latch inside a
  running sprint cut (e29 6 -> 44 cm). `install238_walk2.py`: class <= 1.5 and not already active. A guard that silences a route must
  be checked on every family that shares the route variable, not only the one it was written for.
- A LookAt alpha switched 0 -> 1 in one frame pops the head (125-141 m/s2); the nodes interpolate the target, not the alpha - ramp it.
- Telemetry booleans arrive as the string 'True' in the LTP rows: count `== 'True'` / `in (True, 'True')`, never `is True`.

## Failed examples (real)
- V2.36 straight start: root accelerated 470 vs capsule 165-245 cm/s2 -> MM played it at 0.7-0.84 (slow motion); the plan must use the
  measured capsule (or bind the capsule to the clip).
- V2.16 cut / reversal clips authored on a different path than the capsule -> 35-96 cm drags until remapped onto the measured path.
- V2.38: re-aiming a foot that lands in 0.12 s by 38 cm made a 18-22 cm pelvis drop; the re-aim share must scale with the time left.
