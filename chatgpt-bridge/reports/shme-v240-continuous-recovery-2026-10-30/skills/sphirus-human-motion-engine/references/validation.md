# SHME validation

## Harness (PIE-only, production map never dirtied)
`Tools/SHME_V1_20260925/qa.sh '<json>'` → `qa_pie.py`: starts PIE, spawns the QA floor/fixtures and `BP_LTP_QA` into the GAME world (`summon` cheat + configure), ends on `LTP_FINISHED`/`PBI_FINISHED`, then `post_check.py` asserts the editor world is clean. Each run resets every `DA_SHM_Response_Default` field to the schema default (`shm_profiles.py`) and applies `shme_flags` overrides, sets `TelemetryEnabled` and labels the component.

Request keys: `label`, `suite` (1 turns, 2 jumps, 3 regression, 5 reversals, 6 stairs, 7 wall, 8 corridor, 10 starts/stops), `fps`, `shme_flags` (e.g. `{"HumanStateEnabled": false}` = baseline), `shots`.

Evidence: `Saved/Codex/SHME_V1_20260925/Evidence/<label>.json` (LTP pose/camera telemetry), `<label>_metrics.json` (slide proxy, pelvis, camera), `<label>_shm.json` (SHME telemetry: speed, accel, yaw rate, turn angle, turn/brake/reversal/traction/recovery demand, support side, contact confidences, stability margin, capture error, COM/CP/foot target, landing, clearances, width, constrained/open, boom/shoulder, camera offset, air weight, cost).

## A/B discipline
Same suite/FPS/profile; baseline = `HumanStateEnabled false`. Change one subsystem flag at a time (e.g. only `CameraPhysicalSignalsEnabled`, only `BodyCouplingBlend`). Keep the protected rows (short taps, CP stop gates, 10 FPS stop acquisition, reversal pivots, stand-air jump) in every A/B.

## Required scenarios
Suites 1, 2, 3, 5, 10 at 30 FPS and suite 10 at 10 FPS; 6 (stairs), 7 (wall), 8 (corridor) for camera; then the real house/exterior with the player camera. Physical keyboard/mouse/gamepad and achieved 60 FPS are the user's acceptance runs — never claim them from injected input.

## V1.1 findings that change how to test
- FootPlacement only corrects what its release rules allow: the landing slide was a radius release (fixed by LandingSupport);
  diagonal walk-stop slide is a drift in the AAMS walk-stop clip tails with footspeed 0 (FootPlacement on/off gives the same
  slide) -> needs clip-range/selection work, not plant tuning; sprint-stop settle is the idle re-centring the body onto a capsule
  that stopped ~10-14 cm behind the COM (fixed by SHM_UpdateSettle).
- The QA tap stages follow a walk stop within 0.2 s: any post-stop behaviour must be tested against the tap rows.
- `align.py <label>` aligns SHME telemetry (gt) to LTP pose telemetry (t) by speed matching; `body_metrics.py` gives torso
  lean / counter-yaw / wobble per stage.

## V1.2 findings that change how to test
- Idle-entry slides are stance mismatches (AAMS stop end stance vs the Ranger idle), not FootPlacement: measure the feet in
  WORLD space around `HasVelocity` falling and the idle takeover; `pos` moving while feet are static is the settle.
- The first PIE after any PoseSearch database change runs with a cold index: Motion Matching reports 'None' for ~0.4 s at
  the first selections (spawn walk, landings) and the slide proxy explodes (100+ cm). Always run twice; use the second.
- Owned copies made with duplicate_asset inherit PoseSearchBranchIn notifies that do NOT register with the database; remove
  the inherited track and add the BranchIn again (dirties + save the database), then verify the member list.
- Camera: measure framing at the true apex instant (pawn max z) separately from the max camera-relative height, which
  peaks in early descent; report contact height above rest, time within 3 cm and within 1 cm.
- Target error (planned foot target vs touchdown): `target_error.py <label>` (SHME telemetry only).

## V1.3 findings
- In this project's strafe control the QA 90/180 cases are strafe pivots and travel reversals: yaw angular momentum stays
  below 1 kg m^2/s; use braking impulse + reversal demand as the turn discriminator, not L_z.
- RecoveryDemand (capture error) is ~0 in every unperturbed harness stage except sprint reversals (0.77, 2 frames) and
  wall impacts (1.0). A recovery-step route cannot be validated by the current suites; `RouteForceRecovery` exercises the
  database route mechanically. A perturbation scenario (push, slope, uneven landing) is needed for real validation.
- ABP telemetry `SHMABP|...` (`abp_evidence.py`, keys ready/hv/wait/entry/hold/blk/fam/brake/lhold) is the tool for every
  idle-takeover question; align gt to LTP t by the end-time offset.
- Wall suite stages vary run to run by several cm (contact chaos); judge the suite max and the release stages.

## V1.3.1 findings
- Ground truth for any routing claim is the MM node's final database per frame (`SHMABP|mmdb|mmanim`, PostSelection), and
  it is stale whenever the MM branch is not relevant: read it together with `idle` (takeover) and the throttle state.
- A standing perturbation needs three things to reach a recovery clip: the takeover released (`SHM_IdleWait`), the search
  not throttled (SearchThrottleTime 0 while routed), and a database whose entries are only the recovery clips.
- Shove timing is game time: the LTP protocol starts ~3 s after PIE start (`off = gt - t`); suite 2 idle window gt 3.0-4.5,
  suite 10 first sustained walk gt 12.3-13.8. A shove before the protocol positions the pawn is wasted.
- The QA protocol teleports to fixed points; house runs need `house:true, origin:[600,1000,238]` (interior floor z 150).
- Check vendor databases in memory (`probe_vendor_dbs.py`) after any clip duplication: inherited BranchIn tracks register
  project copies into `PSD_SM_LocoTransitions` (runtime contamination, never on disk).
- The index of the PSN_Dense_All set rebuilds at PIE start after any member database change: the first ~8 s of a run log
  "AsyncBuildIndex skipped"; do not judge routed frames from that window.

## V1.3.2 findings
- Turn-in-place is measured with `tip_report.py` (planted-foot travel per stage, pelvis-vs-actor yaw, selection, takeover):
  the AAMS+GR baseline is a rotating statue (feet 3 cm/frame, root offset never accumulates); judge a fix by foot travel
  on the no-clip stages and by which clip plays on the large ones. Screenshots at 0.1 s drop PIE to ~4 FPS: measure
  without shots, capture separately.
- A one-change rerun per hypothesis is the only reliable method here: three "obvious" fixes (rotation-mode function,
  layer enable, foot-placement gate) each measured as no effect or worse.

## V1.3.3 findings
- True-speed review: harness `slomo` (global time dilation) + `shots` 0.1 -> `make_gif.py` timed GIFs; 10 Hz sheets stay
  the quick look. Judge transitions with `snap_report.py` (per-frame skeletal delta at every MM selection switch).
- Directional snaps are chooser database switches (double/triple within 0.1 s) with 12-17 cm pelvis / 20-26 cm foot
  jumps; blend time is not the lever. Diagonal "lean" is the off-axis camera, the skeleton is symmetric.
- Camera framing proxy `cam_frame.py` (head elevation angle from the camera): flat -5 deg, stairs up down to -22.

V1.3.1 closure (2026-09-26): protocol-less harness runs (`no_ltp`) can move: `move` {start, gait walk|jog|sprint, segments
  [[seconds, input_angle_deg], ...], stop} drives the same Enhanced Input console injection as the protocol actor
  (`Input.+action IA_Move X Y`; gait tap = jog, hold = sprint), optionally with the `yaw` schedule (look turns while moving);
  `house` + `origin` + `yaw0` teleport the pawn to the origin facing yaw0 (before the observer camera aims); `open_doors`
  ["VerandaDoor"] sets the hinged-door Blueprint's R4_IsOpen in the PIE world. redir_report.py <label> [stage-regex] prints
  per-stage dV / redirection demand / TurnClass / speed loss / families / clips / planted-foot skating / COM z / blocked.
  House facts: ground floor z 150 (capsule 238), lawn 100-115; the veranda door hinge is at x 775 so the open leaf blocks
  x 775 - walk the opening at x ~840; the porch riser from the lawn exceeds the step height; living-room starts run into
  furniture (protocol suites need >= 4 m clear along +x). 10 FPS setups: 20.8 cm with SHME off vs 23.4 on (AAMS stop).

## V1.3.7 findings (2026-09-27)
- The RENDERED body is the pawn component `Manny` = MetaHuman `SKM_MH_MainCharacter_BodyMesh` (anim class
  `ABP_GR_MetaHuman`), retargeted from the invisible Motion Matching mesh `CharacterMesh0` (Travisty mascot). The harness
  `mh_*` keys are the invisible mesh; visible-body keys are `vb_*` (pelvis, spine_03 `vb_chest`, spine_05, head, balls,
  feet, upper arms). Judge posture on `vb_*`: the visible lower-trunk pitch reads 4-10 deg higher than the source.
  `stance_report.py --vb`, `curve_report.py` (outside / inside foot, toe yaw vs tangent), `transition_report.py`
  (root-relative head / pelvis acceleration = pop), `timeline.py` (per-sample owners / clip / posture).
- ABP telemetry flags: `so` = CP_StopOwned, `sto` = CP_StartOwned, `iuw` idle upper-body weight, `ssw` stop-settle
  wait, `lkr` smoothed look rate, `bra` / `brr` breathing weight / rate.
- The idle takeover freezes the Motion Matching branch (an inactive BlendListByBool child is not updated): whatever
  pose the MM held when the takeover engaged becomes the stance snapshot. Stops carry `SHM_StopSettle` (1 until their
  final foot plant) and the takeover waits for it.
- A trunk posture metric on the pelvis->neck line hides S-curves: correct / measure the lower (pelvis->spine_03) and
  upper (spine_03->neck) segments separately.
- Real-map capture: MediaIO FileMediaOutput at the NATIVE PIE viewport size (a different desired size fails with
  "Render Target size doesn't match"); encode with the scratchpad `shmvid.ps1` (scales / evens the frames).
- `error_gate.py` classes: PoseSearch "searches skipped" right after any database edit (re-index; rerun), the
  MetaHuman / fabric material VT errors are pre-existing level content.

## V1.3.8 findings (2026-09-27)
- Reproduce with the REAL player input path. Mouse look is `IA_Look` -> `BP_GR_InputBase` (controller) ->
  `TW_BeforeNativeLook` -> pawn `TW_CameraLookPulse` (camera-intent rebase, `TW_LastLookTime`) -> sensitivity
  (`MouseYawSensitivity` 0.2 x legacy 2.5 = 0.5 deg per unit) -> `AddYawInput`. `pc.add_yaw_input` skips all of that.
  Harness: `"look":"ia"` injects open-loop mouse deltas (`Input.+action IA_Look X=..`); closed-loop injection rings because
  the camera rig also moves the control yaw. Sprint = held `IA_Ranger_GaitShift`; mid-run gait changes via `gait_events`.
- A "freeze" detector must not gate on speed alone: contact stops (speed ~0-110) hid the clamped-clip freeze in V1.3.7 runs.
  `gait_freeze_report.py` classes: base stall (MM time not advancing), legs static (rendered feet fore-aft range < 10 cm while
  moving), hard stop, montage takeover, MM ping-pong. 180 s runs, several starts; the V1.3.8 freeze needed 12-60 s to appear.
- Telemetry of the MM selection is NOT what the player sees when a DefaultSlot montage plays: log the montage's animation
  asset (`mona`, harness key) for every turn / contact test. Standing mouse turns are owned by `BP_GR_Player.GR_UpdateIdleTurn`
  montages, not by the SHM turn-in-place MM route underneath.
- Measure stance DURING the turn (0.1-2.4 s after the step, `turn_audit.py`), not only at the end of the hold.
- GR_CORE_CONTACT (BP_GR_Player EventGraph) plays a root-motion contact montage on any front block, including steep landscape;
  the MM layer underneath then ping-pongs in a vendor 180 pivot tail. Long real-map runs leave the refuge (no boundary).

## V1.3.9 (2026-09-27)
- Harness: `pvars` (pawn vars + spring arm) and `cvars` (SHME component vars) per tick; `null` segment angle = stick
  release (sequential starts in one run).
- Reports: `start_audit` (first swing / preslide), `stop_audit` (stop family), `rec_audit` (recovery → loop),
  `gait_switch` (mid-run gait events), `head_spikes` (per-frame pops; ignore duplicated rows), `curve_report` +
  `curve_pelvis` (15-35 deg/s matrix), `stair_cam` with rig telemetry.
- SHME cost differs between editor processes (0.65 vs 0.88 ms mean for the same build): compare perf within one process.
- Running-speed shoves are absorbed without a recovery family (capture-error detector); test recovery → locomotion at
  walk, and check jog for the absence of a lock.

## V2.1 (2026-10-14) - transition continuity measurement
- Pops: `Tools/SHME_V21_20261014/pop_report.py` (root-relative upper-body acceleration, > 25 m/s2 events, owner attribution).
  Dedup harness rows that share one game time and skip frames next to > 0.1 s gaps, else hitches read as 54-68 m/s2 pops. At
  10 FPS (dt 0.1) the pop metric is blind: judge P2 by stop selections (14 CP stop entries / 18 stop-database entries in
  suite 10 @ 10 FPS = V2 baseline) and the V2 metric bundle.
- Natural ranges on the QA floor: walk upper body ~4-15 m/s2, jog 10-20, sprint 25-30 (sprint "pops" at 25-32 are the loop).
- `jumps.py` counts start-clip re-picks (same clip, time jumps back 0.2-0.4 s = replayed push-off) and cross-clip hopping;
  `gait_report.py` per tempo change; `camseries.py` / `cam_report.py` for framing speed and camera excess acceleration.
- A/B rules that held: interleave variants per scenario in one editor process; pass explicit pbi/abp values every run (qa_pie
  never resets them); compare only runs within ~15 % telemetry rate; restart the editor at ~38 GB (PIE leak ~0.6 GB/run).

## V2.9 (2026-10-16) - legs on uneven ground, turn coherence, moving turns
- Surfaces (qa_pie `boxes` [name,x,y,z,sx,sy,sz,pitch,yaw,roll], PIE only): lfoot / rfoot strip 10 cm, 8 deg ramp, 10 deg
  cross slope, 18 cm steps. Judge the POST-STOP IDLE: ball gap to the trace (driver ball + gzl/gzr), pelvis height vs the
  single adaptation at the stop end, foot pitch / roll vs the surface. A flat test proves nothing about adaptation.
- Knee: hinge = dot(knee-plane normal, calf local Z) for flexion >= 8 deg (+1 ok, < 0 backward, < 0.7 twisted); the same
  value on the visible MetaHuman calf. Knee-vs-toe angles are unreliable with a plantarflexed foot. Scan every owned clip
  after any IK bake (probe_clipknees.py scan()).
- Turn coherence (turns.py): per capsule-rate window cap-hip separation, hip / chest lag to 50 % of the capsule turn, yaw
  steps, planted-foot spin. In-place turn acceptance after V2.9: cap-hip <= ~45 deg (180 turns ~70 = clip-authored root lead),
  hip lag <= 0.35 s, no walk-start snap.
- Standing-turn legs: compare in-game hip-line vs planted-foot yaw (turns.py hip-foot) with the CLIP's own value
  (probe_tip180_feet.py: 180_L 62, 180_R 38, 90_L 55, 90_R 30 deg); turnslip.py separates a ball pivot (ball still, foot
  yaws) from sliding. Excess over the clip = plant-lock type, not the clip.
- Moving turns (cuts.py): events = input direction change > 25 deg in 0.15 s while moving; speed loss, alignment time,
  peak lateral g, plants (contact by HEIGHT - sprint plants still slide 30-90 cm/s), outside-foot first plant, pelvis brake
  dip, database sequence (av_CurrentSelectedDatabase now logged by name). Upper-body pops: pop_report.py per window.
- Never run two A/B loops at once (use ab_safe.sh); never move a runner job file that may be executing (runner wedge).
## V2.10 (2026-10-16) - entry timing, leg-roll flips, settled idle
- Moving-turn timeline: `cut_timeline.py <label> t0 t1` (speed, velocity / actor / input yaw, database, clip + clip time, redirect frames /
  hold / class, ball contact, pelvis, lateral g) with avars Phase27_SelectedObject / Phase27_SelectedTime. Judge the clip time at entry
  against the clip phase table (`probe_cutclip.py` + `cutclip_table.py`: speed drop, facing / travel 10-50-90 %, plants, pelvis min).
- Leg-roll flips: `calfjump.py` (per-frame calf-Z change while moving, driver vs visible): production walk 77.5 deg max / 11-13 frames > 30
  per run before, 8.5 / 0 after the V2.10 loop repair.
- Uneven-ground idle: `strip_idle.py` (last 1 s median: pelvis above the LOWER / higher floor, knee flexion) - legs.py's idle flexion is a
  maximum that includes the stop transition.
- Spawn idle knee: `idle_knee.py` (hinge, kt, hinge-axis vs foot) over t 0-2 s.
- Harness: v210_ab.sh base = the V2.10 production passed explicitly (behaviour and abp flags persist across runs); PRE pre_base.py reloads
  the saved ABP every run; warm the bridge databases with one discarded run after every editor (re)start (first-use index hitch).
- Single-variable FootPlacement / LegIK tests in memory: pre_fp210.py (pelvis struct on the node; PLANT settings via the ABP presets
  PlantSettings_* because the node's PlantSettings pin is bound to Get_FootPlacementPlantSettings), pre_legik.py (LegsDefinition text).

## V2.11 (2026-10-16) - arm carriage, direction timeline, push / reversal timelines
- `arms.py <run> --carriage` (per start: elbow lateral + abduction medians idle / start 0-0.8 s / loop 1.2-3.2 s, dip, time below both
  idle and loop) and `--turns` (per TIP montage: elbow / hand over the idle before it); chest frame from vaz_/maz_spine_03.
- `dirtl.py` (camera yaw, control yaw, wanted direction = control + stick angle, CMC acceleration yaw, velocity yaw, capsule, chest yaw;
  per segment max |cam-ctl|, max |acc-want|, facing, settle). `gaitl.py` (speed / velocity / acceleration / gait / database / clip /
  CP flags / redirect / push per frame; per input segment v in / min / end, reversal time, peak deceleration, clip families).
  `recov_table.py` (direction-change events: normal / planned hard / overflow? from redirect ownership, planted-ball creep and pops).
- Harness facts: `"look":"ia"` sends IA_Look every tick, but TW_BeforeNativeLook ignores |look| < 0.0001, so zero-value ticks do not count
  as "looked" (the camera auto-follow test is valid). The tap release head / shoulder pops (30-35 m/s2 on 55-68 ms capture frames) and
  sprint shoulder pops (V2.10 baseline 39-63) are pre-existing - compare against the before run of the same scenario.
- mem_guard restarted the editor four times in this pass (38 GB): update EDITOR_LOCK with the new log name and warm the databases.

## V2.12 (2026-10-17) - tools and harness facts
- Real keys: `qa_pie` move `{"keys": [[t, "W"|"S"|"A"|"D"|"LeftShift", 1|0], ...]}` sends `Input.+key / Input.-key` through the player's
  mapping context (EnhancedInput forced keys). Stage label `mv_kb[s]_<angle|rel>_<n>_<held WASD>`.
- `arms212.py <run> --starts / --cycles / --detail` (chest frame, w = normalised direction rate - the V2.11-era w was clipped to 0 by a
  non-unit vector), `loop_arms212.py` (offline loop cycle x phase), `back212.py` (keys held, Shift, CR_Backpedal, target / shown gait, max
  speed, velocity vs chest / camera, one-frame dv/dt, back clips, forward-clip-while-back), `tip212.py` (per turn montage: arms, shrug,
  trunk pitch / roll, pelvis drop, steps, reverse / early-W chains), `push212.py` (episodes, overspeed walk, switch contact slip, pitch rate),
  `recov212.py` (reversal event: stances with slip, load / settle / push, push timing, arm / trunk reaction, route, redirect flags),
  `recov_src.py` (clip survey: speed / travel / facing / plants with slip).
- Never edit a bash script that a running batch is executing (bash reads it incrementally: the tail ran a shifted fragment); write to
  `.new` and `mv`.
- New databases index on first use: a candidate's first run after the build can search an empty database ("None" selection) - warm it.
- GameViewport.IsUnique() PIE-end crash recurred once (pre-existing); the batch relaunches and repeats the run.
- A/B and capture base flags must EQUAL the saved production (the harness abp_flags override the CDO for that run). V2.12: the v212_ab3
  base carried SHM212_RdRev / RevTurnMode 1.0 while the saved ABP held 0.0, so the first "final production" captures of reversal scenes
  (W release -> S, S+A, push after a reversal, cut -> reverse) ran the dormant recovery candidate. Before publishing, scan the evidence of
  every published run for the dormant modes' own avars (here av_SHM212_RevOn, a CutRev database in av_CurrentSelectedDatabase) and compare
  the base flag block with verify_prod212.txt.
- Runner jobs queued while an A/B batch runs can be swept by its mem_guard editor restart (moved to b2runner/swept); the waiting run_v2.sh
  then hangs until its timeout - kill it (process tree) and requeue; never leave such waiters alive.
- `pushpose212.py <runs>`: per push episode the runtime trunk pitch peak (pelvis -> spine_05 vs actor yaw) and the pelvis drop (median of
  the 1 s before minus the minimum to +0.3 s after).
- `Tools/SHME_PIV_20261017/pivdrop.py <runs>`: brake pivot read-out from the S press (real-key stage with S held, camera prefix allowed, or a
  scripted mv_<gait>_180 reversal): pelvis drop from the 0.6 s pre-S median, time back within 4 cm, trunk pitch max, pivot clip span.
- V2.13 tools: `dirchange213.py <runs> [--tl]` (every direction-change event on one timeline: intent angle, first MM switch, component /
  ABP episode spans + classes, heading 90 % time, vmin / brake distance / re-accel, |a|max, pelvis drop, trunk pitch, clip timeline),
  `armswing213.py` (hand forward excursion + upper-arm pitch range per 0.5 s), `push_window213.py` (BranchIn entry window rebuild),
  `verify_prod213.py`. Harness cvars now carry RedirectTime / RedirectEnd / RedirectDirLatched / DesiredVelocity / TurnClass.
- V2.14 tools (Tools/SHME_V214_20261017/): `verify_prod214.py` (modes incl. the dormant-off table, DA values, clip windows via notify
  events, database entries with None / Rollbacks counts, file hashes vs checkpoint/baseline_v213), `push_exclude214.py` (the
  PoseSearchExcludeFromDatabase range of the walk push clips - check it before moving an entry window), `build_v214_revdb.py` /
  `build_v214_revpush.py` (databases from a seed schema; stale None entries after deleting a copy -> delete and recreate the database),
  `Saved/Codex/SHME_V214_20261017/req/probe_entry.py` (clip ball-vs-pelvis table for pose matching). Telemetry avars carry
  SHM214_PushRevOn / RevEndT / TailOn / RtPrev and SHM211_Push. A DSL variable that does not exist compiles WITH WARNINGS and reads 0 /
  'err' in telemetry: ensure_vars + assert on B.list_variables before rebuilding a function; the ABP normally compiles WITH_WARNINGS, so an
  installer's ok check must not require a warning-free status.
- V2.15 tools (Tools/SHME_V215_20261017/): `contact215.py <run> --switch=<clip>|--t=<s> [--win=a,b] [--all-switches]` = the transition
  contact definition used for every V2.15 number: ball point, per-foot ground = 10th-percentile ball height, contact <= 1.5 cm and
  < 60 cm/s, DRAG = on the ground and >= 60 cm/s (a planted foot sliding), roll = 1.5-4 cm and moving (toe roll / skimming step, never
  counted as slip), support phase from the ball's fore-aft position vs the pelvis (early / mid / late / swing), frames and fps printed.
  `contactslip.py` stance totals include long idle stances (a 6 s stance accumulates idle drift) - use contact215 windows for transitions.
  `dbremove215.py`: PoseSearch has no remove API and deleting a clip's BranchIn track does NOT remove the entry - retargeting the BranchIn
  notify's `database` to a scratch database and re-saving the clip does (the entry moves), then delete the scratch database.
  `verify_prod215.py`, `scan_dormant215.py` (also checks pawn behavior_flags candidates).
- Comparisons across versions only with the same definition: V2.13 "exit slip 0.4-2.3" = push212 +-0.1 s at the switch frame, V2.14
  "23-27" = contactslip landing of the first sprint stance - two metrics (V2.15 report section 6).
- dirchange213 'world' now uses the control yaw (row cy): with an observer camera the old camrot-based label read 'world -175' for a
  run that moved to -90 (V2.14 'side camera changes the keys' was this label error; the key frame is the control rotation).
- A/B variant files are sourced inside v21x_ab.sh: never name a bash array BF / AF / PF / SX / PRE / POST / CON there (PF=(...) clobbered
  the pbi_flags map and the variant silently kept its default). Pass LR_LOG as the NEWEST editor log at batch start (a stale log after a
  memory restart gives 'rows 0' for every run while the runs themselves happen).
- Runner jobs run WHILE a harness PIE session is active (the PIE job returns at once): an installer queued during a batch hits its own
  'PIE running' assert - wait for the batch (AB212_DONE) before any editor mutation.
- A/B base flag maps must carry every new switch at its saved default; a pawn variable is NOT settable by pbi_flags (DA_PBI_Prototype):
  the harness run raises and v212_run.sh waits forever (kill the batch tree).
- V2.16 tools (Tools/SHME_V216_20261018/): `contact216.py <run> [--t0 --t1 --frames --json]` = REAL-floor contact (harness gzl/gzr
  line traces): per foot calibration b0 (ball, slow frames, 10th pct) / a0 (ankle while the ball is down), classes DRAG / pivot / PIVSLIDE
  / SKIM / HOVER (<6 cm, <=60 cm/s: a 'planted' foot that never reaches the floor - V2.15 push stance floated 2-6 cm) / SINK / air;
  contacts per foot, net per point type, drag path; never sum feet. `sum216.py` (chain + per-foot worst), `crouch216.py`, `w2s216.py`
  (Shift latency / push clip / speed times / step intervals / arms), `tip216.py` (per montage: first-frame mpos / mslw / mbt / yaw / lock
  / ball travel + handoff contacts), `prot216.py <prefix> [<base>]`, `final216.py` (event-windowed tables), `verify_prod216.py` (DB leak
  checks incl. vendor PSD_SM_LocoTransitions mtime and turn clips vs baseline sha). Whole-run windows mix sprint start / final stop
  contacts (~40 cm in both versions) - compare EVENT windows.
- qa_pie rows `mpos` / `mslw` / `mbt` (montage position, slot local weight, blend time) since V2.16; new scenarios p_w2s_mid / late /
  tap / dir / rel in v212_run.sh.
- duplicate_asset of a clip copies its BranchIn notifies and syncs the COPY into those databases (vendor PSD_SM_LocoTransitions too);
  clearing the copy's BranchIn `database` (set None, save) removes it - removing the track does not. Re-dirtied clips / vendor DB make
  mem_guard REFUSE: kill the A/B loop before fixing (memory note mem-guard-double-editor-trap).

## V2.23 measurement tools (2026-10-22, Tools/SHME_V223_20261022/)
- qa_pie.py rows now carry the position-authority chain: ax (capsule), avx / avy, mwl / mrl / mry (MM mesh world + relative offset),
  vwl / vwy (visible body component), rmp (root motion playing), apv (spring-arm pivot).
- trace223.py <run> --thr=: per frame the visible-pelvis displacement split into capsule-jump / mesh offset / MM root / MM pelvis /
  visible retarget / camera layers -> classifies a 'teleport' (none of them jumped in the V2.23 jog reversal: it was content).
- rev223.py: reversal timeline (pelvis vs capsule along the heading, camera distance, selected clip / time).
- win223.py: one line per window (contact221 per foot worst net / drag / skim / sink, pelvis-capsule range, clip chain).
- cad223.py: speed / cadence / ground step vs implied step / MM play rate in a steady window (human reference in the docstring).
- cam223.py: camera world path vs capsule path, screen position / jitter of the chest, jerk, look latency (camera vs control yaw), FOV.
- clipspeed223.py (editor): native root speed / root yaw / contacts of clips (find a sprint-authored clip on a jog path).
Rule: classify a reported 'jump' with trace223 before touching any blend / camera; compare variants in the SAME session at fixed step
(o was bit-identical across 5 sessions, but a mem_guard relaunch without -UseFixedTimeStep silently turns a batch real-time).
