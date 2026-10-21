# SHME V2.20 — kod ve graf değişiklik özetleri

Her betiğin kendi açıklaması (docstring), değiştirilmeden. Betikler projenin kendi araçlarıdır; ücretli kaynak animasyon ya da varlık içermez.

## Üretime alınanlar (sırasıyla)

### `install_v220_pivotplant.py`
```
install_v220_pivotplant.py (editor job) - V2.20 target 2: the late-reverse knee twist is added at runtime by the FootPlacement +
LegIK chain (v220k30 r_cutrev_r2, deterministic 30 FPS: knee bend-plane rate 1241 deg/s with both on, 533 FootPlacement off, 521 LegIK
off, orientation / stride warping and the visible-body retarget unchanged). The plant settings used there are PlantSettings_Default
= LockRotation: the planted foot's yaw is held while the reversal pivots on it, the hips yaw over it and the knee is wrung until the
60 deg unplant angle releases it (the spike at lift-off). PivotAroundBall on the same frames (v220l30 pb): 1384 -> 537 deg/s and equal or
smaller slides in every reversal tested. New (knob SHM220_PivotOn, 0 = off): MontTick SHM220_PivotPlant = FlipOn OR RecOn OR RtPrev OR
(SHM_RedirectActive AND speed > 220); Get_FootPlacementPlantSettings gets an outer Select(Index = SHM220_PivotPlant, 0 = the existing
result, 1 = PlantSettings_Walk (PivotAroundBall, Default's radii)). Walk / stop / landing selection unchanged. V217_SAVE saves.
```

### `install_v220_tiphand.py`
```
install_v220_tiphand.py (editor job) - V2.20 target 3: in-place reverse turn taken over at the request, from the real pose.
Verified (dump_GR_UpdateIdleTurn + v218d7 / v219 t_tiprev): with the V2.17-V2.18 hand path on (GR217_TipHand, MinT 0.12) the new
montage still started only when the first one had reached its end: the START branch (IfThenElse_1) needs Op7 = Op6 AND Op18, and Op18
= Op17 AND (interval OR hand) where Op17 = (camera look settled for TW_LastLookTime ... OR |yaw| in the large-angle range). A reverse
request IS a camera swing (look not settled) at |yaw| 15-85 -> Op17 false until the old montage had turned the actor far enough.
New: IfThenElse_1.Condition = Op7 OR (hand2 AND Op6): on the hand-over tick the look-settle / large-angle gate is bypassed (Op6 keeps
the not-moving / look-driven / aim conditions). The montage bins (|yaw| ranges) pick the new turn from the CURRENT remaining yaw; the
new dynamic montage blends in from the playing montage's pose on the same slot (the old root motion stops with it, nothing doubles).
Pawn knob GR217_TipHand stays 0 (candidate) unless promoted. builtins.V220_SAVE saves, V220_DRY probes. Prints TH220 {...}.
```

### `install_v220_tipdelta.py`
```
install_v220_tipdelta.py (editor job) - V2.20 target 3, revision 2: one hand-over per reverse request.
Measured (v220w30 t_tiprev / t_tiprev2 th, 30 FPS fixed step): with the TH220 start gate the new montage starts 0.03-0.04 s after the
request (base 0.20-0.27 s), but it RE-FIRES every GR218_TipHandMinT (0.13 s: montages 8 > 9 > 10 > 11, R drag 43.9 cm). Owner: the
reverse test is Yaw * GR213_TurnDelta0 < 0 and GR213_TurnDelta0 is refreshed (function entry, VariableSet_32 = SelectFloat_62) only while
NO montage plays; a hand-over chains montages without a gap, so TurnDelta0 keeps the FIRST turn's delta and every following tick of the
new turn reads as another reversal.
New: SelectFloat_62.bPickA = NOT IsAnyMontagePlaying OR (GR217_TipHand > 0.5 AND GR_TurnMontage changed since the last tick: object path
text vs GR220_TurnMontName, stored right after VariableSet_32). The tick after a hand-over (any dt) re-bases TurnDelta0 on the current
remaining yaw; a further genuine reversal (yaw sign against the new turn) still hands over. Knob off -> unchanged V2.19 graph result.
builtins.V220_SAVE saves, V220_DRY probes. Prints TD220 {...}.
```

### `install_v220_tipsettle.py`
```
install_v220_tipsettle.py (editor job) - V2.20 target 3, revision 3: the hand-over turn is chosen from the SETTLED request.
Measured (v220x30 th, TIP delta re-base on): one hand-over per request, 0.03-0.04 s after it, but it fires while the camera is still
swinging: t_tiprev picks its bin at d -58 (camera 18 -> 0 two frames later) -> 45 deg clip, ends at d -31 (below the start range: the
body stays 31 deg off the camera); t_tiprev2 picks at d 48 of a 180 request -> 45 deg clip + a second 135 turn, done at 7.40 s (base
6.03). The TH220 bypass removed the look-settle / large-angle gate (Op17) entirely.
New: IfThenElse_1.Condition = Op7 OR (hand2 AND Op6 AND (settled OR CallFunction_60 large |yaw|)), settled = now - TW_LastLookTime
(CallFunction_58) >= GR220_TipHandSettle (pawn, default 0.05 s): the hand-over waits until the mouse / stick has stopped for a
moment (not for the first montage to end, and not for the 0.16 s idle gap); large angles still start at once. builtins.V220_SAVE.
```

### `install_v220_stopface.py`
```
install_v220_stopface.py (editor job) - V2.20 B) stop entry keeps the current support / facing.
Measured (stops220.py on v219f / v218f finals, v220v30 r_cutrev_r): every release from a SPRINT that faces its movement (SprintFaceMove:
actor yaw = input direction, here -90 while the camera looks at 0) enters the forward stop SHM_A_RR_M_Relaxed_Run_Stop_F_* and in the
same 0.6 s the look-driven actor yaw swings back to the camera (ay -87 > -64 > -31 > -12 > 0 at 410 > 147 cm/s): the stop clip's feet
are carried round a 90 deg arc while the capsule still slides sideways -> L 95-102 cm drag (r_cutrev_l / r, v218f and v219f alike),
R 55 (chain_scurve), 32-48 (k_ws_cam). Owner: BP_GR_Player GR_Impl_CP_PhysicalRedirect RInterpTo_Constant (CallFunction_22), whose
InterpSpeed keeps the look-driven rate when the input is released.
New (profile fields, DA_GR_LocomotionBehavior, default OFF): GR220_StopFaceHold > 0.5 -> while on the ground with NO input acceleration
and Speed2D > GR220_StopFaceHoldSpeed (default 5 cm/s) the body yaw rate is 0: the stop is played in the travel facing the body
already has; once standing, the existing in-place turn (GR_UpdateIdleTurn) turns the body to the camera with its own steps.
Any input restores the normal rate the same tick. builtins.V220_SAVE saves (value-checked: the DA keeps StopFaceHold 0). STOPFACE220.
```

### `fix_v220_stopface_rate.py`
```
fix_v220_stopface_rate.py (editor job): STOPFACE220 revision 2. Measured v220z30 r_cutrev_r sf: the actor yaw went -90 -> 0 in ONE frame
at the release - RInterpTo_Constant returns the TARGET when InterpSpeed <= 0 (UE convention), so the 'hold' rate 0.0 snapped instead of
holding. The hold now selects 0.01 deg/s (no visible rotation, no snap). Knob GR220_StopFaceHold stays 0 in the DA. Prints SF2 {...}.
```

### `fix_v220_stopface_err.py`
```
fix_v220_stopface_err.py (editor job): STOPFACE220 revision 3 - the hold only for a LARGE facing error.
Measured (v220b30 sf, 30 FPS fixed step): r_cutrev_r / l stop L 74.7 / 76.4 -> 3.8 / 3.9 cm (body faced its sprint direction, 90 deg off
the camera), but k_ws_cam (W released, S pressed 0.1 s later while the camera turns; facing error 18 deg) got worse (L 14 -> 40, R 17 ->
31): the 0.1 s no-input gap engaged the hold and shifted the following pivot's foot choice. A small facing error is the normal
look-driven lag (warping absorbs it); the slide owner was the 90 deg sprint-facing swing.
New: hold AND |NormalizedDelta(control yaw, actor yaw)| > GR220_StopFaceHoldMinErr (profile field, default 45 deg). Prints SF3 {...}.
```

### `fix_v220_stopface_delay.py`
```
fix_v220_stopface_delay.py (editor job): STOPFACE220 revision 4 - the hold needs a REAL release, not a one-frame input gap.
Measured (fixed step 30 FPS, production vs single knob off): r_cutrev_l0 R 11.4 -> 1.0 cm and r_cutrev_r1 R 10.1 -> 0.7 cm with
GR220_StopFaceHold 0 (gait slew off: unchanged): the D -> A key change gives one input frame with zero acceleration, the body faces 45+ deg
off the camera after the cut, the hold froze the yaw for that frame and the reversal chain changed. A stick crossing its dead zone does the
same. New: PhysicalRedirect stores GR220_LastInputT (game time of the last frame WITH input acceleration) at its entry; the hold also
needs now - GR220_LastInputT > GR220_StopFaceDelay (profile field, default 0.15 s). Prints SF4 {...}.
```

### `fix_v220_stopface_input.py`
```
fix_v220_stopface_input.py (editor job): STOPFACE220 revision 5 - "no input" = the player's movement INPUT, not the CMC acceleration.
Measured (fixed step 30 FPS): with the 0.15 s release delay (rev 4) r_cutrev_l0 / r1 still R 11.4 / 10.1 cm (hold off: 1.0 / 0.7): the
CMC current acceleration also reads zero while a reversal step is driven by root motion, so the hold froze the yaw in the middle of the
reversal although the key was held. Now both the hold's no-input test (the InRange(-1, 1) node of rev 1) and the GR220_LastInputT
refresh (rev 4) read VSizeXY(GetLastMovementInputVector) (> 0.1 = input); DA / profile GR220_StopFaceDelay 0.08 s (covers a 1-2 frame key
change gap at 20-30 FPS). Prints SF5 {...}.
```

### `install_v220_gaitslew.py`
```
install_v220_gaitslew.py (editor job) - V2.20 C) a gait DOWN-change sheds speed like a body, not like a speed limiter.
Measured (v219f p_j2s_tap / p_tapretrig, real time): a 0.12 s Shift release-repress during the sprint drops the capsule 490 -> 300 cm/s
in 0.25 s (~760 cm/s2: CalculateMaxSpeed returns the jog speed at once and the CMC brakes the excess at once), the shown gait steps
down, the jog loop plays 1.3-1.5x while the capsule re-accelerates and the sprint loop is re-entered at 2.13 at 417 cm/s -> L 22.7 /
29.6 cm net (33-47 drag) at the re-entry; V2.18/V2.19 'sprint loop re-entry slide' is this chain.
New (profile field GR220_GaitDownDecel cm/s2, DA_GR_LocomotionBehavior, default 0 = off): BP_GR_Player CalculateMaxSpeed returns
max(target, min(previous result, Speed2D) - GaitDownDecel * (now - previous time)) while on the ground: a lower gait target lowers the
limit at a human deceleration (the CMC then follows the limit), increases are immediate, and the limit never sits above the real speed
(a wall / turn speed loss is not undone). A short re-press therefore keeps the sprint (and its loop) with a small speed dip; a held
release coasts down to jog. Members GR220_MaxSpeedOut / GR220_MaxSpeedT. builtins.V220_SAVE saves (DA value-checked). GAITSLEW220.
```

### `fix_v220_gaitslew_shift.py`
```
fix_v220_gaitslew_shift.py (editor job): GAITSLEW220 revision 2 - only a RELEASED Shift slews the speed limit down.
Measured (fixed step 120 FPS, r_cutrev_r2, per-window calibration): a sprint cut lowers the limit 490 -> 416 at its first frame; the slew
spread that over 0.06 s (mws 473 > 463 > 453 ...), the cut kept more speed, the path changed from 5.04 s on and the late-reverse foot
sweep (RevTurn_L_Lfoot entry) touched the floor: L 6.0 (V2.19) -> 38.1 cm; slew off (ngs): 5.9. A cut / turn cap is not a gait change.
New: the slew's condition also needs NOT GR_ShiftHeld (the sprint key is up); a cut while Shift is held drops the limit at once as in V2.19.
Prints GS2 {...}.
```

### `fix_v220_gaitslew_target.py`
```
fix_v220_gaitslew_target.py (editor job): GAITSLEW220 revision 3 - the slew follows the TARGET gait, not the Shift key.
Measured (fixed step 120 FPS): with rev 2 (NOT GR_ShiftHeld) the late reverse is back to V2.19 (L 5.9 cm) but p_tapretrig lost its gain
(L 5.0 -> 13.2, jog dropout again): on the re-press GR_ShiftHeld is true at once while GR_TargetGait stays RUN for ~0.25 s, so the limit fell
to the jog speed at once. New: the NOT(GetGR_ShiftHeld) input is replaced by NOT(GR_TargetGait == SPRINT) (ToInteger(Byte) in 1.5..2.5):
a cut cap while the sprint is targeted drops the limit at once (V2.19), a lower target gait (released or re-pressed Shift, gait toggle) slews.
Prints GS3 {...}.
```

### `swingclear220.py`
```
swingclear220.py (editor job): V2.20 copy of swingclear219.py with a configurable swing gate (cfg min_height, default 2.5 cm = V2.19).
V2.20 use: the run stops SHM_A_RR_M_Relaxed_Run_Stop_F_L/Rfoot carry the TRAILING foot forward at 165-450 cm/s only 0.9-5.6 cm above
the floor (clipfeet220.py) - a floor skim that reads as a 46-48 cm slide at runtime; with min_height -99 the speed alone marks the swing.
V2.19 text:
Measured (v219q60 / q120 r_cutrev_r, clip probe clipfeet.json): SHM216_RevTurn_L_Rfoot carries the free RIGHT foot through the turn
at 8-9 cm ball height (0.63-0.80) while it travels fast; at runtime the transition offset from the cut clip lowers it to the floor at
300-770 cm/s -> a sweep counted as a 24-28 cm slide at 60-120 FPS (3-6 cm at 20-30 FPS: a later cut phase at the flip).
Edit: in the given windows, a SWING foot (ball above the clip floor + 2.5 cm, i.e. not in stance) moving faster than vmin cm/s
(component space) gets its ball lifted to at least 'height' cm above the clip floor; the lift is smoothed (+-3 keys, eased at the
window edges), the foot keeps its rotation, the leg is re-solved as a hinge (ae.solve_leg, knee hint = the current knee), ik_foot
follows. Stance keys and every other bone are untouched. builtins.V219_SC = {'clips': {path: [[foot, t0, t1], ...]}, 'height': 14,
'vmin': 120, 'dry_run': bool}. Prints SC219 [...] (max lift per foot, frames edited, leg_guard result).
```

### `promote220.py`
```
promote220.py (editor job): V2.20 promotion of the decided candidates into the saved production defaults.
builtins.V220_PROMO = {'abp': {...}, 'pawn': {...}, 'da': {...}, 'save': bool}. ABP = ABP_GR_MotionMatchingBase CDO (child inherits), pawn =
BP_GR_Player CDO (+ BP_PBI_Player CDO when it holds its own value), DA = DA_GR_LocomotionBehavior. Refuses with unexpected dirty packages
or PIE. Prints PROMO220 {before, after, saved}.
```

## Kurulu ama kapalı

### `install_v220_recsearch.py`
```
install_v220_recsearch.py (editor job) - V2.20 target 1: no pose re-search while the recovery step is in its SUPPORT phases.
Verified (v219s r_cutrev_r0 / l0 hC, real time, 0.18 s stall in the brake stance): the stall frame advanced the clip only ~0.05 s,
the next frame MM re-searched and re-entered the SAME recovery clip at its entry window start (L_Lfoot 1.13 -> 1.00, R_Lfoot 1.23 ->
1.10) = the brake foot went back to a past contact: 33 cm slide. Also the second-direction exit (r0_w) left the clip mid re-placement.
New (knob SHM220_RecHold, 0 = off): MontTick SHM220_RecWin = 0.08 s < now - RecT0 < SHM220_RecHoldT (0.62 s: entry -> brake ->
re-placement landing); EventGraph SHM220_Search = NOT (RecWin AND CurrentSelectedDatabase == SHM217_DB_Recover); the AnimGraph Motion
Matching node's bShouldSearch pin <- SHM220_Search. The authored recovery plays through its support phases (a release / new
direction is latched by the input at once and served when the window ends); outside it MM searches normally. V217_SAVE saves.
```

### `install_v220_pivotscope.py`
```
install_v220_pivotscope.py (editor job) - V2.20 target 2, scope revision. Measured (fixed step v220x60 / x120 r_cutrev_r2): with the pivot
plant on, the late-reverse knee plane rate drops at every FPS (20: 1033 -> 567, 60: 1211 -> 893, 120: -> 914 deg/s) but the LANDING of the
reversal foot at RevTurn entry (clip 0.64-0.69, 0.1 s after the RevTurn start) slides more at high frame rates (120 FPS L 11.6 -> 38.1 cm,
r_cutrev_r R 13.7 -> 22.8): PivotAroundBall is already active while the foot is still arriving. The knee spike is at the planted foot's
LIFT-OFF (RevTurn ~1.0-1.2). New knobs (ABP, default 0 = the promoted V2.20 behaviour): SHM220_PivotT0 - the RevTurn term only counts once
the selected clip time >= T0 (Phase27_SelectedTime); SHM220_PivotNoRd > 0.5 drops the generic (RedirectActive AND speed > 220) term.
DSL: SHM220_PivotPlant = PivotOn AND (FlipOn OR RecOn OR (RtPrev AND time >= T0) OR (NoRd < 0.5 AND RedirectActive AND speed > 220)).
builtins.V217_SAVE saves (PivotOn stays 1, T0 / NoRd stay 0 unless promoted). Prints PS220 {...}.
```

## Ölçüm / doğrulama araçları (salt okunur)

### `knee_stage220.py`
```
knee_stage220.py <run> [t0 t1] [--leg=l] : V2.20 knee bend-plane by POSE STAGE, same frames: driver mesh (mx_: MM + FootPlacement +
LegIK output of the AAMS driver skeleton) vs visible body (vx_: Manny after the runtime retarget). Per frame: knee bend angle, bend-plane
normal angle change per second (continuity-safe: sign aligned to the previous normal), knee offset toward the hip midline, and the clip.
Plane rates are only reported where the knee is bent > 20 deg (a straight leg has no stable plane).
```

### `tip220.py`
```
tip220.py <run>... : in-place turn hand-over read-out. Montage sequence with actor yaw (ay) and camera yaw (cy); the REQUEST time =
first frame the requested yaw (cy - ay) changes sign against the running turn; the hand-over latency = request -> next montage start;
max actor yaw rate (deg/s) after the request (a one-frame dump shows as a spike); worst contact216 net / drag per foot 3.0-6.5 s.
```

### `stops220.py`
```
stops220.py <run>... : every STOP entry (selected database name contains 'Stop', previous one did not) with the capsule speed at
entry, entry clip / time, and the worst contact216 net / drag per foot in [entry, entry + 1.3 s]. Separates sprint-speed stops.
```

### `cliprate220.py`
```
cliprate220.py <run> [t0 t1] : per frame selected clip, clip time, clip-time rate (d clip time / d world time; 1.0 = authored
speed), capsule speed and selected DB, in a window. Shows distance-matched / play-rate scaled playback (rate != 1).
```

### `clipfeet220.py`
```
clipfeet220.py (editor job): per key of a clip (builtins.V220_CF = {'clip': path, 't0': s, 't1': s}): root speed, and per foot the
ball height above the clip's own floor (5th percentile) and ball speed in the ROOT frame (stance = ~0 in root-relative world motion
means planted; the world foot speed = root speed - ball root-frame speed). Read-only. Prints CF220 rows.
```

### `diverge220.py`
```
diverge220.py <runA> <runB> [--eps=0.5] : first game time at which two runs' driver feet (mh_ball_l / mh_ball_r) differ by more than eps
cm, and the max difference before it. Separates a real motion change from a contact-metric change: contact216 calibrates the floor (b0)
over the WHOLE run, so a change late in a run (e.g. the final stop) moves the contact numbers of earlier windows with identical motion.
```

### `ctrunc220.py`
```
ctrunc220.py <t0> <t1> <run>... : contact216 per foot (worst net / drag) in [t0, t1] measured on a copy of the run TRUNCATED at t1 + 0.3 s,
so the floor calibration (b0 / a0, computed by contact216 over all rows of the file) only sees frames up to the window. Two variants
with identical motion before t1 then give identical numbers (whole-run calibration let a later change, e.g. the final stop, move the
numbers of an earlier window). The temporary copy <run>_tr220 is deleted after the measurement.
```

### `input_latency220.py`
```
input_latency220.py (editor job, PIE only, no asset change): which part of the 2-frame key -> movement delay is the harness.
In one PIE session, from a slate POST-tick callback (where the harness injects): A) EnhancedInputLocalPlayerSubsystem.inject_input_vector_for_action
(IA_Move, (0,1,0)) - the Enhanced Input injection a real device feeds into the same input tick; B) the harness path, console 'Input.+key W'.
Per frame after each injection: engine frame number, CMC last input vector (what the movement consumed this frame) and Speed2D.
Prints IL220 {...}: frames from the injection frame to the first frame the movement saw the input, for A and B.
```

### `cmp220.py`
```
fps219_cmp.py <tag>... [--sc=a,b] : V2.19 frame-rate comparison. For every scenario and tag (v219<tag>_<sc>_<var>_r1, warm-up r9
excluded): the CLIP SEQUENCE in the event window (distinct consecutive selections, so a different motion class shows directly), recovery
entry (rec218 logic: first Recover clip / RecOn), worst contact216 net / drag per foot in the final217 window, and the median / max
frame dt. One block per scenario.
```

### `fps220_cmp.py`
```
fps220_cmp.py <prefix>... [--sc=a,b] : V2.20 copy of fps219_cmp.py taking FULL run prefixes (v219x20, v220x20, v220x60 ...) so V2.19 and
V2.20 fixed-step runs sit in one table. For every scenario and prefix (<prefix>_<sc>_<var>_r1, warm-up r9
excluded): the CLIP SEQUENCE in the event window (distinct consecutive selections, so a different motion class shows directly), recovery
entry (rec218 logic: first Recover clip / RecOn), worst contact216 net / drag per foot in the final217 window, and the median / max
frame dt. One block per scenario.
```

### `final220.py`
```
final220.py <before_prefix> <after_prefix> [--out=name] : V2.20 copy of final219.py (before = v219f = the FINAL V2.19 production batch,
after = the single final V2.20 production batch v220f; tags V2.19 / V2.20). Added: the FINAL sprint stop of every scenario that ends in one
(first stop-database entry after 7.0 s -> [entry, entry + 1.3 s]; the V2.19 windows never covered it) and the in-place reverse turns.
V2.19 text: V2.18 copy of final217.py (before = v217z2 = the FINAL V2.17 production batch incl. the
yaw-snap fix, measured in the previous session with the same harness; after = the single final V2.18 production batch v218f). Event-windowed before / after tables for REPORT_V218 (per foot, never summed;
worst contact net / drag path over the repeats, sink frames, per-run list kept in the json). Same windows and the same metric code
(contact216) for both sides. before = V2.16 production measured in THIS session (v217b1: V2.16 + the yaw-snap fix, which is not a
transition change), after = the single final V2.17 production batch. Variant tags are taken from the labels (<prefix>_<scenario>_<var>_rN).
Windows (absolute run time, harness start 2.0 s):
  r_cutrev_l / r : entry + turn [5.30, 6.60], exit to the sprint loop [6.60, 7.60]
  r_cutrev_r0 / l0 (very early reverse) [5.10, 6.60]; r_cutrev_r1 [5.20, 6.60]; r_cutrev_r2 [5.55, 6.85]
  k_cut_back : cut [4.95, 5.85], backpedal entry + run [5.85, 7.60]
  chain_sscut [4.95, 6.90] (+ pelvis min); chain_scutrel [4.9, 11.5]; r_wcurve [4.9, 9.5]; r_kb2 [4.9, 8.5]
  p_w2s* / p_j2s* : last Shift rising edge ts -> [ts - 0.1, ts + 1.8]
Writes Saved/Codex/SHME_V217_20261019/<out>.json and prints markdown rows.
```

### `verify_prod220.py`
```
verify_prod220.py (editor job, read-only): V2.20 production check = verify_prod219.py (V2.18/V2.19 knobs, databases, leak checks, vendor
mtimes, TIP clips) + the V2.20 knobs: ABP SHM220_PivotOn / SHM220_RecHold, pawn GR217_TipHand / GR218_TipHandMinT / GR220_TipHandSettle,
DA_GR_LocomotionBehavior GR220_StopFaceHold / GR220_StopFaceHoldSpeed / GR220_GaitDownDecel / GR215_RevBrake* (must stay off); PSD_RR_Stop
entries; the two re-cleared stop clips' sha256 (differs from checkpoint/pre_stopclear = the V2.20 edit is in). builtins.V220_VF =
{'expect': {...}, 'da_expect': {...}, 'pawn_expect': {...}}. Prints VERIFY220 {json}; 'leaks' empty = PASS.
```
