# V2.31 working notes (for the report; chronological, raw)

## Session 1 (2026-10-26 14:19 ->)
- p0: fresh fixed-30 editor, verify_p0 (V2.30 expectations) ALL_OK. Checkpoint pre_v231 (101 assets + tools, 114 MB).
- swl12 bimodality: same-input V2.30 runs differ from PIE frame 2 in 2/38 cases (FeetIK output curve SHM_HCo_ik_foot_l_RX 5.7592 vs 6.10)
  and, even with an identical start, from the move start (t 2.20, PelvisOffset 10 um) -> first sprint pivot Rfoot vs Lfoot vendor clip ->
  A_LB_Walk_Bwd at a different loop time -> B_F P29 (6.6 cm) or P6 (46.5). The game is sensitive to tiny differences; content must be
  safe for either selection. Not the owner: anim tick (pawn meshes already AlwaysTickPoseAndRefreshBones, URO off; Face only when rendered),
  real time (only perf laps). Open: tick ordering / unknown.
- swl12 P6 owner: the 245 cm/s jog B_F design entered from a back-WALK at -63 cm/s: planted foot 2-4 m/s drag at floor level (DRAG) + the
  clip-bound capsule jump -18 -> -86 cm/s (DesV of the 245 design at ct 0.19).
- e29 60/120 FPS: all SPRINT exits of an authored B_F clip go to the V2.14 post-reversal window (PSD_SHM214_RevPush, push stance re-entry
  for vendor pivots) at every FPS (12-42 cm exit slides); at 60/120 the B_F hold ended one frame before the next S, so the F_B entry blended
  from the RevPush pose (h60 e29_load: 36.9 cm DRAG/SLIP at 6.92).
- slope sprint 175: TIP montage end frame with the request back and velocity 0: ABP family still 0 (component start family 4 one frame
  later) -> original chooser -> PSD_Dense_Stand_Sprint_Pivots one frame (M_Neutral_Sprint_Turn_L_180_Rfoot @1.10) -> head 29/18/16 cm.
- step-up hover (ter_drop_walk 28 cm): CMC step-up raises the capsule 28 cm in 0.13 s, SwingLift (capsule-relative) decays only with
  tau 0.12 -> swing foot to 21 cm above the step top, 0.43 s hover. Step-down: capsule stays on top until its centre is 37 cm past the edge
  (perch), leading foot lowered only as fast as FootPlacement lowers the pelvis (38 -> 2 cm in 0.5 s).
- rear diagonal: steady -112.5 = RearLeft + OW 22.5 deg: no planted slip in the steady state; the drags (22-33 cm) are in the -90 -> -112.5
  TRANSITION (OW changes while a foot is planted + MM Left -> RearLeft switch).
- support_slide (reauthor230): metric error (lower foot incl. swing; anchors move into swing). slide231.py audit in B1.
- contact231.py: SKIM/PIVOT/SLIP/DRAG classifier on visible balls; the V2.30 'all-clip slip' mixed pivots/skims. Production defects outside
  reversals show up: SHM_A_CP2_Jog_Fwd_Stop 27-30 cm (final stop), Jog_Bwd_Start 32-54 cm (release cases, j30_slow), c29_combo walk L/R
  direction change 46-49 cm, c30_calm walk stop 22-33 cm.
- automation: editor CRASH (Assertion GameViewport.IsUnique(), SLevelViewport.cpp:5196, at PIE end) during A1 after swl14_s1; v231_ab
  relaunched WITHOUT -UseFixedTimeStep (V219_EDARGS only exported inside relaunch()) -> rest of A1 and all of A2 ran variable-step: invalid,
  A2 rerun (A2B). Fixed: lib231 exports the mode by default, v231_ab relaunch uses editor_launch230 + RELAUNCH_ARGS log + FPSCHECK per run.
- exec rewire traps (twice): disconnect() of an exec input drops ALL sources -> a production path skipped (exitpush_b: IfThenElse_8; inspect:
  PerfLapCam ELSE path). Repaired (fix_v231_exitpush_c, fix_v231_inspect_tick). Rule: print exec_in before/after every rewire.
pending qa.sh fast-fail edit (file locked while a batch runs) -> apply between batches
