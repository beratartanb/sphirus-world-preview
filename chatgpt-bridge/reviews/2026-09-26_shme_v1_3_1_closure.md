# SHME V1.3.1 closure on the V1.3.3 build (2026-09-26)

**Acceptance: PARTIAL V1.3.1 closure on the V1.3.3 build** (section 10). Scope agreed with the user: keep the V1.3.3 build (turn-in-place, recovery L/R split, commit
latch, DOF) and work the V1.3.1 gate items that its own report (section 16) left open. No rebuild, no new subsystem,
vendor untouched, map byte-identical. Numbers: PIE QA harness, injected Enhanced Input, 30 FPS unless stated; slide =
09-21 proxy (cm); skating = curve-independent planted-foot travel while SHME contact confidence >= 0.8 (V1.3.1 section 9).
Evidence root `Saved/Codex/SHME_V131C_20260926/`, runs `v131c_*` in `Saved/Codex/SHME_V1_20260925/Evidence/`.

## 1. Checkpoint and state

Checkpoint `Saved/Codex/SHME_V131C_20260926/Checkpoint/sha256.txt` (642 hashes, the V1.3.3 file set: vendor AAMS
assets, SHME component / profiles / databases / clips, ABPs, player and camera Blueprints, production map
`bb9cf344160013cd...`). Open items taken from V1.3.1 section 16 and V1.3.3 section 8: (1) 10 FPS held-stance regression,
(2) 1x review, (3) StartTransfer authoring, (4) turn physics selecting motion, (5) APA consumer, (6) multi-step
recovery / exit, (7) plant-foot agreement (closed in V1.3.2/V1.3.3: 100 % episode-level), (8) sprint-wall skating,
(9) cold index, (10) diagonal-stop bisect, (11) stairs 47.8 anomaly, (12) hard-turn route gated off; plus the V1.3.1
spec's real-house moving test (section 35) and the walk / jog 45 / 90 / 180 validation (section 18) that the protocol
never covered.

## 2. 10 FPS held-stance starts: attribution (spec 22)

The 21-23 cm proxy slides sit on the **positioning stop before each start** (the `*_setup` stages), not on the start.
Paired 10 FPS runs of the start suite on the final build, SHME master off vs on (`v131c_s10lo_off`, `v133m_s10lo`):

| setup stage (10 FPS) | proxy slide, SHME OFF | SHME ON | skating OFF (L / R) | skating ON (L / R) |
|---|---|---|---|---|
| start_l_0_tap | 20.6 | 22.2 | 5.7 / 11.4 | 5.5 / 11.1 |
| start_l_0_sustained | 20.8 | 22.3 | 14.2 / 11.3 | 14.1 / 11.5 |
| start_l_-45_tap | 20.6 | 23.4 | 3.9 / 11.4 | 7.4 / 10.7 |
| start_l_45_tap | 20.6 | 22.4 | 5.5 / 10.9 | 2.7 / 11.0 |
| start_l_45_sustained | 20.8 | 22.4 | 15.4 / 7.0 | 16.8 / 11.5 |
| start_r_0_tap | 10.7 | 8.3 | 5.5 / 11.1 | - |
| start_r_-45_tap | 5.3 | 21.3 | 4.2 / 11.5 | - |
| start_r_45_tap | 15.8 | 12.5 | 5.5 / 11.4 | - |
| suite max | 20.8 | 23.4 | | |

Findings. (a) With SHME entirely off the same setups slide 20.6-20.8 cm: the "regression" is a property of the AAMS
stop at 0.1 s frames (the CP-owned distance-matched stop, `so=true` on every one of these frames), not of SHME; SHME
adds 1.5-3 cm on the left-side setups and one bimodal outlier (`r_-45_tap` 5.3 vs 21.3, the same stage flips between
two stop clips run to run with SHME off as well: `r_45_tap` 15.8 vs 12.5). (b) The 10 FPS run selects a different stop
clip than 30 FPS for the same approach (`SHM_M_Neutral_Walk_Stop_F_Rfoot` at 10 FPS, `SHM_A_CP2_Jog_Fwd_Stop` at
30 FPS): the speed sample at the stop decision differs at 0.1 s. (c) The contact-based skating metric puts the real
planted-foot travel at 11-17 cm in both states (30 FPS: 3-10 cm), so about half of the proxy number is the proxy's
coarse sampling at 10 FPS. SHME's own state is dt-aware (all filters `1 - exp(-dt/tau)`, all timers in seconds), and
the stance hold is active on good and bad setups alike (V1.3.1). **Not fixed and not fixable from SHME's side without
touching the vendor stop**: the spec's "materially improve" is NOT met; what this pass adds is the proof of where it is
(and is not). Stance preservation was not disabled.

## 3. Turn physics: walk / jog / sprint x 45 / 90 / 180 (spec 15-18)

New harness capability (`qa_pie.py` `move` schedule): protocol-less runs drive the same Enhanced Input console
injection the protocol actor uses (`Input.+action IA_Move X Y`, gait via `IA_Ranger_GaitShift`: tap = jog, hold =
sprint), so an input-direction change of 45 / 90 / 180 deg at a chosen gait is a deterministic stage. Two turn kinds:
**input redirection** (control yaw fixed, the desired velocity rotates: the strafe-turn the look-driven rig makes) and
**look turn** (forward input held, control yaw steps 45 / 90 / 180: the body turn a mouse makes). Per stage, from SHME
telemetry: entry speed, peak |dV|, peak velocity angle, peak `RedirectionDemand`, `TurnClass` (0 normal / 1 committed /
2 hard / 3 reversal), peak brake demand, minimum speed, speed loss, time to regain 90 % of the entry speed, SHME
families, Motion Matching clips, planted-foot skating.

(tables: `turn_tables.md`; summary here)

| gait, turn | v_in | dV peak | demand | class | v_min | loss | regain | family | selected motion | skating L / R |
|---|---|---|---|---|---|---|---|---|---|---|
| walk 45 (input) | 126 | 83 | 0.30 | 0 normal | 126 | 0 | 0.20 s | 0 | Walk_FwdRight strafe | 0 / 0 |
| walk 90 (input) | 126 | 159 | 0.58 | 1 committed | 105 | 21 | - | 0 | Walk_Right + Walk_Box_F_RR (3 fr) | 0 / 0 |
| walk 180 (input) | 113 | 239 | 0.87 | 3 reversal | 1 | 113 | 0.72 s | 0 | CT_Walk_Rear + Walk_Pivot_F_B_Lfoot (23 fr) | 0 / 0 |
| jog 45 (input) | 300 | 207 | 0.75 | 1 committed | 287 | 13 | 0.24 s | 0 | Jog_FwdRight | 2.0 / 2.0 |
| jog 90 (input) | 277 | 356 | 1.30 | 2 hard | 225 | 52 | 0.33 s | 0, 2 | Jog_Right + CP2_Jog_Left_Pivot (6 fr) | 2.4 / 2.5 |
| jog 180 (input) | 264 | 509 | 1.86 | 3 reversal | 4 | 260 | 1.08 s | 0, 2, 3 | RB_Jog_Rear + CP2_Jog_Fwd_Pivot (23 fr) | 3.2 / 4.9 |
| walk 45 (look) | 130 | 86 | 0.31 | 0 | 130 | 0 | 0.22 s | 0 | Walk_Fwd (body turns under the camera) | - |
| walk 90 (look) | 125 | 164 | 0.60 | 1 | 109 | 16 | 0.23 s | 0 | Walk_Fwd + Walk_Box_F_RR (1 fr) | - |
| walk 180 (look) | 120 | 223 | 0.81 | 3 | 0 | 120 | 0.57 s | 0 | Walk_Fwd + Walk_Pivot_F_B_Rfoot (9 fr) | - |
| jog 45 (look) | 290 | 200 | 0.73 | 1 | 290 | 0 | 0.21 s | 0 | Jog_Fwd | - |
| jog 90 (look) | 235 | 243 | 0.88 | 2 | 235 | 0 | 0.21 s | 0, 2 | Jog_Fwd + CP2_Jog_Fwd_Pivot (1 fr) | 3.1 / 1.5 |
| jog 180 (look) | 150 | 450 | 1.64 | 3 | 5 | 145 | 0.50 s | 0, 2 | Jog_Fwd + CP2_Jog_Fwd_Pivot (6 fr) | 4.1 / 2.2 |
| sprint 45 (input) | 476 | 329 | 1.20 | 2 hard | 468 | 8 | 0.24 s | 0 | Sprint_FwdRight strafe | 2.1 / 2.8 |
| sprint 90 (input) | 468 | 517 | 1.88 | 2 hard | 252 | 217 | - | 0, 2 | Jog_Right + CP2_Jog_Left_Pivot (11 fr) | 2.8 / 2.4 |
| sprint 180 (input) | 419 | 719 | 2.62 | 3 reversal | 6 | 413 | - | 0, 2, 3 | RB_Run_Rear + LR_Run_Pivot_F_B_Rfoot (27 fr) + Pivot_B_F (7 fr) | 0.3 / 1.7 |
| sprint 180 -> forward | 267 | 715 | 2.61 | 3 | 8 | 259 | 0.74 s | 0, 2, 3 | Sprint_Fwd + LR_Run_Pivot_B_F_Lfoot (21 fr) | 3.3 / 0 |

The physical response scales as the spec asks: demand grows with speed and angle (walk 90 0.58 < jog 45 0.75 < sprint 45
1.20 < jog 90 1.30 < jog 180 1.86 < sprint 90 1.88 < sprint 180 2.62), a jog 45 (0.75) costs more than a walk 90 (0.58), reversals lose the whole speed and take
0.5-1.1 s to regain it, 45 / 90 turns at walk keep the speed. **Motion selection**: the reversal and hard classes coincide
with AAMS's own pivot clips (`Walk_Pivot_F_B`, `CP2_Jog_*_Pivot`) chosen by the AAMS chooser from the trajectory; SHME's
hard-turn route to the pivot databases stays gated OFF (V1.3.1 item 12: live, it overrides that choice and costs slide),
so SHME's classification is consumed as PBI severity (`SHM_DCSeverity`) and as the family / telemetry, not as a
database override. That is the honest state of "turn physics drives selection": it drives the body response and the
classification; the pivot clip itself is AAMS's, and it is the right one. Skating during turns 1.4-4.9 cm (jog), 0 at walk.

## 4. Multi-step recovery and recovery exit (spec 31-32)

**Tooling added**: a second deterministic pulse in the QA shove (`QAPerturbTime2 / X2 / Y2` profile fields,
`QAPerturbDone2` component flag; the tick fires `SHM_QAPerturb` again when `QAPerturbTime2 > 0`). Three double-shove
runs from standing (first pulse 420 cm/s right at 3.8 s, as the V1.3.3 strong shove) against the single-shove reference
`v133q3_str_s2`:

| run | second pulse | first episode (family 6) | after the second pulse | verdict |
|---|---|---|---|---|
| `v131c_q_same_s2` | +300 same direction at 4.2 s (during the recovery step, speed 292 -> 570) | 3.95-4.28 s, capture error 0.98, urgency 0.96, `SHM_RecS_RL_Rfoot` | `Grounded` false from 4.41 s: the capsule leaves the floor at 5.6 m/s lateral (AAMS `A_CT_StableFall`, then `Land_Stand_Light`, exec 7 landing support) | no second recovery by design (airborne); the QA impulse mid-step is not a physical shove but a launch: test artifact |
| `v131c_q_double_s2` | -420 opposite at 4.5 s (speed 259 -> 161) | 3.96-4.29 s, same clip | capture error 0.00, urgency <= 0.19, brake-and-replant (exec 5) then landing support after a short fall | the opposing pulse cancels the residual motion: no second step is warranted, and none fires (correct) |
| `v131c_q_late_s2` | +420 same direction at 5.6 s (after the first recovery settled, speed 43 -> 446) | 4.10-4.43 s, `SHM_RecS_RL_Lfoot` | push detected (`PerturbState` 1.0 at 5.66) but `FootTargetConfidence` 0.12 and capture error 0.35 at the push frame; contact confidence 0.0 and the support side flips twice (5.86, 5.96) while the push term decays (0.57 by 6.0 s); when capture error (0.81-0.92) and confidence (0.53-0.77) finally coincide at 6.0-6.03 s the demand `cperr x PerturbState` is 0.38-0.5, under `RouteRecoveryDemand` 0.45 at first and the family never latches; the body brakes (exec 5) and does not step | **gap found and located**: a second shove of the same strength ~1.3 s after a recovery produces no second step because the post-recovery support / contact state is not yet trustworthy when the push lands; the planner's exit criteria (new support established, capture error reduced, demand below threshold) are therefore met too early on the first episode |

Recovery exit as built (unchanged): the family holds `RouteMinHold` 0.35 s, then leaves when the candidate drops (demand
below `RouteRecoveryDemand` 0.45 or the step target loses confidence); a second episode needs `RouteCooldown` 0.6 s unless
the family changes. The first-episode lengths above (0.33 s) show the exit is the minimum hold, not a stabilisation
criterion. **Not fixed in this pass**: a change to `PerturbState` decay (hold the push term while contact confidence is
below 0.5) or to the exit criteria touches every route and needs its own perturbation matrix; documented here with the
frame evidence for the next pass.

## 5. APA consumer (spec 29)

Installed, bounded, subtle: the anticipatory postural adjustment SHME already computes (`ApaTimer` / `ApaOffset`, CoP
shift opposite to the first step for `ApaDuration` 0.15 s after an intent onset from rest) now feeds the existing PBI
direction-change severity in the ABP snapshot: `SHM_DCSeverity = max(TurnSeverity, ReversalDemand, ApaCouplingGain x
ApaTimer / ApaDuration)` with `ApaCouplingGain` 0.2 (profile). No new node, no pause: it rides the PBI torso / pelvis
response that already exists (`install_body.py` lerp), so the body prepares into the first step by at most 20 % of the
PBI lean for 0.15 s. Measured effect at start onset (peak |pelvis roll| / |spine roll| in the first 8 frames of each
start stage, `v131c_m_s10` vs the V1.3.3 final `v133m3_s10`): identical on 8 of 12 stages, +2-5 deg pelvis on
`l_45_sustained` / `r_45_sustained`, -1-2 deg spine on three tap stages - within the run-to-run spread, i.e. the consumer
is live but visually below the measurement floor at this gain. Start-suite slide unchanged (7.8 -> 7.6 cm max; one setup
stage moved >= 2 cm). Not judged at 1x by a person.

## 6. StartTransfer (spec 19-21, 28)

State (unchanged from V1.3.1/V1.3.3): `PSD_SHM_StartTransfer_L/_R` + 14 `SHM_StartTransfer_*` clips (walk-start copies,
tagged), family 4 fires for movement onset from a wide / staggered held stance with the unloaded foot chosen from the
support loads; a CP-owned start keeps AAMS's distance-matched start (its foot already comes from SHME through
`CP_TC_Support`), family 4 routes the Motion Matching only for MM-owned starts. This pass did not author new transfer
clips: the V1.3.1 evidence stands (an MM-played start clip against a distance-matched CP start costs 15-25 cm at 30 FPS,
30-36 cm at 10 FPS), and a baked transfer cannot match an arbitrary runtime stance - the held stance is already carried
by the stance snapshot idle + inertial blend into the CP start of the SHME-chosen foot. Where family 4 does fire in this
pass: the real-house lower-stair walk (`v131c_h_stair_walk`, families 0 and 4: a start from the stance the character
held at the foot of the stair) and the real-house start suite (`v131c_h_room_s10`, families 0 / 4 / 5), with no slide
above the flat-floor numbers on those starts. **Spec items 19-21 remain NOT DONE as authored clips**; the decision logic
(stance class, width, stagger, support load, first swing foot) is in place and exercised.

## 7. Real-house moving test (spec 35; map unchanged, PIE only)

Origins from a traced floor map of `L_GR_SphirusHouse` (ground floor z 150, capsule centre 238; lawn 100-115; veranda
door at (775, 1140), rear kitchen door (763, 21), main stair lower flight (157-427, 517-647) rising west to the turn
landing at z ~311). Protocol-less runs (`move` schedule + spawn yaw) and two protocol suites shifted into the house:

| run | where | result |
|---|---|---|
| `v131c_h_stair_walk` | walk 3.5 s west up the lower flight from (600, 582) | COM 246 -> 372 cm (+126) during the walk, 374 -> 425 at the stop (still climbing while decelerating); families 0, 4 (start transfer at onset); skating 2.4 / 4.9 cm on the climb, 14.5 cm right foot on the stair stop; 0 blocked, 0 falling |
| `v131c_h_stair_jog` | jog 3 s, same | COM 242 -> 424 (+182, reaches the turn landing); blocked 17 frames at the landing's west wall (family 5, correct); skating 4.5 / 1.7 |
| `v131c_h_door_walk` / `_jog` | walk / jog south from (775, 900) through the veranda door | door closed (`BP_SphirusHinged` opens on player interaction): blocked family 5 within 2.5 m for 124 / 82 frames, no false idle (idle takeover held off while intent into the door), no stale hold after the stop (stance snapshot idle within 0.25 s) |
| `v131c_h_enter_walk` | walk north from the lawn (775, 1750) to the veranda | climbs the porch step (COM 173 -> 207) then blocked at the closed door for 90 frames; 0 falling |
| `v131c_h_door_walk2` / `_jog2` / `_enter_walk2` | same, door opened in PIE by the harness (`open_doors`) | still blocked at COM y 964 (walk) / 1426 (lawn): traced to the door leaf itself - the hinge is at x 775, so the open leaf stands into the room along the walking line down to y 1000 (the door's interaction box only overlaps); from the lawn the porch's second riser exceeds the step height (COM 175 -> 205 then blocked, family 5) |
| `v131c_h_door_walk3` / `_jog3` | same at x 840 (the clear side of the opening) | **through**: walk 9 m from the room through the open door, across the veranda and down the porch steps to the lawn (COM z 255 -> 143), 0 blocked, families 0 only, skating 4.0 / 8.8 cm over the whole path incl. the step-down, stop on the lawn 5.2 / 5.9; jog: through and down (COM 256 -> 90), 0 blocked, skating 5.0 / 2.5, stop 3.3 / 8.1 |
| `v131c_h_turn_walk` | living room (600, 800): walk east with look-turns 90 / 0 / -90 / 0 | a furniture course: blocked east of the origin within 1 m (39 frames, family 5), then on the 90 look-turn a start from the held stance **played the StartTransfer vocabulary** (`SHM_StartTransfer_RR_Rfoot` x9 + `Walk_Start_RR_Rfoot`, family 4: the first protocol coverage of section 6), 3 m south to the wall (blocked 37), a -90 turn with `Walk_Start_LL_Rfoot`, then `Walk_Bwd_Pivot` at the last turn; no false idle, no stale hold, skating 1.3-8.6 cm |
| `v131c_h_room_s10` | start suite at (500, 800, 238) | max proxy slide 37.0 cm: the sustained and diagonal starts run into the living-room furniture / south wall (794 blocked frames, family 5); the wall-push skating of V1.3.1 item 8 indoors; tap starts 2.0-2.7 cm (flat floor 0.4-7.8); 0 falling |
| camera in enclosed spaces (spec 35 "camera preservation") | gameplay-camera captures on the stair and through the doorway | **finding**: the boom's collision push-in collapses the camera to a few centimetres behind the head on the enclosed lower stair flight and in the doorway (the captured frames show the head or the stair treads, not the body); the GR camera rig's probe / collision settings are the owner (`sphirus-character-camera`), not modified in this pass |
| `v131c_h_hall_s8` | corridor suite at (700, 200, 238), the entry hall | max 23.6 cm on `indoor_surface_yaw_225` (V1.3.1 corridor box 36.7), corner sweeps 0.0 (open hall, no wall to sweep against), corridor entry / exit 7.9 / 7.8; 0 blocked, 0 falling |

## 8. Walls, backward slip, regression, error gate, performance, integrity

**Walls** (`v131c_m_s7`, 30 FPS): suite max 12.5 = V1.3.2 = V1.3.3; per stage identical within 0.1 cm except
`sprint_low_speed` 2.6 -> 8.2. Planted-foot skating (contact metric): sprint_wall_0 5.2 / 13.7, sprint_wall_45 10.0 /
9.1, sprint_wall_75 0 / 0.3, releases 0.5-7.3, jog_wall_75 2.3 / 2.0. **Sprint-into-wall skating (V1.3.1 item 8) is
unchanged (10-14 cm); the impact model was not built.** Backward / wall-retreat: the contact metric from V1.3.1 section 9
is the one used throughout this pass (turn tables, house runs); the old 68 cm proxy is not used.

**Regression matrix (final build of this pass; max proxy slide, cm)**

| suite | V1.3.1 | V1.3.2 | V1.3.3 final | this pass | per-stage >= 2 cm vs V1.3.3 |
|---|---|---|---|---|---|
| starts 30 FPS (s10) | 8.0 | 7.7 | 7.8 | 7.6 | start_r_0_sustained_setup 7.6 -> 5.0 |
| starts 10 FPS (s10lo) | 23.4 | 23.4 | 23.4 | 23.4 (SHME on) / 20.8 (SHME off) | section 2 |
| walls (s7) | 11.8 | 12.5 | 12.5 | 12.5 | sprint_low_speed 2.6 -> 8.2 |
| shoves (family / side) | 1 / 6 / 6 / 6 | 20 % / 10 % side | 100 % side, 100 % db | 6 / 6 / 6, same clips (`RecS_RL_Rfoot` x11) | section 4 |
| turns | suite 1 / 5 sprint only | - | - | walk / jog / sprint x 45 / 90 / 180 measured (section 3) | new coverage |
| real house | start suite (13.7) | 11.9 | 13.5 | stair / door / lawn / hall / room (section 7) | new coverage |

**Error gate** (window `v131c_redir_sprint2 .. v131c_gate_s2`, after the last rebuild + save): 0 SHME Accessed-None,
0 Blueprint runtime errors; 2 `AsyncBuildIndex skipped` lines at 18:59:19 (one frame pair inside the house door runs,
PRE-EXISTING class, 0 in the later window `v131c_h_door_walk .. v131c_gate_s2`), 15 `LogUtils` "editor in play mode"
(QA tooling: the probe jobs and the profile-field failure described below), `LogMaterial` VT entries from house materials
(pre-existing). Harness failure found in this pass: adding profile fields to `shm_profiles.py` invalidates the harness's
profile reset until `build_profiles` runs (V1.3.1 pitfall, repeated): eight house runs failed instantly and were rerun
after the rebuild (chain D).

**Performance** (component laps, ms/frame): starts `v131c_m_s10` mean 0.598 / p95 0.69 / max 1.51 (n 2084); walls 0.604 /
0.70 / 1.85; house starts 0.629 / 0.71 / 1.61; sprint redirection 0.635 / 0.83 / 1.27. Mean and p95 under 1 ms, isolated
max frames 1.3-1.9 ms as in every earlier pass; the second pulse and the APA term are straight-line nodes. No Insights session.

## 9. 1x review (true-speed GIFs, `Saved/Codex/SHME_V131C_20260926/*.gif`)

Workflow from V1.3.3 (time dilation 0.33 + 0.1 s wall screenshots = ~13 game-fps frames, GIF delays from the frame game
times). Fixed observer cameras proved unusable for runs that travel more than a few metres (three captures framed the
spawn point or a wardrobe interior and were discarded); the house and flat 180 captures were redone through the gameplay
camera, which is also the player's own view.

| GIF | run | what a viewer can check |
|---|---|---|
| `v131c_1x_shove_medium.gif` | medium shove 260 from standing (`v131c_cap_shove_med`) | a single lateral recovery step onto the right foot from the routed `SHM_RecS_RL_Rfoot`, weight over the planted left foot, torso following the pelvis, settle into the stance idle; no second step, no pop |
| `v131c_1x_house_stair.gif` | walk up the lower flight of the main stair (`v131c_cap_stair3`, gameplay camera) | what the player sees: the camera collapses onto the head in the enclosed flight (section 7 finding), so the gait itself is NOT reviewable here; the treads pass at walking pace without a hitch; the fixed-observer take (`v131c_cap_stair2`) shows the approach in the workshop room but the character leaves the frame at the flight |
| `v131c_1x_house_door.gif` | walk out through the veranda door and down the porch steps (`v131c_cap_door3`, gameplay camera) | doorway passage with the camera pushed in behind the head at the frame, then the veranda, the two-step descent to the lawn and the stop on grass |
| `v131c_1x_sprint_180.gif` | sprint input reversal (`v131c_cap_sprint180c`) | AAMS run pivot (`LR_Run_Pivot_F_B`) at the reversal, speed loss, replant, re-acceleration |
| `v131c_1x_walk_look_180.gif` | walk with a 180 look turn (`v131c_cap_look180c`) | body turn under the camera, `Walk_Pivot_F_B` clip, foot planting through the turn |

What I checked in frames: the shove frame at mid-step shows one foot in flight and one planted (no double-swing, no
T-pose); the sprint-reversal frame shows the character mid-sprint with the camera following (body in view); the stair and
doorway frames show the camera push-in described in section 7; the walk look-turn capture follows the body turn. The human
judgement (does the recovery look necessary, does the transfer look like weight shift, does 180 carry more consequence
than 90) is the user's at 1x; it is NOT claimed here. Physical devices: NOT_TESTED (injected input only).

## 10. Remaining gaps and acceptance

| V1.3.1 open item | state after this pass |
|---|---|
| 1. 10 FPS held-stance regression | attributed, NOT improved: 20.8 cm with SHME off vs 23.4 on at 10 FPS; AAMS stop at 0.1 s frames, half of it proxy sampling (section 2) |
| 2. 1x review by a person | workflow + five GIFs delivered; judgement open |
| 3. StartTransfer authoring | NOT authored; vocabulary now exercised once by the protocol-less house turn (section 7) |
| 4. Turn physics selecting motion | walk / jog / sprint x 45 / 90 / 180 measured for both turn kinds; classification scales; clips are AAMS's pivots; hard-turn route stays off (section 3) |
| 5. APA consumer | installed (PBI severity preload, gain 0.2); effect below the measurement floor (section 5) |
| 6. Multi-step recovery / exit | second-pulse tooling added; opposing pulse correctly needs no step; reinforcing mid-step pulse launches the capsule (QA artifact); a same-strength pulse 1.3 s later is MISSED because contact confidence / support are not trustworthy yet when the push lands - root cause located, not fixed (section 4) |
| 7 / 13. plant-foot agreement | closed in V1.3.2 / V1.3.3 (100 % episode-level) |
| 8. sprint-wall skating | unchanged 10-14 cm (section 8) |
| 9. cold index | 2 skip lines in the pass, 0 in the final window |
| 10. diagonal-stop bisect | NOT DONE |
| 11. stairs 47.8 anomaly | not rerun (V1.3.2 x5 stands) |
| 12. hard-turn route | gated off, reasoned in section 3 |
| spec 35 real-house moving test | DONE for stair (walk / jog), doorway out (walk / jog, incl. step-down), lawn-in (blocked by the porch riser), hall corridor suite, living-room starts (furniture course), indoor look-turns |
| spec 22 "materially improve" | NOT met (attribution instead) |

Harness additions (project-owned QA only, no gameplay change): `move` schedule, `yaw0`, `open_doors`, second shove pulse,
`redir_report.py`; skill reference and memory updated. Changed assets since the closure checkpoint (7, hashes in
`final_changed.sha256`): `BP_SHM_HumanMotionComponent` (second pulse), `BP_SHM_ResponseProfile` + `DA_SHM_Response_Default`
(4 fields), `BP_SHM_AnthropometryProfile` + `DA_SHM_Anthropometry_Default` (re-saved by the profile builder, values
unchanged), `ABP_GR_MotionMatchingBase` + child (APA term in the snapshot). **Vendor**: 0 files under `Content/AAMS`
newer than the checkpoint. **Production map**: `bb9cf344160013cd...` unchanged. Dirty check after the last run (`save_final.py`): only the response profile data asset (harness per-run reset) was dirty and was saved; `dirty_after` [], `dirty_maps` [].

**Acceptance: PARTIAL V1.3.1 (closure on V1.3.3).** The V1.3.1 FULL gate still fails on: 10 FPS regression not improved,
StartTransfer not authored, multi-step recovery gap, sprint-wall skating, diagonal-stop bisect, human 1x judgement. New
in this pass and technically PASS: walk / jog / sprint turn physics measured and scaling, real-house moving coverage,
recovery second-pulse tooling with a located gap, APA consumer installed, error gate clean, vendor / map integrity.
