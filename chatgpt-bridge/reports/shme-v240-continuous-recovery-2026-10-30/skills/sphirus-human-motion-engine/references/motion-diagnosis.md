# Motion defect diagnosis (A) — separating clip, selection, entry time, support foot, retarget, capsule, IK, additive and physics

Use when a locomotion symptom (slide, pop, dip, "big" start/stop, wrong animation family, lean, lag) must be attributed to an
owner before anything is changed. Owner/acceptance rules stay in `sphirus-character-camera`; tools live in `../scripts/`.

## Data to request / produce before any hypothesis
- The live chain for the exact moment: input → CMC velocity/accel → MM database + clip + time (`mmdb`, `mmanim`, `mmt` =
  `Phase27_SelectedObject/Time`) → CP evaluator ownership + clock (`CP_StartOwned/EvalTime`, `CP_StopOwned/EvalTime`, `LS_StopRight`)
  → warping / FootPlacement → PBI / SHME additive → driver mesh (`mx_*` bones) → runtime retarget → visible body (`vb_*` / `vx_*`).
  Harness: `avars`, `mbones`, `vbones` (Tools/SHME_V1_20260925/qa_pie.py).
- The same moment measured on BOTH meshes (`contactslip.py --mesh=vb` and `--mesh=mx`): equal = upstream of the retarget.
- Repeated runs (>= 2) and the phase/side at the event (support foot, its offset from the capsule).

## Symptom → candidate owners → falsifying test
| Symptom | Candidate owners | Test that can REJECT the hypothesis |
|---|---|---|
| Planted foot slides at a start/stop | (a) evaluator entry pose ≠ current pose (wrong entry TIME), (b) wrong clip SIDE, (c) clip root speed ≠ capsule speed, (d) FootPlacement lock off, (e) retarget | (a) slip only in the first 0.2–0.6 s after CP ownership + varies with release phase (`stopentry.py`, stop-phase scenario); (b) correlate side vs planted foot; (c) compare clip root distance vs capsule distance over the window; (d) `Disable_FootLock` curve / plant settings; (e) mx vs vb equal → not retarget |
| Slide in steady loop | clip content vs stride/orientation warping vs play rate | toggle warping cvars per run; mx vs vb; contact phase (landing / mid / toe-off) of the slide |
| "Big" start / stop, deep dip | clip content vs SHME BrakePosture vs PBI vs FootPlacement pelvis | layer-off variants one at a time (nbrk / npbi / nbody / nfp); if every layer changes < 2 cm the owner is the clip (measure the clip itself: `probe_pz`-style pelvis/knee curve) |
| Deep brake crouch at S from sprint / jog (squat in place) | brake pivot clip vs BrakePosture / PBI | `pivdrop.py` (pelvis drop from the pre-S median) with nbrk / npbi / nfp; 2026-10-17: clip ~15 cm, BrakePosture 2.3, PBI 2.2, FootPlacement 0. Vendor pivot brakes ~2350 cm/s2 vs capsule ~780: MM plays the clip's run phase while the capsule slows and the clip's wide-stance crouch lands at ~0 speed |
| Old cut push continues after a reverse / S key (capsule turns, animation still pushes the old way) | component episode end vs ABP hold / CutTail vs MM search | `dirchange213.py --tl` on one timeline (cv_RedirectEnd / RedirectTime / class, av_SHM_RedirectFrames / HoldDB, MM clip time): 2026-10-17 the component reported RedirectEnd 3 but did not end; the ABP hold is a consequence, the owner is the component (patched at the ABP: velocity-angle re-class) |
| Wrong animation family in turns | gait state vs database route conditions vs chooser | log shown `Gait` vs input gait vs `mmdb` per frame (`turngait.py`); read the route literals (speed / direction windows) in `Update_MotionMatching` |
| Pop at a transition | blend vs clip time jump vs DB switch | per-frame clip time (`mmt`, CP clock) around the peak; a time jump with v→0 is a clock owner (HALT pass) |
| Lean / sway | PBI vs SHME LeanLat vs clip roll | stride-averaged lean with each layer off (`turn_lean.py`) |

Rules
1. One hypothesis, one decisive test, one variable per run; interleave base and variant in one editor process.
2. Never trust a metric before reproducing its raw frames once (print positions/heights per frame for one event).
3. Telemetry names can mislead: `mmanim` is the MM selection UNDER a CP evaluator; a speed-gated skate metric splits a fast
   slide into "plants" and hides it. Validate the measurement, then the hypothesis.
4. A layer whose removal changes the symptom by less than the run-to-run noise is not the owner — say so and move on.

## Failure examples from this project (verified)
- V2.6/2.7 claimed "stop size" fixes from posture metrics while the real defect was the stop ENTRY: the CP relaxed stop always
  enters at ~1.3 s (fixed predicted distance) → planted foot slid 10–37 cm in every walk stop (V2.8 `stopentry.py`).
- `skate_report.py` (speed < 45 cm/s plants) reported taps max 15.9 cm; the height-only contact metric found 21–26 cm slides.
- Pelvis "dip" bake raised the pelvis but leg reach clamped it: a long final step is a FOOTSTEP problem, not a posture problem.
- Wrong clock overridden (V2.8 first start test): `CP_StartEvalTime` looked like the start clock, but the AnimGraph evaluator's
  ExplicitTime pin is `SelectFloat(CP_TC_StartPoseTime, …, TC)`; the new clip ran at ~0.75x with an entry jump and the stance foot
  slid 27 cm. Trace the evaluator PIN source in the AnimGraph (`probe_seqeval.py` / `probe_starttime.py` in Tools/SHME_V28_20261015)
  before overriding a variable; log every clock the pin can read.
- Handoff before the clip meets the loop: the CP start released at the old plant distance (~51 cm, 0.8 s) while the new clip
  only matches the walk loop at its end (1.5 s) → MM picked a crossing pose and slid the stance foot 20 cm sideways. The owner of
  a transition's END must be checked together with its clip.

- Three rejected hypotheses on one 4–7 cm stop-entry slide (V2.8, each with one decisive run): FootPlacement (off → unchanged),
  phase quantisation (24 bins → unchanged), MM database switch (no jump once the clip root was smooth). The owner was the clip's
  root curve + entry time; found by logging the selector's own inputs (`SHM28_BL/BR`, bin, T0) next to the true foot positions.

- V2.10 half-played sprint cut: the bridge database WAS selected, so "clip not used" was wrong. The owner was the ENTRY TIME and the
  episode END: Motion Matching entered the vendor sprint-turn clip at 0.90 s (mid-turn; brake 0.63 s, turn 10/50/90 % at 0.67 / 0.90 /
  1.5 s) and re-entered the other foot variant at 0.90 s, because the clip runs at 716 cm/s vs the project's 490 -> 307 (its slowest
  frames match the trajectory best) and the capsule FACING turned 63 deg in 0.3 s while the velocity needed 0.72 s. Found by logging the
  selection (avars Phase27_SelectedObject / Phase27_SelectedTime) on the capsule timeline (`Tools/SHME_V210_20261016/cut_timeline.py`)
  next to the clip's own phase table (`cutclip_table.py`). A facing bound alone did not move the entry; the decisive fix was the clip's
  "Pose Search: Block Transition In" window (see mm-coverage.md).
- V2.10 spawn-idle knock-knee (hinge 0.47, knee 68 deg inside the toes): FootPlacement horizontal rebalancing, MaxExtensionRatio, heel
  lift and LegIK knee-twist correction were each REJECTED with one run (identical values). Owner = the idle CLIP: a near-straight leg
  (2 deg) whose 0.5-1 cm knee offset points inward; IK that bends the leg keeps that direction. Compare runtime kt / hinge with the
  clip's own values at the clip time actually playing (`probe_idleleg.py`).
- V2.10 "knee snaps" while walking: per-frame calf-axis jumps of 52-77 deg (driver and visible mesh) = a roll flip of the near-straight
  leg baked into the walk loop by the V1.3.7 solver. The hinge metric (flexion >= 8 deg only) cannot see it; use the hinge-AXIS frame
  jump (`calfjump.py`, `v137_animedit.leg_metrics`).
- Do not read a phase MAXIMUM as a state: "both knees 62 / 57 deg on a 10 cm step" (V2.9 table) were maxima over the stop -> idle
  transition; the settled idle has the low leg at its flat flexion and only the raised leg bent (`strip_idle.py`, last 1 s median).

- V2.11 "arms close at walk start, stay, then correct": owners = (1) the CP start clip CONTENT (A_LS_M_Relaxed_Walk_Start_F_R/Lfoot carry the
  upper arms 3-7 deg narrower than the relaxed idle for the whole start - they already held the V2.5/2.6 constant +9 deg, which is why
  that bake "did not work") and (2) the walk LOOP's narrow-arm outlier cycles exactly where the CP start hands off (MM continues at
  3.13-3.17 / 6.567). Runtime == clip at the same clip time (driver == visible), so retarget / post-process / IdleUpperW are not owners.
  Measure the carriage swing-insensitively (elbow lateral + abduction medians: idle / start / loop, `arms.py --carriage`); hand lateral
  is dominated by swing. Lateral axes must be the chest's (record `vaz_/maz_spine_03`): actor-yaw lateral is meaningless while the root
  turns away from the body (in-place turns gave 6 cm "elbows").
- V2.11 in-place turn "action pose, arms out": owner = the SHM_M_Neutral_Stand_Turn_* clips (AAMS Neutral copies, rest abduction 17-18,
  up to 28 deg / hands 41-51 cm), played as DefaultSlot montages by BP_GR_Player.GR_UpdateIdleTurn - not the MM selection underneath.
- V2.11 walk -> sprint "jog-loop wait": the shown gait is speed-staged; Update_MotionMatching's jog route owns 230..400 cm/s while
  accelerating and the sprint route plays the sprint LOOP from 230 cm/s (log Phase27_SelectedObject + av_Gait on the speed ramp, `gaitl.py`).

- V2.12 "the arm fix did nothing at runtime": PSD_LB_WalkLoops / PSD_SHM_TurnInPlace held a SECOND entry of the same clip - the
  pristine bake source copied into /Rollbacks/ kept its PoseSearchBranchIn notify and the database's external-dependency sync added it.
  Legs identical + no arm channel in PSS_Default -> MM tie-picks either copy (v212a played the V2.11 cycle, v212b the pristine one).
  The runtime log shows only the short asset name; list database entries with full paths (`req/probe_dbassets2.py`) and compare the
  compressed pose with raw (`req/probe_compressed.py`) before suspecting the DDC.
- V2.12 walk-start arm "inside" after the start = the walk loop's RIGHT arm dipping to 4-9 deg twice per stride in EVERY cycle (left >= 9)
  and both CP starts handing off into exactly those phases; measure per loop cycle x phase (`loop_arms212.py`, `arms212.py --cycles`),
  never one cycle. The V2.11 "0.59 s" restart residual was a 22 fps capture run against a 30 fps before: compare at the same frame rate.
- V2.12 backward with real keys: IA_Move accumulates TAKE_HIGHEST_ABSOLUTE_VALUE per axis, so W+S held = S (no zero-input gap); S pressed
  at full sprint loses ~73 cm/s in the first frame (2400-2700 cm/s2) then 730-790 cm/s2 - NOT the redirect friction lag
  (RedirectInputNow A/B no change) and NOT TurnSpeedLoss (0 -> no change); owner still open. Shift+W -> D -> S: the component's lateral
  episode keeps the sprint-cut database 0.44 s after the backpedal request (class latched in its first 0.3 s) and MM jumps to the other
  cut clip mid-episode (pelvis 4.4 cm / 79 m/s2).
- V2.12 push "sped-up walk / second start": the V2.11 push route did not cover the WALK database (0.2-0.25 s walk loop at 150-230 cm/s),
  fired without Shift on walk / jog starts (jog start -> RR_Start at 0.07 s with a 45 cm foot slide) and re-fired 0.09 s after a
  post-reversal push ended. Evaluate with `push212.py` (episodes, overspeed walk, database switch contact / slip, trunk pitch rate).

## Evidence to produce
Per hypothesis: the falsifying test, its result (kept / rejected), run labels, the per-frame trace of one representative event,
and the owner named by node/function. Acceptance belongs to `sphirus-character-camera` (player camera, visual review).

## V2.26 authored-clip chain: where the designed foot breaks (2026-10-24, Saved/Codex/SHME_V226_20261024/, tools Tools/SHME_V226_20261024/)
Measure in the WORLD frame, never "clip x vs world x": the clip's component space has forward = +y and lateral = -x (mesh yawed -90); the
root track of the authored clips is 0 (capsule frame), so designed_world_foot(t) = capsule_at_entry + D_table(ct) - D_table(ct_entry) +
clip_ball_y(ct) with ct = av_Phase27_SelectedTime (`req/capterm.py`; clip tables `clipfoot226.py` -> clipfoot226.json). Split the error into
the capsule-clock term (game capsule - designed capsule) and the pose term (visible ball in the capsule frame - clip ball), then remove
stages with cvars (a.AnimNode.FootPlacement / LegIK / StrideWarping / OrientationWarping.Enable 0) in the SAME scenario.
Verified owners (jog reversal F_B / B_F, fixed 30 FPS, v226t9):
- entry (MM time pick + 32 phase bins): planted-foot continuity at entry 2 cm, swing foot 15-20 cm (in the air, blends out in 0.25 s);
- capsule table (`capsule_rev_table.json`, measured): <= 5 cm over 0.9 s - the generator's table did apply;
- FootPlacement OFF: pose term <= 4 cm after the entry blend = the designed foot is realised; FootPlacement ON: the pinned brake foot is
  driven 23 cm backward and returned within 0.4 s (cv_ContactR false meanwhile). Clip curves do not change it: footspeed_l/r kinematic
  (t6), swing floor clamp (t9), Disable_FootLock = 1 (t11) all leave the slip table within 1 cm -> FP's effect is not its lock;
- exit: the component ends the redirect episode at ~0.75 s (SHM_RedirectActive false) -> the ABP leaves the reversal database -> MM
  picks A_RB_Jog_Rear at another foot phase (28 cm foot jump in 0.1 s) while the 1.97 s clip is at ct ~1.0. A DB continuing-pose bias
  (-0.05 -> -0.4, t12) does not keep the clip (the DB switch is upstream) and makes MM skip the reversal entirely in one phase -> reverted.
- plant225 (height-only plant criterion) also counts the design's soft Hermite landing approach (+10 cm at z < 1.5) as planted slide:
  read episodes, not only "worst net".
Slip table (worst planted-foot net cm; production V2.24 pivot vs rv32 32-bin): sw_ph0 16.7/24.6, sw_ph2 26.1/16.7, ph0 49.7/24.6,
ph3 16.6/24.6, rel 30.4/9.0, dbl 35.5/10.2 -> mixed, NOT promoted; posture gain (pelvis -2..+7 vs -11..+6, lean <= 31 vs 46 deg) real.
Open levers: SHM_FootPlaceOff gated while an SHM226 clip is selected (snapshot DSL in install_idle_wait.py, flat ground only), hold the
reversal database for the clip length or design the clip to end at the episode end with the loop phase matched at that speed.

## V2.27 holding an authored clip to its end (2026-10-24, Saved/Codex/SHME_V227_20261024/, tools Tools/SHME_V227_20261024/)
Metrics: `exitjump227.py` (per SHM226 clip span: entry/exit clip time vs length, ABP episode and FootPlacement-off spans, play rate,
max per-frame planted-ball jump inside the clip and in the exit window, what MM selects next, SWITCH list of mid-span clip changes),
`plant227.py` (plant225 + a contact-start variant: a plant episode starts only when low AND horizontal speed < 80 cm/s, so the design's soft
landing approach is not counted), `trace227.py label t0 t1` (per-frame asset / clip time / Hold-Restart-Dead-Thr / component episode / ball
displacement). Verified owners and traps, in the order they were found (each pass measured against the previous one):
- hold alone (pass a): exit jump 9-12 -> 1-3 cm, but back-to-back component episodes never drop rdOn -> no bridge frame -> the hold kept
  the OLD family database (pass b: restart detection via RedirectTime decrease).
- j24_dbl deadlock 115-118 cm (pass c): with the body nearly stopped MM re-entered clip starts inside the held DB every few frames and the
  remaining-time curve jumped back to ~1.9 s -> hold never released. A hold is only valid for the clip INSTANCE the component entered
  (re-entry latch).
- 60 FPS ph0 68 cm (pass d): MM searches every frame; ONE frame after entry it re-selected the opposite-phase clip (P14 ct 0.10 -> P30
  ct 0.03; neighbouring 32-bin clips start near-identical) -> search throttle while the clip plays. Pass d still failed at 60 FPS because
  the throttle condition read the ABP's own episode flag (one frame late): gate from the component's RedirectActive too (pass e).
- j24_dbl 100 cm (pass d): the component ended its episode with RedirectEnd 3 (new intent) and the capsule accelerated forward while the
  held F_B clip ran backward to its end. The hold must die on new-intent / lost ends (pass e); pass c had hidden this because the re-entry
  latch fired on the symptom. Rule: bind a clip hold to (1) the component's episode identity, (2) the clip instance, (3) the intent that
  started it.
- FP off only pays while the clip plays to its end: a release during the clip (j24_rel) -> stop blend 16-18 cm (open).
- the sw_ph2 P6 clip has a floor-level brake-foot redirect + the capsule 12-21 cm ahead of the design table at a late entry (content /
  entry latency, open); ad_ph0 / m180w select no SHM226 clip (N/A, not perfect).
- decisive split (2026-10-24): when a candidate regresses at one FPS, compare it with the SAME content without the mechanism (rv32) and
  with the mechanism in isolation (rhH): ph3 60/120 = 35 (rh) / 41 (rhH) / 41-43 (rv32) vs 15/27 production -> the slide is the content's
  (MM picks bin P4 at 60/120, P21 at 30; capterm: capsule term 26-37 cm, pose term flat), not the hold's. Capsule speed vs time is FPS
  independent (production == candidate curves); what depends on FPS is the bin MM selects at entry.

## V2.28 clock method: animation clock vs capsule clock (2026-10-25, Tools/SHME_V228_20261025/)
Before blaming content for a planted-foot slide, align the two clocks at the entry: moments228.py (request / brake / component episode /
ABP episode / selection / clip-in-pose / brake plant / zero crossing / push / handover, with the entry state) and speedclock228.py (per frame:
actual capsule speed along the old travel vs the clip design table at the selected clip time; the integral of the difference is the drift a
design-fixed planted foot must show). Found: Motion Matching enters the SHM226 clips at ct 0.067-0.10 on the request frame while the capsule
has braked for exactly one frame -> the clip clock leads by 0.035 / 0.056 / 0.065 s at 30 / 60 / 120 FPS = a constant 25 / 55 / 75 cm/s
offset over the whole brake (the GR friction brake has the design slope 636 cm/s2) -> 9 / 24 / 22 cm drift = the V2.27 ph3 60/120 slide.
The V2.27 "entry speed differs by FPS" was a tool artifact (capterm multiplied the position delta by 30 at every FPS); the capsule speed
curve is FPS-independent, only the input latency (request frame 5.258..5.35) and hence the gait phase / bin differ.
Fix verified (clipspeed228.py): with the capsule bound to the clip design the per-frame |v_actual - v_design| is <= 5 cm/s and the integral
~1 cm at 30 and 60 FPS; slip ph0 49.7 -> 13.0 / 5.8 (60), sw_ph2 31 -> 9 / 12, ovl120 23 -> 9 at 60. FootPlacement ON + bound capsule beats
FP off (ph3 12.1 vs 21.9). Traps: zeroing CalculateMaxAcceleration kills the CMC acceleration vector = HasIntent (episode lost, walk stop);
a qa_graph class pin needs a path string; the W>0.3 witness threshold delayed the contract by 3 frames (0.1).
Cancel paths measured (v228t2 rhC): release during the brake -> idle at 57 s + walk start (37 cm, right foot); second request along the
brake direction -> jog pivot + run start (27 cm): both are selection consequences of the hold dying at the intent change, not slides.
Arms / head / torso at the handover (arms228.py): hand per-frame excursion exit-window 11 cm (production pivot 14-17), head 1-2 cm, chest-pelvis
counter-rotation -9..+13 deg before and after = no second preparation.
Head gaze (gaze228.py): derive the head forward from the bone axes at a neutral frame (+Y on this skeleton; +X is up), never from an Euler
component. Settled gaze error 4-8 deg, head-vs-body yaw <= 14 deg, within 10 deg about 0.6 s after the latch; the LookAt nodes already aim
local +Y (a first "tilts down" read was wrong: check the node axis export before changing it).
Terrain (step228.py / ter228.py): reference the plant height to the flat planted-ball offset of the run; the 28 cm jog step saturated the
lift at SwingLiftMax 25 and landed the first foot 4 cm onto the edge with the heel over the void (FootPlacement then pulled it 7 cm down).

## V2.29 method: a pose flip that only one route shows (2026-10-25)
- Measure spine_03 heading minus pelvis heading per frame (MM mesh bone Z axes, wrapped); a >40 deg/frame jump is a twist flip, not a turn.
- List which routes show it (here only the RevTurn clips, never keyboard S) before suspecting OW / PBI / IK: a route-specific flip with
  the same clip time window is content.
- Prove a bake bug by re-running the old bake from its cached source keys and comparing with the clip keys (0.0 deg = nothing else edited
  them), then run the corrected code and count spin frames. Isolation runs of runtime layers are then unnecessary.

## V2.29 method: held-opposite-key control lock audit (2026-10-25)
- Slip and pop tables never show a control lock. For every reversal scenario run `Tools/SHME_V229_20261025/lock229.py`: per request that
  points against the travel and stays held, time until the velocity component along the request turns positive (t_rev), distance
  travelled against it, and the speed against it after 0.3 s (a brake decelerates, a lock keeps or gains speed). LOCK = t_rev > 1.2 s.
- Include repeated reversals at decreasing speed (W>S>W>S>W) and a sweep of the second request time (S 0.8-2.0 s): the V2.28 lock
  appeared only when the second W met the F_B clip in its push phase after an earlier reversal.
- Trace a lock frame by frame through the hold state (Hold / On / Dead / AgainstT / EntrySign / HoldDB / selected clip): a safety that
  fires for one frame and is re-armed next frame by "clip still in the pose" is not a safety; route the case (cancel to the opposite
  family) instead of only killing the hold.

## V2.30 methods (2026-10-26, Saved/Codex/SHME_V230_20261026)
- Route owner at low speed: list every gate's speed condition on the path (EarlyRev frame-0 speed band, component class onset speed,
  hold latch DB). A 40-135 cm/s back-run satisfied none, so the latch kept the vendor sprint-pivot DB -> WalkToSprint head pop. Gate a new
  class by the REQUESTED gait (CMC MaxSpeed), never by recent peak speed or effort: those stay high after a sprint while the player walks.
  Check what the scenario really requests: releasing Shift in this project falls back to RUN (245-300 cm/s), not walk.
- Same-content A/B before any verdict: content edited in place changes every 'before' run; compare route off vs on in ONE session
  (nolr variant), and repeat runs - jog-reversal phase-bin entries are bimodal across sessions (same input: 6.6 / 17.3 / 46.5 cm).
- Slip metric: plant227 counts the family clip only (a V2.29 '0.0' meant the family was not selected); use --fam=_ for all clips, then
  confirm a slide with the ball height (planted z <= 0 while moving 2-4 m/s = skate; z 3-7 cm = low swing).
- Logged clip time is ONE FRAME LATE (anim update of frame N appears in row N+1). A stall frame therefore shows the capsule advancing and
  the clip 'not' - compare the next row before calling a clock desync (V2.29's 81.7 deg cold-start finding was this).
- Arcade sway: isolate every runtime layer first (PBI, spine counter-rotation, curve lean, orientation warping, raw pose, settle/terrain:
  <= 1 cm here); when the clip owns it, re-author at the same cadence (stride scale so play rate ~1, lateral sway attenuation per
  segment, solve_leg + leg_guard, IK foot sync) with an auto lateral-axis + roll-sign check. Expect upper-body acceleration to RISE
  (rate^2) when a slow-motion loop returns to rate 1: judge peaks and amplitudes, not counts above 25 m/s2.
- Idle entry vs authored hold: a one-frame heel-strike difference can let SHM_IdleEntry fire during a 0.15 s release inside a held
  reversal and end the hold before the resume window sees the re-press. Diff every logged value at the onset frame across two runs.

## V2.31 methods (2026-10-26, Saved/Codex/SHME_V231_20261026, tools Tools/SHME_V231_20261026)
- **Contact classifier first** (`contact231.py`, visible balls): SLIP (still, then >= 5 cm), DRAG (on the floor > 25 cm/s for >= 5 cm), PIVOT
  (ball still, foot turns: normal), SKIM (never still: not a contact). Height-only "planted slip" mixes all four. Window tables by EPISODE
  START, not by the worst frame (an episode that began in the previous clip gets blamed on the next one). Dedupe LTP rows with equal t (the
  LTP sometimes logs a frame twice -> 300+ m/s2 fake head pops). Not valid on uneven routes (map_r1): global floor percentiles.
- **Entry state before content**: entry231 (speed, pose source clip + time, entry clip + ct, clip-bound speed jump), exits231 (what MM picks
  after an authored clip), relphase231 (release phase from the visible feet), step231 (capsule step events), trans231 (per clip change).
- **An authored family is only valid for the entry state it was designed from**: the 245 cm/s jog B_F family entered from a back-WALK at
  55 cm/s dragged the brake foot (wrong pose) and jumped the clip-bound capsule. A low-speed family needs another CHOREOGRAPHY (the support
  foot brakes and pushes in place, the swing foot becomes the first step), not the jog design at a lower v0.
- **Effort = choreography, not tempo**: a loaded body gets an extra support (short brake plant -> catch step beyond the stop -> first step
  with the brake foot -> smaller push). Generate one representative bin, check it in game, then all phases; gate bins (drift < 3, IK < 7.5).
  A pinned support foot must lift when the body has passed it by ~36 cm (leg reach), else IK overstretch drags it.
- **Routing frames**: the V2.24 EarlyRev frame uses the JR database BEFORE the component episode exists (stale RedirectSpeed0); the ABP
  family is one frame behind the component (TIP end frame at rest -> vendor pivot tail): gate on what is true on THAT frame.
- **Exit routes matter as much as entries**: every sprint exit of an authored reversal went into the V2.14 RevPush window (12-42 cm) and
  made 60/120 FPS reversals start from a mismatched pose. Check exits231 for every family you add.
- **Run-to-run divergence**: same-input fixed-step runs can differ from PIE frame 2 (FeetIK output) and at the move start (10 um); tiny
  differences flip contact thresholds and MM ties. Judge candidates on repeated runs and on both entry phases, never on one run.

## V2.32 methods (2026-10-27, Saved/Codex/SHME_V232_20261027, tools Tools/SHME_V232_20261027)
- One-frame selection blips (blip232.py): A -> B -> C with B selected for one logged frame = two blends in two frames. Causes found:
  (1) tick order (SHME PostPhysics, ABP PrePhysics: the ABP routes with last frame's state) - NOT fixable globally (IntentTickPrePhysics
  and a live prerequisite both regress swl12 / s180 / wstart); (2) a reversal database without its EXIT loop: when the authored clip ends
  the stale-frame search picks another bin's end pose (B_F DBs: fixed with *RevBwdX = bins + rear loops + forward loop).
- A start clip must begin in the stance the character really stands in: AAMS-derived JogQ starts start 16 cm per foot off the idle ->
  the blend drags both feet. Pinning to the idle helps only true-idle starts; the same clip from a stopping pose gets worse -> needs a
  stand-time route, not content alone.
- Owner isolation before content: a closing-step drag that is not in the clip and not in FP / settle / PBI / brake posture was cured by a
  swing floor guard (T7: swing foot >= planted height + 1.5 cm) - measure the MM output pose (mx_*) vs the clip before editing clips.
- Run-to-run divergence across editor sessions is large (same input: 30 vs 81 cm): decide on same-session, interleaved, repeated runs.
- V2.32 classifier trap: a worst-episode number from contact231 can move by ~9 cm when an unrelated small foot-height change (<= 4 cm) shifts
  the episode start (c29_combo 48.8 -> 57.6 with the T7 floor guard, defect window frame-identical). Before calling a regression, compare the
  ball paths of both runs frame by frame (max diff) and check whether the runs diverge onto another MM branch (j30_rel: 80 cm split after
  the first step = branch divergence, not an owner).
