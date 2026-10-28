# V2.34 working notes (2026-10-28)

Base: V2.33 production (Bridge a4417bc), editor UE 5.8, lock owner v234. Folder Saved/Codex/SHME_V234_20261028, tools Tools/SHME_V234_20261028.

## 1 Camera -> speed / facing dependency (owner trace, fresh graph dumps 04:05)
- `BP_GR_Player.CalculateMaxSpeed` (2 reads), `CalculateMaxAcceleration`, `CalculateGroundFriction` (2), `GetDesiredGait`,
  `GR_Impl_CR_UpdateBackwardIntent`, `GR_Impl_CP_PhysicalRedirect` (2; the actor-yaw writer: RInterpTo_Constant toward the CONTROL yaw in
  LookDrivenLocomotion, SetActorRotation), `GR_UpdateIdleTurn` all classify the move relative to `GetControlRotation`.
  CalculateMaxSpeed: dot(input, control forward) -> LB_SideSpeedScale / LB_BackwardWalkScale => the auto recentre turned a held D from
  side (417 sprint / 112 walk) into forward (490 / 132) and rotated the actor (walk: actor yaw == control yaw every row, v233k2 wturn rec).
- Camera-only readers (GR_UpdateRig TW_/CT_ camera, orbit) keep the control yaw. ABP CP_UpdateTransitionClock / SHM213_MontTick read it
  too (not changed in B1 - check).
- V2.33 latch: 30 deg threshold (small analog corrections ignored) + 0.06 s release blend (a 85 deg offset handed over in 0.06 s = jump).

## 2 V2.34 locomotion frame (DSL SHM_UpdateCameraV21 + install_v234_loco.py)
- InFrameOff: un-handed auto recentre; continuous hand-over by stick angular change + player look (LocoHandK 90 deg), 0 on release.
- LocoYaw: body / locomotion frame for the 7 BP readers (Select(GR234_LocoOn, GR234_LocoYaw, control yaw)).
- Exploration (LocoExploreEnabled): held lateral / forward-diagonal input (20..120 deg off the input frame), moving > 60, no player look
  for CamRecLookHold, no inspect -> the body frame = the input's world direction (the body decides; the camera follows the body);
  a look ends it; after release the body frame is held until a look / new input.

## 3 Sprint upper body: where the V2.33 source change went (stage234.py, same run, straight steady sprint)
- V2.33 report said "in game arm 58 -> 56, head unchanged" (upper232 metric incl. turns). Same-metric stage comparison:
  upper-arm swing 95.3 -> 76.1 deg at the MM mesh AND the visible body (exactly the 0.8 source scale): the arm change DID reach the
  visible body. Hand excursion: MM 46.7 -> 39.4 cm, visible 54.3 -> 46.1 cm (visible +7 cm = longer forearm reach after retarget).
- Neck lateral relative to the pelvis 17.0 (o) vs 16.8 (sc) at the MM mesh -> the source sway reduction is lost BEFORE the MM-mesh
  observation point (MM blend + ABP layers / SHME / PBI). Trunk lean visible +5.6 deg vs MM (retarget pose difference).
- Next: clipstage234 (source point, same metric) + ablations (SHME sway / lean / PBI) to find the lateral owner.

## 4 B1-B5 results (2026-10-28 04:30-06:21)
- Decoupling (camab234, same body version, camera on vs off, keys held): V2.33 prod sprint right 73 cm/s / 297 cm / 92 deg body yaw diff;
  V2.34 L / Lx / C / C2: 0.0 in every field (sprint, walk, jog, analog small corrections jcor after the net-deviation hand-over).
- Manual look DURING the recentre (cam34_jlook / slook retimed into the recentre: 6.4 / 6.8 s): CamRecDelta 2.37 -> 0.00 the frame the look
  starts, seen angle kept, recentre resumes after LookHold (prod 8.4 s, C2 9.0 s jog; 8.8 s sprint). First B2 attempt NOT_TRIGGERED.
- Walk recentre with exploration: settle 1.6 s, rate cap 46 deg/s (CamRecWalkRate 45), slide 7.8 (prod-camera-off 8.0, V2.33 walk rec 12.7).
- Envelope (envtime234): swing-out after the action sturn 1.33 s -> 0.40 s (peak after 11.7 -> 7.4), chain 0.83 -> 0.40, wallturn 0.33 -> 0.
- c29_combo (walk lateral chain) 57.6 -> 12.5 (C) but C2 (stability + body turn rate 150) 30.3; e29_chain 6.5 -> 13.9 (exploration in sprint
  brakes), jstart 42 -> 56 (exploration inside a start) -> B6 C3: exploration starts only in calm normal travel, no turn-rate limit.
- Release-repress owner: component family stays 3 with RevGrace AND the ABP family stays 3, but Update_MotionMatching's default chooser
  searches the dense stand STOP DB without acceleration and the dense stand START DB at the re-press -> B7 ABP reversal-DB keep.
- Forward jog stop (SHM_A_CP2_Jog_Fwd_Stop) closing step: the trailing (left) ball slides back 35 cm then 19 cm forward at z ~0 while the
  capsule already stopped (j30_slow 8.20-8.47 s); in every chain (22 cm). clipstop234 (B6) decides source vs runtime.
- Sprint attitude (s34_straight, 227 straight steady rows, 2 identical reps): calm candidate reaches the visible body: upper-arm 89.5 -> 70.5
  deg, hand 56 -> 43 cm (visible), trunk 29.4 -> 17.7 deg (visible; jog 12.4), shoulder counter-rotation 52 -> 31 deg, neck lateral 12.7 ->
  10.4 cm. Runtime adds ~3 cm neck lateral (not PBI / FootPlacement / SupportShift - MM blending) and +5-6 deg visible trunk (retarget).
