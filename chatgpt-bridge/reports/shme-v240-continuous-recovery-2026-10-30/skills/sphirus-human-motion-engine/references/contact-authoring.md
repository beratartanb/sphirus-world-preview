# Contact-preserving animation authoring and retarget (C)

Use when a start / stop / turn / step clip must be created or corrected so that feet, root and body agree — including the
decision to MOVE footfalls. Diagnosis first (`motion-diagnosis.md`); acceptance in `sphirus-character-camera`.

## Inputs to collect
- The capsule profile the clip will be played against (speed vs time after the input event), measured in game:
  `capsule_profiles.json` from evidence (V2.8: walk stop 132 → 0 cm/s in 0.50 s / 33.3 cm; walk start 0 → 132 in 0.80 s, soft
  first 0.3 s). Clip root motion = this profile, in game units.
- Source poses: the production loop that precedes / follows the clip (its phase table, contact intervals, root speed per loop
  time: `A_LB_Walk_Fwd` 106.4 cm/s of loop time, played ×1.24 in game) and the pose that follows (idle frame with BOTH feet down).
- How the clip will be clocked (MM search, CP evaluator on distance table, elapsed time) — the clock decides what "in sync" means.

## Method (implemented in Tools/SHME_V28_20261015/v28_gen_startstop.py)
1. Plan footsteps explicitly: which foot is planted at the entry, which is in swing, where each lands, when.
   Stops: the swing foot LANDS at its stance position next to the final root (shortened / redirected step); the support foot
   makes a closing step only if it ends > ~4 cm from its stance spot. Starts: weight shift, stepping foot lifts (~0.26 s),
   lands where the loop places it at its heel strike at the time the root has covered the stance-foot / loop geometry.
2. Root = capsule profile. Upper body = source pose (decaying cadence for stops) blended into the target pose (idle / loop).
3. Planted feet: pin the BALL, take the foot rotation from the source (heel roll is part of the source); a trailing foot whose
   source has already toed off holds its last planted rotation. Swing feet: cubic Hermite from the current position + velocity
   to the landing (zero velocity), vertical arc; never move a foot horizontally while it touches the floor.
4. Legs: two-bone IK (`v137_animedit.solve_leg`, knee hint = source knee; V2.10 solver: hinge frames + hint fallback, every write
   checked by `leg_guard` - see authoring.md V2.10); `ik_foot_*` follow the feet.
5. Entry frame = the exact source pose (entry error 0) and exit frame = the exact target pose (no second settle afterwards).
6. Write NEW assets (duplicate, remove inherited PoseSearchBranchIn tracks unless the clip must join a database, rebuild curves),
   keep the originals; select them through a switch so old / new can be compared in one process.

## Checks per generated clip (print, do not trust visually alone)
entry pose error (cm), exit pose error vs target, foot IK error (target unreachable), planted-ball horizontal drift, floor
penetration, pelvis min vs final (a real dip vs standing up from walk height), root travel vs capsule distance, step lengths.
V2.8 result: 12 phase stops + 2 starts, entry / exit error 0, root 33.3 cm, IK error ≤ 1.9 cm (one phase 4.9 cm), drift ≤ 3 cm.

## Failure examples (verified in this project)
- Posture-only bakes (V2.7 low-band) could not remove a deep stop dip: the long final step sets the pelvis height; heel roll /
  early toe-off help, but the real fix is a shorter step.
- Dragging a lifting foot: holding a vertical offset on a foot that the source already lifts makes it slide on the floor
  (V2.8 start, first build: 85 cm "planted" drift) — offsets of a lifting foot are horizontal only and fade over its swing.
- Fixed minimum swing times: a 0.20 s minimum landing time pinned a trailing foot while the hip moved 22 cm ahead → IK
  overstretch (10 cm error); use the natural landing time (≥ 0.12 s) and start the closing step at landing.
- Loop clips in BranchIn databases must stay 0..length (see authoring.md V1.3.8); generated non-loop clips should not inherit them.
- A generated clip is only correct together with its PLAYER: confirm which pin / variable is the evaluator's time, and that the
  owning state lasts until the clip's exit pose (V2.8 start: right clip, wrong clock + early release → 27 cm stance slide).
- Installer idempotency: detect an existing wrap by searching the feeder tree a few levels deep, not one level (V2.8: a shallow
  check double-wrapped the selectors on a re-run; restored from checkpoint and reinstalled).
- Root curve from a raw measured capsule table: 30 fps sampling jitter made the authored root speed 93–144 cm/s frame to frame;
  an elapsed-clock clip then moves the pinned foot by the jitter. Fit a smooth model first (stop: CMC braking
  dv/dt = −(A + F·v); start: v = vmax·smoothstep(t/T)^q) and keep the raw table as evidence. Fit it on IN-GAME capsule positions
  measured from the clip's frame 0 (the last full-speed frame): the table fit (A 235, F 0.5, 15 ms lead, 33.3 cm) counted one
  extra full-speed frame and slid the planted foot ~4 cm; the in-game fit is lead 0, A 195, F 1.2, 29.5 cm (rms 0.15 cm).
  Distance-matched clocks need the inverse table at the clip's own key times (1/30 s), not coarser.
- Entry timing of a phase-matched clip: ABP-side features (GetSocketLocation during the update) are the PREVIOUS frame's pose
  relative to the current actor, so the matched pose is the clip's frame 0 and the clip must enter one frame in (T0 = dt);
  speed-matching T0 through a model with a lead-in put the root 2 cm ahead and slid the planted foot back 3–4 cm.
- More phase bins do not fix a timing error: 12 → 24 bins left the entry slip unchanged until the entry time was corrected.
- The exit pose decides what happens NEXT: stops ending in an arbitrary "both feet down" idle frame (asymmetric stance, 3 cm
  off-centre) made Motion Matching pick other idle times and the following short taps slid 3–5× more (V2.8 tap-cancel windows).
  End in the stance the runtime itself settles in (read the MM idle time after the existing behaviour: here
  af_Stand_Idle_NaturalBaseline_Phase275 at 57.8 s) and test the inputs that FOLLOW the new clip, not only the clip.

## Retarget checks (driver → visible body)
Compare `mx_*` (driver) and `vb_*` (visible) contact slip and stride length on the same run; a difference is a retarget / IK
chain issue (see memory: RTG IK Chains op, GR_LegGoals). A clip with 0 foot error offline can still slide at runtime because of
the entry blend, the clock or warping — runtime contact is measured, never inferred from the clip.
