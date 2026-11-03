# SHME equations (as implemented, V1 2026-09-25)

Units: cm, s, kg. Every filter is time-aware: `alpha = 1 - exp(-dt / tau)`. Source of truth: `Tools/SHME_V1_20260925/shm_src.py` (authoring dialect) → built into `BP_SHM_HumanMotionComponent`.

| Quantity | Equation | Kind | Function |
|---|---|---|---|
| Acceleration | `a += ((v - v_prev)/dt - a) * alpha(AccelFilterTau)` | measured CMC velocity, filtered | SHM_UpdateState |
| Yaw rate | `dyaw = atan2(sin d, cos d)`, `d = yaw - yaw_prev`; rate filtered | measured, filtered | SHM_UpdateState |
| Desired velocity | `dir(input accel) * MaxSpeed * |input accel|/MaxAccel` | CMC intent | SHM_UpdateState |
| Momentum | `p = M * |v_xy|` (kg·m/s) | approximation (M from profile) | SHM_UpdateState |
| Centre of mass | `COM = Σ m_i r_i / Σ m_i`, `r_i = prox + ratio_i (dist - prox)` over 16 segments | approximation over animation bones | SHM_UpdateBody |
| COM velocity | filtered derivative (ComVelFilterTau) | approximation | SHM_UpdateBody |
| Foot contact | on: speed < ContactSpeedOn & height < ContactHeightOn; stays on until speed > Off or height > Off; confidence filtered (ContactConfTau) | heuristic with hysteresis | SHM_UpdateBody |
| Support side | switches only when one confidence exceeds the other by SupportSwitchMargin | heuristic with hysteresis | SHM_UpdateBody |
| Support region | capsule segment from support-foot centre toward the other foot, length × double-support confidence, radius FootHalfLength | approximation | SHM_UpdateBody |
| Stability margin | `radius - dist(pCOM, closest point on region)`; normalised by StabilityScale | approximation | SHM_UpdateBody |
| Capture point (LIP) | `ω = sqrt(g/h)`, `CP = pCOM + v_COM,xy / ω`; confidence 0 when airborne / COM too low / BalancePlanning off | approximation (level ground assumption) | SHM_UpdateBody |
| Capture error | `clamp(-margin(CP)/CaptureScale, 0, 1) * confidence` | heuristic | SHM_UpdateBody |
| Direction-change demand | `dv = v_des - v`; `k = 1/(T μ g)`; brake = `max(-dv·v̂,0) k`, turn = `|dv⊥| k`, total = `|dv| k` | heuristic normalised by traction limit μg over a comfortable redirect time T | SHM_UpdatePlanner |
| Reversal demand | `brake * clamp(-cos(angle(desired, v)), 0, 1)` | heuristic | SHM_UpdatePlanner |
| Measured lateral accel | `a_lat = v * ω_yaw` | measured | SHM_UpdatePlanner |
| Traction excess | `clamp(total - 1, 0, 1)` (demand beyond μg in time T) | heuristic | SHM_UpdatePlanner |
| Recovery demand | `max(captureError * (1 - max(align,0)), tractionExcess)`, attack/release filtered | heuristic | SHM_UpdatePlanner |
| Braking distance | `d = v² / (2 μ g)` | approximation (friction-limited) | SHM_UpdatePlanner |
| Recovery step target | support-foot centre + dir(CP − support) × clamp(len, StepMin, StepReach), on the support plane | planning signal (not IK) | SHM_UpdateFootPlan |
| Landing severity | impact = −min(v_z in air); `sev = clamp((impact − Soft)/(Hard − Soft))·(1 + 0.25·clamp(v_xy/600))` | approximation | SHM_UpdateAir |
| Landing impulse proxy | `J ≈ M · Δv_z` | approximation (not a physics-engine impulse) | SHM_UpdateAir |
| Environment clearance | sphere traces (camera yaw space) L/R/Up/Rear, 2 per frame; shrink fast (EnvShrinkTau), grow slow (EnvGrowTau) | measured traces, filtered | SHM_UpdateEnvA/B |
| Constrained level | `max(widthTerm, 0.5·ceilingTerm, 0.6·rearTerm)`, asymmetric filter (in 2·EnvShrinkTau, out ConstrainTau), Schmitt latch Enter/Exit | heuristic | SHM_UpdateEnvDerived |
| Camera springs | `x'' = ω²(target − x) − 2ωx'` (critically damped, semi-implicit Euler, dt ≤ 0.05) | response model | SHM_UpdateCameraSignals |

Anthropometry defaults: Dempster segment parameters as tabulated in Winter, D. A. (2009) *Biomechanics and Motor Control of Human Movement* (4th ed.), Table 4.1 — mass fraction / COM ratio: head+neck 0.081/1.0, trunk 0.497/0.50, upper arm 0.028/0.436, forearm+hand 0.022/0.682, thigh 0.100/0.433, leg 0.0465/0.433, foot 0.0145/0.50. Mapped onto UE mannequin bones (neck_01→head, pelvis→neck_01, …) — a game approximation, not clinical data.

## V1.2 additions
- Gait phase from foot contacts with a dwell (GaitMinDwell 0.05 s): double support / L stance / R stance / flight; events
  heel-strike and toe-off per side; cycle time between L heel strikes; cadence = 60 / cycle (steps per minute proxy).
- Support load: t = clamp(((x_com - f_L) . (f_R - f_L)) / |f_R - f_L|^2, 0, 1); load_L ~ conf_L (1 - t), load_R ~ conf_R t,
  normalised. Geometric proxy for force-plate loading.
- Centre of pressure (LIP, Kajita 2003 / Hof 2005): p = x_com - (h / g) x_com''  (cm; h = COM height, g = 980 cm/s^2),
  clamped to the support segment (double support) or a foot-half-length disc around the support foot.
- Yaw angular momentum L_z = m r_g^2 omega (kg m^2/s), torque tau_z = I alpha; r_g = 0.14 m for a standing adult about the
  vertical axis (I ~ 1.0-1.5 kg m^2 at 70 kg). Rigid-body approximation.
- Braking impulse J = m (v_peak - v) / 100 (kg m/s) while braking demand > 0.2; landing impulse J = m |v_z| / 100.
- Anticipatory postural adjustment: before a step from rest the CoP moves opposite to the intended direction for
  ~0.15 s (ApaDuration) by ~3 cm (ApaShiftCm) - the body pushes the ground backwards to accelerate the COM forward.
- Camera landing: contact -> recovery weight w with w'' = -omega^2 w - 2 omega w' (critically damped), omega = 6 / t_recover;
  recovery rate = profile land response + 12 (0.5 + 0.5 severity) w.
- PhysicalMotionIntent cost = traction demand + recovery demand + 0.5 (1 - double support) when committing + stance error / 50:
  the physical price of executing the intent now (concept for chooser/tag weighting; not yet consumed).
