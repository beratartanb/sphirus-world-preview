# SPHIRUS: locomotion and character-camera realism pass (2026-09-25)

> **Second pass (appended below as section 10):** standing-jump pop fixed with an owned stand-air loop, and foot-placement plant tuning cuts stop, turn and landing slide broadly. The verdict is still PARTIAL.

**Verdict: PARTIAL ACCEPTANCE.**

- Technical evidence was gathered in-engine on the QA floor fixture and the stairs, corridor and wall fixtures, using injected Enhanced Input at 30 FPS plus 10 FPS stress runs, and viewed through the player camera.
- There was no physical keyboard/mouse/gamepad play and no real-house play, so feel acceptance is still open. That session needs you.

## 1. Skills used
- `sphirus-game-dev-director` routed the task.
- `sphirus-character-camera` was the final authority: its movement-feel, camera-feel, runtime-authority, protected-baseline and verification references.
- `ue-character-and-movement` covered CMC friction and max speed.
- `ue-animation-system` covered PoseSearch DB/schema, chooser and thread-safe update.
- `sphirus-source-control-asset-safety` covered the checkpoint.
- `sphirus-qa-regression` covered the `BP_LTP_QA` suites.

## 2. Runtime authority (verified live)
| Area | Owner |
|---|---|
| Game mode, pawn, player controller, camera | `BP_GM_GR_GraceRanger` → `BP_PBI_Player` (child of `/Game/GraceRanger/BP_GR_Player`) → camera `BP_PCM_GR_Camera`, rig in `BP_GR_Player.GR_UpdateRig` |
| AnimClass | Sandbox `ABP_GR_MotionMatching` → Sandbox `ABP_GR_MotionMatchingBase` |
| Pose selection | `CHT_PBI_PlayerDense` chooser, then `Update_MotionMatching` (thread-safe). CP start/stop gates are unchanged |
| Movement physics | CMC with `BP_GR_Player.CalculateGroundFriction` / `CalculateMaxSpeed`, profile `DA_GR_LocomotionBehavior` |
| Body inertia | `DA_PBI_Prototype` / `BP_PBI_Profile` |

No parallel controller, camera or selection system was added. Every change is inside the existing owners.

## 3. Changes (all compiled and saved through the editor)
1. **Look-driven F↔B reversal pivots.** Root cause: in look-driven mode, W→S / S→W at sprint offered only turn-around clips, which caused a squat of −27 to −30 cm and slide.
   - Added `PSD_LR_ReversePivots` with owned copies `A_LR_Run_Pivot_{F_B_Rfoot,B_F_Lfoot,B_F_Rfoot}` of AAMS `M_Neutral_Run_Pivot_*`. Vendor originals were not touched.
   - Added a branch after the chooser in `Update_MotionMatching`. It fires when the look-driven gait is ≥ jog, velocity along the facing axis opposes acceleration, speed is above 150, and control is aligned with facing (>0.85), so camera-driven turn-arounds keep the turn clips.
   - Added a short hold and a low-FPS term (previous-frame velocity).
   - Profile snapshot vars are set in `CP_UpdateTransitionContext`. The switch is `DA_PBI_Prototype.EnableFacingLockedReversal`.
2. **Reversal grip (physical weight, not delay).** `CalculateGroundFriction` scales friction toward `ReversalGripSpeed` (60) only while braking against facing. The body brakes over about 0.4–0.5 s through real deceleration; there are no timers or play-rate tricks.
3. **Corridor camera snap fix.** `GR_ShoulderClearance` dropped from 37 to 0 in one frame. It is now eased inward with `FInterpTo` (`CameraShoulderInwardSpeed` 10); outward return is progressive.
4. **Camera anticipation probe.** A soft wider sphere trace (radius +30) is min-combined with the thin probe. It is harmless, with a small effect.
5. **Stair camera Z.** `StairHeightMaxLag` 18→28 and `StairHeightResponse` 10→8.
6. **Tried and rejected:**
   - The reversal branch placed before the chooser with bias −1 made slide 46–123 cm worse. It was reverted.
   - `TurnSpeedPenalty` in `CalculateMaxSpeed` worsened foot contact in turns. The node is kept with the value 0.0, which makes it inert.

## 4. Before → after (30 FPS, injected input, QA floor)
| Scenario | Before | After |
|---|---|---|
| Sprint F→B reversal slide L/R | 2.0 / 2.7 cm, pelvis −27 to −30 | 1.6 / 3.0 cm, pelvis −15 |
| Sprint B→F reversal slide L/R | 14.8 / 21.1 cm | 4.1 / 4.3 cm |
| Reversal at 10 FPS | turn-around clip | correct pivot selected |
| Corridor camera max inward step per frame | 38–45 cm (snap) | 15–17 cm, no oscillation, ≥15.6 cm from the wall face |
| Stair camera Z step up / down (jog) | 15.4 / 11.3 cm | 10.0 / 8.0 cm (walk about 5) |
| W+camera 135/180 turns | about 3.2–3.6 cm | unchanged (penalty off) |

## 5. Test matrix (by verification.md row)
| Row | Label | Note |
|---|---|---|
| 1–2 taps (P1) | PASS (technical) | Short starts about 136 cm/s. Tap stop slide 8–20 cm is still open |
| 3–9 starts/stops, sprint stop low-FPS (P2) | PASS (technical) | 10 FPS stop acquired |
| 10–15 turns 45/90/180 | PARTIAL | Clips differ by angle. Slow camera carves carry no momentum cost |
| 16–17 F↔B reversal | PASS (technical) + frames viewed | `v_s5_rev.jpg`: upright, no squat |
| 18 diagonals (P3) | PARTIAL | No second launch. Sustained ±45 stops slide 21–27 cm |
| 19 backward | PASS (technical) | Backpedal gait kept (P12) |
| 20 stationary jump pop | REVIEW_REQUIRED | Pelvis continuous. Takeoff→StableFall handoff at about 1.84 s not frame-reviewed |
| 21–22 forward jump / landing | PARTIAL | P5 distinct. Landing phase slide 13–53 cm is still open |
| 23 crouch (P11) | PASS (technical) | 85 cm/s, headroom, framing |
| 24–25, 27 corridor/doorway/recovery | PASS (technical) + frames viewed | `v_s8_cam.jpg`: no wall or head penetration. Close framing at 135° and corner sweeps |
| 26 wall approach (P10) | PARTIAL | No walk/jog stumble. 22–58 cm slide proxy, possibly an along-wall glide, unverified |
| 28–29 stairs | PASS (technical) | Smoother Z |
| 30 indoor↔outdoor, real house | NOT_TESTED | |
| Physical KB/M, gamepad, real 60 FPS | NOT_TESTED | |

## 6. Visual acceptance
- Stepped player-camera frames were reviewed for the sprint 180 reversal and the corridor camera sweeps.
- Shots drop the game to about 4 FPS, so these are pose/framing checks, not 1× motion review.
- **No human feel acceptance has been given.**

## 7. Technical validation
- **Compile:** `BS_UP_TO_DATE` for all of the following:
  - Sandbox `ABP_GR_MotionMatching`
  - `BP_PBI_Player`
  - `BP_PBI_Profile`
  - `/Game/GraceRanger/BP_GR_Player`
  - the Sandbox `BP_GR_Player`
  - `BP_GR_MotionProfile`
- **Compile warnings:** `ABP_GR_MotionMatchingBase` compiles UP_TO_DATE_WITH_WARNINGS. The warning is an IsValid thread-safety warning on the MM node that was already in the log at editor start (05:13), before this pass.
- **Log errors:** all pre-existing and unrelated:
  - material VT-texture errors (`MI_Ground_MossyNeedles_01`, `MI_Fabric_White_Solid_01`)
  - TextureGraph automation conditions at startup
  - one audio-device crash at 05:06
- **Dirty packages:**
  - No dirty content.
  - `L_GR_SphirusHouse` is marked dirty only in memory, from adding and removing QA fixtures. No fixtures are left.
  - The map file on disk was last written at 07:15, before this pass's checkpoint (07:37). **Do not save the map when closing; choose "Don't Save".**
- **Temporary settings:** t.MaxFPS was restored to 0.

## 8. Remaining issues, next justified pass
1. Diagonal ±45 sustained stops slide 21–27 cm, and tap stops 8–20 cm.
2. Landing-phase slide is 13–53 cm.
3. Stationary jump: review the takeoff→`A_CT_StableFall` handoff frame by frame.
4. Wall contact slide proxy: separate along-wall glide from real foot slide.
5. The walk-stop underlay shows `A_CP2_Jog_Fwd_Stop` in MM telemetry, although the CP evaluator owns the pose. This needs a check.
6. Slow camera carves have no momentum cost. Keep the turn penalty idea off; it hurt contact.
7. Human test: physical KB/M and gamepad in the house at the real target FPS.

## 9. Git / asset safety
- There is no git. The checkpoint is at `Saved/Codex/LocomotionRealism_20260925/Checkpoint`: 318 uassets plus `checkpoint_sha256.txt`.
- **Modified vs checkpoint:**
  - `/Game/GraceRanger/BP_GR_Player`
  - `BP_PBI_Player`
  - `BP_PBI_Profile`
  - Sandbox `ABP_GR_MotionMatchingBase`
  - `Profiles/BP_GR_MotionProfile`
  - `Profiles/DA_GR_LocomotionBehavior`
- **Re-saved:** `DA_PBI_Prototype` and Sandbox `ABP_GR_MotionMatching`.
- **New:** `Experimental/BodyInertia/Reversal/` with `PSD_LR_ReversePivots` and 4 `A_LR_Run_Pivot_*` copies. `F_B_Lfoot` is a copy with its DB membership removed.
- **Untouched:** AAMS/vendor originals (hash-verified), the house map on disk, and scene art.
- **Rollback:** copy the files back from `Checkpoint` with the editor closed, or set `EnableFacingLockedReversal=false` and `ReversalGripSpeed=0` for a soft disable.
- **Tooling:** `Tools/LocomotionRealism_20260925/`. Evidence is in `Saved/Codex/LocomotionRealism_20260925/Evidence/`.

## 10. Second pass (same day, after the 11:58 editor crash)

### 10.1 Standing-jump pop: root cause and fix
- **Cause:**
  - The standing takeoff (`A_CT_JumpTakeoff_Stand`, 0.4 s) ends with the hips forward and the arms up.
  - The air clip for every jump was `A_CT_StableFall`, a running-fall loop with split legs and arm sweeps.
  - At the handover the hips moved 26 cm and the hands 43 cm within about 0.1 s.
  - The legs then split ±30 cm in the air, so the character landed in a stride and both feet slid about 20 cm into idle.
- **Fix, inside the existing owner:**
  - `Update_MotionMatching` → `K2Node_Select_5`, the low-speed airborne branch (<160 cm/s): option 1 now points to the new `PSD_LR_StandAir`.
  - Its only member is `A_LR_StandAir_Loop`, an owned copy of the retargeted Core Motion `am_Jump_Fall_Loop`. It keeps the feet under the pelvis with ±15 cm of leg motion and steady arms.
  - The source clip is untouched (hash-verified).
  - Moving jumps (≥160 cm/s) keep `A_CT_StableFall`.
- **Result:**
  - Hip jump at the handover: 26 → 11–14 cm.
  - Feet in the air: ±30 → ±8 cm.
  - Frames `Evidence/v2_s2_idle.jpg`: the apex shows the legs together and tucked with symmetric arms, not the old split squat with one arm flung out.
  - Standing-jump air-plus-landing slide: 30.8 → 11.5 cm (together with 10.2).

### 10.2 Foot-placement plant tuning (Base AnimBP variables `PlantSettings_Default` / `PlantSettings_Stops`)
- **Finding:** after stops and landings, the idle clip (which has no footspeed curves) cross-blended the feet 11–20 cm at zero speed.
- **A/B:** five variants were compared on the same injected protocols, suites 1/2/3/5/10, at 30 FPS plus 10 FPS stops:
  - A: radius 45 with stop speed 60
  - B: original
  - C: stop speed 60 only
  - D: radius 45 only
  - E: radius 45 with stop speed 40
- **Stop speed 60 rejected:** it helped at 30 FPS but made 10 FPS walk stops much worse. Summed slide went 306 → 402/512, and the sustained forward stop went 5.9 → 27 cm.
- **Adopted E:** `PlantSettings_Default.UnplantRadius` 20→45 and `PlantSettings_Stops.SpeedThreshold` 20→40, persisted on both AnimBP class defaults.

| Metric (summed or per stage, cm) | Original | E (adopted) |
|---|---|---|
| Suite 10 starts/stops, 30 FPS | 295 | 231 |
| Suite 10 starts/stops, 10 FPS | 306 | 239 (stops 220 → 221) |
| Suite 3 regression total | 316 | 251 |
| Walk stop / wall stop | 9.2 / 5.5 | 1.0 / 1.7 |
| Short stops | about 12.5 | about 5 |
| Jog left turn | 32.4 | 4.6 |
| Diagonal starts (±45 sustained) | 17–21 | 3.6–4.0 |
| Sprint stops (suites 1/5) | 7–21 | 2.6–7.8 |
| Sprint 180 left reversal | 17.4 | 1.9 |
| Standing-jump landing | 20.7 | 11.5 |

- **Small regressions accepted:**
  - Fast camera-driven 180° recovery: 3.2 → 7.4 cm.
  - Sustained diagonal walk stops: +1 to +4 cm (they were already the worst rows).
- **Protected behaviours:**
  - P2 holds: the same `M_Neutral_Walk_Stop_*` clips are acquired at 10 FPS.
  - P1: taps unchanged.
  - Crouch, jump distinction and turns: unchanged.

### 10.3 Tooling incidents (evidence integrity)
- **Editor crash (11:58):** an access violation in python311 during the runner tick, right after an AudioMixer hardware timeout (same pattern as 05:06). All assets had already been saved.
  - On relaunch the crash-restore dialog was accepted, which rewrote `L_GR_SphirusHouse.umap` (17:25) from its pre-crash autosave.
  - The loaded world has no `PBI_QA_*` actors, and its game-mode override is the original `BP_GM_GR_GraceRanger`.
  - A byte-for-byte comparison with the post-E2 map is not possible, because no post-E2 hash was recorded.
- **Orphaned PIE watcher:** one from a killed QA chain ended later PIE sessions. The affected D runs were discarded and rerun.
  - Every A/B/C/E number above was recorded before or after the incident.
  - The watcher was fixed to unregister only its own handle, and the orphan was neutralised.

### 10.4 Newly observed issue (not fixed)
- **Jump apex camera:** the camera does not follow the jump height (camera Z relative to the capsule drops to 38 cm at the apex), so the head leaves the top of the frame (`v2_s2_idle.jpg` frames 4–5).
  - Unchanged from the baseline.
  - It needs a camera-owned vertical-follow decision (`GR_UpdateRig`), not an animation change.

### 10.5 Updated remaining issues
1. Walk forward jump air/landing slide is still 51 cm. Walk jumps now also use the stand-air loop below 160 cm/s, and the momentum carry (P5) is physical, so it is unchanged.
2. Sustained diagonal walk stops: 22–31 cm.
3. Idle settle after a sprint stop (`finish`): 18–19 cm. That is the idle cross-blend in the Stops→idle hand-off, which foot placement still releases. The root cause is not yet identified.
4. `wall_retreat` and `camera_backward_settle` slide proxies: 26 and 68 cm (backpedal away from a wall), unverified.
5. Jump apex camera framing (10.4).
6. Physical keyboard/mouse, gamepad, real 60 FPS and real-house play: still NOT_TESTED.

### 10.6 Assets changed in the second pass
- **New:**
  - `/Game/GraceRanger/Experimental/BodyInertia/JumpAir/PSD_LR_StandAir`
  - `.../JumpAir/A_LR_StandAir_Loop`
- **Modified:**
  - Sandbox `ABP_GR_MotionMatchingBase`: Select_5 option, `PlantSettings_*` defaults.
  - Sandbox `ABP_GR_MotionMatching`: `PlantSettings_*` defaults.
- **Checkpoint:** `Saved/Codex/LocomotionRealism_20260925/Checkpoint2_JumpAir/` (both AnimBPs from before the second pass, plus `sha256.txt`).
- **Compile:** all touched Blueprints are `BS_UP_TO_DATE`. The Base keeps its existing IsValid thread-safety warning.
- **Dirty:** no content packages. The house map is dirty in memory only (QA fixture add/remove). **Close the editor with "Don't Save".**
