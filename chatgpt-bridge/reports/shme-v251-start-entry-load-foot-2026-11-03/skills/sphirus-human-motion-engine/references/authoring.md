# Authoring SHME graphs (Blueprint-only project, Turkish editor locale)

No C++ toolchain is installed (no Visual Studio/MSVC; no `Source/`), so SHME is Blueprint. Graphs are generated, never hand-wired:

- `Tools/SHME_V1_20260925/shm_src.py` — function sources in an authoring dialect (Lisp-like).
- `shm_dsl.py` — translator from the dialect to the editor_toolset graph DSL (`BlueprintTools.write_graph_dsl`).
- `shm_build.py` — create assets/variables, rebuild a function (clears the old body), **chain exec pins**, check `LogScript` errors.
- `build_profiles.py`, `build_comp_vars.py`, `build_funcs.py`, `build_tick.py`, `install_camera.py`, `install_body.py`, `attach_comp.py`.

## Locale/tooling traps (each one broke graphs silently at least once)

1. Every DSL built-in (`+ - * / < > and or not select if .x .yaw self`) expands to an ENGLISH node ID that does not exist in the Turkish editor. The translator lowers them to localized nodes (`İşlevsellikler|Operatörler|Ekle/Çıkar/Çarp/Böl/Küçüktür(<)…`, `Matematik|Boolean|ANDBoolean…`, `SelectFloat/SelectVector`, `DotProduct` with unit vectors).
2. The DSL cannot see exec pins here: `if`, sequences and multi-exec continuations fail ("Available: []"), and even plain statements come out **unconnected**. `shm_build.chain_exec` connects entry → every exec node in creation (= statement) order. Keep function bodies straight-line; put all branching in `SHM_Tick` (built with `qa_graph` branch nodes).
3. Promotable operators reject literals on untyped wildcard pins → the translator wraps literals in `MakeLiteralFloat/Int/Bool`.
4. Promotable operators propagate types: a scalar node used once in `vector * scalar` is retyped to a vector and breaks its scalar consumers. Use `(vscale v s)` (typed `Lerp(Vector)` from zero) for vector×scalar.
5. Pure nodes re-evaluate per consumer. A `bind` that depends on a variable later `set` in the same function reads the NEW value in consumers after the set. Store to a variable first, then read the variable (see the fixed PrevBall/LandingTimer/spring code).
6. Variable node IDs drop underscores (`GR_SHM_BoomScale` → `Değişkenler|SHM|GRSHMBoomScaleAl`) and include the variable category; the setter pin keeps the real name.
7. `BreakRotator` outputs single-precision floats that will not connect into double operator chains; compute yaw from vectors with `Atan2(Degrees)`.
8. The log is buffered: flush (`FLUSHLOG`) before reading `LogScript` errors, and also treat "1 node" results as failures.
9. Exec casts/`self` via DSL fail; do the owner cast in `SHM_Tick` with `qa_graph.G.cast`.
10. A component added to a pawn must have `bAutoActivate=true` on the class CDO **and** on the pawn's component template, or it never ticks.
11. Adding a component to a loaded pawn (SCS change) reinstances it; AAMS `BP_Timeline` then holds TRASH_ camera/boom references until the editor restarts. Restart before camera QA after any SCS change.

## V1.2 authoring notes
- Edge memories: `bind` is pure and re-evaluates per consumer; write `(set Prev X)` after the last use of the edge.
- AnimGraph edits from Python: `B.create_node(graph, type_id, IntPoint)`; configure via `node.get_editor_property('node')`
  (struct copy, set fields, write back); wire with qa_graph `connect`; keep an install-state json for idempotency and never
  delete nodes present in the checkpoint dump (`Saved/Codex/SHME_V1_20260925/Graphs/*AnimGraph.txt`).
- Per-frame AnimBP work belongs at the end of the BlueprintUpdateAnimation chain; CP_UpdateTransitionContext is conditional.
- Owned clip copies: duplicate, bake with `controller.set_bone_track_keys` (evaluate with AnimPoseExtensions per frame), remove the
  inherited BranchIn track, add BranchIn + ModifyCost, save the clip and the database, `PoseSearchLibrary.clear_pose_search_databases_management()`.
- Bash heredocs cannot carry `'''`; write scripts with the Write tool.

## V1.3.1 authoring notes
- Object / class pins: never `arg(node, pin, <UObject>)` (str() of the object is rejected silently). Use a typed member
  variable (`ensure_vars` with a UClass + `set_defaults` + `connect(g.get(var), pin)`), or a path string for class pins.
- `KismetMathLibrary:Add_VectorVector` spawns a K2Node_PromotableOperator (qa_graph asserts); use
  `TransformLocation(MakeTransform(offset), v)`, `Lerp(Vector)`, `SelectFloat/SelectVector`.
- Empty PoseSearchDatabase: `DataAssetFactory(data_asset_class=PoseSearchDatabase)` + `create_asset`; set `schema`,
  `normalization_set`; entries come from BranchIn notifies; register in the normalization set's `databases`.
- Installers must create every variable they read in the same script; a failed installer leaves partial graphs: run the
  reset (`fix_mm_routing.py`) before re-installing and never re-dump the graph in between.
- Do not compile or save while PIE runs (both fail silently); kill chains, then `stop_pie` + `post_check`, then mutate.

## V1.3.7 authoring notes (2026-09-27)
- Baked clip edits (project-owned only, backup first): `v137_bake_seg.py` (lower / upper trunk pitch toward idle->loop
  ramps, keep fractions, fade-in, settle tail, roll mode, pelvis height target; legs re-solved), `v137_stance2.py`
  (AAMS "ready" stance -> project quiet stance: body yaw, squared feet with toe yaw on the swing schedule, smoothed
  pelvis drop for reach), `v137_stopsettle.py` (curve `SHM_StopSettle`). Helpers in `v137_animedit.py`.
- UE 5.8 Python: `AnimationDataController.set_bone_track_keys` takes Array[Vector] / Array[Quat] (double);
  `unreal.Quat4f` is opaque (no fields, no ctor args).
- ChooserTable rows are not exposed to Python: reroute databases through SHME-owned variables
  (`SHM_TurnDB` -> `PSD_SHM_TurnInPlace`) instead of editing `CHT_GR_PlayerDense`.
- AnimGraph `ShowPinForProperties` can be set from Python but the pin only appears after a node reconstruct (no API):
  use nodes whose pins exist by default (SequenceEvaluator `ExplicitTime`) and drive time from the snapshot.
- The AAMS stance family (idle / turns / walk starts / stops) is a staggered 53 cm "ready" stance with the hips and
  shoulders yawed 17-21 deg off the root; the project quiet stance is 28 cm square, toes -16 / +20, hips on the root.
- Pawn Blueprint chain: `BP_PBI_Player` -> `/Game/GraceRanger/BP_GR_Player` (asset registry ParentClass); the Sandbox
  `BP_GR_Player` is not in the chain.

## V1.3.8 authoring notes (2026-09-27)
- PoseSearch (UE 5.8 PoseSearchDatabase.cpp): a database entry synchronized from a `PoseSearchBranchIn` notify takes the
  notify range as its SamplingRange; a sequence entry is LOOPING only if SamplingRange is (0,0), i.e. the notify covers the
  whole clip (start <= TriggerTimeOffset, end >= length - offset). BranchIn authored `0..length-0.001` made every loop in the
  SHME redirect databases NON-looping; a redirect episode then created a non-looping player that the loop database kept as
  continuing pose -> clamped on the last frame for 5-133 s (sprint freeze). Always author BranchIn on loops as `0..length`
  (`install_loop_branchin.py`, audit with `v138_branchin_audit.py`); verify with a T3D export (no SamplingRange on loops).
- The PoseSearch DDC key ignores AnimNotify edits: after changing notifies, re-key the database (e.g. a tag) or the old
  index is served "From Cache". A database re-syncs its BranchIn entries in PreSaveRoot, but the full sync keeps orphan
  entries of clips that no longer reference it; entries cannot be removed from Python (protected array).
- A positive ContinuingPoseCostBias penalises continuing: two identical clips in one database then alternate every search.
- Standing-turn clips live in BP_GR_Player.GR_UpdateIdleTurn (8 stand literals + 90 deg Select), gated by a look-settled
  check (`TW_LastLookTime` older than 0.15 s, or |delta| >= 157.5 deg) since V1.3.8.

## V1.3.9 (2026-09-27)
- Curved sprint: straight loops cannot hold a sprint plant on an arc; use the project curved loops (`v139_curve_bake.py`:
  root arc, mid-stance pinned balls, leg re-solve) behind the SHME curve route (`SHM_CurveActive` / `SHM_CurveRate`,
  steadiness gate, bucket-lock throttle, play rate 0.813). The same solver at zero curvature pins straight loops; a stance
  crossing the loop seam is merged into one pinned stance (`seam_merged_*`).
- MM play rate = capsule speed / the database-indexed root speed: after a root-track edit re-key the database
  (`v138_dbrekey.py`, `REKEY_TAG`) or nothing changes.
- Jog starts: never the AAMS `M_Neutral_Run_Start_*` (dash, trunk 57 deg); use the quiet-stance `SHM_JogQ_*` copies in
  `PSD_SHM_JogStartQ_<first swing foot>`.
- Stops: `SHM_StopGait` (snapshot, speed hysteresis, latched at release) gates the CP forward-stop route: >= 0.5 jog stop,
  >= 1.5 run stop (`PSD_RR_Stop`), walk falls through to the chooser's walk stops.
- Camera: the GR rig ignores the SpringArm; distance = `GR_AnticipatedArm`. The shoulder handed to the rig is scaled by
  SHME's shoulder-side clearance (`GR_UpdateSHMSignals`, 0 at <= 60 cm, 1 at >= 150 cm).
- DSL routing: write a state variable before resetting its timer when a re-evaluated bind consumes both (the P8
  recovery lock).

## V2.7 authoring notes (2026-10-15)
- Lengthening a loop clip in place: `controller.set_number_of_frames(FrameNumber(N-1))` then `set_bone_track_keys` with N keys for
  every track; float curves: `AnimationLibrary.get_float_keys` -> `remove_curve` / `add_curve` / `add_float_curve_keys` per cycle;
  re-author every PoseSearchBranchIn state 0..new length with the same database, save clip + database, re-key with a NEW tag.
- Posture bakes that raise the pelvis must respect leg reach: roll a planted foot about its ball (heel lift) before clamping the
  raise; a stretched rear leg may lift vertically (early toe-off) - never move a planted ball horizontally.
- Re-baking from originals: restore the checkpoint .uasset files only with the editor CLOSED; use a new database tag afterwards
  (an old tag can serve a cached index of the earlier bake).

## V2.9 authoring notes (2026-10-16)
- v137_animedit.solve_leg with a knee hint can bake knees bent BACKWARD / rolled off the hinge (76 owned clips): after any
  leg bake run the hinge scan; v29_knee_repair.py fixes the knee plane to the foot-Z hinge keeping the foot transform exactly.
- Vendor turn / pivot content (open the clip, not the name): Run_Turn_* 515 -> 319 cm/s, 2.2 g at clip rate, 26-33 cm brake
  dip, not in any live database; Sprint_Turn_*_090 721 -> 518, turn 10-90 % in 0.8 s clip time (~1.2 s at the project's
  490 cm/s), pelvis dip 16-21 cm; stance balls roll 13-50 cm/s at clip rate (within FootPlacement's plant threshold at
  the project's play rate). Walk turns 7-10 cm/s, pivots ~15 cm/s.
- A support-step turn clip only plays through when the capsule turn follows it: GR caps (TurnLatAccelMax 1400) turn a
  sprint 90 cut in ~0.65 s, the vendor clip needs ~1.2 s; the bridge then leaves mid-turn.
## V2.10 leg solver + leg guard (2026-10-16; Tools/SHME_V1_20260925/v137_animedit.py)
- `solve_leg` (all 11 leg-bake call sites import it) now builds thigh and calf as full frames (`q_from_two`: bone direction + local Z =
  knee-plane normal) and takes the plane from the knee hint only while it is reliable: near-straight (hint offset < 0.2 thigh length) or
  > 25-45 deg off the foot's lateral axis turns it smoothly to the foot axis. Legacy kept as `solve_leg_v137` for A/B only.
  Evidence: production V2.8 generator, same inputs: legacy 26 / 26 clips with backward knees (3-36 frames), new 0 / 26, foot error /
  drift / pelvis identical.
- `leg_guard` runs in `write_tracks` (and in v28_gen_startstop.write before an asset is created): refuses backward / off-hinge knees
  (hinge >= 0.85 where flexion >= 8), hinge-axis disagreement (thigh Z . calf Z >= 0.90), per-frame hinge-axis jumps (> 60 deg, or
  > max(25, 1.2 x the source's own) with a source), bone length change, foot error. Thresholds from 259 vendor clips (hinge min 0.97,
  axis 0.95, jump max 51 deg in fast 180s). A write that fails raises LEG_GUARD_FAIL; pass guard=False only with a stated reason.
- Repair of existing clips: `Tools/SHME_V210_20261016/v210_knee_repair.py` (V2.9 method + axis criterion + near-straight criteria:
  calf-Z vs foot axis > 35 deg, knee OFFSET vs toes > kt_max) keeps the foot transform and flexion exactly; writes through the guard.
- Traps: the hinge metric is blind below 8 deg flexion - roll flips of a near-straight leg (V28 walk stops 112-134 deg / frame, walk loop
  88) and inward knee offsets (stand idle) only show in the axis jump / knee-offset tests; a guard refusal on an UNTOUCHED leg means the
  source already carries the defect (A_SHM28_WalkStop_P00 -> regenerate, do not force).

## V2.11 arm carriage bake (2026-10-16; Tools/SHME_V211_20261016/v211_arm_bake.py)
- Arm-chain-only re-authoring (clavicle / upperarm / lowerarm / hand); root, pelvis, spine, legs, twist bones, curves untouched; a
  readback after the write must show 0.0 deg / 0.0 cm on root / pelvis / spine / legs (the leg guard is not involved).
- Bake from PRISTINE copies (`/Game/ActionAdventureMovementS/Rollbacks/SHME_V211_Arms_Before_20261016/`, copied from the checkpoint
  files and scanned with `scan_paths_synchronous`): every re-bake starts from the original keys, so iterations are idempotent.
- Trap (verified on capture): idle LOCAL rotations are only transferable for the ELBOW / WRIST (lowerarm, hand). Copying the idle's
  clavicle / upper-arm locals onto a clip whose chest is pitched / rolled differently pushed the hands 18-30 cm behind the body ("arm held
  back") and opened one arm while closing the other. The shoulder chain keeps the clip's own sagittal hang; the CARRIAGE (upper-arm
  abduction against the trunk: pelvis->spine_05 axis, spine_03 lateral axis) is driven by a rotation about the trunk forward axis toward a
  target path (idle carriage -> loop mean carriage), smoothed (gauss 4 frames) so the clip's swing stays. Check the sagittal hand offset
  (trunk frame) before / after in every dry run.
- Loop outlier lift: per side, frames whose abduction is > 1 deg below the average of the SAME gait phase in the other cycles (phase =
  nearest leg pose around f + k * period) are slerped toward that phase average; wide / normal frames untouched, means unchanged.
- In-place turns: shoulder chain damped around the clip's own rest (k clavicle 0.3, upper arm 0.4), elbow / wrist from the idle with
  damped motion (0.5 / 0.6), rest carriage re-seated to the idle's trunk-frame abduction. Steps / timing / legs untouched.
- DSL trap: a function created in memory by a FAILED attempt keeps its name after the package reload (until GC); the next
  add_function_graph makes `Name_0` and `(fn Name ...)` finds no entry ("AddEvent|Name does not exist"). Use a fresh name, call
  `collect_garbage()` after reloads, and assert the entry type_id `|Name` before writing the DSL (install_v211_push.py).

## V2.12 contralateral arm floor + bake-source / database traps (2026-10-17; Tools/SHME_V212_20261017/v212_arm_bake.py)
- A loop whose arm narrows in EVERY cycle at the same gait phase is not fixed by the V2.11 outlier lift (it averages the narrow phase with
  itself). Floor mode: per side, target abduction >= (mean of the CONTRALATERAL arm half a cycle away) - 1.5 deg, cap 12.5, lift-only,
  cyclic gauss smooth 3 frames; rotation about the trunk forward axis at the upper arm, 3 iterations (target error <= 0.05 deg, sagittal
  hand change 0.0 cm). Runtime R phase-3 per cycle 8.1/6.5/7.8/9.1/6.2 -> 10.6/11.4/12.3/12.9/11.1 deg, swing kept (9-17 deg).
- Starts must end on the loop carriage AT the handoff phase (loop_abd_at_phase), not on the loop mean.
- TRAP: a loadable bake-source copy of a clip that carries PoseSearchBranchIn becomes a SECOND entry of the production database on the next
  sync. Strip BranchIn from source copies (remove by name + a REAL property change; set_editor_property with an unchanged value sends no
  PostEditChange - setting the orphaned BranchIn object's Database to None did fire the sync) and list the database entries after every
  copy / bake. Owned copies of vendor clips (V2.12 gait push / cut reversal) also carry the vendor BranchIn (e.g. PSD_SM_LocoTransitions):
  drop it on the copy and add one to the owned database.
- DSL trap: `bind` creates a pure node that re-evaluates at EVERY consumer. A value read after a `set` it depends on changes meaning
  (v212f: `revNew = (and revNow (not RevOn))` consumed after `(set RevOn ...)` was always false). Latch such values into a member before the
  dependent `set`.
- Graph-edit trap (UE 5.8): `Multiply_VectorFloat` is created as a promotable operator node (the qa_graph helper rejects it); scale a vector
  with `VLerp(A = 0, B = v, Alpha = s)`. A failed in-memory graph edit of BP_GR_Player cannot be discarded by reloading the class package
  (CDO references null): restart the editor without saving (v2_editor_restart.sh).

## Brake pivot crouch bake (2026-10-17; Tools/SHME_PIV_20261017/piv_bake.py)
- A pelvis-floor raise alone barely moves a braking pivot: at the plant the stance is 75-80 cm wide and the braking leg is straight, so
  the leg-reach clamp allows +1.5-3.4 cm at the critical frames. Shorten the braking stride first: `foot_shift` moves the FRONT (braking)
  foot toward the body along the heading (-20 cm) with smoothstep ramps ONLY inside its swing windows (check ball height per frame) and a
  constant offset through the stance -> no added slip (root yaw constant in the clip, so a component offset is a world offset); then the
  pelvis floor (90 cm, keep 15 % of the dip, reach 0.995) raises 9-11 cm with feet on the new targets, leg_guard on write.
- A low swing (ball 4-5 cm) still counts as swing for the shift but the raise envelope can bump: use rz_smooth 4 there and check the
  ADDED raise step per 0.1 s (<= 3 cm), not the absolute pelvis curve (the source bob is in it).
- Project-owned copies (A_LR_*, A_CP2_*) are baked IN PLACE with a file checkpoint outside Content: no new asset, so no BranchIn copy
  trap; verify the database entry lists after the write (unchanged, verified).

## Push arm-drive damping (2026-10-17; Tools/SHME_V212_20261017/v212_push_posture.py arm_damp)
- The walk->sprint drive's hand excursion was 1.4x the sprint loop's: `arm_damp` pulls upperarm / lowerarm local rotations toward a
  +-arm_win (14 keys) hemisphere-aligned mean quaternion by (1 - arm_damp) inside `arm_range` (normalized clip time, smoothstep edges);
  timing kept, amplitude 0.6x. Measure the result at RUNTIME with armswing213.py against the loop windows of the same run.
- Dynamic-montage root motion drives the capsule translation but the GR pawn keeps writing the actor yaw: a root-motion turn montage
  while moving reads as a moonwalk unless GR yields the rotation while the slot is active (open).

## V2.22 authored upper-body performance (2026-10-22; Tools/SHME_V222_20261022/)
- Diagnose in the CHARACTER frame first (body222.py: head / chest / hands relative to the visible pelvis in the actor-yaw frame, ball
  heights): world direction changes hide the body's own swing. clipscan222.py does the same per clip in root space - compare the
  candidate clip with the loops it hands to (walk / jog / sprint envelopes) before deciding the owner.
- Walk start (gen222_start.py = the V2.8 contact-planned start with a NEW upper body): legs / root / timing unchanged (the installed
  SHM28 distance clock is built from that root curve, keep length + root identical); arms only on a PHASE-COHERENT virtual loop
  clock (toe-off of the stepping foot at T_LIFT -> its heel strike at t_hs), amplitude idle -> loop monotonic (no parked arm, no
  second opening); trunk / neck / head keep the root-consistent path; a designed initiation lean (6 deg about the lateral axis at
  spine_01, peak ~0.35 s, gone by t_hs + 0.3) answers the runtime's backward drift at start onset. Generate from the idle time the
  game actually starts from (68.0 s, not 7.0 s: 5 deg trunk difference). Swap clips through the ABP object variables
  (SHM28_StartL / _R) - the harness sets object vars from '/Game/...' strings.
- Re-acceleration (rb222_revturn.py): keep legs / root / pelvis (readback 0.0 cm), replace spine / neck / head / arms with the jog ->
  sprint loops (blend by the clip's own root speed) at a phase taken from the LEGS of every frame (fore-aft foot separation + its
  slope matched to the loop table, unwrap, monotonic with a 2.2x rate cap, gauss sigma 2); swing amplitude about the loop mean = the
  clip's local stride / the loop's; spine_05 heading-frame orientation = the loops' (residual at spine_01); keep 0.5 of the source
  chest-vs-pelvis twist, applied about the TRUNK axis (a world-vertical rotation swings the lean sideways); entry blend 0.50 -> 0.95 s.
  Traps: heel-strike anchors fail on re-plants (same foot twice = full-cycle jump -> flail); skipping them parks the arms 0.8 s.
  Cache the ORIGINAL keys to JSON once (in-place bakes then always start from the source). Re-key every database a BranchIn points to
  (new tag per bake) and run a warm-up before measuring (first use selects None while the index rebuilds).
