# SHME V1 architecture (2026-09-25)

```
Enhanced Input → CMC (velocity, accel, floor, max speed)            [CMC owns movement physics]
        │
        ▼  BP_SHM_HumanMotionComponent.SHM_Tick (PostPhysics)       [SHME owns physical state + planning]
   SHM_UpdateState      velocity/accel/yaw-rate filters, desired velocity, momentum, grounded, support plane
   SHM_UpdateBody       16-segment COM, COM velocity, foot contact (hysteresis), support side/region,
                        stability margin, LIP capture point + confidence
   SHM_UpdatePlanner    traction-normalised turn/brake/reversal/recovery demand, braking distance
   SHM_UpdateFootPlan   bounded recovery-step target (planning signal)
   SHM_UpdateAir        takeoff record, air height/apex, landing severity/impulse proxy/recovery
   SHM_UpdateEnvA/B     camera-space clearance probes (2 per frame), SHM_UpdateEnvDerived (width,
                        constrained level with hysteresis, open-space confidence, boom/shoulder targets)
   SHM_UpdateCameraSignals  critically damped landing dip / brake carry, apex-aware air-follow weight
   SHM_Debug / SHM_Telemetry / SHM_PerfBegin/End
        │
        ├─► ABP_GR_MotionMatchingBase.SHM_Snapshot (game thread, in CP_UpdateTransitionContext)
        │       → PBI_UpdateDirection severity = lerp(PBI heuristic, max(TurnSeverity, ReversalDemand), BodyCouplingBlend)
        │                                                        [PBI owns the procedural body springs]
        └─► BP_GR_Player.GR_UpdateSHMSignals (first in GR_UpdateRig)
                → desired arm × CamBoomScale, base shoulder × CamShoulderScale, DesiredPivot + CamOffset,
                  CT_UpdateCameraHeight air follow/lag = lerp(profile, SHME targets, CamAirFollowWeight)
                                                        [GR_UpdateRig owns camera + collision resolution]
Motion Matching / CP evaluators still choose the pose; FootPlacement/LegIK still own contact correction.
```

Not integrated in V1 (computed + visualised + logged only): foot-target → IK, capture point → MM query channels, FootPlantStrength → FootPlacement plant settings. Each needs its own A/B before wiring.

## V1.1 execution layer (2026-09-25)

```
SHM_UpdateFootPlan   capture point -> anatomical reach region (facing frame around the support foot: fwd 70 / back 40 /
                     lateral 35 cm) -> ground line trace (slope/step validity) -> FootTarget, SwingSide, StepUrgency,
                     FootTargetConfidence, RecommitDemand (target clamped by reach), FootPlantStrength
SHM_UpdateExecution  state machine with dwell hysteresis (ExecMinDwell 0.08 s): 0 none, 1 weight shift, 2 support transfer,
                     3 committed plant, 4 recovery step, 5 brake-and-replant, 6 reversal recommit, 7 landing support,
                     8 post-stop stabilise; LandingSupportActive -> PlantRadiusOverride; post-stop latch -> HoldStops
SHM_UpdateSettle     one bounded capsule settle per real stop toward the projected COM (so the idle does not re-centre
                     the body with planted feet); gated by entry speed, travelled distance, input-hold time (never after
                     micro taps), double support, 8 cm minimum offset, 25 cm budget, and a wall sweep
Perf laps            CostState / CostPlanner / CostEnv / CostCam
        │
        ├─► ABP SHM_Snapshot -> SHM_LandingSupport -> Get_FootPlacementPlantSettings selects PlantSettings_Landing
        │       (Default settings with UnplantRadius = LandingPlantRadius 150) during the landing recovery window
        └─► ABP SHM_Snapshot -> SHM_HoldStops -> Update_MotionMatching entry keeps the current database (DoNotInterrupt)
                (MotionMatchingPhysicalGuidanceEnabled, default OFF: no measured benefit in V1.1)
```
Flags: FootExecutionEnabled, LandingSupportEnabled, PostStopStabilizationEnabled, SettleEnabled, MotionMatchingPhysicalGuidanceEnabled.

## V1.2 motor model + animation reconstruction (2026-09-26)

```
SHM_UpdateGait       (after SHM_UpdateBody, under SupportAnalysisEnabled) gait phase 0 double / 1 L stance / 2 R stance /
                     3 flight with GaitMinDwell hysteresis, heel-strike/toe-off events, L cycle time, cadence; support load
                     L/R (COM projected on the inter-foot axis x contact confidence); LIP centre of pressure
                     p = x - (h/g) x'' clamped to the support; COM acceleration; yaw angular momentum L_z = m r_g^2 w and
                     torque; braking impulse J = m dv; APA (CoP shift opposite to the step for ApaDuration after an intent
                     onset from rest); PhysicalMotionIntent PMI_Type/Direction/Urgency/Cost (telemetry + concept only)
SHM_UpdateSettle     + SettleActive, stance error vs the Ranger idle stance (IdleStanceLX..RY on the anthropometry), IdleHold,
                     expected-benefit gate (no settle when the stance-preserving idle will hold); SettleEnabled default OFF
SHM_UpdateCameraSignals + landing phase model CamPhase (0 grounded 1 ascend 2 apex 3 descend 4 contact 5 recovery),
                     critically damped CamRecoverWeight, CamLandResponse, CamAirLagTarget/CamFollowTarget/CamResponseTarget
                     (committed descent v_z < -CamDescendSpeed gets follow 0.85 / lag 10 / response 40 at full weight)
        |
        +-> ABP (game thread, END of BlueprintUpdateAnimation after PBI_UpdateForwardJump: SHM_Snapshot, SHM_StanceCapture)
        |       SHM_IdleWait  = feet still settling / settle active before the takeover -> ANDed (NOT) into
        |                        BlendListByBool_5.bActiveValue (the idle takeover)
        |       SHM_IdleEntry = takeover edge (CP_IdleReady and not HasVelocity and not IsFalling and not IdleWait)
        |       SHM_StanceCapture: on entry SavePoseSnapshot 'SHM_StanceHold'
        |       SHM_IdleHold  = decided once per entry (stance error > IdleStanceTolerance after a real stop), kept until
        |                        the next entry; AnimGraph BlendListByBool_21: hold ? LayeredBoneBlend(PoseSnapshot,
        |                        Ranger idle from spine_01) : Ranger idle  -> feeds BlendListByBool_5 pose 0
        +-> BP_GR_Player.GR_UpdateSHMSignals: + GR_SHM_LandResponse (profile land response + SHME boost) wired into
                CT_UpdateCameraHeight's landing-recovery rate; air follow/lag/response take the phase targets with
                CamLagWeight
Animation: 23 owned corrected stop clips /Game/GraceRanger/SHME/Animations/Stops/SHM_* (pelvis+legs held from the last real
step; PoseSearchBranchIn into the project-owned stop databases with ModifyCost -30). Vendor clips untouched.
```
Flags: StanceIdleGateEnabled, CameraLandingPhaseEnabled (+ Cam* / Gait / Apa / Units fields, see REPORT V1.2 section 11).

## V1.3 physical motion routing (2026-09-26)

```
SHM_UpdateRouting    (after SHM_UpdateExecution) family per frame with hysteresis (RouteMinHold / RouteCooldown):
                     0 normal | 1 minor recovery | 2 hard turn (|L_z| > RouteHardTurnAngMom, inert in strafe control) |
                     3 reversal (CP/pivots own the motion) | 5 blocked (intent into an obstacle, sweep BlockedProbe, no
                     progress) | 6 strong recovery. Priority blocked > reversal > recovery > hard turn. Recovery needs
                     RecoveryDemand, plan confidence, speed < RouteRecoveryMaxSpeed, an unloaded swing foot or double
                     support, and a clear sweep support -> FootTarget. RecoveryDirLocal/Distance/Side/Urgency, StanceClass.
        |
        +-> ABP SHM_Snapshot: SHM_Family, SHM_Blocked (blocked suppresses the idle takeover + latch); the takeover entry
        |       edge now carries every BlendListByBool_5 term incl. MovementState == Idle (the wall-push stale hold).
        |       CP_TC_Support/Confidence <- SupportLoadR - SupportLoadL when the load difference > 0.3 (start foot).
        +-> Update_MotionMatching entry: family 1|6 -> PSD_SHM_Recovery ; family 2 -> run/sprint pivot database ;
                else the V1.1 hold branch and the chooser flow.
Vocabulary: /Game/GraceRanger/SHME/Animations/Recovery/ SHM_Rec_* (14, AAMS walk starts) and SHM_RecS_* (16, run starts):
first step kept, root + lower body held from 2 frames after the plant; manifest in Saved/Codex/SHME_V13_20260926.
```

## V1.3.1 integration closure (2026-09-26)

```
SHM_UpdatePlanner    PerturbState: an unexplained speed increase (no intent, or above 1.5 x the CMC max acceleration,
                     > PerturbAccel 300 cm/s^2) latches 1 and decays with PerturbTau 0.6 s. RecoveryDemand = CaptureError x
                     unintended part (1 - intent alignment, or PerturbState) | traction excess; attacks instantly on the push
                     frame. Walking keeps the capture point outside the support by design (CaptureError ~1 while stepping),
                     so the unintended part is what separates a stumble from a step.
                     Recovery demand = CaptureError x PerturbState (push only): intent misalignment is a turn class,
                     traction excess at an obstacle is the blocked class (both produced recovery steps when routed live).
SHM_UpdateRouting    velocity-redirection turn model: DeltaVMag, RedirectionAngle, BrakeRequirement, RedirectionDemand =
                     |dV| / (mu g t_step), TurnClass 0-3; start transfer (family 4) from a held stance for StartTransferMaxTime;
                     RouteRecoveryMaxSpeed 450 (a strong recovery covers a run-speed push).
        |
        +-> ABP SHM_Snapshot: SHM_Family, SHM_StartSide (foot that must step), SHM_IdleWait is also true while a family is
        |       routed (the idle takeover releases the MM branch); guard IsValid(SHME component) with the class pin set by
        |       path string (a Python object as pin default is silently rejected -> class was ActorComponent).
        +-> AnimGraph: MotionMatching.SearchThrottleTime = SHM_IdleWait ? 0 : original (AAMS throttles 1-3 s while
        |       standing; a routed database was never searched inside the family window).
        +-> Update_MotionMatching entry (typed database member variables, not pin defaults):
                family 1|6 -> SHM_RecoveryDB (PSD_SHM_Recovery_v131, 30 entries, DataAssetFactory-created)
                family 4 -> SHM_StartTransferDB_L / _R by SHM_StartSide (PSD_SHM_StartTransfer_L/_R, 7 + 7 walk starts)
                family 2 -> pivots ONLY with RouteHardTurnToDatabase (default off: live, it overrides AAMS's pivot choice,
                +3-6 cm per approach, 84 cm at a wall) ; else V1.1 hold branch + chooser flow
        Recovery from a CP-owned stop: SHM_Snapshot clears CP_StopOwned for families 1/6 (the MM node owns the pose);
        CP_StartOwned is never released (a routed MM start costs 15-25 cm against the distance-matched CP start).
QA: BP_LTP_QA.WorldOffset (instance editable) shifts the protocol's fixed teleports (harness `house`/`origin`);
    QA shove = CharacterMovement.AddImpulse(bVelocityChange) at QAPerturbTime (game time), levels 120/260/420 cm/s.
Metadata: asset metadata tags SHME.* on every recovery / start-transfer clip (set_clip_metadata.py).
```

## V1.3.2 turn-in-place continuity (2026-09-26)

```
Facing owner: GR rig (LookDrivenLocomotion) rotates the ACTOR toward the look, standing or not - untouched.
Root yaw owner while standing: SHME. SHM_Snapshot keeps SHM_RootCounter = -(actor yaw change) while idle (tipOn), applied
  by RotateRootBone_1 on the final pose path (Inertialization_0 -> RotateRootBone_1 -> SaveCachedPose 'ToLayers'); the AAMS
  TurnInPlace_Layer OffsetRootBone is inert in this project (measured) and stays bypassed; foot placement stays ON (it
  keeps planted feet in world; toggling it pops the feet).
Turn state: SHM_TurnActive enters at |counter| > TipEnterAngle (35 deg), exits below TipExitAngle (8) after TipMinTime
  (0.3 s); while active: takeover released (SHM_IdleWait), stance hold released, CP stop latch released, MM routed to
  PSD_Dense_Stand_TurnInPlace (SHM_TurnDB, continuing pose invalidated), counter unwinds at TipUnwindRate (90 deg/s);
  turn end re-enters idle (fresh stance snapshot). Movement releases the counter at TipMoveRelease.
Stance identity: the takeover's non-hold pose = LayeredBoneBlend(base = cached 'MainStates' (AAMS idle / turn clip lower
  body), spine_01+ = Ranger idle) - one lower-body family (AAMS clips or the snapshot of an AAMS stop stance).
Recovery foot side: PSD_SHM_Recovery_L / _R (per PlantFoot) routed by SHM_StartSide when SHM_SideConfident
  (|SupportLoadR - SupportLoadL| > RecoverySideConfidence 0.3), else the combined database. V1.3.3: both are latched
  per recovery episode (SHM_CommitSide / SHM_CommitLatched taken on the first confident frame of family 1|6, held until
  the episode ends); measured 100 % side + database consistency on shoves, 17/18 forced episodes (first frames on the
  combined database until confidence = design). The raw component RecoverySide flips after the plant, so score the
  ABP-committed side (side_agreement.py 'committed side' line), not the raw one.
QA: harness `no_ltp` + `yaw` schedule (look injected with AddYawInput), per-tick yaw / mesh-socket telemetry, tip_report.py.
```

V1.3.4 (2026-09-26/27): committed redirection episode (SHM_UpdateRouting: RedirectActive / DirLatched / Time / End; starts on a
  > 50 deg velocity-vs-desired angle above 120 cm/s, ends on alignment < 25 deg after 0.2 s, 0.7 s timeout, new intent > 45
  deg, or ground / intent / obstacle loss - NOT on speed loss). ABP: SHM_RedirectActive / Frames / Hold (snapshot; the hold
  must read the ABP's gated SHM_Family, the component Family is 2 during turns), Update_MotionMatching entry branch holds
  CurrentSelectedDatabase in SHM_HoldDB (DoNotInterrupt) and skips the tree, AnimGraph SearchThrottleTime = 0.25 s while held.
  Measured: no one-frame skeletal teleports exist at database switches (V1.3.3 numbers were world travel); bursts jog 17 -> 10.
  Camera (SHM_UpdateCameraSignals -> GR_SHM_* pipes): CamBodyZ spring on pelvis-minus-capsule height (stairs framing fix, rest
  offset 2 cm, 3.5 rad/s, attenuated in constrained space), CamShoulderSide follows lateral travel (mirrored diagonals),
  CamIntensity -> boom, accel / turn springs, CamConstrainedRise 22. Recovery: PerturbState held while capture error > 0.35
  (max 0.8 s), family persists until capture error < 0.4 and contact > 0.5 (max 0.7 s). Teleport rebase in SHM_UpdateBody.
  Normalization: SHME databases use PSN_SHM (own set); PSN_Dense_All is back to its 25 vendor databases (the shared set
  changed the AAMS diagonal tap-stop selection). Take Recorder from PIE by script fails ("no valid sources"); MRQ not enabled.

V1.3.5 (2026-09-27): redirect bridge databases PSD_SHM_Redirect_{JogReversal,JogLateral,SprintReversal,SprintLateral}
  (/Game/GraceRanger/SHME/Animations/Redirect; PSS_Default, no normalization set; project clips carry an extra BranchIn
  track per bridge, vendor sprint turns duplicated as SHM_*). Episode latches RedirectClass (2 reversal > 120 deg, 1 lateral,
  0 under 200 cm/s) and gait (sprint > 340); the Update_MotionMatching entry routes frame 1 of an episode to the bridge
  (InterruptOnDatabaseChange), sets CurrentSelectedDatabase, then the V1.3.4 hold keeps it; hold/bridge accept families
  0, 2, 3 (SHM_RedirectFamOK); the alignment exit needs speed > 80. Measured: jog 180 = pivot + rear (2 switches), jog
  bursts 17 -> 5; sprint reversal still alternates mirror pivots. ANY PoseSearch database property change (bias,
  normalization) re-indexes the whole set: the next runs report index skips and select None - wait for 0 skips.
  Camera: chest anchor (spine_03 minus CamChestRestOffset 21, bound +-35, no constrained attenuation, no rise),
  openness = overhead clearance (EnvUpLength 600) x side room -> boom +38 %, shoulder 0.7, FOV -2..+1 outdoors through
  the new GR_SHM_FOVDelta pipe (GR_UpdateRig SetFieldOfView = GR_CameraFOV + delta). Lens C selected: 220 / 238 / 254 cm
  by gait outdoors, 155 indoors. The rig's collision is ONE sphere trace (CameraProbeRadius 14) from the pivot; the
  indoor arm (145 x narrow 0.89) keeps the camera ~60-100 cm behind on the enclosed stair flight at pitch 0.

## V2.0 "Momentum & Contact" (2026-10-14; built, validation pending — see Saved/Codex/SHME_V2_20261014/)

```
SHM_UpdateBodyTargets (after SHM_UpdateRouting, flag BodyTargetsEnabled; 284 nodes): research-backed body targets, each
  behind its own consumer flag (default OFF) and smoothed in the component with critically damped springs:
  LeanLat  (deg, + right)  <- curve lean atan(v * yaw_rate / g) into the turn (CurveLeanDirectEnabled, cap CurveLeanMaxDeg)
                              + APA trunk toward the intent (ApaBodyEnabled)
  LeanFwd  (deg, + fwd)    <- braking posture BrakeLeanDeg x BrakingDemand (BrakePostureEnabled) + APA trunk
  PelvisOffset (cm, character frame x fwd / y right / z up) <- curve inward (PelvisInwardCm), support-loaded lateral shift
                              (SupportShiftEnabled), APA pelvis toward the loaded foot + back (ApaPelvisCm / ApaBackCm),
                              brake drop (BrakeDropCm, gait-scaled), landing absorption (LandingAbsorbEnabled); clamped to
                              PelvisOffsetMaxCm; PelvisOffsetComp = the same vector in the -90 deg mesh component frame
  SwitchWindow / PlantEdge / RedirectPlants <- foot-phase gates (PhaseGatedSwitchEnabled: SwitchWindowSec after a heel
                              strike or after SwitchMaxWait; RedirectPlants = heel strikes inside a redirect episode)
        |
        +-> ABP SHM_Snapshot (install_idle_wait.py): SHM_LeanLat / SHM_LeanFwd / SHM_PelvisOffset / SHM_SwitchWindow /
        |       SHM_PlantEdge / SHM_RedirectPlants / SHM_GateOK (gate scope: moving with intent, no family route, no
        |       redirect episode, not falling, valid CurrentSelectedDatabase) / SHM_HandoverHold (HandoverNeedsPlant: an
        |       episode that ended by ALIGNMENT with the input held keeps the V1.3.4 database hold until the next heel
        |       strike, <= 0.3 s; OR-ed into SHM_RedirectHold)
        +-> PBI_Update (install_body_v2.py): PBI_LateralTarget += SHM_LeanLat / 0.6, PBI_ForwardTarget += SHM_LeanFwd / 0.6
        |       (before the pelvis springs; spine_01/02/03 and clavicles inherit the PBI fractions),
        |       PBI_PelvisTranslation = ClampSizeMax(old) + SHM_PelvisOffset (component frame; applied by the FeetIK layer's
        |       pelvis ModifyBone with Alpha = PBI_Alpha, BEFORE LegIK, so the feet stay planted)
        +-> Update_MotionMatching entry (install_phase_gate.py, installed after the Phase 0 baseline): while
                NOT SHM_SwitchWindow AND SHM_GateOK -> SetDatabaseToSearch(CurrentSelectedDatabase, DoNotInterrupt), tree skipped
Tick (build_tick.py): ReceiveBeginPlay reads IntentTickPrePhysics once: true -> SetTickGroup(PrePhysics) +
  AddTickPrerequisiteComponent(CharacterMovement) + Mesh.AddTickPrerequisiteComponent(this) (the ABP then reads the
  CURRENT frame's routing; bone-derived state is one frame old); false -> PostPhysics (V1 behaviour).
Rules learned: never rebuild SHM_UpdateRouting (its rebuild OOM-crashed a fresh editor at 104 GB on 2026-10-14; new
  routing-adjacent logic goes into the snapshot or a new small function); only_v2.py restricts build_funcs to the new
  function; `v2_check.py` validates DSL/members offline before any editor build.
Validation 2026-10-14 (interleaved same-process A/B, AB_RESULTS_R2.md): CurveLeanDirectEnabled (closed loop) technical PASS -
  trunk lean slope vs atan(v*omega/g) 0.37 -> 0.98 (sprint 25 deg/s), 0.10 -> 0.82 (jog); PhaseGatedSwitchEnabled and
  HandoverNeedsPlant FAIL (every hold adds planted-foot skating, as the protected baseline already recorded); IntentTickPrePhysics
  fewer selection switches but +4-13 cm skating in stop stages (CP gate timing) -> off; LandingAbsorb no effect (landing clips
  already dip 22-27 cm); ApaBody small start improvements. A/B metrics are frame-rate dependent: compare only runs with the same
  telemetry rate (rows/s) in the same editor process; the real-map max switch-jump varies +-8 cm between identical runs.
  Round 3: BrakePosture = stop-event envelope (speed lost since the peak, released over BrakeRecoverSec of standing) adds 1.5-2.3 cm
  at sprint/jog stops; SupportShift 3 cm raises straight-walk pelvis lateral RMS 1.7 -> 2.4-2.7 cm.
Production state 2026-10-14 04:55 (DA_SHM_Response_Default, saved): CurveLeanDirectEnabled / BrakePostureEnabled /
  SupportShiftEnabled / ApaBodyEnabled ON; PhaseGatedSwitchEnabled / HandoverNeedsPlant / IntentTickPrePhysics /
  LandingAbsorbEnabled OFF. qa_pie.py resets every field to the schema default (all off) per QA run - pass shme_flags to test them.
```

## V2.1 transition continuity + cinematic camera (2026-10-14; Saved/Codex/SHME_V21_20261014/, tools Tools/SHME_V21_20261014/)

```
Measurement: pop_report (root-relative upper-body acceleration, events > 25 m/s2 attributed to MM switch / CP flags / layer;
  dedup of same-time harness rows + skip frames next to > 0.1 s gaps - the "54-68 m/s2 pops" of the first matrix were hitches),
  cam_report (chest framing x/y, 0.3 s mean, framing speed, camera excess acceleration vs the root), skate_report, jumps.py
  (MM database / clip switches + same-clip time jumps), gait_report (tempo changes), frames/twist/camseries (per-frame dumps).
Fixes (all A/B'd interleaved in one editor process, promoted 2026-10-14 by promote_v21.py; checkpoint/ + checkpoint/assets_db):
  T3 diagonal vocabulary: ABP IsPivoting trajectory-turn lower bound <- SHM_PivotMinTurn (55 -> 115) and RedirectLateralEpisodeOff
     (snapshot SHM_RdLatSkip: an episode that starts below RedirectLateralMaxAngle 110 deg is no episode / class / hold) ->
     FL<->FR jog swaps stay in the CT_JogSteady directional loops instead of CP2 pivots / lateral redirect bridges.
  T1 PBI handover inertialization (DA_PBI_Prototype): Small/Gait/HardPivot/Landing 0.1/0.16/0.09/0.14 -> 0.25/0.3/0.22/0.25
     (BlendListByBool_15/16/17 = CP start / DI start / CP stop). UE merges same-frame inertialization requests to the MINIMUM.
  T8 start-onset head pop: snapshot SHM_IdleUpperW (quiet-idle upper-body layer) fell with tau 0.05 s while the takeover
     (BlendListByBool_5) still showed the idle branch -> head 2-3 cm jump at every start. Fall tau <- IdleUpperFallTau 0.3.
  T9 start commitment: StartTransferMaxTime 0.9 -> 0.65 (the start family outlived the start clips' sampled range -> MM re-picked
     inside PSD_SHM_JogStartQ_* and replayed the push-off) + ContinuingPoseCostBias -0.22 -> -2.0 on PSD_SHM_JogStartQ_L/R and
     PSD_SHM_SprintStart_L/R (runtime-only field, excluded from the DDC hash: set without notifications = no re-index).
  T5 camera (SHM_UpdateCameraV21, after SHM_UpdateCameraSignals, CamSwapV21Enabled): shoulder side target with hysteresis
     (CamSwapEnter/Exit lateral ratio) + dwell (CamSwapDwell / CamSwapReturnDwell) + critically damped 2nd-order spring
     (CamSwapFreq) + partial mirror (CamSwapAmount). Production "c2": 0.5 / 2.2 rad/s / 0.8 s / 1.0 s / enter 0.6 / exit 0.3.
Rejected: idle takeover blend 0.2 -> 0.35 (T2, mixed), MM PoseReselectHistory 1.0 (does not stop jump-backs: the re-pick lands
  on frames never selected, e.g. one frame before the clip's entry point).
Known open (not V2.1 scope): walk diagonal loops slide 4-10 cm per plant (A_LB_Walk_FwdLeft, A_CT_Walk_RearLeft/RearRight);
  tap glide 15-21 cm (MM crossfade start-transfer -> idle before the stance hold); sprint starts toward lateral / rear directions
  use forward run starts (85 m/s2 spike, no rear/lateral sprint start vocabulary); lateral jog start -> strafe loop torso twist.
Harness/editor rules: qa_pie never resets pbi_flags / abp_flags (pass explicit values every run) and dirties both ABP CDOs + the
  PBI DA (reload before any ABP save: revert_noquit.py / revert_quit.py); build_profiles now keeps saved DA values; PIE runs leak
  ~0.6 GB each (restart at ~38 GB, v21_lib.sh mem_guard); engine assert GameViewport.IsUnique at PIE teardown every 11-19 PIEs
  (chains relaunch + warm up); never edit a script a running chain invokes (bash reads by offset).
```

## V2.2 start vocabulary + tap gate (2026-10-14; Saved/Codex/SHME_V22_20261014/, tools Tools/SHME_V22_20261014/)

```
Locomotion is camera-facing strafing: start clips must END in the destination loop's body orientation (strafe loops CT_Jog_Left/
  Right have the pelvis turned ~72 deg). Turning starts (TurnL/R 090/135/180: body square to a root that rotates) hand over with a
  torso twist; the side-split start DBs only had the strafe / back starts in the R-swing database.
V22-J  SHM_JogStartDB_L/R -> PSD_SHM_JogStartS_L/R: both sides get Bwd / Left / Right / LS_Left / LS_Right strafe starts + both
       045 turn starts; forward starts per first swing foot; 090/135/180 turn starts dropped. Jog start 90 deg window 46-58 -> 19-24.
V22-S  SHM_SprintStartDB_L/R -> PSD_SHM_SprintStartT_L/R: sprint F/FL/FR + relaxed run + the quiet strafe/back jog starts for
       lateral / rear directions (the stance-converted run-start set "S" pushed off at 46-54 m/s^2 toward -135: rejected).
V22-T  SHM_Snapshot feetMoving threshold <- SelectFloat(InRange(SpeedPeak, -1, SHM_TapPeakMax) ? SHM_TapEntrySpeed :
       IdleEntryFootSpeedMax), production 60 / 150 cm/s: after a tap the MM crossfade of the aborted step keeps the rendered
       feet "moving" (the wait measured its own glide); a GLOBAL raise also made walk stops enter the takeover early (25 -> 40).
       SHM_HoldMinPeak (stance-hold literal 30 -> variable, kept 30): 10 halves tap skating again but the held aborted-step
       stance pops the NEXT start (47-61).
All new: databases are created (DataAssetFactory) + filled by BranchIn tracks SHME_V22_<db> on project clips; never edit the
  existing DBs; index by opening them in the asset editor (BuildIndex Succeeded) before any PIE.
Open: jog reversal zero-speed crossing - the one-frame peak (~30, max 49-52) is the SHM_IdleWait flip at speed ~0 with the input
  held, NOT the bridge clip (a backward pivot in PSD_SHM_Redirect_JogReversalP/Q gave the same peaks; not promoted).
Harness: a 0.1 s jog gait tap could land press+release in one input frame (hitch) -> 'jog' runs WALKED (5/10); qa_pie now holds
  it >= 3 game frames; v22_ab.sh reruns any j* run with vmax < 200. ABP database variables are A/B-able through abp_flags
  (object paths; qa_pie loads '/Game/...' strings).
```

## V2.4 weight, turn physics, walk lean, camera roll (2026-10-15; Saved/Codex/SHME_V24_20261014/, tools Tools/SHME_V24_20261014/)

```
Measurement: feel_report.py (per run -> Feel/<label>.json): mouse turns (yaw ramp steps 90/0/-90/0/180/0 at 180 or 720 deg/s
  through IA_Look) rate_max / angular accel at turn start + end / settle / lateral g / lean into the turn; A/D 90 deg cuts
  (heading 90 % time, lateral g, speed loss); stops (time, distance, decel g); starts (t90, accel g). cut_lean.py = peak shoulder
  roll + head-pelvis lateral INTO a move change (first 1 s); lean_stage.py = steady lean (>= 0.6 s into a stage); cam_body.py =
  camera-on-chest slope / corr in the slow body band. v24_compare.py = markdown table + V2.1 Pops / Skate / Cam.
Human reference: comfortable cut / turn 0.3-0.5 g; walk start ~1.0 s, jog 1.0-1.5 s. V2.3 production was 0.9-1.4 g in jog /
  sprint turns and cuts with angular-accel spikes 1800-4400 deg/s^2 (the actor yaw snaps toward the camera at LookTurnRate).
Why data alone failed: actor yaw follows the camera input (RInterpTo_Constant at LookTurnRate[gait] x MapRange(|delta| 65..130 ->
  1..1.6)) and the CMC turns velocity toward the input with time constant 1/GroundFriction (90 deg cut lateral accel ~ F 1.414 v):
  lowering LookTurnRate / friction a little barely changes the lateral g, a lot makes walking sluggish. Physics caps instead:
G1 turn cap (GR_Impl_CP_PhysicalRedirect, BP_GR_Player): InterpSpeed <- min(LookRate, TurnLatAccelMax / max(v, 50) * 57.3,
   TurnSoftK * |delta|) each floored at TurnRateFloor -> rate limited by lateral accel at speed, and a soft start / soft arrival
   (proportional term) instead of a constant-rate snap. Fields on BP_GR_MotionProfile, 0 = off (install_v24_gr.py).
G2 cut cap: GroundFriction <- min(friction, CutLatAccelMax / (1.414 max(v, 40))) (VariableSet_0 <- Select(CutLatAccelMax > 0)).
G3 heavier momentum (DA_GR_LocomotionBehavior): accel 300/440/540 -> 200/300/360, braking 330/470/590 -> 290/410/520,
   StartEaseScale 0.78 -> 0.65 (stops kept short on purpose: humans stop faster than they start).
L1 walk A/D lean: NOT a layer (PBI lateral lean / direction reaction / profile, orientation warping, SHME body flags each change
   the cut lean <= 1 deg). MM passes through the left-step phase of A_LB_Walk_FwdLeft (shoulder roll -8 deg) for ~1 s after a
   W -> A cut. v24_roll_bake.py: per frame counter-rotation -0.5 x shoulder roll about the root heading axis, spread over
   spine_01..03 (pelvis / legs / root untouched -> contacts kept) on A_LB_Walk_FwdLeft/FwdRight/Left/Right +
   A_CT_Walk_RearLeft/RearRight; re-key PSD_LB_WalkLoops, PSD_CT_Walk_RearLeft/RearRight (tag V24R1) + warm runs.
   Walk F->L cut 10.2 deg / 6.1 cm -> 5.4 / 4.1; A/D walk cuts 4.0-8.4 -> 2.2-4.1 deg; skating / pops not worse.
C1 body-anchored camera pivot (SHM_UpdateCameraV21, CamBodyH*): REJECTED / off - chest slow-band motion is 1-2 cm, the pivot
   moved 0.4-0.5 cm: invisible, and gain high enough to read pulls the frame with gait sway.
C2 camera roll (CamRoll*, SHM_UpdateCameraV21 -> comp CamRollV24 -> BP_GR_Player GR_SHM_CamRoll -> GR_UpdateRig MakeRotator
   Roll of the RangerCameraBoom relative rotation): horizon follows the shoulder line roll (upperarm z difference x 1.64 deg/cm),
   gain 0.2, critically damped 2.5 rad/s, clamp 3 deg, only grounded and > 40 cm/s. Corr with body roll 0.45, +-1.2..2 deg.
Final (2026-10-15, 2 interleaved reps, V2.3 prod -> V2.4; promoted by promote_v24.py, verify_v24_final.py ALL_OK from a fresh
  editor): turn angular-accel spikes 2200-4500 -> 700-1350 deg/s2; turn lateral g jog 0.87 -> 0.61, sprint 1.35 -> 0.73, fast
  jog 1.10 -> 0.67; A/D cut g jog 1.04 -> 0.65, sprint 0.99 -> 0.65, swap / reversal 1.13 -> 0.70; starts 0.46/0.66/0.87 ->
  0.71/0.98/1.29 s; stops 0.46/0.67/1.03 -> 0.51/0.74/1.17 s; body catches a mouse turn after ~1.0 s jog / 1.4 s sprint (knob
  TurnLatAccelMax). Pops total 95 -> 83, P2 14/18, Accessed None / index skips 0. Trade-offs: taps skate p90 7.1 -> 7.7;
  slower starts hand over start -> loop at 250-280 cm/s (27-33 m/s2).
Open: walk-stop HALT pop (V2.3 equal): the frame ABP HasVelocity flips false the pelvis moves ~2.8 cm (25-50, up to 74 by frame
  alignment). NOT stride / orientation warping, foot placement, offset root bone, steering, PBI profile / direction reaction,
  SHME brake / body flags, StopEaseScale (12 variants, v24_stopdiag.sh + stop_end.py); clip smooth, no MM same-clip jump.
  Suspects: AnimGraph HasVelocity -> BlendListByBool_5 (idle takeover, 0.1 s Hermite) and SHM_Snapshot SHM_BodyBlend step
  (HasVelocity SelectFloat) -> PBI_DC_Severity.
Harness: behavior_flags write DA_GR_LocomotionBehavior in memory and are never reset (pass the full explicit set every run,
  incl. the four cap fields); localized K2 node type names ("Min(Float)", not FMin) in graph checks; adding fields to
  BP_GR_MotionProfile dirties DA_GR_LocomotionBehavior (save only after a value check: save_grda.py); the yaw ramp with
  look:"ia" is the only way to test mouse turns (camera "excess" in those runs is the orbit, not a defect).
```

## V2.5 human turns, sway, walk-start arms (2026-10-15; Saved/Codex/SHME_V25_20261015/, tools Tools/SHME_V25_20261015/)

```
User feedback on V2.4: arms pressed to the body at walk starts; walk sways; jog / sprint turns feel like a bicycle; sprint
  W+A / W+D stays diagonal like cornering; general slide feel.
Measurement: arms.py / arms_by_clip.py (upper-arm abduction, hand-hip gap; harness field "vbones" = visible-body extra bones,
  "mbones" = MM-mesh bones), sway.py (lateral pp of head / chest / pelvis vs the capsule, shoulder roll, camera roll), turn_shape.py
  (speed loss, path 90 % time, min radius, peak lateral g, body lead over the path), glide.py (within-stride pelvis speed).
A1 arms: the CP start branch (BlendListByBool_15 <- SequenceEvaluator_0 <- CT_GetCPStartSequence) plays
   A_LS_M_Relaxed_Walk_Start_F_Lfoot / A_TC_WalkStart_R (0.4-4 deg arm abduction; loop 11, idle 14). ABP telemetry mmanim is the
   MM selection UNDER the CP branch (M_Ranger_Walk_Loop_F_PureForward_CWF) - not what is shown while CP_StartOwned. Baked +9 deg
   upper-arm abduction (v25_arm_bake.py): game start abduction 5.4 -> 10.4-10.6 deg, hand-hip gap 13.3 -> 17.3-17.5 cm.
L2 sway: SupportShift (+-3 cm pelvis toward the loaded foot, applied through the PBI) + CurveLean closed loop (leanSel = gain x
   (leanRaw - leanMeas) answered the gait's trunk sway with the lean spring's lag and pumped it). Fix: SupportShiftCm 3 -> 0.75 +
   new CurveLeanMeasTau 0.6 s (low-passed leanMeas in SHM_UpdateBodyTargets). Walk head / chest / pelvis 7.5 / 6.4 / 5.0 ->
   2.8 / 2.6 / 2.1 cm pp. Jog head 7-8 cm is clip content (raw A_CT_Jog_Fwd head-pelvis 7.7 cm).
T turns: V2.4 capped the BODY yaw by a / v (vehicle) and the path ran at constant speed (sprint mouse 90: 2 % speed loss, radius
   3.1-3.6 m, body lead 4-12 deg). V2.5 GR_Impl_CP_PhysicalRedirect (install_v25_gr.py / _gr2.py, all default off):
   TurnRateAccelMax (yaw-rate slew, GR_V25TurnRate), TurnSpeedLoss (f = clamp(1 - L (1 - cos theta), Min, 1), L ramps over
   TurnSpeedLossV0..V1, CMC Velocity scaled toward f x MaxSpeed at TurnSpeedLossDecel), SprintFaceMove (Sprint: yaw target =
   input direction for inputs within ~100 deg of the camera forward; the |delta| term then measures target - actor),
   CutChordAware (cut cap factor = max(2 sin(theta/2), 0.5) instead of 1.414; small-angle cuts were over-limited).
Final (2026-10-15, V2.4 prod -> V2.5, 2 interleaved reps x 22 scenarios; promote_v25.py, verify_v25_final.py ALL_OK fresh
  editor): walk sway head/chest/pelvis 7.5/6.3/4.9 -> 2.8/2.6/2.1 cm pp; walk-start abduction 5.4 -> 10.6 deg; sprint W+D path 90 %
  1.57 -> 0.78 s (body faces the input in 0.44 s, radius 4.7 -> 2.3 m); sprint mouse 90 body 1.18 -> 0.67 s, path 1.74 -> 1.03 s,
  speed loss 2 -> 14 %; A/D jog 1.01 -> 0.70 s; peak lateral 0.66-1.03 g (brief); starts / stops unchanged; pops 70 -> 65;
  P2 14/18; errors 0. Production: TurnLatAccelMax 1400, TurnSoftK 6, TurnRateFloor 40, TurnRateAccelMax 1200, CutLatAccelMax 650,
  CutChordAware 1, TurnSpeedLoss 0.6 (V0 150, V1 490, Min 0.5, Decel 900), SprintFaceMove 1; SupportShiftCm 0.75, CurveLeanMeasTau 0.6.
Open: walk-stop halt pop (see V2.4); A/D jog 180 reversal passes walk loops when speed loss engages mid-reversal (26-39 m/s2).
Traps: Multiply_VectorFloat / Add_VectorVector become K2Node_PromotableOperator (qa_graph refuses) - build vectors from
  components. Reloading a Blueprint CLASS package (to discard an aborted install) nulled BP_PBI_Player.GR_Profile and the next
  install saved it: every GR function raised Accessed None each tick (QA rate 5/s). Reload only edited BPs + DAs, probe pawn
  GR_Profile before saving (install_v25_gr2 / promote_v25 guard it). behavior_flags never reset: pass every new field.
```

V1.3.6 (2026-09-27): running freeze NOT reproduced in 8 sustained injected-input cases (freeze_report.py: local-frame skeleton
  still while moving); `mmanim=None` spans are the crouch graph / CP landing stop owning the pose, not freezes. Sprint reversal
  bridges split per pivot foot (PSD_SHM_Redirect_SprintReversal_L / _R, routed by SHM_RedirectSide = latched SupportSide) ->
  sprint 180 = one pivot side. Coupling fade: SHM_BodyBlend x clamp(severity / DCSeverityDeadband) while moving (feeding a flat
  0 severity to the PBI doubled walk spine sway 2.6 -> 6.0); at rest SHME's flat severity calms the AAMS idle (keep blend 1).
  Curve lean: LatAccel (component) -> PBI severity via CurveLeanGain. Settle-quiet gate lives in the idle-ENTRY condition
  (idleNow), never in SHM_IdleWait (IdleWait forces SearchThrottleTime 0 -> re-search skating on stops, starts 7.6 -> 16.7).
  Exertion 0..1 (work-rate rise 25 s, fall 40 s) with only a camera consumer. Turn composition CamTurnComp (16 cm, outside of
  the turn). Sources found, not fixed: jog clip family carries ~7 deg left roll; CP stop / start clips carry the 9-24 deg hunch.
  Any new PoseSearch database or bias needs 2 warm runs before measuring (index skips).

## HALT walk-stop halt pop (2026-10-15; Saved/Codex/SHME_HALT_20261015/, tools Tools/SHME_HALT_20261015/)

```
Owner: NOT HasVelocity / BlendListByBool_5 (idle takeover inactive at the flip: SHM_IdleWait true) and NOT SHM_BodyBlend.
  The CP stop SequenceEvaluator_1 plays CP_StopEvalTime, written by CP_UpdateTransitionClock from a predicted-stop-distance
  table (v^2/2a; last segment ~0.1 cm <-> 0.1 s). When the CMC zeroes the velocity the time jumped 1.688 -> 1.800 s in one
  25 ms frame (pelvis +2.9 cm). HasVelocity flips on the same frame only because both follow v -> 0.
Fix: SHM_StopTimeLimit (ABP fn, called after SHM_StanceCapture = end of BlueprintUpdateAnimation): while the same CP stop is
  owned, CP_StopEvalTime advances at most SHM_StopTimeRateMax x dt (ABP member, prod 2.0, 0 = old behaviour).
  Walk-stop halt peaks st_walk/wst/gait/taps 42/45/28/38 -> 20/17/14/17 m/s2; stops, skating, P2 14/18, errors unchanged;
  head follow-through 1.0-1.4 -> 1.8-2.2 cm. Rate 1.5 lags the clip mid-stop (distance matching runs ~2x near the end).
Diagnosis tip: ABP telemetry 'mmanim' / 'mmt' are the MM selection UNDER the CP branches; sample CP_StopEvalTime / CP_StartEvalTime
  via harness "avars" when so/sto is true.
```

## V2.6 gait logic, start / stop clips, relaxed walk, turn reactions, camera lens (2026-10-15; Saved/Codex/SHME_V26_20261015/, tools Tools/SHME_V26_20261015/)

```
Measurement: v26_metrics.py start (CP start clocks: CP_StartEvalTime / CP_TC_StartPoseTime rate vs game time) | shake (camera
  step-band motion) | stop (head forward excursion over the final stand, settle) | gait (ABP av_Gait timeline); turn_lean.py
  --win=0.75 (stride-averaged sustained tilt / roll / twist into a move change - sprint strides roll +-12 deg, a 0.4 s window
  is not enough); gaitkin.py (cadence, bob, twist, obliquity); harness avars CP_TC_StartRight / SHM_StartRightRelaxed /
  LS_StopUseSample; qa_pie "vbones", "shot_cmd" ('Shot' only traces in 5.8; HighResShot grabs the EDITOR viewport - no game
  screenshots this way).
CP start / stop branches SHOW their own clips (SequenceEvaluator_0 / _1 <- CT_GetCPStartSequence / CT_GetCPStopSequence literal
  pins) while MM telemetry reports the clip under them. Start: right foot -> A_TC_WalkStart_R on CP_TC_StartPoseTime (distance
  clock, 0.72x since the V2.4 walk acceleration = "the first step stretches"); left -> A_LS_M_Relaxed_Walk_Start_F_Lfoot on
  CP_StartEvalTime (1.0x). Stop (LS_StopUseSample true): A_LS_M_Relaxed / A_CT_Ref_Walk_Stop_F_L/R for ~1.1 s, then MM continues
  the settle with SHM_M_Neutral_Walk_Stop_* (PSD_Dense_Stand_Walk_Stops, Integrated).
S2 start: ABP SHM_StartRightRelaxed (install_v26_start.py) -> right-foot starts play A_LS_M_Relaxed_Walk_Start_F_Rfoot (+9 deg arm
  bake) on CP_StartEvalTime. Matching the capsule instead (walk accel 300) makes the left clip run 1.2x - the two start clips are
  authored with different accelerations.
S1 stops (new clip variants, v26_stop_bake.py): from 0.35 s before the root halt the pelvis and upper-body locals are pulled
  toward the final stand (keep 0.45) and both legs re-solved to the original foot transforms (solve_leg): head settle 8-22 ->
  3-10 cm in clip; 4 CP stop clips + 20 SHM MM stop clips; PSD_Dense_Stand_Walk_Stops re-keyed V26S1.
G gait (install_v26_gait.py, BP_GR_Player): GR_TargetGait (input gait; drives CalculateMaxSpeed / MaxAcceleration /
  BrakingDeceleration) vs Gait (shown gait; ABP / camera / turn code) stepped by the speed actually reached (AnimGaitBySpeed,
  thresholds 210 / 190 / 400 / 380, rest 50); SprintReleaseToJog: releasing a sprint hold while moving keeps jog until the
  capsule has been still 0.3 s, tap = walk. Before: sprint release dropped Gait to Walk at 418 cm/s (walk loop at sprint speed).
P1 relaxed walk: SHME WalkRelaxFwdDeg (LeanFwdTarget at walk speeds) - x ~3.8 through PBI_ForwardTarget (/0.6, spread over pelvis
  + 3 spine bones): 3.0 gave +10.7 deg trunk (hunched); production 0.8 (+2.9 deg trunk, head +1.6 cm). The walk carried the
  standing posture (trunk +11 vs +10, upper spine -7.4 arched) - kinematics (cadence 114, bob 4 cm, obliquity 8.7) were normal.
L turn reactions: sprint sustained tilt 11-13.5 -> 4-7 deg via CurveLeanMaxDeg 4 + PBI LateralLean 7 (+ DirectionPelvisYaw 9,
  DirectionShoulderBalance 5, SpineCounterRotation 0.85); the AAMS additive lean (ApplyMeshSpaceAdditive_2, no Alpha pin) did not
  matter; jog diagonal lean = loop content (A_CT_Jog_FwdLeft/FwdRight/Right roll mean x0.4, v26_roll_bake.py km 0.6); sprint loop
  + SHM curve loops (identical poses, curved roots) stride roll -35 % (kf 0.35): shoulder roll pp 25 -> 16 deg. Re-keyed
  PSD_CT_JogSteady / PSD_LB_SprintLoops (V26R1).
C camera: CamRollGain 0.2 -> 0.1, CamBodyFreq 5 -> 3.5 (step-band roll / bob halved); lens on BP_Player_MM RangerGameplayCamera
  (the owner): DOF f/8 focus 260 cm (sharp >= ~1.4 m, background soft beyond ~15 m), vignette 0.2, fringe 0.1, motion blur 0.25
  (max 2 %); the level PPV EX_PostRain_NeutralExposure keeps exposure / bloom 0. Visual acceptance NOT_TESTED.
S3 start toe-off pin (v26_startpin_bake.py): in both relaxed walk-start clips the STEPPING ball drags 4.3 / 3.2 cm on the ground
  before lift-off (A_TC_WalkStart_R is the same motion as A_LS_M_Relaxed_Walk_Start_F_Rfoot - only the clock differed); at the
  authored clock that read as a start skate (skate_report files it under the PRECEDING stop stage). Ball held at frame 0 until it
  lifts, correction fades 3 frames in the air, leg re-solved: drag 0, foot error 0, knee < 1 deg.
Final (2026-10-15, V2.5+HALT prod -> V2.6, 22 scenarios x 2 interleaved reps; promote_v26.py, verify_v26_final.py ALL_OK fresh editor,
  override-free smoke = candidate): right-foot start clock 0.72 -> 1.03x; walk trunk +11 -> +13.8 deg; camera step-band roll / bob
  halved (walk roll rms 0.040 -> 0.020 deg, sprint 0.085 -> 0.043); shown gait Run at 222-228 / Sprint at 410-416 cm/s (was Sprint
  at 148); sprint release -> Run until still, restart = Walk; full sprint stop 410 -> 296 cm / 1.65 -> 1.18 s; sprint W+A/W+D
  sustained tilt 12.6 -> 6.2 deg, head 3.6 -> 1.1 cm (twist kept); walk-stop gesture (head overshoot beyond walk AND stand
  posture) 7.2 -> 4.8-5.1 cm; pops 61.5 -> 58; P2 14/18; errors 0; kinematics unchanged. Trade-off: quick restarts (~2 s after a
  stop) skate p90 +1 cm (start now at authored speed blends from the settle pose); wstart p90 3.9 -> 3.5.
Production: GR SprintReleaseToJog 1, AnimGaitBySpeed 1 (210/190/400/380, rest 50, still 0.3); SHME CamRollGain 0.1, CamBodyFreq 3.5,
  CurveLeanMaxDeg 4, WalkRelaxFwdDeg 0.8; PBI LateralLean 7, DirectionPelvisYaw 9, DirectionShoulderBalance 5, SpineCounterRotation
  0.85; ABP SHM_StartRightRelaxed true; lens on BP_Player_MM. Clip bakes: 4 CP stops + 20 SHM stops, 3 jog loops, sprint loop + 6
  curves, 2 relaxed starts (arms R + toe-off pin L/R). Checkpoints Saved/Codex/SHME_V26_20261015/checkpoint/*.
Stop metric trap: "head excursion over the final stand" grows with ANY walking-posture change (walk relax +1.5 cm) - use the
  overshoot beyond max(walking posture, stand) (v26_metrics stop) to judge the stop gesture itself.
Traps: SelectObject is KismetMathLibrary (not SystemLibrary); E_Gait enum variable = BlueprintEditorLibrary.get_member_variable_type
  + add_member_variable; enum literals 'NewEnumerator0/1/2' (Walk / Run / Sprint) via pin(...).value / value(); anim-node pins
  that are not exposed (ApplyMeshSpaceAdditive Alpha) cannot be wired - remove the added variable instead of reloading the ABP.
```

## V2.7 start / stop size, long walk loop, stop dip, gait-held fast turns (2026-10-15; Saved/Codex/SHME_V27_20261015/, tools Tools/SHME_V27_20261015/)

```
Measurement: stopdip.py (pelvis below the gait level at a stop, knee flexion at the minimum, foot spread), startsize.py (head lat /
  fwd, trunk pitch, pelvis dip over a start), turngait.py (pose-family share by MM database through turns), walkrep.py (cycle-to-
  cycle RMS of hands / head / shoulder roll at equal loop phase: an identical loop gives ~1 cm harness noise). Harness: v27_ab.sh
  (base = V2.6 prod passed explicitly; CON[var] per-variant console; PRE / POST scripts). LR_LOG trap: a mem_guard restart writes a
  NEW editor log - never export LR_LOG by hand across chains (rows 0 = harness read a stale log, not a frozen pawn).
Owners: stop dip / big start are CLIP CONTENT (FootPlacement, BrakePosture, PBI, SHME body targets each < 1-2 cm): relaxed walk stops
  bounce 8-9 cm per step and CP distance matching enters at the last double-support trough; SHM_A_CP2_Jog_Fwd_Stop = 12 cm lunge
  (knee 90); RR run stops 13 cm; AAMS run stops 22 cm (no better stop in the project). Idle stand carries the head 8 cm to one side:
  the first start's lateral shift is the idle weight transfer, not the start clip.
S1 v27_lowband_bake.py: damps the SLOW (moving mean WIN 0.4 s) deviation of pelvis translation and pelvis / spine / neck / head
  rotations from a first->last-frame trend (keep_x/y/z/r), optional z_band (raise troughs below a TRW-s trend); leg reach handled by
  heel roll about the planted ball (<= 40 deg, ball fixed) then early VERTICAL toe-off lift (lift_max) for a stretched rear leg, swing
  pull only off the ground; reports foot error / planted-ball horizontal drift (both 0 in production). Walk starts: pitch 20 -> 12,
  head fwd 20 -> 11.5; game restart pitch 20.9 -> 10.5 deg. Stops in game: walk 3.6 -> 2.9, jog 12.2 -> 9.2, sprint 12.9 -> 9.7 cm
  below the gait level (reach-limited: a shorter final braking step = new stop clip is the remaining fix).
W1 v27_walkvar_bake.py: A_LB_Walk_Fwd (only steady forward walk, 1.37 s one cycle) rebuilt in place as 5 cycles (6.83 s): legs / root
  copied (root continues by D per cycle), upper body seamless periodic variation (spine ~1 deg, arm swing +-18 %, head glances
  +6 / -4 deg), curves repeated; PoseSearchBranchIn re-authored 0..length (looping kept - audit). Refuses a source > 2 s (restore the
  one-cycle original from checkpoint/walkloop with the editor closed before re-running). Hands cycle-to-cycle 1.0 -> 2.0 cm.
T1 install_v27_turn.py: Update_MotionMatching sprint route = Gait==2 AND Speed >= 380 (CallFunction_137) AND Direction +-65 (_138),
  and the jog route (IfThenElse_23, evaluated FIRST) also takes Gait==2 with Speed < 380 (_132) -> ABP members SHM_SprintDBMinSpeed
  (prod 230) / SHM_SprintDBDirMin/Max (+-110); pawn GetDesiredGait forced Run for input 65..110 deg off camera forward
  (CallFunction_23 Max) -> profile SprintSideRunDot (prod -0.36 = off). GR TurnSpeedLoss 0.35 / Min 0.7 (speed carried).
  Sprint DB share: A/D cuts 45 -> 91 %, mouse 90 -> 99 %, fast flicks 70 -> 91 %; gait 59 -> 100 % Sprint; pops 63 -> 57.
```

## V2.9 turn integrity + foot-knee-pelvis (2026-10-16; Saved/Codex/SHME_V29_20261016/, tools Tools/SHME_V29_20261016/)
```
Idle stance hold (V1.2 SHM_StanceHold) is now PRE-IK equivalent. The snapshot is the FINAL driver pose (FeetIK applied) and is
  played upstream of FeetIK, so FootPlacement adapted it a second time on uneven ground. FeetIK_Layer carries 28
  BoneDrivenController nodes (MorphTarget mode -> pose curves SHM_HCi_* before FootPlacement, SHM_HCo_* after LegIK: pelvis
  T/R, ik_foot_l/r TZ/R; value = local - ref, rotation = Euler(local * ref^-1)); EventGraph SHM_HoldDeadapt (after
  SHM_StanceCapture, latched on SHM_IdleEntry) turns them + the snapshot's component sockets into SHM_HC_*; the hold branch
  (PoseSnapshot_4 -> LayeredBoneBlend_5) restores root rotation (counter re-applied downstream), pelvis, feet (TwoBoneIK, bone
  lengths kept) and foot rotation. Kill switch abp flag SHM_HC_Off.
Standing turns: GR_UpdateIdleTurn montages turn the CAPSULE by root motion (RootMotionFromMontagesOnly). SHM_Snapshot no
  longer counters actor yaw while IsSlotActive(DefaultSlot) (the montage still counts as a turn: hold / takeover release,
  fresh stance capture). Kill switch SHM29_TipOld.
Redirect classification (SHM29_CutMode, production 2): peak of max(velocity-vs-desired, INTENT angle = start velocity
  vs current DesiredDir) over the episode's first 0.3 s; non-decisive starts (first-frame intent < 70, i.e. mouse flicks)
  wait until the peak passes 120 (reversal) or the window ends; late activation / upgrade re-routes by resetting
  SHM_RedirectFrames to 1 (the Update_MotionMatching bridge branch fires again). Mode 2: sprint lateral episodes are not
  skipped; SHM_RedirectDB_SL = PSD_SHM_SprintCut (owned copies of the vendor sprint 90 turns + A_LB_Sprint_Fwd). Reversal
  tail: after a reversal episode the bridge is held up to 0.4 s more while < 150 cm/s with input (no walk-loop frames).
  The montage counts as a turn (hold / takeover release) only after 0.3 s (SHM_MontT): releasing on its first frame swapped
  the slot source pose under a ~0-weight montage (one-frame shoulder pop, 70-77 m/s2 on slope turns).
Standing-turn plant settings: Get_FootPlacementPlantSettings returns PlantSettings_Stops (PivotAroundBall, unplant radius 40)
  while SHM_TurnPlant (standing + DefaultSlot turn montage). The default preset (LockRotation, UnplantAngle 60) held the
  planted foot's yaw while the clip pivots on the ball: hip-to-planted-foot 110-119 deg in fast 180s vs 38-62 authored;
  with the pivot preset 37-70 deg, planted-ball slip max 1.6-2 cm.
Rollback: abp flags SHM29_CutMode 0 / SHM29_TipOld true / SHM_HC_Off true = V2.8 logic; ABP copies in
  Saved/Codex/SHME_V29_20261016/checkpoint/ (before_v29_abp_save, before_v29b_save, knee_repair_before for the 76 clips).
```

## V2.10 moving turns + leg integrity (2026-10-16; Saved/Codex/SHME_V210_20261016/, tools Tools/SHME_V210_20261016/)
```
Sprint cut (production): GR BP_GR_Player.GR_Impl_CP_PhysicalRedirect S1 - while SprintFaceMove is active the body-yaw target is the
  VELOCITY direction + at most SprintCutFaceLead (15) toward the input (DA_GR_LocomotionBehavior; MinSpeed 250, MaxAngle 135); velocity
  untouched (no input delay). Profile fields JogTurnFaceLead / MinSpeed / InputCone / MaxAngle (forward-steer bound for look-driven
  gaits) are installed but 0 (no measurable effect on jog: its facing already leads the velocity by <= ~25 deg).
ABP SHM_Snapshot: SHM210_CutTail (0.8 s) / SHM210_TailAngle (8): after the component ends a non-skipped SPRINT lateral episode (velocity
  within 25 deg) the ABP episode continues (SHM_RedirectActive true, SHM_RedirectFrames counting, SHM_RedirectHold) while the velocity is
  more than 8 deg off the input, with input, up to 0.8 s; a new component episode restarts the counter (cStart = rdOn && !SHM210_PrevCompOn).
  SHM210_JogCutMode (0) = test switch that stops skipping jog lateral episodes (rejected candidate, keep 0).
  Note: Update_MotionMatching holds the DATABASE on SHM_RedirectActive && SHM_RedirectFrames > 1.5 (&& Family < 0.5); SHM_RedirectHold
  only stretches the search interval (throttle 0.6 s) - a "tail" on SHM_RedirectHold alone keeps the throttle, not the bridge.
SHM_RedirectDB_SL = /Game/GraceRanger/SHME/Animations/V210/PSD_SHM210_SprintCut: owned copies SHM210_Sprint_Turn_{L,R}_090_{L,R}foot with
  'Pose Search: Block Transition In' [0.78 s, end] + A_LB_Sprint_Fwd (BranchIn 0..length). Entry 0.77 s, continuous play to the push-off.
Leg integrity: 33 owned start clips + the stand idle + the walk loop repaired (v210_knee_repair), the 26 V2.8 walk stop / start clips
  regenerated with the V2.10 solver (prod config). Rollback: checkpoint/before_v210_promote (ABPs, DA, GR, PBI), knee_repair210_before,
  v28_before_regen, walkloop_before_repair, idle_before_repair, baseline_v29; quick: DA SprintCutFaceLead 0, ABP SHM210_CutTail 0,
  SHM_RedirectDB_SL = PSD_SHM_SprintCut.
```

## V2.11 relaxed arms, camera-input direction, sprint push (2026-10-16; Saved/Codex/SHME_V211_20261016/, tools Tools/SHME_V211_20261016/)
```
A1 arms (content, arm chain only, v211_arm_bake.py v3, sources /Game/ActionAdventureMovementS/Rollbacks/SHME_V211_Arms_Before_20261016/):
  A_LS_M_Relaxed_Walk_Start_F_Rfoot / _Lfoot (CP starts): elbow / wrist from the idle decaying to the clip by the handoff (0.88 / 0.77 s);
    upper-arm carriage in the trunk frame idle (12.5 / 15.0 deg) -> loop mean (12.2 / 10.7). A_LB_Walk_Fwd: narrow-arm outlier cycles lifted
    to the same-phase average (71 / 74 frames). SHM_M_Neutral_Stand_Turn_* (TIP montages): shoulder chain damped around its own rest,
    elbow / wrist from the idle, rest carriage = idle. DBs re-keyed: PSD_LB_WalkLoops, PSD_SHM_TurnInPlace.
D1 direction: DA_GR_LocomotionBehavior.CameraIdleOrbitMaxYaw 55 -> 180. Owner of the screen-vs-input gap: BP_GR_Player
  CT_UpdateCameraResponse -> CT_VisualCameraYaw = control yaw + CT_IdleYawOffset (clamp(control - actor, +-CameraIdleOrbitMaxYaw) -
  (control - actor)) + CT_CounterYaw; GR_UpdateRig boom yaw = CT_VisualCameraYaw (ContinuityRevision). Movement input = control yaw
  (BP_ExampleCharacter_MotionMatching EventGraph IA_Move -> GetRight/ForwardVector(GetControlRotation) -> AC_State_AAMS.DetermineMovement),
  control yaw = TW_CameraWorldYaw each tick (BP_GR_Player EventGraph, LookDrivenLocomotion). The idle hold showed the camera up to 125 deg
  away from where W points for 0.3-0.8 s after a fast idle mouse turn; moving cam-ctl <= 1.2 deg (counter yaw).
P1 push (ABP_GR_MotionMatchingBase, install_v211_push.py rev2 + promote_push.py): SHM211_PushGate (DSL) after SHM28_StartStop;
  SHM211_Push = mode AND speed < 420 AND |Direction| < 35 AND no CP start AND no redirect AND ((speed < 200 within 1.0 s AND accel > 120
  AND >= 0.35 s after a redirect episode) OR (pushing AND accel > 30)); EventGraph branch sets SHM211_RouteJog / RouteSprint = PSD_RR_Start
  (relaxed run starts) or the original PSD_CT_JogSteady / PSD_LB_SprintLoops; Update_MotionMatching K2Node_CallFunction_91.Database and
  K2Node_Select_24 / _25 Option 1 read the route members. Rollback: SHM211_PushMode 0.
Unchanged by design (measured): Shift+S during sprint = max speed 490 -> 300 with a 0.6 s braking pivot (A_LR_Run_Pivot_F_B_*) into the
  backward run loops (A_RB_Run_Rear*, diagonals too), no body turn; camera 180 + W = brake, sprint 180 turn, re-acceleration.
```

## V2.12 arm floor, database clean-up, gait push (2026-10-17; Saved/Codex/SHME_V212_20261017/, tools Tools/SHME_V212_20261017/)
```
A arms (content): A_LB_Walk_Fwd re-baked from the pristine source with a CONTRALATERAL FLOOR per side (v212_arm_bake.py, loop_mode floor:
  floor = mean contralateral abduction half a cycle away - 1.5 deg, cap 12.5, lift-only, cyclic smooth); CP starts end on the loop's
  carriage AT the handoff phase (Rfoot 0.317 / Lfoot 0.805 of a cycle). DB clean-up: PSD_LB_WalkLoops entry 8 and PSD_SHM_TurnInPlace
  entries 8-15 were /Rollbacks/ pristine copies (auto-added by BranchIn sync) - removed; the Rollbacks copies carry no BranchIn now.
P push (ABP_GR_MotionMatchingBase): SHM212_Guard (DSL, EventGraph after SHM211_PushGate): push only with sprint intent
  (CharacterMovement max speed > 400), 1.0 s refractory after a push episode unless the speed fell below the arm speed again;
  SHM212_PushWalk latched when the push starts at 110..210 cm/s. EventGraph push branch: RouteJog / RouteSprint = SHM211_DB_Push
  (PSD_SHM212_GaitPush: owned copies of the AAMS Walk_to_Sprint / Run_to_Sprint transitions, vendor entry windows, posture-baked:
  v212_push_posture.py, runtime lean 35.7 deg / pelvis -12 cm; pre-bake files in checkpoint/pre_posture) when PushWalk,
  else SHM212_DB_PushStand (PSD_RR_Start, the V2.11 run starts). Update_MotionMatching: the walk SetDatabaseToSearch
  (K2Node_CallFunction_88) branches to a copy with SHM211_DB_Push while SHM212_WalkPushOn. SHM211_PushMaxSpeed 485 (push until the
  sprint gait shows). Rollback: SHM212_WalkPush 0, SHM211_DB_Push PSD_RR_Start, SHM211_PushMaxSpeed 420 (or checkpoint pre_promote).
Dormant (modes 0, measured, not promoted): SHM212_RdBreak (episode break), SHM212_RdRev + SHM212_RevTurnMode (cut-reversal re-route
  into PSD_SHM212_CutRev_L/R = sprint 180 turn copies; bridge getters of SHM_RedirectDB_SRL/SRR read SHM212_RouteSRL/SRR),
  SHM212_JogPush, SHM212_PhaseGate.
```

## Brake pivot content (2026-10-17; Saved/Codex/SHME_PIV_20261017/)
```
A_LR_Run_Pivot_F_B_{L,R}foot (sprint S, PSD_SHM_Redirect_SprintReversal[_L/_R], PSD_LR_ReversePivots) and A_CP2_Jog_Fwd_Pivot (jog S,
  PSD_SHM_Redirect_JogReversal[P/Q], PSD_CP2_JogPivots) baked in place: braking foot -20 cm during its stance + pelvis floor 90 / keep 15 %
  -> runtime pelvis drop sprint 17.5-21.3 -> 5.1-11.1 cm, jog 19.9 -> 8.9-11.4; trunk lean, root motion, databases unchanged.
  Rollback: checkpoint/pre_bake/*.uasset (editor closed). Untouched: B_F pivots (no crouch), SHM210 sprint cut clips (cut -> S 9-11 cm).
```

## V2.13 direction change + measured motion (2026-10-17; Saved/Codex/SHME_V213_20261017/, tools Tools/SHME_V213_20261017/)
```
Component defect (measured, not fixed in the component): SHM_UpdateRouting sets RedirectEnd 3 ('new intent') for one tick when the
  input reverses inside a lateral episode but the episode goes on (RedirectTime keeps counting, class stays 1) to MaxDwell 0.7 s;
  the ABP then held the SprintCut database and MM kept the old cut push 0.26-0.33 s before the mirror cut (v212q0/q1).
ABP SHM212_Guard (install_v213_guard3.py): SHM213_RevVel (1) = inside a lateral episode an input-vs-VELOCITY angle > SHM213_RevVelAngle
  (110) at > 150 cm/s re-classes the episode as a reversal (SHM212_RevNew -> class 2, frames 1, side) -> the V2.12 reversal bridge
  (SHM212_RdRev 1, RevTurnMode 0) plays the brake pivot in 0.06 s. Intent = CMC CurrentAcceleration (the component's DesiredDir lags).
  Fires once in plain S reversals too (class already 2, no visible change). After the pivot MM still goes jog loop -> run start.
SHM_Snapshot SHM213_RestartOn (0): cStart also on a component RedirectTime reset - never fires (the component does not restart).
SHM213_MontTick + EventGraph (SHM213_RevMont 0, dormant): root-motion DefaultSlot dynamic montage of the owned 180 sprint turn on
  the RevNew frame (input within ~100 deg of the camera forward). Measured v212q4: runs (capsule follows the clip, no foot slide) but
  entry speed 262 -> 432 jump, pelvis 55 cm (vendor crouch), actor yaw NOT rotated by root motion (GR writes the rotation each tick:
  moonwalk), exit into SHM_Rec_* clips -> FAIL. Needs GR yaw yield during the montage + a baked / game-speed turn clip.
BP_GR_Player.GR_UpdateIdleTurn (install_v213_tipint*.py): profile field GR213_TipRev (DA_GR_LocomotionBehavior, 1): a turn montage older
  than 0.35 s is stopped (0.12 s) when the control-actor delta is >= 42 deg with the opposite sign of GR213_TurnDelta0 (the delta latched
  while no montage played); the next tick starts the reverse turn: 1.9 s -> 0.5-0.8 s. Pawn vars cannot be set by the harness
  (pbi_flags write DA_PBI_Prototype): knobs go on BP_GR_MotionProfile.
Movement model M1 (DA_GR_LocomotionBehavior): SprintAcceleration 300, RunAcceleration 270, CutLatAccelMax 450, TurnSpeedLoss 0.5 /
  Min 0.6 (walk untouched by construction: the cut cap a/v exceeds the walk friction, speed loss ramps from 150 cm/s). Sprint W+D
  curve 0.96 -> 0.66-0.71 g, jog W+A<->W+D 0.86 -> 0.71 g, sprint cut 1st-frame |a| 1950 -> 920, S from sprint 1st-frame 1281 -> 938 cm/s2
  (owner of that spike = CMC friction term with RedirectFriction 4.6: 4.6 x v + accel). M2 (380 / 0.6 / TurnLatAccelMax 1100) rejected.
Push content: SHM212_*_to_Sprint re-baked from the vendor source (pitch > 12 deg x 0.15, pelvis floor 93, arm_damp 0.6 = arm bones pulled
  40 % toward their +-0.47 s running mean inside the push window) -> runtime 35.6 -> 31 deg, 12.4 -> 8 cm, hand drive 67-70 -> 56-59 cm;
  A_RR_M_Relaxed_Run_Start_F_* baked in place (pitch > 16 x 0.25, floor 90) -> 36.9 -> 31 deg, 17 -> 12 cm. Entry window 1.13 s tried:
  entry slip 10-12 -> 12.5-16.7 cm, reverted to 1.01. Rollback: checkpoint/baseline_v212piv (all), pre_push / pre_rrstart / pre_window.
```

## V2.14 cut -> reverse chain + walk -> sprint stepping (2026-10-17; Saved/Codex/SHME_V214_20261017/, tools Tools/SHME_V214_20261017/)
```
Component FIX (install_v214_comp.py, no flag): SHM_UpdateRouting's END (Operator_27) and START (Operator_30) are PURE expressions that
  read RedirectDirLatched; SetRedirectDirLatched runs between SetRedirectEnd and the SetRedirectSpeed0/Class/Gait/Side/Phase/Time/Active
  consumers, so every later consumer re-evaluated END/START with the NEW direction (new-intent test 0 deg -> false) = the V2.12/V2.13
  'RedirectEnd 3 for one tick, episode goes on to MaxDwell' defect. Fix: latch END/START into SHM14_EpEnd / SHM14_EpStart right after
  SetTurnClass (before SetRedirectEnd) and point all consumers at them. Measured: RedirectTime -> 0.00 on the reversal tick, episode
  'c1 0.00-0.06, c2 0.06-0.65'. Production therefore turns the V2.13 ABP compensation OFF (SHM213_RevVel 0, SHM212_RdRev 0, rollback
  switches kept) and SHM213_RestartOn ON. The same trap applies to the DSL: a `bind` is inlined at each use - a value that must see the
  PRE-update state of a member has to be `set` into a member BEFORE that member's update (SHM214_RevEndT).
Forward-run reversal content (SHM214_RevTurnMode 1): PSD_SHM214_Rev_L/R (build_v214_revdb.py) = baked brake pivot A_LR_Run_Pivot_F_B_* +
  owned SHM214_Run_Reface_{L,R}_180 (AAMS reface start, first 0.9 s stretched 1.4x by key resampling, entry 0-0.35) + A_LB_Sprint_Fwd; NO
  rear-run loops (they were the backpedal pick). Route in SHM213_MontTick (install_v214_route.py): RevTurnMode & RedirectActive & input
  & camera-forward & sp > 150 & (component class > 1.5 | velocity-vs-input angle > 100, since the component classes 100-120 deg as lateral)
  -> SHM212_RevTurn / class 2 / gait 1 -> the V2.12 CutRev bridge (SHM212_DB_CutRevL/R re-pointed). Pivot picked at +0.08-0.09 s.
  The 'tail' (hold the Rev database after the episode, SHM214_TailSpeed) FAILED: the reface clip is never selected (GR yaws the actor
  fast at low speed; MM prefers sprint fwd / jog) -> production TailSpeed 0 (dormant).
Push-stance re-entry after the reversal (build_v214_revpush.py + install_v214_revpush.py): PSD_SHM214_RevPush = copies SHM214_RevPush_*
  of the re-stepped walk->sprint clips with entry window 1.45-1.65 (push stance, 145->300 cm/s). SHM214_RevEndT = time the forward-
  reversal latch (SHM214_RtPrev) drops; SHM214_PushRevOn = RevTurnMode & PushRevWin > 0 & (now - RevEndT < PushRevWin 0.8 | push still
  active); EventGraph after MontTick: SHM211_DB_Push AND SHM212_DB_PushStand = DB_RevPush else DB_GaitPush / SHM214_DB_PushStand0 (the
  V2.12 push route reads DB_PushStand when the push starts above walk speed - found in the side-camera capture; only with RevTurnMode
  on). qa_graph.disconnect() clears EVERY link of an input pin (a shared join node loses its other branches): use B.break_pins for one
  link, and src() lists all sources of an input, none of an output. With SHM211_PushRdCool 0
  the chain is pivot (0.59 s) -> RevPush 1.47 at +0.68 -> sprint loop +1.80-1.83, no jog loop / run start (r_cutrev_r / l). Late
  reversal (r_cutrev_r2, a true 180 at vmin 60) still goes pivot -> PSD_RR_Start 0.07 (standing start pose) = open.
Walk -> sprint re-step (v212_push_posture.py 'restep' = XY scale points of root path / feet / pelvis + leg re-solve; S1b 0.70 to 1.45 s,
  0.80 @1.75, 0.90 @2.3, 1.0 @2.8, pelvis floor 92): exit-to-loop slip 23-27 -> 2.7-3.8 cm, pitch 30, pelvis drop 6-8 cm. Entry slip
  owner (frame analysis): at the Shift press the walk loop has the planted ball under the pelvis (+2 cm) and the other foot mid-swing
  (+23); the clip at 1.03 has that foot at -39 cm lifted (toe-off done) and the other planted at +33 -> the blend drags the planted foot
  7-10 cm. The matching clip pose is 0.77 s (probe_entry.py), but the V2.12 builder EXCLUDED 0-1.01 s from the database
  (PoseSearchExcludeFromDatabase) - a BlockTransition window start < 1.01 is silently ineffective; push_exclude214.py rebuilds the
  exclusion. Even with 0.77 available MM picks 0.97-1.03 (trajectory cost: accelerating future) unless the window is forced.
```

## V2.15 contact phase / brake-push link / turn-in-place (2026-10-18; Saved/Codex/SHME_V215_20261017/, tools Tools/SHME_V215_20261017/)
```
Walk -> sprint entry (PARTIAL): PSD_SHM215_WalkPush (only the two walk->sprint clips) with its own schema PSS_SHM215_WalkPush = PSS_Default
  copy, trajectory channel weight 0.35 (pose channels unchanged) - a transition-specific selection order; entry 0.70-1.25, exclusion 0-0.70.
  MM now picks by support (left planted -> Lfoot clip 0.93 late left stance; right planted early -> Lfoot clip 1.10 early right stance);
  entry drag 8.7 -> 7.2 cm mean, but the left MID stance case still gets 0.93 (the 0.77-0.88 frames are never chosen, weight 0.12 no better).
Brake -> push link: A_LB_Sprint_Fwd removed from the reversal DBs (it was the stray sprint frames); SHM215_LinkOn starts the push on the
  episode-end tick (SHM211_Push forced in SHM213_MontTick) below SHM215_LinkMaxSpeed 230; PSD_SHM215_RevPushLow (run start 0.17-0.27) only
  below SHM215_LowSpeed 60. Brake pivots = owned copies SHM215_Pivot_F_B_* entered at brake onset (0.73-0.82) in PSD_SHM215_Rev_L/R.
  NOT solved: the pivot entry sweep (planted ball carried 50-100 cm/s along / through the floor during the blend from the cut pose;
  the F_B pivot root never turns while GR turns the actor). Failed candidates (installed, OFF): velocity-line brake in PhysicalRedirect
  (GR215_RevBrakeDecel: real brake vmin 77-81, same sweep), facing hold (GR215_RevYawHold), support-foot pivot routing (SHM215_PivFoot:
  the component ContactL/R are both false in sprint flight - unusable for that decision). Raising MaxAcceleration toward the input on a
  115 deg request only rotates the velocity (cos 115 = 42 % brakes).
Turn in place: TIP clips had ground-skimming steps (ball 3-8 cm while travelling up to 111 cm) -> tip_clearance215.py (step vs pivot by
  travel of both foot ends, sin^1.5 lift 3-8 cm, legs re-solved); SHM215_TipLock sets SHM_FootLockTurn = 1 on the first standing turn
  frame (the lock had decayed to 0.75-0.8 after an interrupt). Remaining: one-frame sweep at the reverse montage blend-in.
Deep cut crouch: SHM210_Sprint_Turn_*_090 own pelvis 87 -> 66-71 cm; pelvis floor (leg reach) and front-foot shortening both failed
  (lateral stance width) - needs content.
```

## V2.16 authored transitions (2026-10-19; Saved/Codex/SHME_V216_20261018/, tools Tools/SHME_V216_20261018/)
```
Root-motion-off rule made operational: a transition clip whose root path differs from the GR capsule path slides planted feet, whatever
the selection. Author it ONTO the measured capsule path (paths216.py profiles -> remap216.py): root = capsule path, every stance anchored
once in the world (ball pinned, heel-toe roll kept), swing errors smoothstep-blended (position AND rotation), lateral stance x0.75,
pelvis toward a floor only within STANCE-leg reach, speed-dependent trunk pitch cap via spine_01..03 (neck counter-rotated), knee hint
hip-relative and summed over +-3 keys (absolute mapped knees flip the knee plane), leg_guard on write.
PRODUCTION (goal 1, PARTIAL): SHM216_Cut_* (entry 0.40-0.78, BlockTransition [0, 0.40]) + SHM216_RevTurn_* (B intention: turn and run
on; entry 0.52-0.68, tail accelerates with the capsule) in SprintCut / Rev_L / Rev_R / RevPush / RevPushLow; SHM210 originals, Reface_180,
Pivot_F_B out of the forward-reversal DBs. Runtime routes BOTH cut sides into one Rev DB -> every RevTurn in both DBs (trajectory picks
the turn direction). A fresh BranchIn has no V2.10 approach-only history: MM entered the cut copy at 0.03 until the block was added.
MM enters a window at its START (trajectory pull): a window is effectively one entry frame; author the clip for that frame.
Wider window (0.45-1.15) -> mid-turn switch to the other foot variant; late window (0.76-0.88) -> worse landing. Kept 0.52-0.68.
Open: reverse entry one contact 15-18 cm (foot lands during the blend), left exit 42-49 cm, cut->S backpedal entry 61-90 cm in 2/3
(V2.14 had 76), second S-cut pelvis 71.9 at runtime vs 76 in the clip (a runtime layer lowers it).
PRODUCTION (goal 2, PARTIAL): walk->sprint links SHM216_W2S_{L,R}foot_{a,b} in PSD_SHM216_WalkLink = ABP SHM211_DB_Push /
SHM214_DB_GaitPush (timewarp216 cadence mode: rate = source step time / target step time(capsule speed) + remap onto the capsule):
4-phase mean worse-foot drag 18.9 -> 15.2 cm, worst 42.8 -> ~22; early / late Shift better, standard / half-step later worse. Compare
candidates against production run IN THE SAME SESSION - the same V2.15 content measured 8.3 vs 14.2 cm mean in two sessions.
Speed-matched warp FAILED (vendor sprint steps at 1.9x = 0.12-0.16 s cadence, out-of-phase exit). CANDIDATE (not promoted): TIP start (tipstart216: ease-in clock + idle start stance) - not better
than V2.15 over repeats (the pre-reverse stance varies with the interrupt; 180 clips worse) - copies in checkpoint/tipstart_candidate.
TIP handoff measured: dynamic montage blend 0.12 s, slot weight 0.25/0.76/1.0 at 0.04/0.08/0.13 s, 180 clip rotates 650 deg/s from
frame 0 -> 14 cm planted-ball sweep exactly during the blend; next lever = runtime support-foot hold during the blend (not built).
```

## V2.17 regressions + recovery step + jog->sprint push (2026-10-19; Saved/Codex/SHME_V217_20261019/, tools Tools/SHME_V217_20261019/)
```
Yaw snap ~2 s after a sprint reversal (both sides): AAMS parent BP_ExampleCharacter_MotionMatching runs ShiftGaitHeld -> ToggleSprint ->
CoreMotion_ApplyPlayerRotationPolicy, which turns controller yaw on for ONE frame (actor snaps 88 deg to the camera, planted foot dragged).
GR owns rotation: BP_GR_Player overrides that event to keep both controller-rotation flags false (install_v217_rotpolicy.py). PRODUCTION.
Left cut -> reverse (MM enters RevTurn_R_Rfoot at 0.53): both clips hold the LEFT foot planted at different ROOT-RELATIVE spots; MM blends
root-relative so the planted ball slid 63-68 cm on the floor. Lift-off clearance / ease (ankle AND ball) did not fix it; the fix is
remap217 'entry_foot' (place the entry stance where the previous clip's exit frame has that foot; offset carried by the stance, blended
out in the swing) + the flip route (SHM217_RevFlip: a reverse > 120 deg from the latched cut direction within 1 s is a reversal at once;
the latch survives a component re-class into an opposite cut; the flip clears SHM_RedirectHold or MM keeps the cut clip). PRODUCTION.
RevTurn tails: cadence warp from 1.3 s (rev_warp.py) + re-plant -> left exit 26.4 -> 7.4 cm; left entry 37.5 -> 3.0 (final z2). Cut->S: 4 backpedal acceleration links
SHM217_BackLink_1..4 (A_RB_Run_Rear from 4 phases, cadence 0.42->0.32 s, re-planted on rear_capsule.json, window [0, 0.2]) in
PSD_RB_Run_Rear -> backpedal entry R 58.5 -> 7.3 cm (L 19 -> 21). PRODUCTION.
Jog->sprint push (new): MontTick's OWN steady-jog start (guard SHM212_JogPush stays 0: the guard push fired in the reversal tail and
replayed walk links at 416 cm/s), held to SHM217_JogLink cm/s, 4 links SHM217_J2S_{L,R}foot_{a,b} (owned Run_to_Sprint,
cadence warp + re-plant + armcap217 lateral hand cap 40 cm) in PSD_SHM217_PushStandJ (RR start entries + links) = SHM212_DB_PushStand /
SHM214_DB_PushStand0; window starts ON landing frames (0.667 / 0.74; MM enters at the window start - starts in a swing left a 14 cm
entry slide); re-press after a release < SHM217_JogArm s is no push (the guard push is cancelled too). PRODUCTION (PARTIAL).
Recovery step (new, CANDIDATE, knob SHM217_Recover = 0): AAMS Run_Turn_180 brake + one re-placement step re-planted on the measured
early-reverse path (paths217.py, rel 0 = the brake-foot landing), own DB PSD_SHM217_Recover routed via SHM212_DB_CutRevL/R while
SHM217_RecOn. Trigger: request latched (reverse vs cut latch, cut age < RecAge, speed > Recover), episode starts on the first loaded-foot
tick within RecWait (component contacts report the landing ~0.3 s after a sprint-cut reverse key: the intent the route reads is the CMC
acceleration that GR rotates physically, ~0.15 s late). Triggers in 2/4 target runs, not on curves, cancel works; FAIL: the re-planted
feet never reach the floor for 1.2-1.4 s (source brake crouch 60 cm vs pelvis raised to 72-80 -> leg reach) and knee medial 17-18 cm.
Open after V2.17: double reversal r_kb2 42-55 cm, very early reverse 30-55 cm, late reverse knee 26 cm, walk->sprint mid R 22.
TIP handoff (CANDIDATE, pawn knob GR217_TipHand = 0): reverse plays the new turn montage at once from the playing one (no Stop -> idle ->
start) - 180 better, 90 worse (R planted 12 cm). Quarter-step walk->sprint windows: not better than V2.16 -> unused.
Traps: PoseSearch DB entry is removed by BranchIn->None only when no other BranchIn on the clip still references the DB; behavior_flags
write DA_GR_LocomotionBehavior (pawn vars need qa_pie pawn_flags, which DIRTY the pawn class package -> memory-guard restart refused;
re-save with pawn_resave.py when the value equals the saved default); DSL bind re-evaluates per consumer (latch into a member first).
```

## V2.18 regressions + jog push isolation + grounded recovery step (2026-10-19; Saved/Codex/SHME_V218_20261019/, tools Tools/SHME_V218_20261019/)
```
Measurement truth (lat218.py, qa_pie frame columns fc / wdt / lix / liy): raw input and CMC acceleration reverse on the SAME frame,
+0.065..0.093 s after the scheduled key (input processing) - the V2.17 "~0.15 s intent delay" was an analysis error. Telemetry rows have
no frame gaps; "gaps" are real long frames (0.06-0.33 s), mostly the FIRST use of a PoseSearch DB in a PIE session. Component contact
flags lag the floor contact 0.07-0.25 s (or miss it): never a trigger. A minimized editor runs PIE at ~3 fps (runs invalid):
unminimize.ps1 before every run. The first PIE use of a DB after its content was rebuilt returns selection None (index build): always
a warm-up run (label r9) after a content edit, never evidence. A D3D12 DEVICE_REMOVED hangs the editor at the crash reporter: kill both,
the A/B loop relaunches (EDITOR_GONE path); remove nothing from b2runner/jobs while a waiter lives.
Knee metrics: knee217 'medial' is hip-line relative - in a pivot / reversal the pelvis is yawed and it reads 20-28 cm while the knee
is over the toes; judge planted knees on the TOE PLANE (knee offset from the hip-ankle-ball plane, stance frames only; rec218.py).
Harness: pawn_flags dirty the pawn packages -> memory-guard restart REFUSED; give such variants POST = req/pawn_reset_save.py.
Jog->sprint push isolated: J2S links re-pointed into PSD_SHM218_JogPush (integrate218_j2s.py), EventGraph branch SHM217_JogOn ->
RouteJog/Sprint = SHM218_DB_JogPush (install_v218_jogroute.py); push-stance DBs back to PSD_RR_Start. Link stance lat_cap 7 (rev 4).
Reverse during a cut: the reverse route rose for ONE frame (opposite cut picked), the episode ended -> curve/jog/push while reversing:
bimodal 5-9 / 37-56 cm. SHM218_FlipLatch (0.6 s) holds the reversal route while the input stays within 60 deg (install_v218_flip.py).
Recovery step (PRODUCTION; final 14/14 entered, both feet land, worst 6.6 cm, 0 triggers in 79 other runs; at ~20 fps capture runs it missed 1/4 - timing risk): AAMS Run_Turn_090 copies, cadence warp + re-plant on paths218.json (rel 0 = reverse frame) in
PSD_SHM218_Recover; trigger = flip with cut age < SHM217_RecAge 0.25 (0.31 = a normal reversal: recovery there slid 42-50 cm);
latch SHM217_RecLen 1.0 (0.6 ended before the re-placement step landed); hold DB = recovery DB (install_v218_rechold.py).
Content rules that worked: window where the cut's NEXT landing foot lands ~0.1-0.17 s after entry (right: L_Lfoot [0.933,1.133]);
left needed the R stance the cut still holds at the flip: R_Lfoot window [1.04,1.12] + entry_foot R from SHM216_Cut_L_090_Lfoot @0.56
(L 2.7 / R 3.1 cm, both feet land). Rfoot variants were wrong-foot picks (53-70 cm): dropped from the DB. pelvis_floor 82 / absolute
knee guard / brake-stance entry with 30-46 cm entry_foot shifts were WORSE (kept as rm218_recover3..5.json evidence only).
Moving push after a pivot: speed cannot separate it from a standing start (both 61-69 cm/s at the push edge); SHM218_LowStand =
push starts during / < 0.8 s after a redirect episode, 30..220 cm/s, NOT inside SHM214_PushRevOn -> RevPushLow (final kb2 worst L 42 -> 24, R 55 -> 33; pivot / lift-off slides remain).
Walk->sprint: new SHM218_W2S_* (V2.17 pipeline, lat_cap 6, half-step windows) in PSD_SHM218_WalkLink: final mid R 22 -> 14 (late exit to the sprint loop 27 in 1/3).
Late reverse NOT solved: RevTurn windows [0.52, 0.60] only limit the ENTRY time of the target clip - MM still left L_Lfoot at 0.70 for L_Rfoot @0.57 in 1/3; plane rate 645-1895 deg/s (knee over the toes, hip-relative twist).
TIP handover NOT solved: the start branch's angle bins (|yaw| at the reverse request 55-85 deg) and the still-rotating first montage
make the new montage start only at the first one's end (GR217_TipHand / GR218_TipHandMinT candidates, off).
```

## V2.19 frame-rate independence + regressions (2026-10-20; Saved/Codex/SHME_V219_20261020/, tools Tools/SHME_V219_20261020/)
```
Frame-rate method: relaunch the editor with V219_EDARGS="-UseFixedTimeStep -FPS=N" (v2_editor_launch.sh passes it; runfps.sh): every
world frame dt = 1/N exactly, runs are DETERMINISTIC (same input -> identical cm values) - A/B differences are causal, one run per
variant. Real variable dt: t.MaxFPS caps (CON variant); stalls: qa_pie 'hitches' [[game_t, s]] (post-tick sleep). Engine "set" is
refused in the editor; GEngine fixed-frame properties are not exposed to Python. The harness key path costs 2 frames (key -> lix),
selection 1 more: a cut starts 0.15 s after the key at 20 FPS, 0.025 s at 120 -> the cut PHASE at a later reverse differs by FPS.
Found frame-rate classes: (1) SHM218_LowStand latched on the first push tick < 220 cm/s - at 20 FPS that tick fell inside the
recovery run-out -> PushLow at 303 cm/s, L 125 cm; LowStand now also requires NOT SHM218_FlipOn (install_v219_lowstand4.py) -> 7 cm,
same class as 30-120 FPS. (2) normal right reversal R sweep grew 3.5 -> 28 cm from 20 to 120 FPS: RevTurn_L_Rfoot carries the free
right foot at 8-9 cm through 0.63-0.80 while it travels 300-770 cm/s; the transition from a later cut phase lowers it to the floor.
swingclear219.py (swing ball >= 14 cm while > 120 cm/s, leg re-solved as a hinge) -> 23.6 -> 9.6 at 60 FPS (rest = exit to the loop).
(3) a 0.13 s stall before the cut key delays that key to one frame -> the motion is classified as the opposite cut (input delivery,
not a logic dependency); a 0.18 s stall inside the brake stance made MM re-pick the recovery clip 0.13 s EARLIER (1.13 -> 1.00) ->
33 cm brake-foot slide (open).
Traps: the MM node BlendTime is an EXPOSED pin (node property ignored); changing the pin default changed nothing either (identical
runs) - transition length is not owned there. 'recovery exit gate' (RevEndT) and Rev DB continuing bias -0.5 had zero effect (removed).
Recovery v8 (production): floor_keep 0 + pelvis_floor 82 (floor_keep 0.3 kept 30 % of the source dip: the real limiter), stance_pull 0.5
(remap217 option: brake / re-placement step pulled fore-aft toward the pelvis, max 12 cm), armcap 30 cm (was 45-48): pelvis min 75 -> 79.
Moving push re-planted on the measured capsule (pushlow219_jobs.py, src = the raw RR start, stance_height 5): kb2 R 17.7 -> 10;
the left toe drag at entry (27 cm) is the transition offset, aligning to the pivot exit made it 76 (rejected).
JogLink 490 (= push max): the J2S link episode outlives the push, so MM never falls back into the RR standing start @0.43 mid-push
(p_j2s 120 FPS L 20.8 -> 4.9, tap 18.8 -> 9.4). Loop-tail entry block on A_LB_Sprint_Fwd [2.0, end]: mixed (one 40 -> 5, another
5 -> 15) - rejected. Late reverse knee: clip plane rate 455 deg/s vs runtime 1190-1210 (runtime IK adds the twist); a clip knee-plane
re-solve made the clip worse (798) - NOT solved. TIP handover: NOT solved (V2.18 analysis stands).
```

## V2.20 transition continuity, support, runtime fixes (2026-10-21; Saved/Codex/SHME_V220_20261021/, tools Tools/SHME_V220_20261021/)
```
Stage isolation (fixed step, deterministic): log the DRIVER mesh after MM+FootPlacement+LegIK (mx_*) and the VISIBLE retarget body
(vx_*), then switch one runtime node family off per variant (console a.AnimNode.<Node>.Enable 0 via CON[...]): knee_stage220.py
(bend-plane rate where bend > 20 deg). Late-reverse knee twist: base 1241 deg/s, FootPlacement off 533, LegIK off 521, warping off
unchanged, visible = driver (retarget innocent) -> owner FootPlacement PlantSettings_Default = LockRotation (planted foot yaw held
through the reversal pivot). Fix (production SHM220_PivotOn 1): Get_FootPlacementPlantSettings gets an outer Select -> PlantSettings_Walk
(PivotAroundBall) only while SHM218_FlipOn / SHM217_RecOn / SHM214_RtPrev / (RedirectActive and speed > 220): 1241 -> 537 deg/s.
Recovery stall time-jump: MM bShouldSearch gate (SHM220_Search = NOT(RecWin AND DB is Recover), telemetry av_SHM220_Search) was
verifiably FALSE through a 0.18 s stall and the clip time still went 1.30 -> 1.07: the rewind is NOT a search re-selection (the hitch
frame advanced the clip only ~0.04 s, the next frame rewound by ~the stall). Candidate kept OFF (SHM220_RecHold 0); owner open
(asset player / blend stack update on a long frame - engine level).
TIP reverse hand-over (production GR217_TipHand 1): three gates in BP_GR_Player.GR_UpdateIdleTurn - (1) start branch IfThenElse_1 =
Op7 OR (hand2 AND Op6 AND (settled OR large |yaw|)) (the look-settle / large-angle gate Op17 had kept the reverse waiting for the first
montage end); (2) GR213_TurnDelta0 is refreshed only while NO montage plays -> chained hand-overs re-fired every MinT (cascade of 4
montages): re-base it when GR_TurnMontage changes (object path text vs GR220_TurnMontName); (3) settle 0.05 s (GR220_TipHandSettle) so
the bin is chosen from the settled camera (else a 45 deg clip for a 90 request, 31 deg left). Result: hand-over 0.10-0.20 s after the
request (was 0.27-0.33), no MM idle gap, done 0.1-0.24 s earlier. TIP + W during the turn: L 28 cm walk-start drag (pre-existing, open).
Sprint stops (stops220.py = every Stop DB entry + per-foot contact in [entry, +1.3 s]; the final217 windows never covered the final stop):
50-105 cm drags had two owners. (a) CONTENT: SHM_A_RR_M_Relaxed_Run_Stop_F_L/Rfoot carry the trailing foot forward at 165-450 cm/s only
0.9-5.6 cm above the floor (clipfeet220.py) -> swingclear220.py with min_height -99 (speed alone marks the swing), height 8, windows
R 0.93-1.47 / L 0.95-1.47: forward sprint stop R 48 -> 3, chain_scurve L 21 -> 2. (b) FACING: a sprint faces its movement
(SprintFaceMove); on release the look-driven yaw swung 90 deg back to the camera in 0.6 s while the stop slid sideways -> GR220_StopFaceHold
(PhysicalRedirect RInterpTo rate ~0 with no MOVEMENT INPUT for > 0.08 s, speed > 5, |control - actor yaw| > 45): lateral sprint stop
L 75 -> 6. TRAPS: RInterpTo_Constant with InterpSpeed <= 0 returns the TARGET (snap) - hold with 0.01, not 0; gate by the facing error (a
0.1 s W->S key gap at 18 deg must not hold); "no input" must be Pawn GetLastMovementInputVector, NOT the CMC current acceleration (zero
while a root-motion reversal step runs with the key held).
Shift re-press: CalculateMaxSpeed dropped to jog at once (490 -> 300 in 0.25 s), the jog loop played 1.3-1.5x and the sprint loop was
re-entered -> 18-30 cm. GR220_GaitDownDecel 250 (limit slews down, never above the real speed, increases immediate) ONLY while the TARGET
gait is below sprint: a sprint cut caps the limit 490 -> 416 with the sprint still targeted - slewing that cap changed the cut path and
(at 120 FPS) put the late-reverse foot sweep on the floor (L 6 -> 38); keying it on GR_ShiftHeld instead failed on the re-press (target
gait lags the key by ~0.25 s). Result: stays in sprint, L 18.5 -> 4.0 (30 FPS), 33.8 -> 4.6 (120 FPS).
Cut -> S (OPEN): the AAMS pivot A_CP2_Jog_Fwd_Pivot is entered at 0.13 and the first re-search after the RedirectHold throttle (~0.3 s)
jumps it to 1.40 (skips 1 s of brake/plant) at every FPS: the capsule turns its velocity 50 -> 160 deg in 0.6 s at >= 100 cm/s while the
clip brakes 303 -> 0 in 0.65 s and plants. Capsule line-brake candidates (GR215_RevBrakeAccel 470; Accel 250/Fric 0.3/Decel 250; Accel
300/Fric 0.3) did not remove the jump (still at the same throttle tick) and raised drag 20 -> 38-46 cm: rejected.
Release during a cut (OPEN): stop entered at clip 0.93-1.00 at 250-260 cm/s (facing error < 45 deg, the hold does not engage).
Measurement traps: (0) contact216 calibrates the floor (b0 / a0) over EVERY row of the run file: a change late in a run (the final
stop) moves the contact numbers of earlier windows whose motion is bit-identical (diverge220.py shows the first foot difference) - an
early-reverse "regression" R 2.7 -> 10.1 was this; measure windows on a copy truncated at t1 + 0.3 s (ctrunc220.py, final220.py ct()).
(1) the V2.19 "r0_w second-direction exit 46 cm" was the FINAL sprint stop (default window 3-9 s) - the exit itself
measures <= 9 cm; (2) fixed-step runs are not bit-exact for every scenario (d_walk 538 vs 591 rows), the d_walk drag change with the
pivot plant had 0 active frames - not caused by it; (3) a mem_guard relaunch inherits V219_EDARGS only when it was exported (runab.sh
EDA=...) - otherwise the rest of a "fixed step" batch runs real time.
Input latency (input_latency220.py, PIE): Enhanced Input injection from the post-tick -> movement sees it the NEXT frame (1); the harness
console key (Input.+key) -> 2 frames. One harness frame is the console forced-key path, not production order.
Graph-builder traps: object == and Greater_DoubleDouble are promotable operators (qa_graph asserts) - use Conv_ObjectToString +
Contains / EqualEqual_StrStr and InRange_FloatFloat; a failed installer leaves in-memory edits - reload the package before the retry.
Pre-existing: ABP SHM213_MontTick "Set SHM213_MontSide" reads a None pawn every frame (tens of thousands of PIE log errors per session).
```

## V2.21 continuity repairs, body settle / terrain body, living camera (2026-10-21; Saved/Codex/SHME_V221_20261021/, tools Tools/SHME_V221_20261021/)
```
Error flow (A): the SHM213_MontTick "null pawn" spam (16 errors / frame) was the DSL translation of LastHitBy (a K2 VariableGet on the
TryGetPawnOwner pawn), not a missing pawn. fix_v221_lasthitby.py rewires every such get to Pawn.GetController (re-run it after ANY
MontTick DSL rebuild). 0 new errors in PIE. Memory: mem_guard still restarts the editor at 38 GB every ~3-4 QA runs - not caused by it.
Recovery rewind (B, PRODUCTION SHM220_RecHold 1): engine source AnimNode_MotionMatching.cpp (5.8) has NO bShouldSearch read; the only
pose hold is ElapsedPoseSearchTime < SearchThrottleTime with a continuing pose that can advance. The V2.20 'not a search' conclusion
was wrong (its gate was dead). install_v221_recthrottle.py: AnimGraph SearchThrottleTime = FMax(old, Select(NOT SHM220_Search,
SHM221_RecThrottle 1.0, 0)). Real time, 0.15-0.18 s hitches in the brake stance: recovery clip rewinds 4/12 runs -> 0/12.
EXIT TRAP: SHM220_RecWin is time-only - the release exit dragged R 18.5 -> 38.2 cm with the hold; install_v221_recexit.py feeds Set
SHM220_Search with OR(previous, NOT SHM217_RecOn) (release / new direction clears RecOn at once) -> 18.5 = base. Tool rewind221.py.
Cut -> S (C, OPEN): the hold works mechanically (install_v221_pivothold.py, SHM221_PivHold, PivSub '_Pivot', PivHoldT 0.8: the AAMS
pivot plays 0.13 -> 0.80 without the 1.27 s jump) but the capsule ROTATES its velocity (49 -> 170 deg at 80-230 cm/s, never stops):
held brake = R 10 -> 65 cm. A real line plant (GR215_RevBrakeAccel 5 / Friction 0 / Decel 400 / MinSpeed 40) stops the capsule on its
line (242 -> 27 cm/s at a constant heading) but MM then plays the jog loop through the brake and enters the pivot at its plant frame:
R 37-68. All rejected (knobs 0). Needs content: a lateral-heading (cut) -> backpedal brake-plant clip pair.
Related (D, measured, open): release mid-cut R 25.6 (StopFaceHoldMinErr 20 / 10 worse: 31.6); W -> S exact reverse L 43 / R 29;
TIP 180 reversed early R 14.6 (yaw rate 506 deg/s); sprint-curve slow motion = sprint DB eligible down to 230 cm/s
(A_SHM_Sprint_Curve at 0.53x, 273-328 cm/s after cuts): SHM_SprintDBMinSpeed 330 / 360 removes it but the jog-curve replacement drags
R 3 -> 54 (rejected).
Small placement steps (4, REJECTED, GR221_TapStepCm 0): a 0.15 s tap moves the capsule 2-4 cm (accel 200 x ease 0.65) while MM plays a
start-transfer STEP -> 8-22 cm drag. install_v221_tapstep.py (pawn GR_Impl_CP_PhysicalRedirect: armed tap -> CMC Velocity toward the
tap direction until TapStepCm) completes 8-19 cm but MM answers with 2-3 steps + a walk stop, rest 0.27 -> 0.80 s, drag not lower.
Next: the root-motion idle steps exist (CoreMotion_Retargeted/AAMS/Idle/am_Stand|Ready_Idle_Step_{Fwd,Bwd}_{L,R}Foot / Left / Right,
+ _NoRM) - route a tap to them like the TIP montages. TRAP: recompiling BP_GR_MotionProfile dropped BP_PBI_Player's GR_Profile to an
explicit None override; saving it killed ALL input (HasIntent never true). Keep the child_profile != None save gate (verify_prod221.py
checks it); repair = req/fix_profile_ref.py.
Body settle (3, PRODUCTION SettleBodyEnabled, Deg 6, DipCm 2, MinSpeed 60, Period 0.9, Tau 0.35): SHM_UpdateBodyTargets, one
forward-then-back trunk pulse exp(-t/Tau) cos(2 pi t / Period) (<= 1.4 s) + knee give on the forward lobe, amplitude = SpeedPeak/300
(0.3..1), only after a real bout (MoveDist > 60 cm), HasIntent fades it in 0.08 s. Adds to the existing brake posture (BrakeLean /
BrakeDrop). Head counter-motion -0.8 -> -1.4..-1.9 cm (walk / jog), sprint LeanFwd 2.3 -> 3.9 -> 0 in 0.7 s; small, visual review.
Terrain body (5, PRODUCTION TerrainBodyEnabled, LeanUp 0.15 / max 2.5, LeanDown 0.1 / max 1.2, cross 0.25 / 3, drop absorb 0.25 / 4):
3 Visibility line traces per frame from the capsule base (+60 / -120 cm): under the capsule, AheadTime x speed (35-140 cm) along the
travel (facing when slow), 30 cm right. Filtered slope (tau 0.25) -> LeanFwdTarget, cross slope -> LeanLatTarget toward the UPHILL
side (the first sign leaned downhill), downhill knee dip, sudden ground drop under the capsule -> pelvis absorb (half when seen
ahead). Slope lean / dip fade with speed 20 -> 80 cm/s (split-height standing must not tilt). Lean chain gain: ~3.4 deg trunk per deg
LeanFwd (0.35 gave +9 deg). Result, trunk pitch vs base: 8 deg hill walk +4.1 / -2.9, jog +3.2 / -2.2, real map climbs +2.4..2.7 /
descents -0.4..-1.7, 10 deg cross slope +2.3 deg uphill; base was identical on flat / up / down ("only the feet react"). Identical at
20 / 30 / 60 / 120 FPS; feet / clip choice unchanged (contact221 equal). Not a stepping change: FootPlacement / LegIK still place feet.
DSL TRAPS: every set re-evaluates its pure binds -> write memories LAST and latch one-shot triggers into a variable (CamStepFire);
explicit spring steps with w*h >= 0.5 kill an impulse at 30 FPS (use an analytic pulse); the source file mixes CRLF / LF (patch both).
Harness traps: v212_run.sh mv() drops a 2nd argument (boxes) -> mvb(); qa_pie sets every shm_profiles.RESPONSE field each run, so
editing shm_profiles.py / comp vars during a batch breaks every later run ("Failed to find property") until rebuilt; IA look is
open-loop - yaw0 is ignored, set a route heading through the yaw path; runab.sh without EDA silently turns a fixed-step batch real
time after a mem_guard restart; a killed batch leaves PIE running (req/end_pie.py). Real map lines: req/probe_route.py (sphere sweeps
on the real collision, Landscape hits only): map_r1 (-500,1000) 135 deg, map_r2 (1000,-500) 270, map_r3 (-500,0) 315.
Tools: contact221 (early calibration), cmp221, terrain221 / terseg221 (segment trunk pitch, slope signal), settle221, smallstep221,
cam221 (FOV pumping, camera jumps / jerk, roll, frame angle, camsteps), rewind221, verify_prod221, promote221 (+ SHME DA).
```

## V2.22 natural start, measured re-acceleration, closer camera (2026-10-22; Saved/Codex/SHME_V222_20261022/, tools Tools/SHME_V222_20261022/)
```
Diagnosis: body222.py (character frame) + clipscan222.py (clip root space) + the CP start clock (CP_StartEvalTime) - the visible start
is the CP branch clip, not the MM pick under it. Production start A_LS_M_Relaxed_Walk_Start_F_L/R raised the forward hand 34-38 cm fwd /
14-15 up (walk loop 25-29 / +1-2), held through a 0.6 s first swing, then a 36 cm snap into the loop. Re-acceleration SHM216_RevTurn_*
carried the vendor sprint-turn upper body (clip pitch 32 deg vs sprint loop 20-25, roll -15..+20, head +-20 cm, hands 69 fwd / 45 up).
PRODUCTION (fresh-editor ALL_OK x3, verify_prod222.py):
  ABP SHM28_StartMode 1 + SHM28_StartL / _R = /Game/GraceRanger/SHME/Animations/V222/A_SHM222_WalkStart_L / _R (gen222_start.py, authoring.md
  V2.22): start hands 0 -> +13 cm -> loop (no lift, no snap), trunk 10.8 -> 18 deg forward fall; restart R 37 -> 5.9 cm, TIP->W 6.9 -> 5.4,
  plain start +1 cm. SHM216_RevTurn_* upper body baked in place (rb222_revturn.py; legs / contacts bit-identical; DBs PSD_SHM214_RevPush,
  PSD_SHM215_RevPushLow, PSD_SHM215_Rev_L / _R re-keyed SHME_V222_RB3): head lateral 43 -> 18 cm, roll +-19 -> +-4, arm abduction 38 -> 14.
  SHME CamCloseEnabled (stand 0.90 / walk 0.88 / jog 0.92 / sprint 0.97 x CamOpenness, tau 0.6): arm 216 / 235 / 260 -> 190 / 216 / 251.
REJECTED: SHM222_TapGate (family 4 -> 0 on a released tap: MM jumped to an idle frame with the foot 19 cm away). OPEN: taps (start-transfer
family stays 0.65 s after a release), side / back starts not regenerated, bump / step stepping content (pilot heel skid 34-48 cm while
the capsule climbs a 20 cm bump), cut->S, release mid-cut, jumps / landings not inspected.
Traps: runab.sh (no EDA) turns fixed-step batches real time after a mem_guard restart - use runfps.sh and check 'dt max'; after a bake +
re-key the first runs select None (warm-up); a verify run in the same editor after harness runs reports the SHME DA dirty (verify first
after a relaunch); the 'A' (original content) capture = editor closed -> file swap -> capture -> restore (restored run bit-identical).
```

## V2.23 jog reversal authority + measured motion (2026-10-22; Saved/Codex/SHME_V223_20261022/, tools Tools/SHME_V223_20261022/)
```
"Teleport toward the camera" in a jog reversal is NOT a position jump: trace223.py (capsule ax / mesh offset mrl / MM root / MM pelvis /
  visible pelvis / camera pivot apv per frame) showed every layer continuous (capsule jump <= 1 cm, residual <= 6 cm/frame). The owner:
  jog S (strafe backpedal) -> W was routed by SHM213_MontTick's forward-run reversal route (camOK + sp > 150) into SHM216_RevTurn_* - a
  SPRINT-authored running turn arc (121 deg root yaw, never below ~140 cm/s, pushes to 416) on a strafe capsule that stops to 0 and
  re-accelerates at 270: legs run on a body that does not travel (slow motion), visible pelvis 15-19 cm behind the capsule for 1.3 s,
  12 cm pelvis drop, deep side-twisting squat (diag capture).
PRODUCTION A1: ABP SHM223_RevRearGate 1 (MontTick: no forward-reversal route while dot(velocity, actor forward) < -0.5 = backpedal) +
  SHM_RedirectDB_JR = PSD_SHM_Redirect_JogReversalQ (V2.2: + SHM_DPP_Jog_Bwd_Pivot, no forward loop). S->W worst contact 51.7 -> 13.3 cm,
  pelvis-capsule -19..+4 -> -1..+11 cm, upright brake + push in the capture; drag sum ~89 -> 106 cm (not solved). Gate 2 (also sideways)
  FAILED: A<->D got the backward pivot (R drag 199 cm) - lateral reversals need lateral pivots in their own database (open).
CANDIDATES OFF (built, measured, not promoted): SHM223_JogPiv_F_B / _B_F (timewarp + remap216 onto a re-push of 420 cm/s2, PSD_SHM223_
  JogReversal), GR223_RevPushAccel (PhysicalRedirect: extra accel after the zero crossing, gait cap window) and SHM223_JrHold (episode kept
  while the push runs). The capsule followed the authored profile, but the push tripped the capture-error RECOVERY database
  (PSD_SHM_Recovery_L, SHM_Rec_*) mid-push even with the hold -> more drag. A faster re-push needs the recovery demand gated first.
OPEN after A1: the backward->forward push leans the VISIBLE trunk to ~51 deg for ~0.4 s (V2.22 RevTurn path 31). Capping the clip's own
  excess pitch (SHM_DPP_Jog_Bwd_Pivot 30.6 -> 11.2 deg, pp223_bwd223b) changed the runtime peak only 57 -> 51: the lean is added at RUNTIME
  (MM mesh pelvis->spine_03 36 deg on an 11 deg clip, visible +15; SHME LeanFwd ~1 during the push; PBI ~5 deg in jog starts). The same
  runtime layer makes jog starts 34 deg on a 10.5 deg clip. Next owner to find: the acceleration-lean chain in the ABP (not the clip).
TRAP: rebuilding SHM213_MontTick from its lisp re-creates the V2.21 LastHitBy translation (camOK = world X): re-apply
  fix_v221_lasthitby.patch after every rebuild (install_v223_reargate.py does it; verify_prod223 checks lasthitby_linked).
TRAP: remap216 / timewarp duplicates inherit the source's BranchIn notifies (production DB membership) - strip every BranchIn whose
  database is not the new one before the DB is re-indexed (bi_strip.py).
Cadence audit (cad223.py, steady 2.5 s windows, fixed 30): ground step / implied step = 0.95-1.02 everywhere (stride warping holds the
  feet); the 'slow motion' owners are PLAY RATES (MM rate = capsule speed / indexed root speed): sprint at the 416 side cap x0.69
  (148 spm, 169 cm steps), walk rear x0.72 (100 spm, 77 cm), jog right x0.84 (136 spm) vs jog left 177 spm. Jog fwd 300 cm/s x1.01,
  164 spm = human-like. Fix = content at those speeds (open).
Jog start 'sprint-like': trunk 34.5 deg peak (steady jog 18-27) at 0.5-0.9 s, hands 35-46 cm forward; the clip itself peaks at 10.5
  (loop 11.7) -> runtime owner: PBI ~5 deg (ProfileEnabled off 34.5 -> 29.1), SHME APA 0; the rest retarget / blend. Open.
Harness: lib223.sh (relaunch keeps -UseFixedTimeStep through the mem_guard restart; newest editor log per batch - a stale LR_LOG after a
  mem restart gave 'rows 0' for a whole batch).
```

## V2.24 jog reversal = request identity + planted foot (2026-10-23; Saved/Codex/SHME_V224_20261022/, tools Tools/SHME_V224_20261022/)
```
20 FPS wrong pivot: on the episode's first frame the capsule had already braked 245 -> 178 cm/s (one 50 ms tick), below
  RedirectBridgeMinSpeed 200 -> RedirectClass 0 -> no bridge -> PSD_CP2_JogPivots served A_CP2_Jog_Fwd_Pivot for a backpedal->forward
  request. FIX (component, PRODUCTION): SpeedOnset = max(Speed, SpeedOnset - RedirectSpeedDecay*dt) classes the episode
  (RedirectSpeedDecay 600 cm/s2; 0 = V2.23) -> same class at 20/30/60/120.
One frame early: the request reverses one tick before the component's episode starts (its velocity is a tick behind) -> the generic
  chooser served A_CP2_Jog_Right_Pivot (LATERAL) for 1 frame in every phase. FIX (ABP, PRODUCTION JRMode >= 2): MontTick SHM224_EarlyRev
  (no episode, input > 150 deg from velocity, 150 < sp < 340) + Update_MotionMatching bridge ELSE -> Branch(EarlyRev) -> SHM_RedirectDB_JR.
Request identity (JRMode >= 1): MontTick latches SHM224_RevIntent on the episode's first frames from dot(v, ACTOR forward): 1 forward
  run -> back, 2 backpedal -> forward, 3 strafe lateral; EventGraph after MontTick writes SHM_RedirectDB_JR = PSD_SHM224_JogRevFwdO /
  BwdO / JogRevLat (one pivot each + loops); lateral never takes the RevTurn arc (A<>D pops 7/291 -> 3/28 m/s2).
Phase-dependent slip = FOOT VARIANT, not search: SHM_DPP_Jog_Bwd_Pivot is entered at 0.87 s in every phase and expects the LEFT ball
  planted; with the right planted the right foot sank 13 cm and slid 37-65 cm. Pose cost could not tell the phases apart (MM picked the
  mirror in every phase when both were in one DB). FIX (content + ABP, PRODUCTION JRMode 3): mirrored copies baked in component space
  (mirror224.py: partner _l/_r, reflect X, reference-pose corrected; mirror-twice exact, tracked bones < 0.4 cm) in their own DBs
  (JogRevBwdM / FwdM); MontTick SHM224_RevMir = intent 2 & right ball 2 cm lower, or intent 1 & left ball 2 cm lower (component
  FootHeightL/R) -> EventGraph picks the M database. 30 FPS backpedal->forward over 10 phases: worst foot 64.7 -> 25.5, mean 36.8 -> 13.9,
  sink -13 -> -4 cm; 20 FPS worst 9.8-32.7. Forward-run -> back is mixed (one phase 35 -> 50), mouse-180+W (RevTurn route) unchanged 55.
TRAP: a removed BranchIn track does NOT remove the clip from the PoseSearch database entry list (even after a restart) - build a fresh DB.
Trunk lean 'added at runtime' (V2.23) was a METRIC mismatch: V2.23 compared clip pelvis->neck pitch (11 deg) with runtime pelvis->spine_03
  (36). Same bone pair, same frames (lean224.py): runtime adds ~0 at the chest (clip p5 +20.2 = MM mesh +20.2), retarget +4 (chest) /
  +11 (lower trunk); the bent read is the CLIP's lumbar flexion (pelvis->spine_03 +26.6 over standing). PBI/APA/brake/warping probes moved it
  <= 3 deg. Content fix (lumbar224.py, spine_01/02 back + spine_04 counter) passed the chest guard only on the jog starts (visible -1.1 deg);
  on the backpedal pivot it changed the chest 3.4 deg and was REJECTED (open: needs authored posture, not a counter-rotation).
Measurement trap: win223 contact is height-based - a planted foot carrying a few mm of IK lift fragments it into fake 40 cm 'slips';
  cross-check with the component contact flags (cslip224.py) before believing a regression.
Editor: a 3 h A/B editor reached 75 GB committed and died in the funcs build (OOM) - relaunch a fresh editor before every build.
```

## V2.25 notes (2026-10-24)

```
Reversal slide owner (open): the VISIBLE foot does not follow the clip foot - F_B brake foot planted in the clip moved 32 cm on screen while
  capsule and clip root matched within 4 cm. Ruled out: stride / orientation warping in AnimationBlendStackGraph_0 (alphas exposed as
  SHM225_SWAlpha / SHM225_OWAlpha multipliers, 1.0 = identical; 0.0 gave byte-identical runs). Next suspects: MM play rate (capsule speed /
  indexed root speed, 0.7-1.2) and FootPlacement plant detection.
Authored JogRev clips (gen225_rev.py, measured capsule table capsule_rev_table.json): better at 20 / 30 FPS, equal or worse at 60 / 120 -
  any reversal candidate needs an FPS sweep before promotion.
Build: comp_vars + profiles and funcs in ONE editor ballooned to 94 GB in write_graph_dsl (3 OOMs); save vars / profiles, relaunch, run funcs
  alone (v225_build3.sh / v225_build4.sh).
Captures: full frame via qa_pie pie_window (editor window narrowed until the docked viewport width % 64 == 0; 1728x940 uncropped).
```

## V2.26 notes (2026-10-24; Saved/Codex/SHME_V226_20261024/, tools Tools/SHME_V226_20261024/)
- Harness state modes (`qa_pie.py`): `state_mode` production (saved SHME DA / ABP defaults untouched) or candidate (production + the run's
  abp/shme flags only); every touched key is restored before the next run; effective state (DA fields, ABP database refs with mtime and
  entry counts, cvars) is recorded at run start and end into `<label>_state.json`; a mismatch marks the run INVALID_STATE (pop_report shows
  status + mode). Replaces the old reset-to-schema-defaults.
- New knobs (DA_SHM_Response_Default): InspectZoomOn (false), InspectTag ("GR_Inspect"), InspectJump 2, StepEdgeOn (false), StepEdgeShift 12,
  StepEdgeShiftFar 18, StepEdgeMin 6->10, StepEdgeStepTime 0.45, StepEdgeStepMax 120, StepEdgeProbe 15, StepPenLiftMax 36,
  SwingLiftMargin 10.5 -> 6 (with the T3g full-deficit lift), InspectRadius 22 -> 12. Component vars: InspectHit*, SwingShiftL/R (V),
  SwingShiftTL/TR. ABP: SHM226_ShiftL/R + two world-space ModifyBones in FeetIK (shift before LegIK).
- Content: SHM226_JogRev_{B_F,F_B}_P0..31 + PSD_SHM226_JogRevBwd/Fwd (full BranchIn windows, footspeed_l/r + Disable_FootLock curves) are
  CANDIDATE assets, not in production; production reversal = V2.24 pivot DBs. Mask sublevel L_GR_CurrentHouseContent: tags + probes saved.
- DSL traps: `select` is float-only (vectors `selv`, strings cannot be selected); actor/component nodes take `:self`; v2_check does not catch
  pin types - a funcs build failure leaves the component dirty (`req/revert_comp_quit.py`, fresh editor).

## V2.27 notes (2026-10-24; Saved/Codex/SHME_V227_20261024/, tools Tools/SHME_V227_20261024/)
- Authored-reversal hold (ABP_GR_MotionMatchingBase, SHM_Snapshot graph patches `install_v227_revhold.py` a..e, no DSL rebuild; knobs are
  ABP vars, 0 = production unchanged): the 64 SHM226_JogRev clips carry the float curve `SHM226_Rev` = remaining clip seconds
  (`add_revcurve227.py`; blends to 0 with the clip weight) -> `SHM227_Rev`. `SHM227_Hold` = RevHold>0.5 & rem > HoldExit (0.25 s) & last
  frame's SHM_RedirectActive & HasIntent & not Dead & not revUp; OR'ed into SHM_RedirectActive and the frame-counter condition, so
  Update_MotionMatching's redirect hold keeps the reversal database until the clip is 0.25 s from its end. `SHM_FootPlaceOff` = FPOff>0.5 &
  rem>0 & |TerrainSlope| < FlatMax (6 deg) & swing lifts < 2 cm & last frame's episode (flat ground only). `SHM227_Thr` (RevHold & rem>0 &
  (last ABP episode OR component RedirectActive) & not Dead) raises the Motion Matching node's SearchThrottleTime to `SHM227_ThrottleT`
  (2.5 s, FMax with the V2.21 recovery throttle): no re-search while the clip can continue; entry (bridge database change), exit (hold
  release = database change) and restarts still search.
- Episode identity guards: `SHM227_Restart` (component RedirectTime decreased = a new component episode while the ABP episode is still held)
  OR'ed into cStart so the bridge frame re-routes the database; `SHM227_Dead` latch until the component restarts: set by a re-entry
  (`SHM227_Rev` rising > 0.05 s while the component episode is over) or by `SHM227_IntentEnd` (component RedirectEnd 3 = new intent, 4 =
  lost; 1 aligned / 2 max dwell keep the hold). Telemetry vars: SHM227_Rev/Hold/Restart/Dead/Thr/IntentEnd (+ curve SHM226_Rev) in
  v212_run.sh avars/acurves.
- Promotion switch `promote227.py` (= promote226 Reversal226 + knobs RevHold/FPOff 1), rollback `req/rollback227.py`, verify gate
  `req/verify_fin227.py` (knobs + 64 curves + V2.26 production verify, prints ALL_OK), final chain `run227_fin.sh <PROMO>`.
- Status 2026-10-24 (REPORT_V227): NOT promoted - knobs 0, production reversal = V2.24 pivot DBs. The hold/FP/throttle mechanisms are
  verified at 20/30/60/120 FPS (exit jump 9-12 -> 0.5-2.7 cm; dbl 100 -> 22 cm; 60 FPS ph0 68 -> 32 = production), but the 32-bin clip
  content fails the FPS criterion at ph3 60/120 (35-42 cm vs 15/27, equal to rv32 alone): a capsule-term mismatch of the bin MM picks at
  that frame rate (P4) against its design table. Promote with promote227.py once the clips' capsule tables match the entry speed per bin.

## V2.28 notes (2026-10-25; Saved/Codex/SHME_V228_20261025/, tools Tools/SHME_V228_20261025/)
- Clip-bound capsule speed (approach B-lite): the authored SHM226 clips carry the designed capsule path as root motion (never consumed:
  ABP root motion mode = montages only) -> float curves SHM226_V (designed speed along the character forward, cm/s) and SHM226_W (= 1,
  blend-weight witness) written by add_speedcurve228.py. ABP SHM_Snapshot (install_v228_clipspeed.py): SHM228_DesV = V / W (W > 0.1),
  SHM228_Cmd = DesV + SHM228_LeadFrames * (DesV - PrevDesV) (the movement update runs before the anim update), SHM228_On = knob
  SHM228_ClipSpeed & W > 0.1 & (ABP episode or component episode) & not Dead -> component contract ClipSpeed / ClipSpeedOn
  (BP_SHM_HumanMotionComponent vars, SHM|V228). BP_GR_Player (install_v228_gr.py + fix_v228_gr2.py): at the end of
  GR_Impl_CP_PhysicalRedirect, Velocity = ActorForward * (ClipSpeed - GetMaxAcceleration * dt * dot(fwd, DesiredDir)) and GroundFriction 0 on
  those frames (the CMC acceleration is kept = HasIntent kept, and pre-compensated); profile knob GR228_ClipSpeed (DA_GR_LocomotionBehavior).
- Cancel paths (install_v228_cancel.py, knobs SHM228_RelHold / SHM228_CancelOn): SHM228_EntrySign (+1 F_B, -1 B_F) latched while a clip is
  in the pose, SHM228_Brake = designed speed still along the entry direction; a lost intent during the brake keeps the hold (the clip-bound
  capsule brakes to the designed zero, the stop comes from the brake stance); a new intent along the brake direction is a CANCEL: SHM_HoldDB
  := the other family database (SelectObject), one interrupting SetDatabaseToSearch on the steady hold path (Update_MotionMatching), the
  entry sign flips, the re-entry latch is disarmed for one frame (PrevRev := 10).
- Inspection: the LookAt skeletal controls (spine_03 / neck_01 / head) already aim the bone local +Y (forward on this skeleton; verified,
  not changed); the component identifies the target by object-name continuity (InspectPrevHitName, InspectIdOn), switches
  after InspectSwitchOn s of dwell on a new candidate without dropping the latch, focus = actor location (InspectFocusMode 1).
- Terrain: true-edge landing shift (SHM_UpdateBodyTargets): edge = probe rise minus the continuous-slope rise (tan(TerrainSlope) * 2 *
  StepEdgeProbe) > StepEdgeMin; landing already on the high side -> +StepEdgeShift, still short -> -StepEdgeShort (new key, 12); lift
  ceiling candidate SwingLiftMax 36.
- Promotion: promote228.py (groups motion / cancel / terrain / stepedge / inspect, rollback), verify gate req/verify_fin228.py, final chain
  run228_fin.sh "<groups>".
- Outcome (REPORT_V228): groups motion / cancel / terrain / stepedge / inspect promoted (promote228.py); verify gate req/verify_fin228.py.
  Cancel path details: the safety SHM228_AgainstT counts only in the push phase (DesV * EntrySign < 0); the reroute lifts the V2.27 search
  throttle for one frame via SHM228_ThrOK; ten reversal bins regenerated by gen228_rev.py (brake foot already on the floor -> the other foot).

## V2.29 effort / RevTurn content fix / release resume (2026-10-25, Saved/Codex/SHME_V229_20261025/)
```
RevTurn content (bug fix, production): the sprint / jog camera-180 'reversed body' was a full chest-vs-pelvis revolution in 6-10 frames of
  SHM216_RevTurn_R_Lfoot / R_Rfoot. Owner: rb222_revturn.py kept-twist term used an UNWRAPPED yaw difference; x KEEP_TWIST 0.5 a 360 error
  became a 180 deg spine_01 twist. rb229_revturn.py = the same bake, wrapped; legs / root / pelvis readback 0.0 cm. Check any bake that
  differences headings: wrap BEFORE scaling. Checkpoint: checkpoint/revturn/.
Effort (SHM_UpdateState, DA_SHM EffortEnabled): EffortE += dt*Gain*demand (|a_h| above EffortA0 per EffortA1 x speed fraction + tiny
  sustained sprint term), recovers with EffortTauRec only while the demand is ~0 (standing / looking / calm walking never build it);
  EffortEUse = low-pass(E, EffortUseTau 1.2) drives the scales (a maneuver must not slow itself); EffortReqLoad = the support load
  latched at the frame the request direction changes (x turn amount), decays EffortReqTau 0.6. Scales -> BP_GR_Player:
  CalculateMaxAcceleration x EffortAccScale, PhysicalRedirect redirect friction x EffortTurnScale (clip-speed frames untouched).
  Production values: Gain 1.6, TurnK 0.5, AccK 0.5, LoadK 0.6, TauRec 5.
Resume (ABP SHM229_ResumeWin 0.2): the V2.28 RelHold gate reads OR(Brake, PostT < ResumeWin): a released brake keeps its clip 0.2 s past
  the zero crossing so a re-press continues the same clip's push (j24_rel 33.9 -> 11.1 cm, no vendor start).
Push-phase cancel (ABP SHM229_PushCancel 1, install_v229_pushcancel.py): SHM228_Cancel := OR(old, PushCancel & clip in pose &
  DesV*EntrySign < -1 & intent along the brake direction & AgainstT > 0). Fixes the V2.28 lock where the one-frame Dead (latched only
  while no component episode runs) was re-armed on the old family and the clip-bound capsule ran backward against a held W.
Open owner: low-speed back-run (< RedirectEpisodeMinSpeed 120) + W -> vendor PSD_Dense_Stand_Sprint_Pivots tail -> WalkToSprint head pop.
```
