---
name: sphirus-human-motion-engine
description: Technical owner of the SPHIRUS Human Motion Engine (SHME) — the Blueprint biomechanical layer between player intent, CMC, Motion Matching, Procedural Body Inertia and the GraceRanger camera. Use for SHME data contracts (BP_SHM_* component/profiles), its equations (segment COM, support/stability, capture point, traction-normalised turn/brake/reversal demand, landing severity, camera-space environment perception, critically damped camera signals), feature flags, performance budget and SHME A/B validation. Feel targets and final acceptance stay with sphirus-character-camera.
---


> Action-level procedure (intent -> support -> plan -> source -> integration -> visible body): `sphirus-natural-motion`. Editor write / test gates: `sphirus-safe-unreal-iteration`.
# SPHIRUS Human Motion Engine (SHME)

SHME gives the character a persistent, filtered physical state and turns it into bounded signals that the EXISTING owners consume. It is a planning/response layer, not a simulation: every output is an approximation over CMC kinematics and animation-driven bone data.

## Authority

- `sphirus-character-camera` decides what the body/camera must feel like, owns the protected baseline and gives the final verdict. SHME never overrides it.
- CMC owns movement physics; Motion Matching/CP evaluators own the pose vocabulary; FootPlacement/LegIK own contact correction; PBI owns procedural body springs; `BP_GR_Player.GR_UpdateRig` owns the camera. SHME only feeds them.
- Generic engine mechanics route to the `ue-*` skills (movement, animation, IK, physics/traces, input).

## Where it lives (verified 2026-09-25)

| Asset | Role |
|---|---|
| `/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent` | Runtime owner. Attached to `BP_PBI_Player` as `SHM_HumanMotion`; ticks PostPhysics; `SHM_Tick` is the only place with branching (flags, probe phase, telemetry rate, self-profiling) |
| `BP_SHM_ResponseProfile` / `DA_SHM_Response_Default` | Feature flags, filter time constants, thresholds, camera/body gains |
| `BP_SHM_AnthropometryProfile` / `DA_SHM_Anthropometry_Default` | Segment masses/COM ratios, foot/step geometry, limits |
| `BP_GR_Player.GR_UpdateSHMSignals` (+ `GR_SHM_*` vars) | Camera consumer: boom scale, shoulder scale, pivot offset, airborne follow fraction/lag |
| `ABP_GR_MotionMatchingBase.SHM_Snapshot` (+ `SHM_DCSeverity`, `SHM_BodyBlend`) | Body consumer: game-thread snapshot; blended into `PBI_UpdateDirection` severity |

V1.1 adds the execution layer (state machine, actionable foot plan, landing support, post-stop settle, MM hold); V1.2 adds the motor model (gait phase, support load, CoP, momenta, APA, PhysicalMotionIntent), the stance-preserving idle, the owned corrected stop clips and the camera landing phase model — see architecture.md. `Tools/SHME_V1_20260925/` holds every builder/installer (DSL sources in `shm_src.py`).

Details of every function, equation and consumer: [architecture](references/architecture.md). Equations and sources: [biomechanics](references/biomechanics.md).

## Feature flags (all on `DA_SHM_Response_Default`)

`HumanStateEnabled` (master) · `SupportAnalysisEnabled` · `BalancePlanningEnabled` · `TurnPlanningEnabled` · `FootPlanningEnabled` · `LandingResponseEnabled` · `CameraPhysicalSignalsEnabled` · `AdaptiveCameraEnvironmentEnabled` · `DebugVisualizationEnabled` · `TelemetryEnabled` · V1.1 `FootExecutionEnabled` `LandingSupportEnabled` `PostStopStabilizationEnabled` `SettleEnabled` (default off since V1.2) `MotionMatchingPhysicalGuidanceEnabled` (off) · V1.2 `StanceIdleGateEnabled` `CameraLandingPhaseEnabled`. With `HumanStateEnabled=false` every consumer receives neutral values (boom/shoulder 1.0, zero pivot offset, profile air-follow values, body blend 0) — the pre-SHME baseline. `BodyCouplingBlend` scales the PBI blend.

## Rules

1. Consumers must stay neutral when their flag is off; verify with a HumanStateEnabled=false A/B run before claiming any improvement.
2. One variable per experiment (see [validation](references/validation.md)); reject a model that improves a metric while player-camera motion gets worse.
3. Keep bodies straight-line and frame-rate independent (`alpha = 1 - exp(-dt/tau)`); no raw finite differences into consumers.
4. Never describe SHME values as measured physics. Label: measured (CMC velocity, trace hits), approximation (COM, capture point, impulse proxy), heuristic (demand normalisation, environment confidence), animation data (bones).
5. Authoring constraints in this project (Turkish editor locale, no C++ toolchain): see [authoring](references/authoring.md) — it documents the DSL translator, exec-chaining and the pitfalls that silently break graphs.

## Motion-matching node gates (verified V2.39 - read before forcing any database switch)
- `Update_MotionMatching` (the MM node's update function) is a pure route: a branch chain ending in `SetDatabaseToSearch` calls; the live
  `CurrentSelectedDatabase` is written by `Update_MotionMatching_PostSelection` = what MM ACTUALLY selected, not what was requested.
- A forced `SetDatabaseToSearch(..., ForceInterrupt*)` does NOT search while the node's `SearchThrottleTime` (FMax chain: redirect hold,
  V2.21 / V2.27 throttles) holds: the request waited until an episode-class change released the throttle for a frame (0.3-0.6 s late).
  Release the throttle for the switch frames (`SHM239_TkOn`) - `bShouldSearch` (bound to `SHM220_Search`) and the blend time were not it.
- Every new selection blends over `BlendTime` 0.5 s (HermiteCubic, 4 active blends); telemetry reports the dominant asset.
- Ownership: while an authored plan's clip weight runs, ONE owner branch at the function entry keeps the plan's database and skips all
  class routing (`install239_own.py`); decisions use LATCHED state, never a curve that blends during inertialization (a Back takeover's
  target curve 0 -> 1000 passed 564 and read as 'Opp').

## Performance budget

Targets (not facts): state+planner <= 0.20 ms, probes <= 0.25 ms, camera <= 0.20 ms, total <= 1.0 ms average; investigate above 1.5 ms. `SHM_PerfBegin/End` self-profile the whole SHME tick (`CostMs`, `CostAvgMs`, `CostMaxMs`, telemetry `cost`). Blueprint VM cost dominates; a C++ port would be the next step if the budget tightens.

## Load as needed (V2.8 specialties)
| Need | Read |
|---|---|
| Attribute a motion defect to its owner with a falsifiable test (A) | [motion-diagnosis](references/motion-diagnosis.md) |
| Author / correct a contact-preserving clip, move footsteps, retarget checks (C) | [contact-authoring](references/contact-authoring.md) |
| Motion Matching coverage, "no clip / not selected / unsuitable", transition limits (D) | [mm-coverage](references/mm-coverage.md) |
| Terrain, step, slope, bump, slip, landing tiers (E) | [environment-reactions](references/environment-reactions.md) |
| Support / momentum intents and their acceptance (B) | `sphirus-character-camera/references/support-momentum-intents.md` |
| Contact-slip metric, 2×2 protocol, images (F) | `sphirus-qa-regression/references/locomotion-visual-qa.md` |

Tools (run with the engine Python, read harness evidence only): `scripts/contactslip.py <label> [--mesh=vb|mx] [--top=N]`,
`scripts/stopentry.py <label> [--mesh=] [--win=0.6]`; editor job `scripts/clip_inventory.py` (run through the project runner, e.g.
`bash Tools/SHME_V2_20261014/run_v2.sh .agents/skills/sphirus-human-motion-engine/scripts/clip_inventory.py inv 900`).

## Validation

Scenario set, A/B protocol, telemetry fields and evidence locations: [validation](references/validation.md). Final acceptance: `sphirus-character-camera` verification gate (player camera, real level, physical devices).
