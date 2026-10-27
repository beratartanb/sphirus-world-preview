# V2.32 working notes (raw, chronological)

## Plan (2026-10-27)
Base: V2.31 production (efcf466), editor closed, EDITOR_LOCK UNLOCKED, checkpoint pre_v232 (181 files, 141 MB: pawn/ABP/SHME/DA/profiles/
camera BPs/map + V226 + V231 animation folders + tools).
Stages (each group a separate candidate, flags first, production switch only after the gate):
 S1  fresh fixed-30 editor: verify231 ALL_OK; read-only camera rig trace (GR_UpdateRig / PCM / visual yaw / input yaw); baseline camera
     world-path telemetry for the camera scenarios; motion baselines for the open defects (30 + 60 where FPS-dependent).
 M-A loaded family: per-entry gate (real support foot / phase / entry speed / blend order) -> safe fallback where the design does not fit;
     regenerate the bad bins (P21/P29/P30 + the 4750 entry) instead of using the family everywhere.
 M-B swl12 60 FPS bad phase: source vendor pivot -> back-walk blend vs the slow clip first support -> entry from the real plant phase.
 M-C AAMS backward start from stand: own short back start (stand / light back drift / unfinished brake distinguished).
 M-D walk / jog stop closing step: foot plant + capsule brake + weight settle consistent.
 M-E side / rear-diagonal transitions (c29_combo, -90 -> -112.5): OrientationWarping on a planted foot + support continuity.
 M-F release / re-press j30_rel_3200 / 3450: cancel by brake + support phase.
 EF  effort visible: catch-step choreography extended (support transfer, settle step, measured push, short recovery).
 CAM cinematic 3/4 follow: SHME camera layer (no new framework): bounded visual azimuth offset driven by the real body turn, gait-scaled,
     openness / collision scaled, look input priority (no accumulation, no control-yaw write, input frame = control yaw), settle back.
 T   terrain: 28-30 cm step up both feet as one action; step down (geometric drop vs body landing prep).
 AUT IsUnique assertion narrow study; per-run time; log growth.
 FIN A/B/C/D body x camera; FPS 20/30/60/120 + real time; media; promote; clean-reopen verify; publish.

## Session 1 (2026-10-27 01:20 ->)
- s1: fresh fixed-30 editor, verify231 (V2.31 expectations) ALL_OK. Production baselines (26 runs, 14 min): camera scenarios cam32_* (new:
  w45 / j90 / s90 / s90l / s180 / brk2 / wallturn / look / idlelook / analog / chain) + motion defects.
- CAMERA chain (graph dumps V2.29 + this session): movement input = CONTROL yaw (AAMS IA_Move -> GetControlRotation); the boom rotation =
  MakeRotator K2Node_CallFunction_43 (Roll = GR_SHM_CamRoll, Pitch = control, Yaw = Select(ContinuityRevision, CT_VisualCameraYaw
  [control + idle offset + counter yaw], TW_CameraWorldYaw)); every collision trace of GR_UpdateRig is built from that rotator. -> an orbit
  added to that yaw is visual only (no input-frame feedback) and collision-checked. Walk / jog are DIRECTIONAL (actor yaw stays on the view
  while travelling sideways: cam32_j90 alpha -7 deg throughout); only sprint turns the body to the travel (alpha -97 in cam32_s90).
  -> orbit target = body yaw rel. view + 0.5 x travel dir rel. view (sin-shaped), speed-scaled 2 / 8 / 14 deg, side room + indoor scale,
  lag 0.8 s + critically damped smoother, look input priority (hold 1.2 s, faster settle 0.4 s), inspection off, teleport reset.
- MOTION baselines (fixed 30, window/whole-run worst, cm): e29_chain 25.4 (BackLink_1), e29_load 15.0, 4750 15.5, swl12 11.0,
  j30_rel_3200 35.0 / 3450 24.5 / j30_slow 37.9 (backward start), c29_combo 48.8, a29_angb 33.5, c30_calm 33.3 (stop closing step).
- ONE-FRAME SELECTION BLIPS (blip232.py): 139 in 82 V2.31 runs, 26 in 26 S1 runs. Two classes: (a) an authored B_F clip ends (ct 1.46 ->
  another B_F bin at its END 1.47 for one frame -> exit family): visible balls jump 440-640 cm/s in that frame (e29_load / 4750 / j30_slow);
  (b) start: idle -> vendor start clip (1 frame) -> owned JogQ copy. Owner = tick order: SHME component TG_PostPhysics, mesh / ABP
  TG_PrePhysics after the CMC -> the ABP routes with LAST frame's SHME state (new trajectory searched in the old DB). Candidate tk = PIE-only
  live tick prerequisite (SHME before the mesh, after the CMC).
- C backward start (j30_slow 37.9): idle -> start blend moves both feet 82-145 cm/s for 0.1 s, then the clip root lags the CMC capsule:
  SHM_JogQ_af_Loco_Jog_Bwd_Start_AAMS root is still for 0.2 s, then -35 / -98 / -154 cm/s; the CMC capsule moves from the first frame.
  FootPlacement: input foot speed > SpeedThreshold 60 -> never plants during the blend. Candidate sb = V2.28 clip-bound capsule start term
  (witness curve SHM232_SW + backward intent).
- D stop closing step (c30_calm 33.3): the stop clip lifts the closing foot 5.6 cm (stopfix232 dry scan: most owned stops 3-10 cm, 6 below
  3 cm), but in game the foot runs 0.7-5.6 cm UNDER the floor band -> a runtime owner lowers it 6-8 cm (settle / FootPlacement / pelvis):
  isolation variants oSET / oFP / oRAW in B2 before any content change.
- E walk direction change (c29_combo 45 -> 90): the MM switch FwdRight -> Right happens with the LEFT foot planted; the blend rotates it 108 deg
  and slides it 23 cm; PlantSettings_Walk UnplantAngle 45 releases it. Candidates pa90 / pa120 (live_plant): the planted foot pivots on the ball.
- T step up (ter_drop_walk 28 cm): lead foot fine (V2.31 steplift); the TRAILING foot leaves the low ground early (z 0 -> 7 cm while the
  capsule rises 28 cm in 0.17 s, leg reach) and swings 17 cm over the step top; the visible pelvis needs 0.9 s to follow the capsule rise
  (~20 cm below its normal height for 0.5 s) -> high-knee hover look. Next: FootPlacement pelvis settings (fpprobe232.py).
- IsUnique assertion: SLevelViewport::EndPlayInEditorSession check(GameViewport.IsUnique()) = another holder of the PIE FSceneViewport shared
  ref at PIE end. 4 / 2038 runs over all logs (3 / ~450 in V2.31, 0 in ~1000 V2.29-V2.30 runs); crash runs were not captures (MediaCapture is
  the only shared holder in the enabled plugins' source); no engine PDBs (callstack unsymbolised). Soak study piesoak232.py (bare PIE cycles
  vs harness end path) planned.
- B1 camera (same editor, fixed 30): orbit is VISUAL ONLY - capsule path / control yaw / travel direction relative to the control yaw identical
  to production in every scenario (d_pos 0.0 cm, d_ctl 0.00 deg; cam_corr 6 deg = one-frame timing of a scripted 360 look). Realised orbit
  (c1s / c1 / c1l): sprint 90 deg turn 7.6 / 11.5 / 16.4 deg, brake + second request 6.4 / 9.7 / 13.9, wall turn 3.6 / 5.4 / 7.7 (side
  room), jog 1.5-3.2, walk 0.2-0.7, mouse look <= 1.3, idle look / corridor / inspection / mouse 180 flick / sprint 180 = 0. Jerk95 and the
  min camera-capsule distance unchanged. BUT the arc builds AFTER the body turn (lag 0.8 + smoother ~1.3 s): 3/4 time unchanged except the
  left turn (0.40 -> 0.67 / 1.20 s). Round 2 (B5): lag 0.3, smoother 5 rad/s, sprint 16 deg (c2), body-only (c2b).
- B2 tick order (tk, live) vs o: swl12 11.6 -> 52.6, s180 35.9 -> 71, wstart 14.2 -> 33.7, d_sprint 16 -> 27, e29_chain 25 -> 34, 4900
  15 -> 24 (worse); j30_slow 38 -> 26, c29 49 -> 46 (better). REJECTED: the system is tuned around the one-frame lag (V2.28 lead frames,
  CP gates). The existing owner is the V2.0 flag IntentTickPrePhysics (rejected 2026-10-14 for the same reason; B9 re-checks it).
- D isolation: c30_calm 33.3 (o) = 33.3 settle off = 32.4 FootPlacement off = 32.3 all IK / warping off -> NOT a runtime layer; the clip's
  closing step skims the floor (stopfix232 minclear dry: low travel 15-33 cm in many walk stops, max lift needed <= 2.2 cm).
- C backward / turn starts: the start bind (sb) works where it is on (planted foot 1-3 cm/s) but the slide is mostly the idle -> start
  BLEND: the AAMS-derived JogQ starts begin 16 cm per foot away from the production idle stance (CP2 / LS / RR starts 4-11 cm), + 2-4 cm
  drift inside the clips before the first lift. pinstart232 (ball pinned at the idle ball until the lift, hand-over 0.3 s) queued (B11).
- Loaded family: B_F loaded (gen231_loaded defaults) 32 / 32 pass the gate; F_B P29 passes with b_short 16; P21 / P30 fail any variant
  (the plan double-lands the other foot) -> production F_B P21 / P30 as the safe fallback inside PSD_SHM231L_LoadRevFwd (build_v232_dbs).
- B_F end-of-clip blips: owner = the B_F DBs hold no forward exit loop (F_B DBs hold theirs: no F_B blips) -> PSD_SHM232_*RevBwdX (+ fwd loop),
  A/B bfx / bfxl in B10.
- Upper body audit (upper232, straight stages): walk arm 27 cm / head lateral 4.5 cm / trunk +4 deg; jog 40 / 9 / 11; sprint 60 / 14 /
  29 deg forward lean (+ -5 -> 32 deg into the sprint) -> B7 owner isolation (PBI / curve lean / settle / spine counter / raw).
- T step up (terrain232, S1): pelvis lag max 27 cm, settle 0.97 s; trailing foot 11 cm over its landing ground, 0.13 s hover. T6 DSL
  (SwingPelvisComp: swing target lowered by the pelvis lag, floored at path ground + margin) written, build pending.
- B4 pa90 / pa120 NOT_TRIGGERED: qa_pie live_plant failed (PlantSettings_Walk is not editable on the anim instance) -> results identical
  to o. Re-run as pb90 / pb120 through the ABP CDO (qa_pie abp_flags '<struct>.<field>', restored per run) in B12.
- Automation: the A/B memory guard restarted the editor at ~02:41 (private memory 35-39 GB) under the log name shmv21_a20.log (v21 lib
  naming); the runs continued in the same fixed-30 mode (FPSCHECK ok). Log greps must cover every session log.
- B5 camera round 2: c2 (lag 0.3, smoother 5, sprint 16) - the arc now starts inside the turn (beta 1.4 / 4.5 / 9.7 / 13 deg at 6.2 / 6.6 /
  7.2 / 8.4 s of cam32_s90), max 13.7 (sprint 90), 12.9 (brake + second request), 8.2 (wall), left-turn 3/4 time 0.40 -> 0.93 s; jerk95 /
  min distance / look windows unchanged; c2b (body only) differs only in jog strafe (0.4 vs 2.3) and analog. Sprint 180 = 0 by design: the
  jog / sprint reversal families are STRAFE (alpha -6..-9 deg all through: the body keeps facing the view and runs backward).
- B8 stopfix minclear written in place (29 owned stop clips, checkpoint pre_v232/.../Stops): NO measurable effect (c30_calm 33.3 -> 33.4;
  the in-game dip is in the MM OUTPUT pose: mx ball -6.1 vs clip). -> revert the clips from the checkpoint at the session end (unverified
  change); owner isolation round 2 (PBI off / brake posture off) + T7 swing floor guard (fg) in C1.
- B9 IntentTickPrePhysics (existing owner) = the live tk result (e29_load 14.0, j30_slow 26.1, c29 45.6 identical; blips 15 -> 6) ->
  tick order REJECTED (B2 regressions swl12 / s180 / wstart belong to it).
- B10 B_F exit-loop DBs: blips (10 runs) o 18 / bfx 13 (B_F->B_F->jog loop gone) / bfxl 8 (every B_F->B_F blip gone; the remaining:
  slow family -> J2S (its X DB had only the walk loop: jog loop added for the P build) and start blips); worst-slide numbers equal within
  the noise. bfxl = production B_F DBs with the exit loop + the loaded B_F catch-step family.
- B11 pinstart (in place, 17 JogQ starts): idle backward starts 38 -> 22 (j30_slow 37.9 -> 22.0 / +sb 19.9, jback / d_back 38 -> 21.8) but
  non-idle starts worse (j30_rel_3200 35 -> 54) and turn starts worse (jstart 48.6 -> 68.9). The remaining first 0.1 s = the START blip
  (vendor af_Loco start one frame). Second form (C1 pre-step): idle-stance COPIES SHM232_IS_* of the 9 straight starts next to the restored
  originals in the same start DBs (Motion Matching chooses by pose: idle stance -> copy, other poses -> original); turn starts unchanged.
- B12 pb90 / pb120 (applied: 'SHM_STATE candidate touched PlantSettings_Walk.unplant_angle'): every metric identical to o (pivot counts
  too) -> the unplant angle is not the gate: the blended foot speed exceeds SpeedThreshold 60 so FootPlacement never plants that foot at
  the MM switch. E stays OPEN (owner = the blend at the directional switch with a planted foot; no promotion).
- C1 pre-step: the IS copies joined the start DBs (in_db true) but the quit was REFUSED (dirty: the 6 start DBs updated in memory + the
  ABPs touched by the struct-field abp flag): saved the 6 start DBs (PSD_SHM_JogStartQ_L/R, JogStartS_L/R, SprintStartT_L/R), reloaded the
  ABPs / DA, C1 restarted without the duplicate step. Rollback of the IS copies = delete SHM232_IS_* + re-save those 6 DBs (their earlier
  state was not checkpointed: the copies are the only change in them).
- CHECKPOINT GAP (own mistake): stopfix232 scanned /Game/GraceRanger/Animations too; 6 clips outside SHME/Stops were written (minclear,
  04:10) without a checkpoint copy: 4 A_CT_Sample_M_Relaxed_* (SampleCandidates, no referencers: inert) and A_CT_Ref_Walk_Stop_F_L/R
  (SampleReference, referenced by both ABP_GR_MotionMatchingBase assets). Change = swing-foot lift <= 1.2 cm on part of the closing step,
  legs re-solved (leg guard passed). Not exactly reversible (no copy; OneDrive version history is the only source). Kept and reported.
  Rule: checkpoint every folder a generator SCANS, not only the target folder.

## 07:15 LastHitBy in the orbit block (CRITICAL camera finding) + P1 aborted
- Since the orbit install (b1b 02:41) every PIE frame logged 3x `Accessed None ... LastHitBy (Pawn)` at Set CamOrbitTarget / LookT / PrevCtl
  (SHM_UpdateCameraV21): the DSL line `(Piyon|GetControlRotation :self OwnerChar)` was translated as Controller::GetControlRotation(self =
  Pawn.LastHitBy) - the V2.21 MontTick translator bug again. Control yaw read 0 => orbit target = sin(body yaw vs WORLD X), look gate dead.
  The harness runs with yaw0 = 0, so the c1/c2 camera numbers looked plausible; a player whose view is not at world X would get a constant
  orbit when running straight. ALL earlier camera evidence (b-series) is therefore invalid and is re-measured in P2C (incl. yaw0 30 invariance).
- Side effect: ~3 error lines per frame (~100k per editor log) = log-text memory growth (V2.30 owner) -> the 38 GB memory restarts.
- Fix: Tools/SHME_V232_20261027/fix_v232_lasthitby.py (V2.21 patch on the component graphs, saved) + build_funcs.py now re-applies the
  patch after every function rebuild. Checkpoint: checkpoint/pre_lhb232/BP_SHM_HumanMotionComponent.uasset.
- P1 aborted: run232_p1.sh had been started twice; instance 2 queued bfx_write2 (DB rebuild) at 06:43:55 into the running P PIE session
  -> game thread frozen at frame 72, run TIMEOUT, runner hung from 06:50 (post_check / qa_pie jobs pending). Editor killed 07:12 (reason
  logged), all chain shells stopped. The X DBs were already written correctly by instance 1 (06:42); IS copies neutralised 06:43.

## 10:45 P2 / F / ISO -> PROMOTE_GO (camera, bfexit, loadedbf, floorguard)
- P2 (fixed 30, interleaved, 2 rep, 27 scenarios): o median 20.3 / >20 cm 28 of 54 / blips 82 -> P 16.1 / 23 of 53 / 57. Big wins: e29_chain
  25.4 -> 6.5, e29_load 15.0 -> 6.5..12.4, 4750 15.5 -> 6.5..11.1, 4900 15.0 -> 11.1..13.6, c30_calm 33.3 -> 17.9, a29_angb 33.5 -> 21..23,
  cam32_brk2 16.5..19.3 -> 11.1..11.5. Apparent regressions: c29_combo 48.8 -> 57.6, j30_rel_3450 24.5 -> 27.3.
- Camera after the LHB repair: body independence d_pos 0.0 / d_ctl 0.00 / d_vin 0.0 in all 12 camera scenarios; orbit 13.7 (sprint 90),
  12.9 (brake + 2nd request), 8.2 (wall), 2.3 (jog 90), 2.2 (analog), 0.5 (walk 45), 0.1 (mouse look), 0 (idle look / sprint 180 strafe);
  view-heading invariance: cam32_s90y (view turned 30 deg by real look input) orbit 13.7 = cam32_s90 13.7. (yaw0 is ignored by the open-loop
  IA look -> first s90y run was a plain s90.)
- F (o vs P, 10 scenarios): median 60 25.1 -> 16.3, 120 29.8 -> 16.3, 20 16.5 -> 9.0, real 28.7 -> 14.2; blips 27->10 / 9->9 / 19->11 /
  12->5. e29_chain 60: 26.1 -> 19.8; e29_load 120: 29.8 -> 15.3; 4750 20: 21.9 -> 7.0. j30_rel_3200 worse at 120 (14.1 -> 34.8) and 20
  (30.9 -> 38.0), better at real (30.7 -> 23.8). Orbit identical at every fixed FPS (13.7), jerk95 unchanged; real-time jerk max spikes
  (36.8 / 61.6) sit on frame hitches (previous dt 0.09-0.15 s) with orbit 0 at that frame.
- ISO (fixed 30, o / fg / bfxl / Pnf / P, 2 rep): c29_combo owner = fg alone (48.8 -> 57.6, bfxl / Pnf = 48.8). BUT the max ball difference
  o vs fg over the whole run is 3.9 cm and the defect window (vendor walk pivot -> A_LB_Walk_Left) is frame-identical: the worst-episode
  number changes because the contact classifier segments the episode differently (start i0 260 vs 272). Not a physical regression.
  j30_rel_3450: fg alone 19.4 / 24.5; P vs Pnf diverge after the first step (80 cm path split at 6.4 s, MM branch) and the worst moves to a
  later stop clip -> branch divergence, not an owner.
