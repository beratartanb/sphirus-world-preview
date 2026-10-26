# V2.29 working notes (facts as measured; fixed 30 unless stated)
- Sprint camera-180 reversal "ters/bozuk": spine_03 heading vs pelvis turned through a full revolution in 6-10 frames (twist jump 93-159 deg/frame,
  pops 290-324 m/s2) in s29_cam / s29_cam2 / b_cam180 / chain_sprint (and the jog j24_m180w RevTurn route). Keyboard S reversals (s29_ws/sa/dg/dbl/rel,
  b_s2back) had none. Owner = CONTENT: SHM216_RevTurn_R_Lfoot (frames 29-33, 94-97) and SHM216_RevTurn_R_Rfoot (31-39). Cause = V2.22 bake
  rb222_revturn.py kept-twist term yS = yaw(spine_05) - yaw(pelvis) without wrapping: when the turning clip's chest and pelvis headings
  straddle +-180 the raw difference is off by 360, KEEP_TWIST 0.5 made it a 180 deg rotation of spine_01 about the trunk axis.
  Proof: re-running the OLD computation from the cached original keys reproduces the current keys exactly (max 0.0 deg); the wrapped
  computation removes every spin frame (max chest-vs-pelvis jump 14.9 deg = the clean L clips). Fix = rb229_revturn.py (same bake, wrapped).
  After: SPIN 0, twist jump <= 15 deg, pops 33-70.
- Disappearance not reproduced at fixed 30: visible pelvis <= 28 cm from the capsule, camera never < 188 cm from the head, chest on screen in
  every frame (screen229: 0 off-screen frames), render flags vvis/vrr logged. The full-revolution torso flip is the visible defect.
- Effort baseline (agil229): sprint 90 cut commits in 0.67 s keeping 294 cm/s; S-cut chain: each later cut commits in 0.40-0.63 s keeping
  250-310 cm/s; rested and loaded hard-left identical (no memory of previous effort).
- Directions (a29_*): travel heading = request at every 22.5 deg (err <= 1 deg), no stepping in a continuous camera turn, analog magnitude kept
  (0.35/0.7/1.0 -> 46/88/126 cm/s), digital W+D 126 < W 132 cm/s; walk is look-driven strafe (actor = camera yaw); 8 clip directions + OW;
  skate at sector boundaries: -112.5 14.1 cm, 85/95 6.7, 22.5 4-5 vs 2-3 on the clip angles.
- Walk framing (cam229): A/D walk chest x range 0.31 half-widths, camera-capsule lateral offset range 28 cm, 13 rebounds; diagonals leave the
  body at x -0.16 instead of -0.28; owners: V2.23 follow soft zone (12/10 cm, world-stored) + V2.1 half shoulder swap from 60 cm/s.
- Release->re-press (j24_rel): the V2.28 RelHold ended in the frame the re-pressed key reached the CMC; MM picked Jog_Bwd_Start_AAMS from the
  brake stance (33.9 cm). SHM229_ResumeWin 0.2: the same clip continues its push (ct 0.44 -> 1.64, capsule = designed speed): 11.1 cm;
  ph0 / dbl / sw_ph2 unchanged.
- Harness traps: bash ${2:+...{$2}} closes at the first } (a stray } broke 6 candidate requests: each waited the 900 s timeout); a DSL anchor
  that also exists in the V1 camera function makes a count==1 assert fail (patch inside the target fn).
