"""SHME V1 function sources (authoring dialect, see shm_dsl.py).
Units: cm, s, kg. Filters use alpha = 1 - exp(-dt/tau) (frame-rate independent).
All bodies are straight-line (no exec branching in this editor locale): conditional state uses select/selv/selb;
subsystem gating (feature flags, probe phase, telemetry rate) lives in SHM_Tick (built by build_tick.py).
Every value is an APPROXIMATION or HEURISTIC over animation-driven bone data and CMC kinematics;
nothing here is a musculoskeletal or rigid-body simulation."""

FUNCS = []
def fn(name, params, returns, src): FUNCS.append((name, params, returns, src))

# ---------------------------------------------------------------- Phase A: refs + human physical state
fn('SHM_Init', [], [], r'''
(fn SHM_Init ()
  ; OwnerChar is set by SHM_Tick (exec cast built with direct node wiring)
  (bind c OwnerChar)
  (set Mesh (Sınıf|Character|MeshAl :self c))
  (set MoveComp (Sınıf|Character|CharacterMovementAl :self c))
  (set Capsule (Sınıf|Character|CapsuleComponentAl :self c))
  (set CamBoomScale 1.0)
  (set CamShoulderScale 1.0)
  (set EnvLeft (R EnvSideLength))
  (set EnvRight (R EnvSideLength))
  (set EnvUp (R EnvUpLength))
  (set EnvRear (R EnvRearLength))
  (set WasGrounded true)
  (set PrevVelocity (Dönüşüm|GetVelocity :self c))
  (set Initialized true))
''')

fn('SHM_UpdateState', [('dt', 'float')], [], r'''
(fn SHM_UpdateState (dt)
  (set DeltaTime dt)
  (bind v (Dönüşüm|GetVelocity :self OwnerChar))
  (bind pos (Dönüşüm|GetActorLocation :self OwnerChar))
  (bind idt (/ 1.0 (max dt 0.0001)))
  (bind aa (- 1.0 (exp (/ (- dt) (R AccelFilterTau)))))
  (bind araw (vscale (- v PrevVelocity) idt))
  (set Accel (+ Accel (vscale (- araw Accel) aa)))
  (set PrevVelocity v)
  (set Velocity v)
  (set Position pos)
  (set PlanarVelocity (vec (.x v) (.y v) 0.0))
  (set Speed (vlenxy v))
  (set VerticalSpeed (.z v))
  (bind ia (Piyon|Bileşenler|CharacterMovement|GetCurrentAcceleration :self MoveComp))
  (set InputAccel ia)
  (set HasIntent (> (vlenxy ia) 1.0))
  (set DesiredDir (Matematik|Vektör|Normalize2D(Vector) :A (vec (.x ia) (.y ia) 0.0) :Tolerance 0.0001))
  (bind ms (Bileşenler|Hareket|GetMaxSpeed :self MoveComp))
  (set MaxSpeedNow ms)
  (bind amax (max (Piyon|Bileşenler|CharacterMovement|GetMaxAcceleration :self MoveComp) 1.0))
  (bind imag (clamp (/ (vlenxy ia) amax) 0.0 1.0))
  (set DesiredVelocity (vscale DesiredDir (* ms imag)))
  (bind fwd (Dönüşüm|GetActorForwardVector :self OwnerChar))
  (set Facing fwd)
  (bind ry (Matematik|Trig|Atan2(Degrees) :Y (.y fwd) :X (.x fwd)))
  (bind d0 (- ry PrevYaw))
  (bind dyaw (Matematik|Trig|Atan2(Degrees) :Y (Matematik|Trig|Sin(Degrees) :A d0) :X (Matematik|Trig|Cos(Degrees) :A d0)))
  (bind ya (- 1.0 (exp (/ (- dt) (R YawRateFilterTau)))))
  (bind yraw (* dyaw idt))
  (bind yerr (- yraw YawRate))
  (bind ystep (* yerr ya))
  (bind yr (+ YawRate ystep))
  (set YawAccel (+ YawAccel (* (- (* (- yr YawRate) idt) YawAccel) ya)))
  (set YawRate yr)
  (set PrevYaw ry)
  (set Yaw ry)
  (set Grounded (not (Hareket|IsFalling :self MoveComp)))
  (set FootZ (- (.z pos) (Bileşenler|Kapsül|GetScaledCapsuleHalfHeight :self Capsule)))
  (set MomentumKgMs (* (A BodyMassKg) (/ (vlenxy v) (R CmPerMeter))))
  (bind sp (vlenxy v))
  (set Gait (select (< sp 10.0) 0.0 (select (< sp 200.0) 1.0 (select (< sp 400.0) 2.0 3.0))))
  ; V2.29 effort (HEURISTIC over measured CMC kinematics): EffortE = short-term exertion 0..1 from horizontal acceleration above walking
  ; level (x speed fraction) + a small sustained-sprint term; recovers (tau EffortTauRec) only while the demand is ~0 (standing, looking
  ; around or calm walking never build it). EffortLoad = low-pass |a_h| / EffortLoadA (the support is busy with the current impulse);
  ; EffortLoadDir = EffortLoad x (1 - dot(acc dir, desired dir)) / 2 = load against a NEW direction only (a single brake / push along the
  ; request costs nothing). GR consumes EffortAccScale (max acceleration) and EffortTurnScale (redirect friction): 1.0 = neutral.
  (bind efOn (R EffortEnabled))
  (bind ah (vlenxy Accel))
  (bind wd (* (clamp (/ (- ah (R EffortA0)) (max (R EffortA1) 1.0)) 0.0 2.0) (clamp (/ sp (max (R EffortMinSpeed) 1.0)) 0.0 1.0)))
  (bind ws (* (R EffortSprintGain) (clamp (/ (- sp (R EffortSprintV0)) 200.0) 0.0 1.0)))
  (bind dem (+ wd ws))
  (bind rec (select (> dem 0.05) 0.0 (/ EffortE (max (R EffortTauRec) 0.1))))
  (set EffortE (select efOn (clamp (+ EffortE (* dt (- (* (R EffortGain) dem) rec))) 0.0 1.0) 0.0))
  (bind la (- 1.0 (exp (/ (- dt) (max (R EffortLoadTau) 0.01)))))
  (set EffortLoad (select efOn (+ EffortLoad (* (- (clamp (/ ah (max (R EffortLoadA) 1.0)) 0.0 1.0) EffortLoad) la)) 0.0))
  (bind adir (Matematik|Vektör|Normalize2D(Vector) :A (vec (.x Accel) (.y Accel) 0.0) :Tolerance 0.0001))
  (bind dd (+ (* (.x adir) (.x DesiredDir)) (* (.y adir) (.y DesiredDir))))
  (set EffortLoadDir (select (and efOn HasIntent) (* EffortLoad (clamp (* 0.5 (- 1.0 dd)) 0.0 1.0)) 0.0))
  ; V2.29c request load: latched at the moment the requested direction CHANGES (> ~45 deg in one frame = a new key / stick request):
  ; the support's current load x how far the new request turns away (90 deg = full); decays with EffortReqTau. A steady sprint has no
  ; load -> the first cut is free; a request that arrives while the previous brake / cut is still loading the support is limited.
  (bind dch (* 0.5 (- 1.0 (+ (* (.x DesiredDir) (.x EffortPrevDir)) (* (.y DesiredDir) (.y EffortPrevDir))))))
  (bind newReq (and (and efOn HasIntent) (> dch 0.15)))
  (bind rq0 (* EffortReqLoad (exp (/ (- dt) (max (R EffortReqTau) 0.01)))))
  (set EffortReqLoad (select efOn (select newReq (max rq0 (* EffortLoad (clamp (* 2.0 dch) 0.0 1.0))) rq0) 0.0))
  (set EffortPrevDir (selv HasIntent DesiredDir EffortPrevDir))
  ; V2.29b: the scales read EffortEUse = EffortE low-passed (EffortUseTau): the PREVIOUS efforts limit the next maneuver, a maneuver's own
  ; exertion barely limits itself (v1 slowed a single rested sprint reversal 1.37 -> 2.2 s)
  (set EffortEUse (select efOn (+ EffortEUse (* (- EffortE EffortEUse) (- 1.0 (exp (/ (- dt) (max (R EffortUseTau) 0.01)))))) 0.0))
  (set EffortAccScale (select efOn (max (R EffortScaleMin) (- 1.0 (* (R EffortAccK) EffortEUse))) 1.0))
  (set EffortTurnScale (select efOn (max (R EffortScaleMin) (* (- 1.0 (* (R EffortTurnK) EffortEUse)) (- 1.0 (* (R EffortLoadK) EffortReqLoad)))) 1.0)))
''')

# ---------------------------------------------------------------- Phase B: COM + support + stability + capture point
# COM = sum(m_i * r_i) / sum(m_i); r_i = proximal + ratio_i * (distal - proximal)   (Dempster via Winter 2009, Table 4.1)
fn('SHM_UpdateBody', [('dt', 'float')], [], r'''
(fn SHM_UpdateBody (dt)
  (bind pelvis (bone "pelvis")) (bind neck (bone "neck_01")) (bind head (bone "head"))
  (bind uaL (bone "upperarm_l")) (bind laL (bone "lowerarm_l")) (bind hL (bone "hand_l"))
  (bind uaR (bone "upperarm_r")) (bind laR (bone "lowerarm_r")) (bind hR (bone "hand_r"))
  (bind thL (bone "thigh_l")) (bind caL (bone "calf_l")) (bind ftL (bone "foot_l")) (bind bL (bone "ball_l"))
  (bind thR (bone "thigh_r")) (bind caR (bone "calf_r")) (bind ftR (bone "foot_r")) (bind bR (bone "ball_r"))
  (set PelvisLocation pelvis)
  (bind mHN (A Mass_HeadNeck)) (bind mT (A Mass_Trunk)) (bind mUA (A Mass_UpperArm)) (bind mFA (A Mass_ForearmHand))
  (bind mTh (A Mass_Thigh)) (bind mSh (A Mass_Shank)) (bind mF (A Mass_Foot))
  (bind rUA (A Com_UpperArm)) (bind rFA (A Com_ForearmHand)) (bind rTh (A Com_Thigh)) (bind rSh (A Com_Shank)) (bind rF (A Com_Foot))
  (bind sumw (+ mHN mT (* (+ mUA mFA mTh mSh mF) 2.0)))
  (bind cHN (+ neck (vscale (- head neck) (A Com_HeadNeck))))
  (bind cT (+ pelvis (vscale (- neck pelvis) (A Com_Trunk))))
  (bind cArms (+ (vscale (+ uaL (vscale (- laL uaL) rUA)) mUA) (vscale (+ uaR (vscale (- laR uaR) rUA)) mUA)
                 (vscale (+ laL (vscale (- hL laL) rFA)) mFA) (vscale (+ laR (vscale (- hR laR) rFA)) mFA)))
  (bind cLegs (+ (vscale (+ thL (vscale (- caL thL) rTh)) mTh) (vscale (+ thR (vscale (- caR thR) rTh)) mTh)
                 (vscale (+ caL (vscale (- ftL caL) rSh)) mSh) (vscale (+ caR (vscale (- ftR caR) rSh)) mSh)))
  (bind cFeet (+ (vscale (+ ftL (vscale (- bL ftL) rF)) mF) (vscale (+ ftR (vscale (- bR ftR) rF)) mF)))
  (bind com (vscale (+ (vscale cHN mHN) (vscale cT mT) cArms cLegs cFeet) (/ 1.0 (max sumw 0.001))))
  (bind idt (/ 1.0 (max dt 0.0001)))
  (bind ca (- 1.0 (exp (/ (- dt) (R ComVelFilterTau)))))
  (bind teleC (> (dist com PrevCom) 100.0))
  (set ComVelocity (selv teleC ComVelocity (+ ComVelocity (vscale (- (vscale (- com PrevCom) idt) ComVelocity) ca))))
  (set PrevCom com)
  (set Com com)
  (set ProjectedCom (vec (.x com) (.y com) FootZ))
  (set ComHeight (- (.z com) FootZ))
  ; ---- foot contact: bone world speed + height above the support plane, with on/off hysteresis
  ; V1.3.4 external-transform rebase: a teleport (foot jump > 100 cm in one frame) must not read as foot speed / skating
  (bind teleJ (or (> (dist bL PrevBallL) 100.0) (> (dist bR PrevBallR) 100.0)))
  (bind spL (select teleJ 0.0 (* (dist bL PrevBallL) idt))) (bind spR (select teleJ 0.0 (* (dist bR PrevBallR) idt)))
  (bind hgL (- (.z bL) FootZ)) (bind hgR (- (.z bR) FootZ))
  (set FootSpeedL spL) (set FootSpeedR spR) (set FootHeightL hgL) (set FootHeightR hgR)
  (set PrevBallL bL) (set PrevBallR bR)
  (set ContactL (and Grounded (selb ContactL (and (< FootSpeedL (R ContactSpeedOff)) (< FootHeightL (R ContactHeightOff)))
                                             (and (< FootSpeedL (R ContactSpeedOn)) (< FootHeightL (R ContactHeightOn))))))
  (set ContactR (and Grounded (selb ContactR (and (< FootSpeedR (R ContactSpeedOff)) (< FootHeightR (R ContactHeightOff)))
                                             (and (< FootSpeedR (R ContactSpeedOn)) (< FootHeightR (R ContactHeightOn))))))
  (bind fa (- 1.0 (exp (/ (- dt) (R ContactConfTau)))))
  (set ConfL (+ ConfL (* (- (select ContactL 1.0 0.0) ConfL) fa)))
  (set ConfR (+ ConfR (* (- (select ContactR 1.0 0.0) ConfR) fa)))
  (bind fcL (vscale (+ ftL bL) 0.5)) (bind fcR (vscale (+ ftR bR) 0.5))
  (set FootCenterL fcL) (set FootCenterR fcR)
  ; support side with switch margin (0 = left, 1 = right)
  (bind sw (R SupportSwitchMargin))
  (bind side (select (> ConfL (+ ConfR sw)) 0.0 (select (> ConfR (+ ConfL sw)) 1.0 SupportSide)))
  (set SupportSide side)
  (bind sc (selv (< side 0.5) fcL fcR))
  (bind oc (selv (< side 0.5) fcR fcL))
  (set SupportCenter sc)
  (bind ds (min ConfL ConfR))
  (set DoubleSupport ds)
  ; support region = capsule segment (support foot -> other foot weighted by double support), radius = foot half length
  (bind a2 (vec (.x sc) (.y sc) 0.0))
  (bind oc2 (vec (.x oc) (.y oc) 0.0))
  (bind b2 (+ a2 (vscale (- oc2 a2) ds)))
  (set SupportA a2) (set SupportB b2)
  (bind rad (A FootHalfLength))
  (set SupportRadius rad)
  (bind pc2 (vec (.x com) (.y com) 0.0))
  (bind mcm (- rad (dist pc2 (closest pc2 a2 b2))))
  (set StabilityMarginCm mcm)
  (set StabilityMargin (clamp (/ mcm (R StabilityScale)) -1.0 1.0))
  ; ---- linear inverted pendulum capture point: omega = sqrt(g/h), CP = pCOM + v_com / omega  (planning signal only)
  (bind h (max (- (.z com) FootZ) (A MinComHeight)))
  (bind om (sqrt (/ (R Gravity) h)))
  (set Omega om)
  (bind cp (+ pc2 (vscale (vec (.x ComVelocity) (.y ComVelocity) 0.0) (/ 1.0 om))))
  (set CapturePoint (vec (.x cp) (.y cp) FootZ))
  (bind cmm (- rad (dist cp (closest cp a2 b2))))
  (set CaptureMarginCm cmm)
  (bind conf (select (and (R BalancePlanningEnabled) (and Grounded (> (- (.z com) FootZ) (* (A MinComHeight) 0.6)))) (max ConfL ConfR) 0.0))
  (set CaptureConfidence conf)
  (set CaptureError (* (clamp (/ (- cmm) (R CaptureScale)) 0.0 1.0) conf)))
''')

# ---------------------------------------------------------------- Phase B2: gait phase, support load, CoP, momenta, APA, intent
# Gait phase from the hysteretic foot contacts with a dwell; support load = COM projection along the inter-foot axis weighted
# by contact confidence; CoP from the LIP relation p = x - (h/g) x'' clamped to the support (approximation, not a sensor);
# L_z = m r_g^2 yaw_rate, tau_z = I yaw_accel (rigid-body yaw approximation); J_brake = m dv; APA = CoP shift opposite to
# the intended step for ApaDuration after an intent onset from rest (Winter 2009 ch.4/5, Hof 2005 capture point).
fn('SHM_UpdateGait', [('dt', 'float')], [], r"""
(fn SHM_UpdateGait (dt)
  (bind cand (select (not Grounded) 3.0 (select (and ContactL ContactR) 0.0 (select ContactL 1.0 (select ContactR 2.0 GaitPhase)))))
  (set GaitDwell (+ GaitDwell dt))
  (bind switch (and (> (abs (- cand GaitPhase)) 0.5) (or (> GaitDwell (R GaitMinDwell)) (not Grounded))))
  (set GaitPhase (select switch cand GaitPhase))
  (set GaitDwell (select switch 0.0 GaitDwell))
  (set HeelStrikeL (and ContactL (not PrevContactL))) (set HeelStrikeR (and ContactR (not PrevContactR)))
  (set ToeOffL (and (not ContactL) PrevContactL)) (set ToeOffR (and (not ContactR) PrevContactR))
  (set PrevContactL ContactL) (set PrevContactR ContactR)
  (bind now (İşlevsellikler|Zaman|GetGameTimeinSeconds))
  (set GaitCycleTime (select (and HeelStrikeL (> LastStrikeTimeL 0.0)) (- now LastStrikeTimeL) GaitCycleTime))
  (set LastStrikeTimeL (select HeelStrikeL now LastStrikeTimeL))
  (set Cadence (select (> Speed 20.0) (/ 60.0 (max GaitCycleTime 0.3)) 0.0))
  ; support load (0..1 each, sum 1 while grounded)
  (bind d (- FootCenterR FootCenterL))
  (bind dl (max (vlenxy d) 1.0))
  (bind t (clamp (/ (dot (- ProjectedCom FootCenterL) d) (* dl dl)) 0.0 1.0))
  (bind wl (+ (* ConfL (- 1.0 t)) 0.001)) (bind wr (+ (* ConfR t) 0.001))
  (set SupportLoadL (select Grounded (/ wl (+ wl wr)) 0.0))
  (set SupportLoadR (select Grounded (/ wr (+ wl wr)) 0.0))
  ; COM acceleration (filtered, same tau as the COM velocity) and LIP centre of pressure
  (bind idt (/ 1.0 (max dt 0.0001)))
  (bind ca (- 1.0 (exp (/ (- dt) (R ComVelFilterTau)))))
  (set ComAccel (+ ComAccel (vscale (- (vscale (- ComVelocity PrevComVel) idt) ComAccel) ca)))
  (set PrevComVel ComVelocity)
  (bind hg (/ (max ComHeight 30.0) (R Gravity)))
  (bind praw (- ProjectedCom (vscale (vec (.x ComAccel) (.y ComAccel) 0.0) hg)))
  (bind pseg (closest praw FootCenterL FootCenterR))
  (bind off1 (- praw SupportCenter))
  (bind pone (+ SupportCenter (vscale (normal off1) (min (vlenxy off1) (A FootHalfLength)))))
  (bind pcop (selv (> DoubleSupport 0.3) pseg pone))
  (set CoP (selv Grounded (vec (.x pcop) (.y pcop) FootZ) ProjectedCom))
  ; yaw angular momentum / torque (kg m^2/s, N m) and braking impulse (kg m/s)
  (bind rg (A RadiusOfGyrationYawM))
  (bind iz (* (A BodyMassKg) (* rg rg)))
  (set AngularMomentumZ (* iz (* YawRate 0.0174533)))
  (set YawTorque (* iz (* YawAccel 0.0174533)))
  (set BrakeImpulse (select (> BrakingDemand 0.2) (* (A BodyMassKg) (/ (max (- SpeedPeak Speed) 0.0) (R CmPerMeter))) 0.0))
  ; anticipatory postural adjustment: intent onset from rest -> CoP shift opposite to the step for ApaDuration
  (bind onset (and (and HasIntent (not PrevIntent)) (< Speed 10.0)))
  (set ApaTimer (select onset (R ApaDuration) (max (- ApaTimer dt) 0.0)))
  (set PrevIntent HasIntent)
  (set ApaActive (> ApaTimer 0.0))
  (set ApaOffset (vscale DesiredDir (* (- 0.0 (R ApaShiftCm)) (/ ApaTimer (max (R ApaDuration) 0.01)))))
  ; physical motion intent: type, signed direction (deg, + left), urgency, selection cost (concept for chooser/routing)
  (bind sdir (Matematik|Trig|Atan2(Degrees) :Y (.z (cross Facing DesiredDir)) :X (dot Facing DesiredDir)))
  (set PMI_Direction (select HasIntent sdir 0.0))
  (set PMI_Type (select (not Grounded) 7.0 (select (> LandingTimer 0.0) 8.0 (select (> ReversalDemand (R ExecReversal)) 5.0
                (select (> RecoveryDemand (R ExecRecovery)) 6.0 (select (and HasIntent (> (abs PMI_Direction) 45.0)) 4.0
                (select (and HasIntent (< Speed 30.0)) 1.0 (select (and (not HasIntent) (> Speed 30.0)) 3.0 (select HasIntent 2.0 0.0)))))))))
  (set PMI_Urgency (clamp (max TractionDemand (max RecoveryDemand LandingSeverity)) 0.0 1.0))
  (set PMI_Cost (+ TractionDemand (+ RecoveryDemand (+ (* (- 1.0 DoubleSupport) (select (> PMI_Type 2.5) 0.5 0.0)) (/ StanceError 50.0))))))
""")

# ---------------------------------------------------------------- Phase C: turn / braking / reversal physical planner
# dv = v_desired - v; demands are |dv| components normalised by the traction-limited acceleration mu*g over a
# comfortable redirect time T:  demand = (|dv| / T) / (mu * g).  a_lat(measured) = v * omega.  d_brake = v^2 / (2 mu g).
fn('SHM_UpdatePlanner', [('dt', 'float')], [], r'''
(fn SHM_UpdatePlanner (dt)
  (bind moving (> Speed 10.0))
  (bind vh (Matematik|Vektör|Normalize2D(Vector) :A PlanarVelocity :Tolerance 0.0001))
  (bind vhat (selv moving vh Facing))
  (bind dv (- DesiredVelocity PlanarVelocity))
  (bind along (dot dv vhat))
  (bind lat (vlenxy (- dv (vscale vhat along))))
  (bind gmu (* (R TractionMu) (R Gravity)))
  (bind T (max (R RedirectTime) 0.05))
  (bind k (/ 1.0 (* T gmu)))
  (bind brakeRaw (clamp (* (max (- along) 0.0) k) 0.0 1.0))
  (bind turnRaw (clamp (* lat k) 0.0 1.0))
  (bind totRaw (* (vlenxy dv) k))
  (bind align (select HasIntent (clamp (dot DesiredDir vhat) -1.0 1.0) 1.0))
  (set IntentAlign align)
  (set TurnAngle (select (and HasIntent moving) (acosd align) 0.0))
  (bind revRaw (* brakeRaw (clamp (- align) 0.0 1.0)))
  (bind aA (- 1.0 (exp (/ (- dt) (R DemandAttackTau)))))
  (bind aR (- 1.0 (exp (/ (- dt) (R DemandReleaseTau)))))
  (set TurnSeverity (+ TurnSeverity (* (- turnRaw TurnSeverity) (select (> turnRaw TurnSeverity) aA aR))))
  (set BrakingDemand (+ BrakingDemand (* (- brakeRaw BrakingDemand) (select (> brakeRaw BrakingDemand) aA aR))))
  (set ReversalDemand (+ ReversalDemand (* (- revRaw ReversalDemand) (select (> revRaw ReversalDemand) aA aR))))
  (set RequiredAccel (/ (vlenxy dv) T))
  (set LateralAccelDemand (* Speed (abs (* YawRate 0.0174533))))
  (set TractionDemand totRaw)
  (bind excess (clamp (- totRaw 1.0) 0.0 1.0))
  (set TractionExcess excess)
  ; V1.3.1 perturbation state: a speed INCREASE the actuator cannot explain (no intent, or above the movement component's
  ; max acceleration) is an external push; it decays with PerturbTau. Walking keeps the capture point outside the support
  ; by design (CaptureError ~1 while stepping), so recovery demand needs the unintended part: misalignment with intent,
  ; or a push.
  (bind dspd (- Speed SpeedPrev))
  (bind amax (max (Piyon|Bileşenler|CharacterMovement|GetMaxAcceleration :self MoveComp) 1.0))
  (bind pushRaw (select (and (and Grounded (> dspd (* (R PerturbAccel) dt))) (or (not HasIntent) (> dspd (* (* amax 1.5) dt)))) 1.0 0.0))
  ; V1.3.4: the push memory does not fade while the capture error is still unsettled (a shove's consequence unfolds over the
  ; next few hundred ms as the COM moves), bounded by PerturbMaxHold
  (set PerturbHoldTime (select (> pushRaw 0.5) 0.0 (+ PerturbHoldTime dt)))
  (bind ptbDecay (or (< CaptureError (R PerturbHoldError)) (> PerturbHoldTime (R PerturbMaxHold))))
  (set PerturbState (select (> pushRaw 0.5) 1.0 (select ptbDecay (* PerturbState (exp (/ (- dt) (R PerturbTau)))) PerturbState)))
  ; recovery = capture error caused by an external push. Intent misalignment is a redirection (turn / reversal classes) and
  ; traction excess at an obstacle is the blocked class: with the route live, both produced recovery steps inside
  ; intentional turns, stops and wall impacts (V1.3.1 matrix: sprint_90 stop 35 cm, jog wall 84 cm).
  (bind recRaw (clamp (* CaptureError PerturbState) 0.0 1.0))
  ; a push is an impulse: the demand attacks instantly on the push frame (reflex), otherwise the usual attack/release
  (set RecoveryDemand (select (> pushRaw 0.5) (max RecoveryDemand recRaw) (+ RecoveryDemand (* (- recRaw RecoveryDemand) (select (> recRaw RecoveryDemand) aA aR)))))
  (set SupportDemand (clamp (* (max TurnSeverity BrakingDemand) (+ 0.5 (* (- 1.0 StabilityMargin) 0.5))) 0.0 1.0))
  (set BrakingDistance (/ (* Speed Speed) (* gmu 2.0)))
  (set SpeedPrev Speed))
''')

# ---------------------------------------------------------------- Phase D: bounded recovery-step target (planning signal)
fn('SHM_UpdateFootPlan', [], [], r'''
(fn SHM_UpdateFootPlan ()
  ; V1.1 actionable plan: capture point -> anatomical reach region (facing frame around the support foot) -> ground validation
  (bind fwd2 (Matematik|Vektör|Normalize2D(Vector) :A (vec (.x Facing) (.y Facing) 0.0) :Tolerance 0.0001))
  (bind right2 (vec (- (.y fwd2)) (.x fwd2) 0.0))
  (bind base (vec (.x SupportCenter) (.y SupportCenter) 0.0))
  (bind to (- (vec (.x CapturePoint) (.y CapturePoint) 0.0) base))
  (bind lx (dot to fwd2)) (bind ly (dot to right2))
  (bind cx (clamp lx (- (R ReachBackward)) (R ReachForward)))
  (bind cy (clamp ly (- (R ReachLateral)) (R ReachLateral)))
  (bind exceed (max (abs (- lx cx)) (abs (- ly cy))))
  (set ReachExceeded (> exceed 5.0))
  (set RecommitDemand (clamp (/ exceed 40.0) 0.0 1.0))
  (bind t2 (+ base (+ (vscale fwd2 cx) (vscale right2 cy))))
  (bind (x0 hit ok) (Çarpışma|LineTraceByChannel :Start (vec (.x t2) (.y t2) (+ FootZ 60.0)) :End (vec (.x t2) (.y t2) (- FootZ 80.0)) :TraceChannel "TraceTypeQuery1" :bTraceComplex false :bIgnoreSelf true))
  (bind (bh io tm dd loc ip nrm) (Çarpışma|BreakHitResult :Hit hit))
  (bind gz (select ok (.z ip) FootZ))
  (set GroundNormal (selv ok nrm "(X=0,Y=0,Z=1)"))
  (set GroundValid (and ok (and (> (.z nrm) (R GroundMaxSlopeCos)) (< (abs (- gz FootZ)) (R GroundMaxStep)))))
  (set FootTarget (vec (.x t2) (.y t2) gz))
  (set FootTargetFacing (Matematik|Vektör|Normalize2D(Vector) :A (selv HasIntent DesiredDir fwd2) :Tolerance 0.0001))
  (set SwingSide (- 1.0 SupportSide))
  (set StepUrgency (clamp (max RecoveryDemand (* CaptureError CaptureConfidence)) 0.0 1.0))
  (set FootTargetWeight (clamp (max StepUrgency (* BrakingDemand 0.5)) 0.0 1.0))
  (set FootTargetConfidence (* FootTargetWeight CaptureConfidence (select GroundValid 1.0 0.3)))
  (set FootTargetValid (and Grounded (and GroundValid (> FootTargetConfidence 0.05))))
  (set FootPlantStrength (* (clamp (- 1.0 TractionExcess (* RecoveryDemand 0.5) (* RecommitDemand 0.5)) 0.0 1.0) (max ConfL ConfR))))
''')

# ---------------------------------------------------------------- V1.1 execution state machine
# 0 NONE 1 MINOR_WEIGHT_SHIFT 2 SUPPORT_TRANSFER 3 COMMITTED_PLANT 4 RECOVERY_STEP 5 BRAKE_AND_REPLANT
# 6 REVERSAL_RECOMMIT 7 LANDING_SUPPORT 8 POST_STOP_STABILIZE. A candidate must persist ExecMinDwell before it becomes the state.
fn('SHM_UpdateExecution', [('dt', 'float')], [], r'''
(fn SHM_UpdateExecution (dt)
  (bind land (and (R LandingSupportEnabled) (and Grounded (> LandingTimer 0.0))))
  (set LandingSupportActive land)
  ; post-stop stabilisation latch: engages only once stopped after a real braking event; releases on input,
  ; when the fore-aft stance stagger has recovered, or at a safety cap
  (bind fwd2 (Matematik|Vektör|Normalize2D(Vector) :A (vec (.x Facing) (.y Facing) 0.0) :Tolerance 0.0001))
  ; stance offset: max of fore-aft stagger and how far the feet's mean sits from the projected COM (braking stance)
  (bind mid (vscale (+ FootCenterL FootCenterR) 0.5))
  (set Stagger (max (abs (dot (- FootCenterL FootCenterR) fwd2)) (abs (dot (- mid ProjectedCom) fwd2))))
  (bind still (and (R PostStopStabilizationEnabled) (and Grounded (and (not HasIntent) (< Speed 10.0)))))
  (set BrakePeak (max BrakingDemand (* BrakePeak (exp (/ (- dt) 1.0)))))
  (bind engage (and still (> BrakePeak (R PostStopBrakeMin))))
  (bind release (or (< Stagger (R PostStopStaggerRelease)) (> PostStopTime (R PostStopMaxTime))))
  (bind post (and still (and (or engage PostStopActive) (not release))))
  (set PostStopTime (select post (+ PostStopTime dt) 0.0))
  (set PostStopActive post)
  (set HoldStops post)
  (bind cand (select land 7.0 (select (> ReversalDemand (R ExecReversal)) 6.0 (select (and (> BrakingDemand (R ExecBrake)) (not HasIntent)) 5.0
     (select (and (> RecoveryDemand (R ExecRecovery)) (> CaptureConfidence 0.5)) 4.0 (select (> TurnSeverity (R ExecCommit)) 3.0
     (select (> (max TurnSeverity BrakingDemand) (R ExecTransfer)) 2.0 (select post 8.0 (select (> TurnSeverity (R ExecMinorTurn)) 1.0 0.0)))))))))
  (set ExecCandidateTime (select (< (abs (- cand ExecCandidate)) 0.5) (+ ExecCandidateTime dt) 0.0))
  (set ExecCandidate cand)
  (bind promote (and (> ExecCandidateTime (R ExecMinDwell)) (> (abs (- cand ExecState)) 0.5)))
  (set ExecAge (select promote 0.0 (+ ExecAge dt)))
  (set ExecState (select promote cand ExecState))
  (set PlantRadiusOverride (select (and land (R FootExecutionEnabled)) (R LandingPlantRadius) 0.0)))
''')

# post-stop capsule settle: move the gameplay capsule toward the real (projected) COM while stabilising so the
# idle does not re-centre the body onto a capsule that stopped short; FootPlacement keeps planted feet fixed in world.
fn('SHM_UpdateSettle', [('dt', 'float')], [], r'''
(fn SHM_UpdateSettle (dt)
  (bind off (vec (- (.x ProjectedCom) (.x Position)) (- (.y ProjectedCom) (.y Position)) 0.0))
  (bind mag (vlenxy off))
  (set SettleOffset mag)
  ; one settle per stop: window = standing still after a braking event; ends when the offset first converges or the
  ; per-stop budget (SettleMaxOffset) is used; re-armed only by new input (never chases idle weight shifts)
  (bind still (and (R PostStopStabilizationEnabled) (and Grounded (and (not HasIntent) (< Speed 10.0)))))
  (set SettleDone (and (not HasIntent) (or SettleDone (and still (or (< mag (R SettleMinOffset)) (> SettleEvent (R SettleMaxOffset)))))))
  ; V1.3.6: quiet support = COM speed under SettleQuietSpeed for SettleQuietTime while still; the idle takeover waits for it
  (set SettleQuietTimer (select (and still (< (vlenxy ComVelocity) (R SettleQuietSpeed))) (+ SettleQuietTimer dt) 0.0))
  (set SettleQuiet (> SettleQuietTimer (R SettleQuietTime)))
  ; only a real stop from sustained motion (micro taps never reach SettleMinEntrySpeed -> protected tap behaviour untouched)
  (set SpeedPeak (max Speed (* SpeedPeak (exp (/ (- dt) 1.5)))))
  ; distance travelled in this bout of movement (reset after 0.2 s standing still): micro taps travel ~10 cm
  ; a new bout starts when input returns after >0.2 s standing still (uses the previous StillTime, so update it after)
  (set MoveDist (select (and HasIntent (> StillTime 0.2)) 0.0 (+ MoveDist (* Speed dt))))
  (set StillTime (select still (+ StillTime dt) 0.0))
  ; input hold duration of the last press: a micro tap (protected P1) never qualifies for a settle
  (set LastIntentHold (select HasIntent LastIntentHold (select (> IntentHold 0.0) IntentHold LastIntentHold)))
  (set IntentHold (select HasIntent (+ IntentHold dt) 0.0))
  ; V1.2 expected-benefit gate: the settle only pays when the idle animation would re-centre the body onto the capsule;
  ; with the stance-preserving idle (StanceIdleGateEnabled and a held stance) the body stays where it stopped, so a
  ; capsule move would only drag planted feet (jog/wall/stairs side effects in V1.1)
  (bind benefit (not (and (R StanceIdleGateEnabled) IdleHold)))
  (bind ok (and (and (and (R SettleEnabled) benefit) (> DoubleSupport (R SettleMinDoubleSupport))) (and (and still (and (and (and (> SpeedPeak (R SettleMinEntrySpeed)) (> MoveDist (R SettleMinMoveDist))) (> (max LastIntentHold IntentHold) (R SettleMinIntentHold))) (not SettleDone))) (< mag (R SettleMaxOffset)))))
  ; wall guard: no settle when an obstacle lies along the settle direction (body braced against a wall)
  (bind dir (Matematik|Vektör|Normalize2D(Vector) :A off :Tolerance 0.0001))
  (bind org (+ Position (vec 0.0 0.0 20.0)))
  (bind (xw hitw blocked) (Çarpışma|SphereTraceByChannel :Start org :End (+ org (vscale dir 60.0)) :Radius 30.0 :TraceChannel "TraceTypeQuery1" :bTraceComplex false :bIgnoreSelf true))
  (bind a (- 1.0 (exp (/ (- dt) (R SettleTau)))))
  (bind step (vscale off (select (and ok (not blocked)) a 0.0)))
  (set SettleEvent (select HasIntent 0.0 (+ SettleEvent (vlenxy step))))
  (set SettleApplied (+ SettleApplied (vlenxy step)))
  (set SettleActive (> (vlenxy step) 0.02))
  (Dönüşüm|AddActorWorldOffset :self OwnerChar :DeltaLocation step :bSweep true :bTeleport false)
  ; V1.2 stance vs idle stance (actor frame): the Ranger idle takeover crossfades to a fixed neutral stance; from a wide
  ; diagonal-stop stance that crossfade drags a planted foot 20-29 cm. IdleHold keeps the stop motion until compatible.
  ; the idle pose lives in the MESH frame (AAMS root-yaw offset rotates the mesh under the capsule after turns): mesh right
  ; vector = character forward for the -90 yaw mannequin mount, mesh forward = character left
  (bind mfw (Matematik|Vektör|Normalize2D(Vector) :A (Dönüşüm|GetRightVector :self Mesh) :Tolerance 0.0001))
  (bind rtv (vec (- 0.0 (.y mfw)) (.x mfw) 0.0))
  (bind rl (- PrevBallL Position)) (bind rr (- PrevBallR Position))
  (bind el (vlenxy (vec (- (dot rl mfw) (A IdleStanceLX)) (- (dot rl rtv) (A IdleStanceLY)) 0.0)))
  (bind er (vlenxy (vec (- (dot rr mfw) (A IdleStanceRX)) (- (dot rr rtv) (A IdleStanceRY)) 0.0)))
  (set StanceErrL el) (set StanceErrR er)
  (set StanceError (max el er))
  (set IdleHold (and Grounded (> (max el er) (R IdleStanceTolerance)))))
''')

# ---------------------------------------------------------------- Phase D2 (V1.3): physical motion family routing
# Converts the motor signals into ONE family per frame with hysteresis (min hold, cooldown): the ABP routes the family to
# a database. Blocked = intent into an obstacle with no progress (wall push): not an idle, never a stance hold.
fn('SHM_UpdateRouting', [('dt', 'float')], [], r"""
(fn SHM_UpdateRouting (dt)
  (bind org (+ Position (vec 0.0 0.0 25.0)))
  (bind ddir (Matematik|Vektör|Normalize2D(Vector) :A DesiredDir :Tolerance 0.0001))
  (bind (xb hitb wall) (Çarpışma|SphereTraceByChannel :Start org :End (+ org (vscale ddir (R BlockedProbe))) :Radius (R BlockedRadius) :TraceChannel "TraceTypeQuery1" :bTraceComplex false :bIgnoreSelf true))
  (bind blockedNow (and (and HasIntent Grounded) (and wall (< Speed (R BlockedMaxSpeed)))))
  ; V1.3.7 hysteresis: once blocked, stay blocked while still stopped with intent (the probe follows the swept input)
  (set BlockedTime (select blockedNow (+ BlockedTime dt) (select (and (and Blocked HasIntent) (< Speed (R BlockedMaxSpeed))) BlockedTime 0.0)))
  (set Blocked (> BlockedTime 0.08))
  ; recovery candidates from the capture point plan; support-side gate: the swing foot must be unloaded or double support
  (bind swingLoad (select (< SwingSide 0.5) SupportLoadL SupportLoadR))
  (bind supportOk (or (> DoubleSupport 0.5) (< swingLoad (R RouteSwingLoadMax))))
  ; the planned step must be feasible: a clearance sweep from the support toward the foot target (a step into a wall is
  ; never a recovery; the body would push off instead, which is the blocked family)
  (bind (xs hits stepBlocked) (Çarpışma|SphereTraceByChannel :Start (+ SupportCenter (vec 0.0 0.0 25.0)) :End (+ FootTarget (vec 0.0 0.0 25.0)) :Radius 15.0 :TraceChannel "TraceTypeQuery1" :bTraceComplex false :bIgnoreSelf true))
  (bind recCand (and (and Grounded (and (not Blocked) (not stepBlocked))) (and (and (> RecoveryDemand (R RouteRecoveryDemand)) (> FootTargetConfidence (R RouteRecoveryConfidence))) (and (< Speed (R RouteRecoveryMaxSpeed)) supportOk))))
  (bind strong (> Speed (R RouteStrongRecoverySpeed)))
  ; velocity redirection (primary turn physics under strafe control): dV = v_desired - v, normalised by what one support
  ; step can deliver through traction (mu g t_step ~ 275 cm/s); braking part = -dV . v_hat; yaw momentum is secondary
  (bind vxy (vec (.x Velocity) (.y Velocity) 0.0))
  (bind dvel (- (vec (.x DesiredVelocity) (.y DesiredVelocity) 0.0) vxy))
  (bind dvm (vlenxy dvel))
  (set DeltaVMag dvm)
  (bind vhat (Matematik|Vektör|Normalize2D(Vector) :A vxy :Tolerance 0.0001))
  (bind dhat (Matematik|Vektör|Normalize2D(Vector) :A DesiredVelocity :Tolerance 0.0001))
  (set RedirectionAngle (select (and (> Speed 30.0) HasIntent) (acosd (clamp (dot vhat dhat) -1.0 1.0)) 0.0))
  (set BrakeRequirement (max 0.0 (- 0.0 (dot dvel vhat))))
  (bind cap (max (* (R TractionMu) (* (R Gravity) (R RedirectStepTime))) 1.0))
  (set RedirectionDemand (select (and Grounded HasIntent) (clamp (/ dvm cap) 0.0 3.0) 0.0))
  ; 0 normal, 1 committed, 2 hard, 3 reversal (by demand + angle, never by angle alone)
  (set TurnClass (select (and (> RedirectionAngle (R RedirectReversalAngle)) (> RedirectionDemand (R RedirectCommitted))) 3.0 (select (> RedirectionDemand (R RedirectHard)) 2.0 (select (> RedirectionDemand (R RedirectCommitted)) 1.0 0.0))))
  ; V1.3.4 committed redirection episode: latched at the onset of a real direction change while moving; ends only on
  ; alignment (after a minimum dwell), timeout, a genuinely new intent, or loss of ground / intent / speed. The ABP holds
  ; the Motion Matching database for the episode (no A -> B -> C reselection from trajectory noise).
  ; V2.30 low-speed reversal: a recently running body (SpeedPeak above walk) reversing above RedirectLowRevSpeed is a reversal episode
  ; V2.31: the same low-speed reversal while moving FORWARD along the facing, only for a JOG-mode request (RedirectLowRevPeak < MaxSpeedNow <
  ; RedirectLowRevFwdMax; sprint faces its travel and reverses with the RevTurn route): the release -> re-press inside a brake (j30_rel: forward
  ; walk-stop at 45-64 cm/s) became an EarlyRev clip without an episode (no clip-bound capsule, no hold) -> AAMS jog start. FwdMax 0 = V2.30
  (bind lrDot (dot vhat (normal (vec (.x Facing) (.y Facing) 0.0))))
  (bind lowRev (and (and (> (R RedirectLowRevSpeed) 0.5) (or (< lrDot -0.7) (and (> lrDot 0.7) (< MaxSpeedNow (R RedirectLowRevFwdMax))))) (and (> MaxSpeedNow (R RedirectLowRevPeak)) (> RedirectionAngle (R RedirectReversalClassAngle)))))   ; the REQUESTED gait is jog / sprint (CMC max speed above any walk; a walk right after a sprint stays out); a BACKPEDAL (moving against the facing) only: sprint faces its travel, so lateral / camera reversals keep the V2.29 rule
  (bind rdCand (and (and Grounded HasIntent) (and (> Speed (select lowRev (min (R RedirectLowRevSpeed) (R RedirectEpisodeMinSpeed)) (R RedirectEpisodeMinSpeed))) (> RedirectionAngle (R RedirectEpisodeAngle)))))
  (bind gapKeep (and (R RevGapKeep) (and (< (abs (- Family 3.0)) 0.5) (< SHM234_GapT (R RevGraceTime)))))
  ; V2.35: with no input dhat is zero (acos 90 deg) = a 'new intent' that ended the episode in the gap; only a real input is a new intent there
  (bind rdNewIntent (and (or HasIntent (not gapKeep)) (> (acosd (clamp (dot dhat RedirectDirLatched) -1.0 1.0)) (R RedirectNewIntentAngle))))
  ; alignment needs real speed: the velocity direction of a near-stopped body is noise (ended episodes mid-pivot)
  (bind rdAligned (and (> Speed 80.0) (< (acosd (clamp (dot vhat RedirectDirLatched) -1.0 1.0)) (R RedirectAlignAngle))))
  ; V2.35 release gap: inside a reversal (family 3) a release shorter than RevGraceTime does not end the episode - the authored clip keeps
  ; playing (search throttle + clip-bound capsule stay on); ending it here let MM jump to a full-speed bin's frame 0 and the re-press
  ; blended two clip speed curves (capsule 64 -> 198 cm/s, j30_rel_3200 46.5 cm)
  (bind rdLost (or (not Grounded) (or Blocked (and (not HasIntent) (not gapKeep)))))
  (bind rdEnd (and RedirectActive (or rdLost (or (and rdAligned (> RedirectTime (R RedirectMinDwell))) (or (> RedirectTime (R RedirectMaxDwell)) rdNewIntent)))))
  (bind rdStart (and (R RedirectHoldEnabled) (and rdCand (or (not RedirectActive) rdEnd))))
  (set RedirectEnd (select rdEnd (select rdLost 4.0 (select rdNewIntent 3.0 (select rdAligned 1.0 2.0))) 0.0))
  (set RedirectDirLatched (vlerp RedirectDirLatched dhat (select rdStart 1.0 0.0)))
  (set RedirectSpeed0 (select rdStart Speed RedirectSpeed0))
  ; bridge class latched at the episode start: 0 none (walk / small), 1 lateral, 2 reversal; gait 0 jog, 1 sprint
  ; V2.24 frame-rate-stable classing: the speed BEFORE the first braked frame (decays at RedirectSpeedDecay cm/s2; 0 = plain Speed)
  (set SpeedOnset (select (> (R RedirectSpeedDecay) 0.5) (max Speed (- SpeedOnset (* (R RedirectSpeedDecay) dt))) Speed))
  (bind rdClassNow (select (and (R RedirectBridgeEnabled) (or (> SpeedOnset (R RedirectBridgeMinSpeed)) lowRev)) (select (> RedirectionAngle (R RedirectReversalClassAngle)) 2.0 1.0) 0.0))
  (set RedirectClass (select rdStart rdClassNow RedirectClass))
  (set RedirectGait (select rdStart (select (> SpeedOnset (R RedirectSprintSpeed)) 1.0 0.0) RedirectGait))
  (set RedirectSide (select rdStart SupportSide RedirectSide))
  (set RedirectPhase (select rdStart GaitPhase RedirectPhase))
  (set RedirectTime (select rdStart 0.0 (+ RedirectTime dt)))
  (set RedirectActive (or rdStart (and RedirectActive (not rdEnd))))
  ; a hard turn needs a real redirection angle: a straight acceleration also has a large |dV| (approach starts were classified hard turns)
  (bind hardCand (and (and Grounded HasIntent) (or (and (and (> RedirectionDemand (R RedirectHard)) (> RedirectionAngle (R RouteHardTurnAngle))) (> Speed (R RouteHardTurnMinSpeed))) (and (and (> Speed (R RouteHardTurnMinSpeed)) (> TurnAngle (R RouteHardTurnAngle))) (> (abs AngularMomentumZ) (R RouteHardTurnAngMom))))))
  (bind revCand (> ReversalDemand (R ExecReversal)))
  ; priority: blocked > reversal (the CP/pivot vocabulary already brakes, replants and recommits) > recovery > hard turn.
  ; RouteForceRecovery is a QA-only switch that exercises the recovery route whenever a step is feasible.
  (bind forced (and (R RouteForceRecovery) (and (and Grounded (not Blocked)) (and (and (not stepBlocked) (< Speed 60.0)) (and (not HasIntent) (> SpeedPeak 80.0))))))
  ; start transfer: movement onset from rest in a wide/staggered held stance -> the first step comes from the one-step
  ; vocabulary (support-compatible, planted feet), then normal locomotion; bounded by StartTransferMaxTime
  ; V1.3.9: onset from rest by the CURRENT speed (SpeedPeak stayed high for ~1.5 s after a stop, so a restart during the stop
  ; settle skipped the start vocabulary); StartTransferTime resets whenever the intent drops, so a held input cannot re-trigger
  (bind onsetRest (and (and HasIntent (< Speed 40.0)) (and Grounded (not Blocked))))
  (bind stanceOff (or (and (> StanceClass 0.5) (< StanceClass 2.5)) (> StartTransferTime 0.0)))
  ; V1.3.9: EVERY onset from rest routes the first step (quiet stance included): the quiet-stance, per-foot start vocabulary
  ; for walk / jog / sprint makes the first swing foot the unloaded one (stanceOff no longer required)
  ; once begun, the start keeps its family while the intent holds (the body leaves 'rest' within ~0.35 s, before the first
  ; swing of a jog / sprint start has landed); a NEW start still needs rest; bounded by StartTransferMaxTime (startCand)
  (set StartTransferTime (select (and (R StartTransferEnabled) (or onsetRest (and (> StartTransferTime 0.0) HasIntent))) (+ StartTransferTime dt) 0.0))
  (bind startCand (and (and (R MotionRoutingEnabled) (R StartTransferEnabled)) (and (> StartTransferTime 0.0) (< StartTransferTime (R StartTransferMaxTime)))))
  ; V1.3.4: a recovery episode ends only with trustworthy support (capture error and contact confidence), not on the minimum hold
  (bind isRecPrev (or (> Family 5.5) (and (> Family 0.5) (< Family 1.5))))
  (bind recStay (and (and isRecPrev Grounded) (and (< FamilyTime (R RecoveryMaxHold)) (or (> CaptureError (R RecoveryExitError)) (< (max ConfL ConfR) (R RecoveryExitContact))))))
  ; V2.34 release-repress: a re-press in the reversal's own direction within RevGraceTime continues the reversal (not a from-rest start)
  ; B10: the release gap itself keeps the reversal family for at most RevGraceTime (no input -> cand 0 would end the family before the re-press)
  (bind rgap (and (> (R RevGraceTime) 0.0) (and (not HasIntent) (and (< (abs (- Family 3.0)) 0.5) (< SHM234_GapT (R RevGraceTime))))))
  (bind rkeep (and (> (R RevGraceTime) 0.0) (and HasIntent (and (< SHM234_RevAgo (R RevGraceTime)) (> (+ (* (.x DesiredDir) (.x SHM234_RevDir)) (* (.y DesiredDir) (.y SHM234_RevDir))) (R RevGraceDot))))))
  (bind cand (select Blocked 5.0 (select (or revCand (or rkeep rgap)) 3.0 (select (and (R MotionRoutingEnabled) (or recCand (or forced recStay))) (select strong 6.0 1.0) (select startCand 4.0 (select (and (R MotionRoutingEnabled) hardCand) 2.0 0.0))))))
  (set FamilyTime (+ FamilyTime dt))
  (set FamilyCooldown (+ FamilyCooldown dt))
  (bind isRec (or (> Family 5.5) (and (> Family 0.5) (< Family 1.5))))
  (bind candRec (or (> cand 5.5) (and (> cand 0.5) (< cand 1.5))))
  ; V2.35: a REAL reversal request (revCand: intent against the travel at speed) takes over a hard-turn episode at once - the hard-turn
  ; minimum hold kept family 2 while the reversal clip was needed (60 FPS release-repress j30_rel_3200 51 cm); other holds stay
  (bind revOver (and (R RevOverHard) (and revCand (and (> cand 2.5) (and (< cand 3.5) (< (abs (- Family 2.0)) 0.5))))))
  (bind allowed (or revOver (or (or (> cand 4.5) (and (> cand 3.5) (< cand 4.5))) (or (< cand 0.5) (and (> FamilyTime (R RouteMinHold)) (or (not candRec) (> FamilyCooldown (R RouteCooldown))))))))
  (bind leaving (and (> Family 0.5) (< FamilyTime (R RouteMinHold))))
  (bind switch (and (> (abs (- cand Family)) 0.5) (and allowed (not (and leaving (< cand 0.5))))))
  ; the switch decision is latched once (a bind re-evaluates at every consumer, and the Family / FamilyTime writes change it)
  (set RouteSwitch switch)
  (set FamilyCooldown (select (and RouteSwitch isRec) 0.0 FamilyCooldown))
  ; V1.3.9 P8: Family is written BEFORE FamilyTime resets - cand is a bind re-evaluated here, and with FamilyTime already 0
  ; recStay (FamilyTime < RecoveryMaxHold, running capture error ~0.9 every step) re-selected recovery on every exit:
  ; a shove while jogging with the input held stayed in family 6 for 4.5 s, re-latching every 0.43 s
  (set Family (select RouteSwitch cand Family))
  (set FamilyTime (select RouteSwitch 0.0 FamilyTime))
  (set SHM234_RevAgo (select (< (abs (- Family 3.0)) 0.5) 0.0 (+ SHM234_RevAgo dt)))   ; V2.34 release-repress memory
  (set SHM234_GapT (select HasIntent 0.0 (+ SHM234_GapT dt)))
  (set SHM234_RevDir (selv (and HasIntent (< (abs (- Family 3.0)) 0.5)) DesiredDir SHM234_RevDir))
  ; compact recovery vector (facing frame: x forward, y right) for selection and telemetry
  (bind fwd2 (Matematik|Vektör|Normalize2D(Vector) :A (vec (.x Facing) (.y Facing) 0.0) :Tolerance 0.0001))
  (bind rt2 (vec (- 0.0 (.y fwd2)) (.x fwd2) 0.0))
  (bind rel (- FootTarget SupportCenter))
  (set RecoveryDirLocal (vec (dot rel fwd2) (dot rel rt2) 0.0))
  (set RecoveryDistance (vlenxy rel))
  (set RecoverySide SwingSide)
  (set RecoveryUrgency StepUrgency)
  ; stance class for the next start/turn: 0 neutral, 1 wide, 2 staggered, 3 recovery stance
  (bind fd (- FootCenterR FootCenterL))
  (bind width (abs (dot fd rt2))) (bind stag (abs (dot fd fwd2)))
  (set StanceClass (select isRec 3.0 (select (> stag (R StanceStaggerDepth)) 2.0 (select (> width (R StanceWideWidth)) 1.0 0.0))))
  ; the family the ABP may route to a database: recovery only when RouteRecoveryToDatabase (off until PIE selection is verified)
  (bind famRec (or (or (and (> Family 0.5) (< Family 1.5)) (> Family 5.5)) (and (> Family 3.5) (< Family 4.5))))
  ; the hard-turn route overrides AAMS's own pivot selection; it is classification-only until validated (flag default off)
  (bind famHard (and (> Family 1.5) (< Family 2.5)))
  (set FamilyRoute (select (or (and famRec (not (R RouteRecoveryToDatabase))) (and famHard (not (R RouteHardTurnToDatabase)))) 0.0 Family))
  (set PMI_Type (select Blocked 9.0 PMI_Type)))
""")

# QA-only deterministic shove: called from SHM_Tick behind a branch (QAPerturbEnabled and TelemetryEnabled and not done and
# game time > QAPerturbTime). LaunchCharacter adds velocity in the actor frame (x forward, y right).
fn('SHM_QAPerturb', [], [], r"""
(fn SHM_QAPerturb ()
  (bind fwd2 (Matematik|Vektör|Normalize2D(Vector) :A (vec (.x Facing) (.y Facing) 0.0) :Tolerance 0.0001))
  (bind rt2 (vec (- 0.0 (.y fwd2)) (.x fwd2) 0.0))
  ; a velocity change on the movement component keeps the character walking (LaunchCharacter would switch it to falling)
  (bind first (not QAPerturbDone))
  (Piyon|Bileşenler|CharacterMovement|AddImpulse :self MoveComp :Impulse (+ (vscale fwd2 (select first (R QAPerturbX) (R QAPerturbX2))) (vscale rt2 (select first (R QAPerturbY) (R QAPerturbY2)))) :bVelocityChange true)
  (set QAPerturbDone2 (not first))
  (set QAPerturbDone true))
""")

LAP = r'''
(fn {name} ()
  (bind (s p) (İşlevsellikler|Zaman|GetAccurateRealTime))
  (bind d (- p {ref}))
  (set {var} (* (select (< d 0.0) (+ d 1.0) d) 1000.0))
  (set PerfLap p))
'''
fn('SHM_PerfLapState', [], [], LAP.format(name='SHM_PerfLapState', ref='PerfT0', var='CostState'))
fn('SHM_PerfLapPlanner', [], [], LAP.format(name='SHM_PerfLapPlanner', ref='PerfLap', var='CostPlanner'))
fn('SHM_PerfLapEnv', [], [], LAP.format(name='SHM_PerfLapEnv', ref='PerfLap', var='CostEnv'))
fn('SHM_PerfLapCam', [], [], LAP.format(name='SHM_PerfLapCam', ref='PerfLap', var='CostCam'))

# ---------------------------------------------------------------- Phase E: airborne + landing
# impact speed = lowest vertical velocity seen in the air (CMC zeroes vz on landing); impulse proxy J = M * dv.
fn('SHM_UpdateAir', [('dt', 'float')], [], r'''
(fn SHM_UpdateAir (dt)
  (bind air (not Grounded))
  (bind takeoff (and air WasGrounded))
  (bind landing (and Grounded (not WasGrounded)))
  (set TakeoffVelocity (selv takeoff Velocity TakeoffVelocity))
  (set TakeoffFootZ (select takeoff FootZ (select air TakeoffFootZ FootZ)))
  (set AirTime (select air (select takeoff 0.0 (+ AirTime dt)) 0.0))
  (bind mvz (select air (min MinVerticalSpeed VerticalSpeed) MinVerticalSpeed))
  (bind impact (max (- mvz) 0.0))
  (bind sevRaw (clamp (/ (- impact (R LandingSoftSpeed)) (max (- (R LandingHardSpeed) (R LandingSoftSpeed)) 1.0)) 0.0 1.0))
  (bind hz (clamp (/ Speed 600.0) 0.0 1.0))
  (bind sev (clamp (+ sevRaw (* hz sevRaw 0.25)) 0.0 1.0))
  (set LandingSeverity (select landing sev LandingSeverity))
  (set LandingImpulse (select landing (* (A BodyMassKg) (/ impact 100.0)) LandingImpulse))
  (bind rt (select landing (lerp (R LandingRecoverMin) (R LandingRecoverMax) sev) LandingRecoverTime))
  (set LandingRecoverTime rt)
  (set LandingTimer (select landing rt (max (- LandingTimer dt) 0.0)))
  (set LandingResponse (* LandingSeverity (/ LandingTimer (max LandingRecoverTime 0.01))))
  (set MinVerticalSpeed (select air mvz 0.0))
  (bind ah (select air (- FootZ TakeoffFootZ) 0.0))
  (set AirHeight ah)
  (set ApexHeight (select air (max ApexHeight ah) (select landing ApexHeight 0.0)))
  (set AirborneState (select air (select (> VerticalSpeed 0.0) 1.0 2.0) 0.0))
  (set WasGrounded Grounded))
''')

# ---------------------------------------------------------------- Phase F: adaptive camera-space environment perception
# 4 sphere probes from the upper body in CAMERA yaw space, two per frame (A: left/right, B: up/rear).
# Clearance filtered asymmetrically: shrinks fast (safety), grows slowly (hysteresis against one clear frame).
ENV_COMMON = r'''
  (bind pcm (Oyun|GetPlayerCameraManager :PlayerIndex 0))
  (bind (cr cpt cy) (Matematik|Döndürücü|BreakRotator :InRot (Kamera|GetCameraRotation :self pcm)))
  (bind yawRot (Matematik|Döndürücü|MakeRotator :Roll 0.0 :Pitch 0.0 :Yaw cy))
  (bind org (+ Position (vec 0.0 0.0 50.0)))
  (bind rad (R EnvProbeRadius))
  (bind aS (- 1.0 (exp (/ (- dt) (R EnvShrinkTau)))))
  (bind aG (- 1.0 (exp (/ (- dt) (R EnvGrowTau)))))
'''
fn('SHM_UpdateEnvA', [('dt', 'float')], [], r'''
(fn SHM_UpdateEnvA (dt)''' + ENV_COMMON + r'''
  (bind right (Matematik|Vektör|GetRightVector :InRot yawRot))
  (bind lenS (R EnvSideLength))
  (bind (xL hitL okL) (Çarpışma|SphereTraceByChannel :Start org :End (- org (vscale right lenS)) :Radius rad :TraceChannel "TraceTypeQuery2" :bTraceComplex false :bIgnoreSelf true))
  (bind (bhL ioL tmL dL) (Çarpışma|BreakHitResult :Hit hitL))
  (bind cL (select okL (+ dL rad) lenS))
  (set EnvLeft (+ EnvLeft (* (- cL EnvLeft) (select (< cL EnvLeft) aS aG))))
  (bind (xR hitR okR) (Çarpışma|SphereTraceByChannel :Start org :End (+ org (vscale right lenS)) :Radius rad :TraceChannel "TraceTypeQuery2" :bTraceComplex false :bIgnoreSelf true))
  (bind (bhR ioR tmR dR) (Çarpışma|BreakHitResult :Hit hitR))
  (bind cR (select okR (+ dR rad) lenS))
  (set EnvRight (+ EnvRight (* (- cR EnvRight) (select (< cR EnvRight) aS aG)))))
''')
fn('SHM_UpdateEnvB', [('dt', 'float')], [], r'''
(fn SHM_UpdateEnvB (dt)''' + ENV_COMMON + r'''
  (bind fwd (Matematik|Vektör|GetForwardVector :InRot yawRot))
  (bind lenU (R EnvUpLength)) (bind lenB (R EnvRearLength))
  (bind (xU hitU okU) (Çarpışma|SphereTraceByChannel :Start org :End (+ org (vec 0.0 0.0 lenU)) :Radius rad :TraceChannel "TraceTypeQuery2" :bTraceComplex false :bIgnoreSelf true))
  (bind (bhU ioU tmU dU) (Çarpışma|BreakHitResult :Hit hitU))
  (bind cU (select okU (+ dU rad) lenU))
  (set EnvUp (+ EnvUp (* (- cU EnvUp) (select (< cU EnvUp) aS aG))))
  (bind (xB0 hitB okB) (Çarpışma|SphereTraceByChannel :Start org :End (- org (vscale fwd lenB)) :Radius rad :TraceChannel "TraceTypeQuery2" :bTraceComplex false :bIgnoreSelf true))
  (bind (bhB ioB tmB dB) (Çarpışma|BreakHitResult :Hit hitB))
  (bind cB (select okB (+ dB rad) lenB))
  (set EnvRear (+ EnvRear (* (- cB EnvRear) (select (< cB EnvRear) aS aG)))))
''')
fn('SHM_UpdateEnvDerived', [('dt', 'float')], [], r'''
(fn SHM_UpdateEnvDerived (dt)
  (bind width (+ EnvLeft EnvRight))
  (set CorridorWidth width)
  (bind rawW (clamp (/ (- (R OpenWidth) width) (max (- (R OpenWidth) (R NarrowWidth)) 1.0)) 0.0 1.0))
  (bind rawU (* (clamp (/ (- 200.0 EnvUp) 80.0) 0.0 1.0) 0.5))
  (bind rawB (* (clamp (/ (- 250.0 EnvRear) 170.0) 0.0 1.0) 0.6))
  (bind raw (max rawW (max rawU rawB)))
  (bind aIn (- 1.0 (exp (/ (- dt) (* (R EnvShrinkTau) 2.0)))))
  (bind aOut (- 1.0 (exp (/ (- dt) (R ConstrainTau)))))
  (set ConstrainedLevel (+ ConstrainedLevel (* (- raw ConstrainedLevel) (select (> raw ConstrainedLevel) aIn aOut))))
  (set Constrained (selb Constrained (> ConstrainedLevel (R ConstrainExit)) (> ConstrainedLevel (R ConstrainEnter))))
  (set OpenSpaceConfidence (* (clamp (/ (- (min EnvLeft (min EnvRight EnvRear)) 150.0) 130.0) 0.0 1.0) (- 1.0 ConstrainedLevel)))
  (set CamBoomScale (- (+ 1.0 (* (R CamOpenBoomBonus) OpenSpaceConfidence)) (* (R CamNarrowBoomReduction) ConstrainedLevel)))
  (set CamShoulderScale (lerp 1.0 (R CamNarrowShoulderScale) ConstrainedLevel))
  (set EnvPhase (- 1 EnvPhase)))
''')

# ---------------------------------------------------------------- Phase G: camera <- body physical coupling
# critically damped spring per axis: x'' = w^2 (target - x) - 2 w x'   (semi-implicit Euler, dt clamped)
fn('SHM_UpdateCameraSignals', [('dt', 'float')], [], r'''
(fn SHM_UpdateCameraSignals (dt)
  (bind w (R CamSignalFreq))
  (bind h (min dt 0.05))
  (bind tL (* LandingResponse (R CamLandingDip) -1.0))
  (set CamLandingVel (+ CamLandingVel (* (- (* w w (- tL CamLandingOffset)) (* w CamLandingVel 2.0)) h)))
  (set CamLandingOffset (+ CamLandingOffset (* CamLandingVel h)))
  (set CamBrakeDir (selv (> Speed 20.0) (Matematik|Vektör|Normalize2D(Vector) :A PlanarVelocity :Tolerance 0.0001) CamBrakeDir))
  (bind tB (* BrakingDemand (R CamBrakeCarry) (select Grounded 1.0 0.0)))
  (set CamBrakeVel (+ CamBrakeVel (* (- (* w w (- tB CamBrakeOffset)) (* w CamBrakeVel 2.0)) h)))
  (set CamBrakeOffset (+ CamBrakeOffset (* CamBrakeVel h)))
  ; ---- V1.3.4 grounded body-height target: the skeleton hangs below the capsule on stairs / slopes (foot placement pulls
  ; the hips down onto the treads); the camera pivot follows the pelvis height, critically damped at CamBodyFreq (slow
  ; enough to ignore gait bobbing), grounded only, bounded by CamBodyMax
  (bind bodyOn (and Grounded (R CamBodyFollowEnabled)))
  ; V1.3.5 body anchor = chest (spine_03) minus its rest height over the capsule; the pelvis anchor is kept as the fallback
  (bind chestZ (.z (bone "spine_03")))
  (set CamBodyDz (select (R CamAnchorChest) (- (- chestZ (.z Position)) (- (R CamChestRestOffset) (R CamBodyRestOffset))) (- (.z PelvisLocation) (.z Position))))
  ; in constrained space (enclosed stair, doorway) the pivot must not follow the hips down: the collision needs height
  ; V1.3.5: the anchor follow is NOT attenuated in constrained space (the camera must climb with the chest on the enclosed stair)
  (bind tZ (select bodyOn (clamp (- CamBodyDz (R CamBodyRestOffset)) (- 0.0 (R CamBodyMax)) (R CamBodyMax)) 0.0))
  (bind wb (R CamBodyFreq))
  (set CamBodyVel (+ CamBodyVel (* (- (* wb wb (- tZ CamBodyZ)) (* wb CamBodyVel 2.0)) h)))
  (set CamBodyZ (+ CamBodyZ (* CamBodyVel h)))
  ; ---- travel-relative shoulder: the over-the-shoulder side follows sustained lateral travel so mirrored diagonals
  ; compose mirrored (+1 = the profile's shoulder, -1 = the other shoulder), filtered at CamShoulderTau
  (bind rtv (vec (- 0.0 (.y Facing)) (.x Facing) 0.0))
  (bind vh (Matematik|Vektör|Normalize2D(Vector) :A PlanarVelocity :Tolerance 0.0001))
  (bind lat (select (and Grounded (> Speed 60.0)) (dot vh rtv) 0.0))
  (bind latN (clamp (/ (- (abs lat) (R CamShoulderLatDead)) (max (- (R CamShoulderLatFull) (R CamShoulderLatDead)) 0.01)) 0.0 1.0))
  (bind sideT (select (R CamShoulderTravelEnabled) (lerp 1.0 (select (< lat 0.0) -1.0 1.0) latN) 1.0))
  (set CamShoulderSide (+ CamShoulderSide (* (- sideT CamShoulderSide) (- 1.0 (exp (/ (- h) (max (R CamShoulderTau) 0.01)))))))
  ; ---- movement camera intensity (speed, acceleration, braking, redirection), blended, no hard gait switch
  (bind accAlong (dot Accel vh))
  (set LatAccel (select (and Grounded (> Speed 60.0)) (dot Accel rtv) 0.0))
  (bind iRaw (clamp (+ (+ (* 0.6 (/ Speed 490.0)) (* 0.2 (clamp (/ (abs accAlong) 800.0) 0.0 1.0))) (+ (* 0.1 BrakingDemand) (* 0.1 (clamp (/ RedirectionDemand 2.0) 0.0 1.0)))) 0.0 1.0))
  (set CamIntensity (+ CamIntensity (* (- (select Grounded iRaw 0.0) CamIntensity) (- 1.0 (exp (/ (- h) (max (R CamIntensityTau) 0.01)))))))
  ; ---- acceleration lag / braking catch-up along travel and a small lateral lag on redirection (springs)
  (bind tA (* (clamp (/ (- 0.0 accAlong) 800.0) -1.0 1.0) (R CamAccelCarry) (select Grounded 1.0 0.0)))
  (set CamAccelVel (+ CamAccelVel (* (- (* w w (- tA CamAccelOffset)) (* w CamAccelVel 2.0)) h)))
  (set CamAccelOffset (+ CamAccelOffset (* CamAccelVel h)))
  (bind dvLat (dot (- (vec (.x DesiredVelocity) (.y DesiredVelocity) 0.0) PlanarVelocity) rtv))
  (bind tT (* (clamp (/ (- 0.0 dvLat) 400.0) -1.0 1.0) (R CamTurnCarry) (select (and Grounded (> Speed 60.0)) 1.0 0.0)))
  (set CamTurnVel (+ CamTurnVel (* (- (* w w (- tT CamTurnOffset)) (* w CamTurnVel 2.0)) h)))
  (set CamTurnOffset (+ CamTurnOffset (* CamTurnVel h)))
  ; ---- V1.3.5 lateral escape: when the rear clearance is short, shift the pivot toward the side with more clearance (bounded,
  ; filtered) so the rig's own boom trace finds space beside the character instead of collapsing onto the head
  ; the trigger is the rig's REAL boom contraction (spring arm TargetArmLength against a slow-decay envelope of itself),
  ; not the horizontal rear sweep, which reads open along a stair flight while the boom collides with the treads
  (bind armC (Aktör|GetComponentByClass :self OwnerChar :ComponentClass "/Script/Engine.SpringArmComponent"))
  (bind armLen (Sınıf|SpringArmComponent|TargetArmLengthAl :self armC))
  (set CamArmRef (max armLen (* CamArmRef (- 1.0 (* 0.4 h)))))
  (set CamContraction (clamp (- 1.0 (/ armLen (max CamArmRef 1.0))) 0.0 1.0))
  (bind rearTight (max (clamp (/ (- 220.0 EnvRear) 150.0) 0.0 1.0) (clamp (/ (- CamContraction 0.25) 0.35) 0.0 1.0)))
  (bind sideBias (clamp (/ (- EnvRight EnvLeft) 80.0) -1.0 1.0))
  (bind tS (* (* (R CamSideShiftMax) sideBias) (* rearTight (select Grounded 1.0 0.0))))
  (set CamSideShift (+ CamSideShift (* (- tS CamSideShift) (- 1.0 (exp (/ (- h) (max (R CamSideShiftTau) 0.01)))))))
  ; ---- V1.3.5 openness: exterior breathes (longer boom via CamOpenBoomBonus, less shoulder, small FOV change), continuous
  ; openness keyed on overhead clearance (interior ceilings < 300 cm) and side / rear room: 0 indoors, 1 in the open
  (set CamOpenness (* (clamp (/ (- EnvUp 300.0) 250.0) 0.0 1.0) (clamp (/ (- (min EnvLeft (min EnvRight EnvRear)) 150.0) 150.0) 0.0 1.0)))
  (set CamFOVDelta (* CamOpenness (lerp (R CamOpenFOVDeltaWalk) (R CamOpenFOVDeltaSprint) (clamp (/ CamIntensity 0.6) 0.0 1.0))))
  ; ---- V1.3.6 exertion: physical-work rate above a walking reference (speed^2 term, acceleration, braking, redirection,
  ; climb, recovery episodes), first-order rise toward the work rate, slow fall at rest; bounded 0..1; no gameplay effect
  (bind spN (clamp (/ Speed (max (R ExertionSpeedRef) 1.0)) 0.0 2.0))
  (bind work (+ (+ (* spN spN) (* (R ExertionBrakeGain) BrakingDemand)) (+ (* (R ExertionRedirectGain) (clamp (/ RedirectionDemand 2.0) 0.0 1.0)) (+ (* (R ExertionClimbGain) (max VerticalSpeed 0.0)) (select (or (> Family 5.5) (and (> Family 0.5) (< Family 1.5))) (R ExertionRecoveryGain) 0.0)))))
  (set ExertionWork (select (R ExertionEnabled) (* work (select Grounded 1.0 0.5)) 0.0))
  (bind exTarget (clamp (* 0.5 ExertionWork) 0.0 1.0))
  (set Exertion (clamp (+ Exertion (* (- exTarget Exertion) (- 1.0 (exp (/ (- h) (max (select (> exTarget Exertion) (R ExertionRiseTau) (R ExertionFallTau)) 0.1)))))) 0.0 1.0))
  ; ---- V1.3.6 turn composition: during a turn the pivot lags toward the OUTSIDE of the turn (opposite to the yaw-rate
  ; direction) so the body moves inward through the frame first and the camera converges after; bounded, filtered
  (bind turnComp (* (clamp (/ (* (- 0.0 YawRate) (clamp (/ Speed 300.0) 0.0 1.5)) 90.0) -1.0 1.0) (R CamTurnCompGain)))
  (set CamTurnComp (+ CamTurnComp (* (- (select (and Grounded (> Speed 100.0)) turnComp 0.0) CamTurnComp) (- 1.0 (exp (/ (- h) (max (R CamTurnCompTau) 0.01)))))))
  ; ---- pivot offset: brake + accel (along travel) + turn (lateral) + side escape + landing + body height + (bounded) rise
  (set CamOffset (+ (+ (vscale CamBrakeDir (+ CamBrakeOffset CamAccelOffset)) (vscale rtv (+ (+ CamTurnOffset CamSideShift) CamTurnComp))) (vec 0.0 0.0 (+ (+ CamLandingOffset CamBodyZ) (* (R CamConstrainedRise) ConstrainedLevel)))))
  (set CamAirFollowWeight (clamp (/ AirHeight (max (R CamAirWeightHeight) 1.0)) 0.0 1.0))
  ; ---- landing phase model: 0 grounded, 1 ascend, 2 apex, 3 descend, 4 contact, 5 landing recovery
  (bind vz VerticalSpeed)
  (bind landing (and Grounded (not CamPrevGrounded)))
  (bind airPhase (select (> vz (R CamApexSpeed)) 1.0 (select (< vz (- 0.0 (R CamApexSpeed))) 3.0 2.0)))
  (set CamPhase (select Grounded (select landing 4.0 (select (> LandingTimer 0.0) 5.0 0.0)) airPhase))
  ; recovery weight: reset to 1 at contact, then critically damped toward 0 with omega = CamRecoverFreq / recover time
  (bind wr (/ (R CamRecoverFreq) (max LandingRecoverTime 0.05)))
  (set CamRecoverWeight (select landing 1.0 CamRecoverWeight))
  (set CamRecoverVel (select landing 0.0 CamRecoverVel))
  (set CamRecoverVel (+ CamRecoverVel (* (- (* wr wr (- 0.0 CamRecoverWeight)) (* wr CamRecoverVel 2.0)) h)))
  (set CamRecoverWeight (clamp (+ CamRecoverWeight (* CamRecoverVel h)) 0.0 1.0))
  ; consumers: land response target (boost scaled by severity, weighted by recovery) and the phase-aware air lag
  (set CamLandResponse (* (R CamLandingResponseBoost) (+ 0.5 (* 0.5 LandingSeverity)) CamRecoverWeight))
  ; landing preparation = a committed descent (below -CamDescendSpeed), so the apex arc keeps the V1 apex framing
  (bind descend (< vz (- 0.0 (R CamDescendSpeed))))
  (set CamAirLagTarget (select descend (R CamAirDescendLag) (R CamAirMaxHeightLag)))
  (set CamFollowTarget (select descend (R CamAirDescendFollow) (R CamAirFollow)))
  (set CamResponseTarget (select descend (R CamAirDescendResponse) (R CamAirHeightResponse)))
  ; descend keeps its own full weight until contact (the air-height weight fades out exactly when the camera must arrive)
  (set CamLagWeight (select descend 1.0 CamAirFollowWeight))
  ; last: pure bindings re-evaluate per consumer, so the edge memory is written after every use of `landing`
  ; boom: the env-derived scale carries the narrow reduction; the open bonus is re-applied here on the overhead-keyed openness
  (set CamBoomScale (* (- CamBoomScale (* (R CamOpenBoomBonus) OpenSpaceConfidence)) (+ (+ 1.0 (* (R CamOpenBoomBonus) CamOpenness)) (* (R CamIntensityBoom) (+ CamIntensity (* 0.3 Exertion))))))
  (set CamShoulderScale (* (* CamShoulderScale CamShoulderSide) (lerp 1.0 (R CamOpenShoulderScale) CamOpenness)))
  (set CamPrevGrounded Grounded))
''')

# ---------------------------------------------------------------- diagnostics
fn('SHM_Debug', [], [], r'''
(fn SHM_Debug ()
  (İşleme|HataAyıklama|DrawDebugSphere :Center Com :Radius 5.0 :Segments 8 :LineColor "(R=1,G=0.75,B=0,A=1)" :Duration 0.0 :Thickness 1.0)
  (İşleme|HataAyıklama|DrawDebugSphere :Center ProjectedCom :Radius 4.0 :Segments 8 :LineColor "(R=1,G=1,B=0,A=1)" :Duration 0.0 :Thickness 1.0)
  (İşleme|HataAyıklama|DrawDebugSphere :Center CapturePoint :Radius 5.0 :Segments 8 :LineColor "(R=1,G=0,B=0,A=1)" :Duration 0.0 :Thickness 2.0)
  (İşleme|HataAyıklama|DrawDebugLine :LineStart (+ SupportA (vec 0.0 0.0 FootZ)) :LineEnd (+ SupportB (vec 0.0 0.0 FootZ)) :LineColor "(R=0,G=1,B=0,A=1)" :Duration 0.0 :Thickness 3.0)
  (İşleme|HataAyıklama|DrawDebugSphere :Center SupportCenter :Radius (A FootHalfLength) :Segments 10 :LineColor "(R=0,G=1,B=0,A=1)" :Duration 0.0 :Thickness 1.0)
  (İşleme|HataAyıklama|DrawDebugSphere :Center FootTarget :Radius (* FootTargetWeight 10.0) :Segments 8 :LineColor "(R=0,G=1,B=1,A=1)" :Duration 0.0 :Thickness 1.0)
  (İşleme|HataAyıklama|DrawDebugLine :LineStart ProjectedCom :LineEnd (+ ProjectedCom (vscale PlanarVelocity 0.3)) :LineColor "(R=1,G=1,B=1,A=1)" :Duration 0.0 :Thickness 2.0)
  (İşleme|HataAyıklama|DrawDebugLine :LineStart ProjectedCom :LineEnd (+ ProjectedCom (vscale DesiredVelocity 0.3)) :LineColor "(R=0,G=0.4,B=1,A=1)" :Duration 0.0 :Thickness 2.0)
  (İşleme|HataAyıklama|DrawDebugLine :LineStart SupportCenter :LineEnd FootTarget :LineColor "(R=0,G=1,B=1,A=1)" :Duration 0.0 :Thickness 2.0)
  (İşleme|HataAyıklama|DrawDebugSphere :Center FootCenterL :Radius (+ 2.0 (* ConfL 6.0)) :Segments 6 :LineColor "(R=1,G=0.3,B=0.3,A=1)" :Duration 0.0 :Thickness 1.0)
  (İşleme|HataAyıklama|DrawDebugSphere :Center FootCenterR :Radius (+ 2.0 (* ConfR 6.0)) :Segments 6 :LineColor "(R=0.3,G=0.3,B=1,A=1)" :Duration 0.0 :Thickness 1.0)
  (İşleme|HataAyıklama|DrawDebugString :TextLocation (+ Position (vec 0.0 0.0 110.0)) :Text (str "exec " (fs ExecState) " urg " (fs StepUrgency) " plant " (fs FootPlantStrength) " rec " (fs RecoveryDemand)) :TextColor "(R=1,G=1,B=1,A=1)" :Duration 0.0))
''')

fn('SHM_PerfBegin', [], [], r'''
(fn SHM_PerfBegin ()
  (bind (s p) (İşlevsellikler|Zaman|GetAccurateRealTime))
  (set PerfT0 p)
  (set TickCount (+ TickCount 1)))
''')
fn('SHM_PerfEnd', [('dt', 'float')], [], r'''
(fn SHM_PerfEnd (dt)
  (bind (s p) (İşlevsellikler|Zaman|GetAccurateRealTime))
  (bind d (- p PerfT0))
  (bind ms (* (select (< d 0.0) (+ d 1.0) d) 1000.0))
  (set CostMs ms)
  (set CostAvgMs (+ CostAvgMs (* (- CostMs CostAvgMs) 0.02)))
  (set CostMaxMs (max (* CostMaxMs 0.999) CostMs))
  (set TelemetryTimer (+ TelemetryTimer dt)))
''')

fn('SHM_Telemetry', [], [], r'''
(fn SHM_Telemetry ()
  (set TelemetryTimer 0.0)
  (set TelemetryLine   ; V2.33: no PrintString - qa_pie copies this line into the SHM side file (Output Log growth owner)
    (str "SHM|" TelemetryLabel "|gt=" (fs (İşlevsellikler|Zaman|GetGameTimeinSeconds))
         "|spd=" (fs Speed) "|acc=" (fs (vlenxy Accel)) "|yawr=" (fs YawRate) "|gr=" (bs Grounded)
         "|turn=" (fs TurnAngle) "|tsev=" (fs TurnSeverity) "|brk=" (fs BrakingDemand) "|rev=" (fs ReversalDemand)
         "|trac=" (fs TractionDemand) "|rec=" (fs RecoveryDemand) "|ptb=" (fs PerturbState) "|sup=" (fs SupportSide) "|cl=" (fs ConfL) "|cr=" (fs ConfR)
         "|ds=" (fs DoubleSupport) "|stab=" (fs StabilityMarginCm) "|cperr=" (fs CaptureError) "|cpm=" (fs CaptureMarginCm)
         "|comh=" (fs ComHeight) "|com=" (vs Com) "|cp=" (vs CapturePoint) "|ft=" (vs FootTarget) "|ftw=" (fs FootTargetWeight)
         "|fps=" (fs FootPlantStrength) "|air=" (fs AirHeight) "|land=" (fs LandingSeverity) "|lresp=" (fs LandingResponse)
         "|envL=" (fs EnvLeft) "|envR=" (fs EnvRight) "|envU=" (fs EnvUp) "|envB=" (fs EnvRear) "|width=" (fs CorridorWidth)
         "|con=" (fs ConstrainedLevel) "|open=" (fs OpenSpaceConfidence) "|boom=" (fs CamBoomScale) "|shoulder=" (fs CamShoulderScale)
         "|camoff=" (vs CamOffset) "|lata=" (fs LatAccel) "|exr=" (fs Exertion) "|exw=" (fs ExertionWork) "|ctc=" (fs CamTurnComp) "|ccon=" (fs CamContraction) "|copen=" (fs CamOpenness) "|cfov=" (fs CamFOVDelta) "|cside=" (fs CamSideShift) "|cbz=" (fs CamBodyZ) "|cdz=" (fs CamBodyDz) "|cside=" (fs CamShoulderSide) "|cint=" (fs CamIntensity) "|cacc=" (fs CamAccelOffset) "|cturn=" (fs CamTurnOffset) "|airw=" (fs CamAirFollowWeight) "|cost=" (fs CostMs) "|costavg=" (fs CostAvgMs)
         "|exec=" (fs ExecState) "|urg=" (fs StepUrgency) "|recommit=" (fs RecommitDemand) "|ftc=" (fs FootTargetConfidence)
         "|gv=" (bs GroundValid) "|lsup=" (bs LandingSupportActive) "|post=" (bs PostStopActive) "|stag=" (fs Stagger) "|hold=" (bs HoldStops) "|bpk=" (fs BrakePeak) "|setoff=" (fs SettleOffset) "|setapp=" (fs SettleApplied) "|swing=" (fs SwingSide)
         "|rdc=" (fs RedirectClass) "|rdg=" (fs RedirectGait) "|rda=" (bs RedirectActive) "|rdt=" (fs RedirectTime) "|rdz=" (fs RedirectEnd) "|fcl=" (vs FootCenterL) "|fcr=" (vs FootCenterR) "|fam=" (fs Family) "|rdem=" (fs RedirectionDemand) "|rang=" (fs RedirectionAngle) "|dv=" (fs DeltaVMag) "|tcls=" (fs TurnClass) "|blk=" (bs Blocked) "|rdir=" (vs RecoveryDirLocal) "|rdist=" (fs RecoveryDistance) "|rside=" (fs RecoverySide) "|rurg=" (fs RecoveryUrgency) "|stcls=" (fs StanceClass) "|gait=" (fs GaitPhase) "|ldl=" (fs SupportLoadL) "|ldr=" (fs SupportLoadR) "|cop=" (vs CoP) "|Lz=" (fs AngularMomentumZ) "|Jb=" (fs BrakeImpulse) "|apa=" (bs ApaActive) "|cyc=" (fs GaitCycleTime) "|pmi=" (fs PMI_Type) "|pmid=" (fs PMI_Direction) "|pmiu=" (fs PMI_Urgency) "|pmic=" (fs PMI_Cost) "|cph=" (fs CamPhase) "|crw=" (fs CamRecoverWeight) "|stance=" (fs StanceError) "|ihold=" (bs IdleHold) "|setact=" (bs SettleActive) "|v2ll=" (fs LeanLat) "|v2lf=" (fs LeanFwd) "|v2po=" (vs PelvisOffset) "|v2cl=" (fs CurveLeanDeg) "|v2lm=" (fs CurveLeanMeasDeg) "|v2bd=" (fs BrakeDrop) "|v2sw=" (bs SwitchWindow) "|v2rp=" (fs RedirectPlants) "|v2apa=" (fs ApaFrac) "|cS=" (fs CostState) "|cP=" (fs CostPlanner) "|cE=" (fs CostEnv) "|cC=" (fs CostCam))))
''')

# ---------------------------------------------------------------- V2.0 (2026-10-14): body targets + phase gates
# Research-backed targets (Saved/Codex/SHME_V2_20261014/RESEARCH_LESSONS.md), each behind its own consumer flag so an A/B
# changes exactly one thing. Everything is smoothed HERE with critically damped springs (x'' = w^2 (t - x) - 2 w x', semi-
# implicit Euler, dt <= 0.05) and the ABP only adds the values to the existing PBI targets / pelvis translation:
#   LeanLat (deg, + = lean toward the character's right)    <- curve lean atan(v * yaw_rate / g) into the turn (A7), APA trunk
#   LeanFwd (deg, + = forward)                                <- braking posture (A4/A15), APA trunk toward the intent (A1)
#   PelvisOffset (cm, character frame x fwd / y right / z up) <- curve inward shift (A7), support-loaded lateral shift (A3),
#                                                               APA pelvis (A1), brake drop (A4), landing absorption (A10)
#   PelvisOffsetComp = the same vector in the mesh component frame of the -90 deg mannequin mount (+X = character left,
#                      +Y = character forward, +Z = up), the convention of PBI_PelvisTranslation
#   SwitchWindow / PlantEdge / RedirectPlants <- foot-phase gates for Update_MotionMatching (Bollo foot-phase matching, A5)
# Yaw-rate sign: UE yaw increases clockwise seen from above (a RIGHT turn), so a positive yaw rate leans / shifts right (+).
fn('SHM_UpdateBodyTargets', [('dt', 'float')], [], r"""
(fn SHM_UpdateBodyTargets (dt)
  (bind h (min dt 0.05))
  (bind moving (and Grounded (> Speed (R CurveLeanMinSpeed))))
  ; ---- W3b curve lean: lateral acceleration v * omega (cm/s^2) against gravity -> lean angle into the turn
  (bind omega (* YawRate 0.0174533))
  (bind alat (* Speed omega))
  (bind leanRaw (Matematik|Trig|Atan2(Degrees) :Y alat :X (R Gravity)))
  ; round 2 (2026-10-14): closed-loop residual - the clips already lean 0.36 (sprint) / 0.11 (jog) of the reference and the
  ; open-loop add overshot (slope 1.47 / 1.84). Measured trunk lateral lean = chest (spine_03) over pelvis in the facing frame
  ; (includes the clip, the PBI and this very contribution -> the spring settles where measured ~ reference x gain)
  (bind fwdL (Matematik|Vektör|Normalize2D(Vector) :A (vec (.x Facing) (.y Facing) 0.0) :Tolerance 0.0001))
  (bind rtL (vec (- 0.0 (.y fwdL)) (.x fwdL) 0.0))
  (bind dch (- (bone "spine_03") (bone "pelvis")))
  (bind leanMeas (Matematik|Trig|Atan2(Degrees) :Y (dot dch rtL) :X (max (.z dch) 1.0)))
  (set CurveLeanMeasDeg leanMeas)
  ; V2.5 L2: low-pass the measured trunk lean (CurveLeanMeasTau, 0 = raw) - the closed loop answered the gait's step-to-step
  ; trunk sway with the lean spring's lag and pumped it; a turn lean is sustained, the gait sway averages out
  (bind aLM (select (> (R CurveLeanMeasTau) 0.001) (- 1.0 (exp (/ (- 0.0 h) (max (R CurveLeanMeasTau) 0.01)))) 1.0))
  (bind leanMeasF (+ CurveLeanMeasSlow (* (- leanMeas CurveLeanMeasSlow) aLM)))
  (bind leanSel (select (R CurveLeanClosedLoop) (* (R CurveLeanResidualGain) (- leanRaw leanMeasF)) leanRaw))
  (bind leanCurve (select (and (R CurveLeanDirectEnabled) moving) (clamp leanSel (- 0.0 (R CurveLeanMaxDeg)) (R CurveLeanMaxDeg)) 0.0))
  (set CurveLeanDeg leanCurve)
  ; the filter memory is written after its last read (DSL rule: memories last)
  (set CurveLeanMeasSlow leanMeasF)
  ; inward pelvis shift (cm, + right) scaled by the lateral acceleration, same side as the lean
  (bind inward (select (and (R CurveLeanDirectEnabled) moving) (* (R PelvisInwardCm) (clamp (/ alat (max (R PelvisInwardAccelRef) 1.0)) -1.0 1.0)) 0.0))
  ; ---- W3a visual APA: fraction of the anticipatory window (ApaTimer counts down from ApaDuration after an onset from rest)
  (bind apaF (select (R ApaBodyEnabled) (clamp (/ ApaTimer (max (R ApaDuration) 0.01)) 0.0 1.0) 0.0))
  (set ApaFrac apaF)
  (bind fwd2 (Matematik|Vektör|Normalize2D(Vector) :A (vec (.x Facing) (.y Facing) 0.0) :Tolerance 0.0001))
  (bind rt2 (vec (- 0.0 (.y fwd2)) (.x fwd2) 0.0))
  (bind dF (dot DesiredDir fwd2))
  (bind dR (dot DesiredDir rt2))
  ; pelvis toward the LOADED foot (the body settles over the stance leg before the swing leg lifts) and slightly back
  (bind apaRight (* (* apaF (R ApaPelvisCm)) (clamp (* (- SupportLoadR SupportLoadL) 2.0) -1.0 1.0)))
  (bind apaBack (* (* apaF (R ApaBackCm)) (- 0.0 dF)))
  (bind apaLeanF (* (* apaF (R ApaLeanDeg)) dF))
  (bind apaLeanR (* (* apaF (R ApaLeanDeg)) dR))
  ; ---- W3d support-loaded lateral shift while moving (the clips carry most of it; this adds a small loaded-side bias)
  (bind supShift (select (and (R SupportShiftEnabled) (and Grounded (> Speed (R SupportShiftMinSpeed)))) (* (R SupportShiftCm) (clamp (- SupportLoadR SupportLoadL) -1.0 1.0)) 0.0))
  ; ---- W3c braking posture: pelvis drop + forward lean by braking demand, gait-scaled (walk softer than sprint)
  (bind gaitS (select (< Gait 1.5) (R BrakeDropWalkScale) (select (< Gait 2.5) (R BrakeDropJogScale) 1.0)))
  ; round 3 (2026-10-14 04:30): BrakingDemand is a short pulse the body spring never follows (stop dip -0.5 cm in round 2);
  ; the posture must follow the STOP EVENT: deceleration envelope = speed lost since the recent peak (0 -> 1 as the body stops,
  ; only after a real bout: SpeedPeak > 100 cm/s, input released), held through the last step and released over
  ; BrakeRecoverSec of standing (StillTime, triple flexion -> upright, research A4/A15)
  (bind decel (clamp (/ (- SpeedPeak Speed) (max SpeedPeak 1.0)) 0.0 1.0))
  (bind bout (clamp (/ (- SpeedPeak 100.0) 150.0) 0.0 1.0))
  (bind recov (clamp (- 1.0 (/ StillTime (max (R BrakeRecoverSec) 0.05))) 0.0 1.0))
  (bind stopEnv (* (* decel bout) (select (not HasIntent) recov 0.0)))
  (bind brakeOn (and (R BrakePostureEnabled) Grounded))
  (bind drop (select brakeOn (* (* (R BrakeDropCm) gaitS) (max stopEnv (clamp BrakingDemand 0.0 1.0))) 0.0))
  (bind brakeLean (select brakeOn (* (R BrakeLeanDeg) (max stopEnv (clamp BrakingDemand 0.0 1.0))) 0.0))
  (set BrakeDrop drop)
  ; ---- W3g landing absorption: drop by the landing response (severity x remaining recovery window)
  (bind landDrop (select (and (R LandingAbsorbEnabled) Grounded) (* (R LandingDropCm) (clamp LandingResponse 0.0 1.0)) 0.0))
  ; ---- V2.21 motion-end settle: one forward-then-small-back trunk pulse + knee give after a real bout comes to rest
  (bind stillNow (and Grounded (and (not HasIntent) (< Speed 10.0))))
  (bind settleStart (and (and (R SettleBodyEnabled) stillNow) (and (and (not SettleWas) (> SpeedPeak (R SettleBodyMinSpeed))) (> MoveDist 60.0))))
  (bind sAmp0 (select settleStart (clamp (/ SpeedPeak 300.0) 0.3 1.0) SettleAmp))
  (bind sAmp1 (select HasIntent (* sAmp0 (exp (/ (- 0.0 h) 0.08))) sAmp0))
  (bind sT (select settleStart 0.0 (+ SettleT dt)))
  (bind sShape (select (< sT 1.4) (* (exp (/ (- 0.0 sT) (max (R SettleBodyTau) 0.05))) (Matematik|Trig|Cos(Degrees) :A (* 360.0 (/ sT (max (R SettleBodyPeriod) 0.1))))) 0.0))
  (bind settleLean (select (R SettleBodyEnabled) (* (* (R SettleBodyDeg) sAmp1) sShape) 0.0))
  (bind settleDip (select (R SettleBodyEnabled) (* (* (R SettleBodyDipCm) sAmp1) (max sShape 0.0)) 0.0))
  (set SettleLean settleLean)
  ; ---- V2.21 terrain body: slope ahead / cross slope / step-down from 3 line traces on the real collision
  (bind terrOn (and (R TerrainBodyEnabled) Grounded))
  (bind tdir (selv (> Speed 30.0) (Matematik|Vektör|Normalize2D(Vector) :A PlanarVelocity :Tolerance 0.0001) fwd2))
  (bind trt (vec (- 0.0 (.y tdir)) (.x tdir) 0.0))
  (bind dA (clamp (* Speed (R TerrainAheadTime)) 35.0 140.0))
  (bind baseZ (- (.z Position) 86.0))
  (bind pA (+ Position (vscale tdir dA)))
  (bind pR (+ Position (vscale trt 30.0)))
  (bind (tx0 th0 tok0) (Çarpışma|LineTraceByChannel :Start (vec (.x Position) (.y Position) (+ baseZ 60.0)) :End (vec (.x Position) (.y Position) (- baseZ 120.0)) :TraceChannel "TraceTypeQuery1" :bTraceComplex false :bIgnoreSelf true))
  (bind (tbh0 tio0 ttm0 tdd0 tloc0 tip0 tnrm0) (Çarpışma|BreakHitResult :Hit th0))
  (bind (txA thA tokA) (Çarpışma|LineTraceByChannel :Start (vec (.x pA) (.y pA) (+ baseZ 60.0)) :End (vec (.x pA) (.y pA) (- baseZ 120.0)) :TraceChannel "TraceTypeQuery1" :bTraceComplex false :bIgnoreSelf true))
  (bind (tbhA tioA ttmA tddA tlocA tipA tnrmA) (Çarpışma|BreakHitResult :Hit thA))
  (bind (txR thR tokR) (Çarpışma|LineTraceByChannel :Start (vec (.x pR) (.y pR) (+ baseZ 60.0)) :End (vec (.x pR) (.y pR) (- baseZ 120.0)) :TraceChannel "TraceTypeQuery1" :bTraceComplex false :bIgnoreSelf true))
  (bind (tbhR tioR ttmR tddR tlocR tipR tnrmR) (Çarpışma|BreakHitResult :Hit thR))
  (bind g0 (select tok0 (.z tip0) baseZ))
  (bind gA (select tokA (.z tipA) g0))
  (bind gR (select tokR (.z tipR) g0))
  (bind slRaw (Matematik|Trig|Atan2(Degrees) :Y (clamp (- gA g0) -60.0 60.0) :X dA))
  (bind xsRaw (Matematik|Trig|Atan2(Degrees) :Y (clamp (- gR g0) -25.0 25.0) :X 30.0))
  (bind aT (- 1.0 (exp (/ (- 0.0 h) (max (R TerrainSlopeTau) 0.02)))))
  (bind slope (select terrOn (+ TerrainSlope (* (- slRaw TerrainSlope) aT)) (* TerrainSlope (- 1.0 aT))))
  (bind cross (select terrOn (+ TerrainCross (* (- xsRaw TerrainCross) aT)) (* TerrainCross (- 1.0 aT))))
  (bind upL (* (R TerrainLeanUpGain) (max slope 0.0)))
  (bind dnL (* (R TerrainLeanDownGain) (min slope 0.0)))
  ; the slope lean belongs to TRAVEL (fades in over 20..80 cm/s): standing on split heights the ahead probe must not tilt the trunk
  (bind mv (clamp (/ (- Speed 20.0) 60.0) 0.0 1.0))
  (bind terrLean (select terrOn (* mv (clamp (+ upL dnL) (- 0.0 (R TerrainLeanDownMax)) (R TerrainLeanUpMax))) 0.0))
  ; cross slope: the trunk balances toward the UPHILL side (b3: + gain moved the chest 1.9 deg downhill)
  (bind terrLat (select terrOn (clamp (* (- 0.0 (R TerrainCrossLeanGain)) cross) (- 0.0 (R TerrainCrossLeanMax)) (R TerrainCrossLeanMax)) 0.0))
  (bind terrDip (select terrOn (* mv (min (* (R TerrainDownDipPerDeg) (max (- 0.0 slope) 0.0)) (R TerrainDownDipMax))) 0.0))
  ; step-down: the ground under the capsule falls by > 4 cm within a frame; a drop already seen ahead (planned) absorbs half
  (bind gDz (select TerrainInit (- g0 TerrainGroundZ) 0.0))
  (bind aheadDrop (select terrOn (max (- g0 gA) 0.0) 0.0))
  (bind planned (> TerrainAheadDrop 6.0))
  (bind dropHit (min (* (* (R TerrainDropAbsorbGain) (select planned 0.5 1.0)) (max (- 0.0 gDz) 0.0)) (R TerrainDropAbsorbMax)))
  (bind dropDip (select (and terrOn (< gDz -4.0)) (max dropHit TerrainDropDip) (* TerrainDropDip (exp (/ (- 0.0 h) (max (R TerrainDropTau) 0.02))))))
  ; ---- targets (character frame) and critically damped springs
  (set LeanLatTarget (+ (+ leanCurve apaLeanR) terrLat))
  ; V2.6 P1: relaxed walk posture - a small forward relax at walking speeds only (weight 40..100 in, 170..230 out)
  (bind relaxIn (clamp (/ (- Speed 40.0) 60.0) 0.0 1.0))
  (bind relaxOut (clamp (/ (- 230.0 Speed) 60.0) 0.0 1.0))
  (bind walkRelax (select Grounded (* (R WalkRelaxFwdDeg) (* relaxIn relaxOut)) 0.0))
  (set LeanFwdTarget (+ (+ (+ brakeLean apaLeanF) walkRelax) (+ settleLean terrLean)))
  ; V2.25 T2: planned step preparation - the pelvis moves toward the level seen AHEAD before the capsule changes height; the capsule's
  ; own height change (gDz) then releases it (continuous pelvis instead of a one-frame pop). Only seen steps within the limits.
  (bind spOn (and (R StepPrepEnabled) (and terrOn (> Speed 20.0))))
  (bind spDiff (- gA g0))
  (set StepPrepPlan (select (and spOn (and (> (abs spDiff) (R StepPrepMin)) (< (abs spDiff) (R StepPrepMax)))) (* (R StepPrepGain) spDiff) 0.0))
  ; V2.25 T2c: the capsule's own height change is absorbed by the offset (pelvis world-continuous) and released in the human order;
  ; shared intermediates are stored in variables (T2b's shared nested selects ran the funcs build out of memory)
  (set StepPrepCapDz (select TerrainInit (- (.z Position) StepPrepPrevZ) 0.0))
  (set StepPrepPrevZ (.z Position))
  (set StepPrepActT (select (> (abs StepPrepCapDz) 6.0) 0.30 (max 0.0 (- StepPrepActT dt))))
  (set StepPrepAct (or (> (abs StepPrepCapDz) 6.0) (and (> StepPrepActT 0.0) (> (abs StepPrepCapDz) 1.0))))
  (set StepPrepRel (select StepPrepAct 0.0 (select (or (and ContactL (not StepPrepPrevCL)) (and ContactR (not StepPrepPrevCR))) 1.0 StepPrepRel)))
  (set StepPrepPrevCL ContactL)
  (set StepPrepPrevCR ContactR)
  (set StepPrepZ (select StepPrepAct (- StepPrepZ StepPrepCapDz) StepPrepZ))
  (bind aSp (- 1.0 (exp (/ (- 0.0 h) (max (R StepPrepTau) 0.02)))))
  (bind aSpR (- 1.0 (exp (/ (- 0.0 h) (max (R StepPrepReleaseTau) 0.02)))))
  (bind aSpH (- 1.0 (exp (/ (- 0.0 h) (max (R StepPrepHoldTau) 0.02)))))
  (bind aHeld (select (< StepPrepRel 0.5) aSpH aSpR))
  (bind aFree (select (> (abs (- StepPrepZ StepPrepPlan)) 2.0) aHeld aSp))
  (set StepPrepZ (select spOn (+ StepPrepZ (* (- StepPrepPlan StepPrepZ) (select StepPrepAct 0.0 aFree))) 0.0))
  (set StepPrepSeen (select (> (abs StepPrepPlan) 0.1) 1.0 0.0))
  (bind pot (vec apaBack (+ (+ inward supShift) apaRight) (- 0.0 (+ (max drop landDrop) (+ settleDip (+ terrDip dropDip))))))
  (bind potLen (vlen pot))
  ; V2.25 T2: the prepared step height is added AFTER the 4 cm vector clamp with its own limit
  (bind potC (selv (> potLen (R PelvisOffsetMaxCm)) (vscale pot (/ (R PelvisOffsetMaxCm) (max potLen 0.001))) pot))
  (set PelvisOffsetTarget (+ potC (vec 0.0 0.0 (clamp StepPrepZ (- 0.0 (R StepPrepHoldMax)) (R StepPrepHoldMax)))))   ; V2.25 T2b hold clamp
  (bind wl (R CurveLeanFreq))
  (set LeanLatVel (+ LeanLatVel (* (- (* wl wl (- LeanLatTarget LeanLat)) (* wl LeanLatVel 2.0)) h)))
  (set LeanLat (+ LeanLat (* LeanLatVel h)))
  (bind wf (R BodyTargetFreq))
  (set LeanFwdVel (+ LeanFwdVel (* (- (* wf wf (- LeanFwdTarget LeanFwd)) (* wf LeanFwdVel 2.0)) h)))
  (set LeanFwd (+ LeanFwd (* LeanFwdVel h)))
  (set PelvisOffsetVel (+ PelvisOffsetVel (vscale (- (vscale (- PelvisOffsetTarget PelvisOffset) (* wf wf)) (vscale PelvisOffsetVel (* wf 2.0))) h)))
  (set PelvisOffset (+ PelvisOffset (vscale PelvisOffsetVel h)))
  ; component frame of the -90 deg mount: +X = character left (= -right), +Y = character forward, +Z = up
  (set PelvisOffsetComp (vec (- 0.0 (.y PelvisOffset)) (.x PelvisOffset) (.z PelvisOffset)))
  ; ---- W2a / W2b foot-phase gates
  (bind strike (or HeelStrikeL HeelStrikeR))
  (set PlantEdge strike)
  (set StrikeAge (select strike 0.0 (+ StrikeAge dt)))
  (set SwitchWindow (or (not (R PhaseGatedSwitchEnabled)) (or (not Grounded) (or (< StrikeAge (R SwitchWindowSec)) (> StrikeAge (R SwitchMaxWait))))))
  (bind rdStart (and RedirectActive (not PrevRedirectActive)))
  (set RedirectPlants (select rdStart 0.0 (select (and RedirectActive strike) (+ RedirectPlants 1.0) (select RedirectActive RedirectPlants 0.0))))
  (set PrevRedirectActive RedirectActive)
  ; V2.21 memories (written last: the binds above read the previous values)
  (set SettleT sT)
  (set SettleAmp sAmp1)
  (set SettleWas stillNow)
  (set TerrainLean terrLean)
  (set TerrainSlope slope)
  (set TerrainCross cross)
  (set TerrainDropDip dropDip)
  (set TerrainGroundZ g0)
  (set TerrainAheadDrop aheadDrop)
  ; ---- V2.24 swing-foot clearance (SwingLiftEnabled): the swing foot's target is lifted by the deficit against the ground AHEAD of it
  (bind slOn (and (R SwingLiftEnabled) (and Grounded (> Speed 40.0))))
  (bind slDir (Matematik|Vektör|Normalize2D(Vector) :A PlanarVelocity :Tolerance 0.0001))
  (bind slA (* (R SwingLiftAhead) Speed))
  (bind pL (+ FootCenterL (vscale slDir slA)))
  (bind pR2 (+ FootCenterR (vscale slDir slA)))
  (bind (sx1 sh1 sok1) (Çarpışma|LineTraceByChannel :Start (vec (.x pL) (.y pL) (+ baseZ 70.0)) :End (vec (.x pL) (.y pL) (- baseZ 90.0)) :TraceChannel "TraceTypeQuery1" :bTraceComplex false :bIgnoreSelf true))
  (bind (sbh1 sio1 stm1 sdd1 sloc1 sip1 snrm1) (Çarpışma|BreakHitResult :Hit sh1))
  (bind (sx2 sh2 sok2) (Çarpışma|LineTraceByChannel :Start (vec (.x pR2) (.y pR2) (+ baseZ 70.0)) :End (vec (.x pR2) (.y pR2) (- baseZ 90.0)) :TraceChannel "TraceTypeQuery1" :bTraceComplex false :bIgnoreSelf true))
  (bind (sbh2 sio2 stm2 sdd2 sloc2 sip2 snrm2) (Çarpışma|BreakHitResult :Hit sh2))
  ; V2.25 T1: the foot's own ground (gate reference) and the MAX ground along the swing path (0.5 / 1.0 / 1.5 x ahead)
  (bind (sxu1 shu1 soku1) (Çarpışma|LineTraceByChannel :Start (vec (.x FootCenterL) (.y FootCenterL) (+ baseZ 70.0)) :End (vec (.x FootCenterL) (.y FootCenterL) (- baseZ 90.0)) :TraceChannel "TraceTypeQuery1" :bTraceComplex false :bIgnoreSelf true))
  (bind (sbhu1 siou1 stmu1 sddu1 slocu1 sipu1 snrmu1) (Çarpışma|BreakHitResult :Hit shu1))
  (bind (sxu2 shu2 soku2) (Çarpışma|LineTraceByChannel :Start (vec (.x FootCenterR) (.y FootCenterR) (+ baseZ 70.0)) :End (vec (.x FootCenterR) (.y FootCenterR) (- baseZ 90.0)) :TraceChannel "TraceTypeQuery1" :bTraceComplex false :bIgnoreSelf true))
  (bind (sbhu2 siou2 stmu2 sddu2 slocu2 sipu2 snrmu2) (Çarpışma|BreakHitResult :Hit shu2))
  (bind pLh (+ FootCenterL (vscale slDir (* slA 0.5))))
  (bind pRh (+ FootCenterR (vscale slDir (* slA 0.5))))
  (bind pLf (+ FootCenterL (vscale slDir (* slA 1.5))))
  (bind pRf (+ FootCenterR (vscale slDir (* slA 1.5))))
  (bind (sxh1 shh1 sokh1) (Çarpışma|LineTraceByChannel :Start (vec (.x pLh) (.y pLh) (+ baseZ 70.0)) :End (vec (.x pLh) (.y pLh) (- baseZ 90.0)) :TraceChannel "TraceTypeQuery1" :bTraceComplex false :bIgnoreSelf true))
  (bind (sbhh1 sioh1 stmh1 sddh1 sloch1 siph1 snrmh1) (Çarpışma|BreakHitResult :Hit shh1))
  (bind (sxh2 shh2 sokh2) (Çarpışma|LineTraceByChannel :Start (vec (.x pRh) (.y pRh) (+ baseZ 70.0)) :End (vec (.x pRh) (.y pRh) (- baseZ 90.0)) :TraceChannel "TraceTypeQuery1" :bTraceComplex false :bIgnoreSelf true))
  (bind (sbhh2 sioh2 stmh2 sddh2 sloch2 siph2 snrmh2) (Çarpışma|BreakHitResult :Hit shh2))
  (bind (sxf1 shf1 sokf1) (Çarpışma|LineTraceByChannel :Start (vec (.x pLf) (.y pLf) (+ baseZ 70.0)) :End (vec (.x pLf) (.y pLf) (- baseZ 90.0)) :TraceChannel "TraceTypeQuery1" :bTraceComplex false :bIgnoreSelf true))
  (bind (sbhf1 siof1 stmf1 sddf1 slocf1 sipf1 snrmf1) (Çarpışma|BreakHitResult :Hit shf1))
  (bind (sxf2 shf2 sokf2) (Çarpışma|LineTraceByChannel :Start (vec (.x pRf) (.y pRf) (+ baseZ 70.0)) :End (vec (.x pRf) (.y pRf) (- baseZ 90.0)) :TraceChannel "TraceTypeQuery1" :bTraceComplex false :bIgnoreSelf true))
  (bind (sbhf2 siof2 stmf2 sddf2 slocf2 sipf2 snrmf2) (Çarpışma|BreakHitResult :Hit shf2))
  (bind guL (select soku1 (.z sipu1) baseZ))
  (bind guR (select soku2 (.z sipu2) baseZ))
  (bind gL (max (max (select sokh1 (.z siph1) baseZ) (select sok1 (.z sip1) baseZ)) (select sokf1 (.z sipf1) baseZ)))
  (bind gRt (max (max (select sokh2 (.z siph2) baseZ) (select sok2 (.z sip2) baseZ)) (select sokf2 (.z sipf2) baseZ)))
  (set SwingPathMaxL (- gL baseZ))
  (set SwingPathMaxR (- gRt baseZ))
  ; V2.25 T1b: lift only in a CONFIRMED swing (> 0.10 s out of contact): a planted foot whose contact flag drops for a frame never lifts
  (set SwingAirTL (select ContactL 0.0 (min 1.0 (+ SwingAirTL dt))))
  (set SwingAirTR (select ContactR 0.0 (min 1.0 (+ SwingAirTR dt))))
  ; V2.26 T3c: a slowing swing foot over a platform the body has not climbed keeps its lift (no decay into the step before the plant)
  (bind swL (and slOn (and (> SwingAirTL 0.10) (> FootSpeedL (R SwingLiftMinSpeed)))))
  (bind swR (and slOn (and (> SwingAirTR 0.10) (> FootSpeedR (R SwingLiftMinSpeed)))))
  ; V2.26 T3d: a foot inside a platform the body has not climbed (local ground above the support ground, foot centre below it)
  (bind penL (and slOn (and (> (- guL g0) (R SwingLiftRiseMin)) (< (.z FootCenterL) (+ guL 3.0)))))
  (bind penR (and slOn (and (> (- guR g0) (R SwingLiftRiseMin)) (< (.z FootCenterR) (+ guR 3.0)))))
  ; V2.24 C3: only where the ground ahead rises over the support ground (no lift on flat or downhill)
  ; V2.25 T1 gate: rise of the swing path over the ground under the FOOT (not the capsule's plane)
  ; V2.26 T3a: rise ahead over the foot's own ground OR the foot's own ground over the SUPPORT ground (g0): a foot already over a platform
  ; the body has not climbed yet keeps its lift until the capsule rises
  (bind wRL (clamp (/ (- (max (- gL guL) (- guL g0)) (R SwingLiftRiseMin)) (max (R SwingLiftRiseRamp) 0.1)) 0.0 1.0))
  (bind wRR (clamp (/ (- (max (- gRt guR) (- guR g0)) (R SwingLiftRiseMin)) (max (R SwingLiftRiseRamp) 0.1)) 0.0 1.0))
  ; V2.26 T3g: targets against the POSE foot (final foot minus the lift already applied) - the old form converged to half the deficit
  ; V2.31 T5: the CAPSULE step-up (CMC step: baseZ +28 cm in 0.13 s) carries the pose foot up with it, but the lift (a capsule-relative offset)
  ; only decayed with SwingLiftTauDown -> the swing foot rose to 21 cm above the step top and hovered 0.43 s. The lift loses the capsule's
  ; rise of this frame at once (world foot height continuous); SwingLiftBaseComp 0 = V2.30
  (bind dBase (select (and (> (R SwingLiftBaseComp) 0.5) (> SHM231_SwBaseZ -1.0e8)) (max 0.0 (- baseZ SHM231_SwBaseZ)) 0.0))
  ; V2.32 T6 (SwingPelvisComp > 0): the lift may go NEGATIVE (the swing foot lowered toward the lagging pelvis), so the clamp is skipped
  (bind pcOn (and slOn (> (R SwingPelvisComp) 0.0)))
  (bind sLLc (select pcOn (- SwingLiftL dBase) (max 0.0 (- SwingLiftL dBase))))
  (bind sLRc (select pcOn (- SwingLiftR dBase) (max 0.0 (- SwingLiftR dBase))))
  (bind fzL (- (.z FootCenterL) SwingLiftL))
  (bind fzR (- (.z FootCenterR) SwingLiftR))
  (bind tL (max (select swL (* wRL (clamp (- (+ gL (R SwingLiftMargin)) fzL) 0.0 (R SwingLiftMax))) 0.0) (select penL (clamp (- (+ guL 7.5) fzL) 0.0 (R StepPenLiftMax)) 0.0)))   ; V2.26 T3d/T3e/T3g
  (bind tR (max (select swR (* wRR (clamp (- (+ gRt (R SwingLiftMargin)) fzR) 0.0 (R SwingLiftMax))) 0.0) (select penR (clamp (- (+ guR 7.5) fzR) 0.0 (R StepPenLiftMax)) 0.0)))
  ; ---- V2.32 T6: after a capsule step-up the visible pelvis needs ~0.9 s to follow (FootPlacement pelvis spring, SuddenMotionOnly
  ; compensation) while the swing foot follows the capsule-relative pose -> the trailing foot swung 17 cm over the step top under a lowered
  ; pelvis (raised-knee hover). The swing target is lowered by SwingPelvisComp x the pelvis lag (running pelvis height above the capsule
  ; base minus now), never below the highest ground on its path + SwingLiftMargin; a penetrating foot keeps its platform lift.
  (bind pzRel (- (.z (bone "pelvis")) baseZ))
  (bind plag (max 0.0 (- SHM232_PelvMean pzRel)))
  (bind lowL (max (- 0.0 (* (R SwingPelvisComp) plag)) (- (+ gL (R SwingLiftMargin)) fzL)))
  (bind lowR (max (- 0.0 (* (R SwingPelvisComp) plag)) (- (+ gRt (R SwingLiftMargin)) fzR)))
  (bind tLf0 (select (and pcOn (and swL (> plag 2.0))) (max lowL (select penL tL 0.0)) tL))
  (bind tRf0 (select (and pcOn (and swR (> plag 2.0))) (max lowR (select penR tR 0.0)) tR))
  ; ---- V2.32 T7 swing floor guard (SwingFloorGuard cm > 0): a swing foot (no contact) whose POSE foot centre (final minus the lift) is
  ; under its own planted height above its ground (SHM232_FootH0, learned in contact) + SwingFloorGuard is lifted to it (max 6 cm). Walk
  ; stops / starts: the stop-posture / body-inertia pelvis dip carried the closing swing foot 3 cm under its planted level while the planted
  ; foot was IK-held (c30_calm: the ball skimmed 33 cm along the floor; the clip itself lifts it 5.6 cm)
  (bind fhL (- (- (.z FootCenterL) SwingLiftL) guL))
  (bind fhR (- (- (.z FootCenterR) SwingLiftR) guR))
  (bind fgOn (and slOn (> (R SwingFloorGuard) 0.0)))
  (bind tgL (select (and fgOn (and SHM232_FootH0Init (not ContactL))) (clamp (- (+ SHM232_FootH0L (R SwingFloorGuard)) fhL) 0.0 6.0) 0.0))
  (bind tgR (select (and fgOn (and SHM232_FootH0Init (not ContactR))) (clamp (- (+ SHM232_FootH0R (R SwingFloorGuard)) fhR) 0.0 6.0) 0.0))
  (bind tLf (max tLf0 tgL))
  (bind tRf (max tRf0 tgR))
  (bind aUp (- 1.0 (exp (/ (- 0.0 h) (max (R SwingLiftTauUp) 0.01)))))
  (bind aDn (- 1.0 (exp (/ (- 0.0 h) (max (R SwingLiftTauDown) 0.01)))))
  (bind aCt (- 1.0 (exp (/ (- 0.0 h) (max (R SwingLiftTauContact) 0.005)))))
  ; V2.24 C3 release: in contact the lift goes fast (the stance foot belongs to FootPlacement)
  (set SwingLiftL (select slOn (+ sLLc (* (- tLf sLLc) (select (> tLf sLLc) aUp (select (and ContactL (not penL)) aCt aDn)))) 0.0))   ; V2.26 T3d: no fast release while penetrating
  (set SwingLiftR (select slOn (+ sLRc (* (- tRf sLRc) (select (> tRf sLRc) aUp (select (and ContactR (not penR)) aCt aDn)))) 0.0))
  ; V2.26 T3b landing shift onto a step (candidate: StepEdgeOn). Probes: mid 0.5x (siph), landing 1.0x (sip), far 1.5x (sipf)
  (bind gmL (select sokh1 (.z siph1) baseZ))
  (bind glL (select sok1 (.z sip1) baseZ))
  (bind gfL (select sokf1 (.z sipf1) baseZ))
  (bind gmR (select sokh2 (.z siph2) baseZ))
  (bind glR (select sok2 (.z sip2) baseZ))
  (bind gfR (select sokf2 (.z sipf2) baseZ))
  ; V2.26 T3c landing estimate = stance foot + travel x step length; probes +-StepEdgeProbe around it; a rise between them = the landing straddles an edge
  (bind stepLen (clamp (* Speed (R StepEdgeStepTime)) 30.0 (R StepEdgeStepMax)))
  (bind pLandL (+ FootCenterR (vscale slDir stepLen)))
  (bind pLandR (+ FootCenterL (vscale slDir stepLen)))
  (bind pLa (- pLandL (vscale slDir (R StepEdgeProbe))))
  (bind pLb (+ pLandL (vscale slDir (R StepEdgeProbe))))
  (bind pRa (- pLandR (vscale slDir (R StepEdgeProbe))))
  (bind pRb (+ pLandR (vscale slDir (R StepEdgeProbe))))
  (bind (exa1 eha1 eoka1) (Çarpışma|LineTraceByChannel :Start (vec (.x pLa) (.y pLa) (+ baseZ 70.0)) :End (vec (.x pLa) (.y pLa) (- baseZ 90.0)) :TraceChannel "TraceTypeQuery1" :bTraceComplex false :bIgnoreSelf true))
  (bind (ebha1 eioa1 etma1 edda1 eloca1 eipa1 enrma1) (Çarpışma|BreakHitResult :Hit eha1))
  (bind (exb1 ehb1 eokb1) (Çarpışma|LineTraceByChannel :Start (vec (.x pLb) (.y pLb) (+ baseZ 70.0)) :End (vec (.x pLb) (.y pLb) (- baseZ 90.0)) :TraceChannel "TraceTypeQuery1" :bTraceComplex false :bIgnoreSelf true))
  (bind (ebhb1 eiob1 etmb1 eddb1 elocb1 eipb1 enrmb1) (Çarpışma|BreakHitResult :Hit ehb1))
  (bind (exa2 eha2 eoka2) (Çarpışma|LineTraceByChannel :Start (vec (.x pRa) (.y pRa) (+ baseZ 70.0)) :End (vec (.x pRa) (.y pRa) (- baseZ 90.0)) :TraceChannel "TraceTypeQuery1" :bTraceComplex false :bIgnoreSelf true))
  (bind (ebha2 eioa2 etma2 edda2 eloca2 eipa2 enrma2) (Çarpışma|BreakHitResult :Hit eha2))
  (bind (exb2 ehb2 eokb2) (Çarpışma|LineTraceByChannel :Start (vec (.x pRb) (.y pRb) (+ baseZ 70.0)) :End (vec (.x pRb) (.y pRb) (- baseZ 90.0)) :TraceChannel "TraceTypeQuery1" :bTraceComplex false :bIgnoreSelf true))
  (bind (ebhb2 eiob2 etmb2 eddb2 elocb2 eipb2 enrmb2) (Çarpışma|BreakHitResult :Hit ehb2))
  (bind eLa (select eoka1 (.z eipa1) baseZ))
  (bind eLb (select eokb1 (.z eipb1) baseZ))
  (bind eRa (select eoka2 (.z eipa2) baseZ))
  (bind eRb (select eokb2 (.z eipb2) baseZ))
  ; V2.26 T3f: hold the shift while the foot is over the platform (own ground above the support ground) and not yet planted
  (bind holdL (and (> SwingShiftTL 1.0) (and (not ContactL) (> (- guL g0) (R SwingLiftRiseMin)))))
  (bind holdR (and (> SwingShiftTR 1.0) (and (not ContactR) (> (- guR g0) (R SwingLiftRiseMin)))))
  ; V2.28 T4: a TRUE edge = the rise between the two landing probes minus what the continuous slope (TerrainSlope, deg) would produce
  ; over their 2 x StepEdgeProbe span exceeds StepEdgeMin (a 15 deg slope over 30 cm rises 8 cm: not an edge). Landing case from the
  ; landing probe itself: already on the high side (past the edge by < StepEdgeProbe) -> lengthen the step by StepEdgeShift so the heel
  ; is on the platform; still on the low side (short of the edge by < StepEdgeProbe) -> shorten by StepEdgeShort so the toe does not
  ; catch the edge and the NEXT foot takes the step whole.
  (bind slopeRise (abs (* (Matematik|Trig|Tan(Degrees) :A TerrainSlope) (* 2.0 (R StepEdgeProbe)))))
  (bind riseL (- eLb eLa))
  (bind riseR (- eRb eRa))
  (bind edgeL (> (- riseL slopeRise) (R StepEdgeMin)))
  (bind edgeR (> (- riseR slopeRise) (R StepEdgeMin)))
  (bind highL (> (- glL eLa) (* 0.5 riseL)))
  (bind highR (> (- glR eRa) (* 0.5 riseR)))
  (bind seL (select (and (R StepEdgeOn) (and swL edgeL)) (select highL (R StepEdgeShift) (* -1.0 (R StepEdgeShort))) (select holdL SwingShiftTL 0.0)))
  (bind seR (select (and (R StepEdgeOn) (and swR edgeR)) (select highR (R StepEdgeShift) (* -1.0 (R StepEdgeShort))) (select holdR SwingShiftTR 0.0)))
  ; held while planted (a constant shift on a FootPlacement-locked foot keeps the visible foot still); ramps like the lift in swing
  (set SwingShiftTL (select ContactL SwingShiftTL (+ SwingShiftTL (* (- seL SwingShiftTL) (select (> seL SwingShiftTL) aUp aDn)))))
  (set SwingShiftTR (select ContactR SwingShiftTR (+ SwingShiftTR (* (- seR SwingShiftTR) (select (> seR SwingShiftTR) aUp aDn)))))
  (set SwingShiftL (selv (R StepEdgeOn) (vscale slDir SwingShiftTL) (vec 0.0 0.0 0.0)))
  (set SwingShiftR (selv (R StepEdgeOn) (vscale slDir SwingShiftTR) (vec 0.0 0.0 0.0)))
  (set SHM231_SwBaseZ baseZ)
  ; V2.32 T6 running pelvis height above the capsule base: follows only while the pelvis is near it (a step-up lag never pulls it down)
  (bind aPm (- 1.0 (exp (/ (- 0.0 h) 1.0))))
  (set SHM232_PelvMean (select (not SHM232_PelvInit) pzRel (select (and Grounded (< (abs (- pzRel SHM232_PelvMean)) 4.0)) (+ SHM232_PelvMean (* (- pzRel SHM232_PelvMean) aPm)) SHM232_PelvMean)))
  (set SHM232_PelvInit true)
  ; V2.32 T7 planted foot-centre height above its own ground (follows only in contact; first contact initialises)
  (bind aH0 (- 1.0 (exp (/ (- 0.0 h) 0.3))))
  (set SHM232_FootH0L (select ContactL (select SHM232_FootH0Init (+ SHM232_FootH0L (* (- fhL SHM232_FootH0L) aH0)) fhL) SHM232_FootH0L))
  (set SHM232_FootH0R (select ContactR (select SHM232_FootH0Init (+ SHM232_FootH0R (* (- fhR SHM232_FootH0R) aH0)) fhR) SHM232_FootH0R))
  (set SHM232_FootH0Init (or SHM232_FootH0Init (and ContactL ContactR)))
  (set SwingGroundL (- gL baseZ))
  (set SwingGroundR (- gRt baseZ))
  (set TerrainInit true))
""")

# ---------------------------------------------------------------- V2.1 (2026-10-14): cinematic shoulder swap
fn('SHM_UpdateCameraV21', [('dt', 'float')], [], r"""
(fn SHM_UpdateCameraV21 (dt)
  (bind h (min dt 0.05))
  ; first frame: start on the profile shoulder (+1) without easing in from 0
  (bind tgt0 (select CamV21Init CamSideTarget 1.0))
  (bind side0 (select CamV21Init CamSide2 1.0))
  (bind vel0 (select CamV21Init CamSide2Vel 0.0))
  ; sustained lateral travel in the facing frame (+ right), the same signal the V1.3.4 swap uses
  (bind rtv (vec (- 0.0 (.y Facing)) (.x Facing) 0.0))
  (bind vh (Matematik|Vektör|Normalize2D(Vector) :A PlanarVelocity :Tolerance 0.0001))
  (bind lat (select (and Grounded (> Speed (R CamSwapMinSpeed))) (dot vh rtv) 0.0))   ; V2.29: swap only above CamSwapMinSpeed
  ; hysteresis: leave the profile side (+1) only for clear travel to the left, come back once that travel is gone
  (bind onRight (> tgt0 0.0))
  (bind wantFlip (select onRight (select (< lat (- 0.0 (R CamSwapEnter))) 1.0 0.0) (select (> lat (- 0.0 (R CamSwapExit))) 1.0 0.0)))
  (bind timer (select (> wantFlip 0.5) (+ CamSideTimer dt) 0.0))
  (bind dwell (select onRight (R CamSwapDwell) (R CamSwapReturnDwell)))
  (bind flip (> timer dwell))
  (bind tgt (select flip (- 0.0 tgt0) tgt0))
  (set CamSideTimer (select flip 0.0 timer))
  (set CamSideTarget tgt)
  ; critically damped second order toward the target (semi-implicit Euler, dt <= 0.05)
  (bind w (R CamSwapFreq))
  (bind vel1 (+ vel0 (* (- (* w w (- tgt side0)) (* w vel0 2.0)) h)))
  (bind side1 (clamp (+ side0 (* vel1 h)) -1.0 1.0))
  (set CamSide2Vel vel1)
  (set CamSide2 side1)
  ; rebuilt shoulder scale: narrow-space scale x eased (partial) side x openness
  (bind sideEff (lerp 1.0 side1 (R CamSwapAmount)))
  (bind base (lerp 1.0 (R CamNarrowShoulderScale) ConstrainedLevel))
  (bind openF (lerp 1.0 (R CamOpenShoulderScale) CamOpenness))
  (set CamShoulderScaleV1 CamShoulderScale)
  (set CamShoulderScale (select (R CamSwapV21Enabled) (* (* base sideEff) openF) CamShoulderScale))
  ; ---- V2.4 C1 body-anchored pivot: chest (spine_03) offset over the capsule in the facing frame (+ right / + forward)
  (bind sp (bone "spine_03"))
  (bind bx (- (.x sp) (.x Position)))
  (bind by (- (.y sp) (.y Position)))
  (bind bLat (+ (* bx (.x rtv)) (* by (.y rtv))))
  (bind bFwd (+ (* bx (.x Facing)) (* by (.y Facing))))
  ; slow rest mean (the standing / gait posture of the clip) - only the deviation from it moves the camera
  (bind ar (- 1.0 (exp (/ (- 0.0 h) (max (R CamBodyHRestTau) 0.05)))))
  (bind rl (select CamV24Init (+ CamBodyLatRest (* (- bLat CamBodyLatRest) ar)) bLat))
  (bind rf (select CamV24Init (+ CamBodyFwdRest (* (- bFwd CamBodyFwdRest) ar)) bFwd))
  (bind bodyHOn (and (R CamBodyHEnabled) Grounded))
  (bind tl (select bodyHOn (clamp (* (R CamBodyHGain) (- bLat rl)) (- 0.0 (R CamBodyHMax)) (R CamBodyHMax)) 0.0))
  (bind tf (select bodyHOn (clamp (* (R CamBodyHGain) (- bFwd rf)) (- 0.0 (R CamBodyHMax)) (R CamBodyHMax)) 0.0))
  (bind wb (R CamBodyHFreq))
  ; critically damped second order (V1 pattern: velocity first, then the position from the NEW velocity variable)
  (set CamBodyLatVel (+ CamBodyLatVel (* (- (* wb wb (- tl CamBodyLat)) (* wb CamBodyLatVel 2.0)) h)))
  (set CamBodyFwdVel (+ CamBodyFwdVel (* (- (* wb wb (- tf CamBodyFwd)) (* wb CamBodyFwdVel 2.0)) h)))
  (set CamBodyLat (+ CamBodyLat (* CamBodyLatVel h)))
  (set CamBodyFwd (+ CamBodyFwd (* CamBodyFwdVel h)))
  (set CamOffset (+ CamOffset (+ (vscale rtv CamBodyLat) (vscale Facing CamBodyFwd))))
  ; rest means written LAST (their binds feed tl / tf above)
  (set CamBodyLatRest rl)
  (set CamBodyFwdRest rf)
  ; ---- V2.4 C2 camera roll with the body (shoulder line of the animated source mesh, + = leaning right)
  (bind ua (bone "upperarm_l"))
  (bind ub (bone "upperarm_r"))
  (bind bodyRoll (* (- (.z ua) (.z ub)) 1.64))
  (bind rollOn (and (and (R CamRollEnabled) Grounded) (> Speed 40.0)))
  (bind trl (select rollOn (clamp (* (R CamRollGain) bodyRoll) (- 0.0 (R CamRollMax)) (R CamRollMax)) 0.0))
  (bind wr (R CamRollFreq))
  (set CamRollVel (+ CamRollVel (* (- (* wr wr (- trl CamRollV24)) (* wr CamRollVel 2.0)) h)))
  (set CamRollV24 (+ CamRollV24 (* CamRollVel h)))
  ; ---- V2.21 living camera (CamV221Enabled, all x CamFxScale): heel-strike step dip, look-ahead, speed FOV
  ; a teleport / respawn / PIE start (capsule moved > 2 m in one frame, or the first frame) restarts the V2.21 filters
  (bind tele (or (not CamV221Init) (> (vlenxy (- Position CamV221Pos)) 200.0)))
  (bind cOn (and (R CamV221Enabled) Grounded))
  (bind fx (select (R CamV221Enabled) (clamp (R CamFxScale) 0.0 2.0) 0.0))
  ; step: a verified heel strike (component contact edge), not closer than CamStepMinInterval to the last one, alternating feet
  ; (the same foot again only after 0.6 s) - a double or mis-detected contact never re-kicks the camera
  (bind sideNow (select HeelStrikeL -1.0 (select HeelStrikeR 1.0 0.0)))
  (bind age (+ CamStepAge dt))
  (bind newSide (or (> (abs (- sideNow CamStepSide)) 0.5) (> age 0.6)))
  (bind okStep (and (and cOn (> Speed 40.0)) (and (> (abs sideNow) 0.5) (and (> age (R CamStepMinInterval)) newSide))))
  (bind g1 (lerp (R CamStepGainWalk) (R CamStepGainJog) (clamp (/ (- Speed 150.0) 150.0) 0.0 1.0)))
  (bind gS (lerp g1 (R CamStepGainSprint) (clamp (/ (- Speed 320.0) 150.0) 0.0 1.0)))
  ; the trigger is latched ONCE (CamStepFire): every later set re-evaluates its pure inputs after CamStepAge / Side changed
  (set CamStepFire okStep)
  ; analytic critically damped pulse z = -A (w a) e^(1 - w a), peak -A at a = 1/w: frame-rate independent (no explicit spring step)
  (bind ws (max (R CamStepFreq) 1.0))
  (bind aN (select CamStepFire 0.0 age))
  (bind amp (select CamStepFire gS CamStepVel))
  (bind wa (* ws aN))
  (set CamStepZ (select cOn (- 0.0 (* (* amp wa) (exp (- 1.0 wa)))) (* CamStepZ 0.8)))
  (set CamStepVel amp)
  (set CamStepCount (select CamStepFire (+ CamStepCount 1.0) CamStepCount))
  (set CamStepSide (select CamStepFire sideNow CamStepSide))
  (set CamStepAge aN)
  ; look-ahead along the real travel direction, grows with speed, slow and bounded; it never rotates the view
  (bind laD (lerp (R CamLookAheadWalk) (R CamLookAheadSprint) (clamp (/ (- Speed 130.0) 360.0) 0.0 1.0)))
  ; V2.23: camera yaw frame (the player's view), shared by the view look-ahead and the perceptual follow below
  (bind pcm3 (Oyun|GetPlayerCameraManager :PlayerIndex 0))
  (bind (cr3 cp3 cy3) (Matematik|Döndürücü|BreakRotator :InRot (Kamera|GetCameraRotation :self pcm3)))
  (bind yr3 (Matematik|Döndürücü|MakeRotator :Roll 0.0 :Pitch 0.0 :Yaw cy3))
  (bind cfw (Matematik|Vektör|GetForwardVector :InRot yr3))
  (bind crt (Matematik|Vektör|GetRightVector :InRot yr3))
  (bind folOn (R CamFollowEnabled))
  ; V2.23 view look-ahead: along the view only for travel with the view, sideways x CamLookSide, never toward the camera
  (bind laV (+ (vscale cfw (* laD (clamp (dot vh cfw) 0.0 1.0))) (vscale crt (* (* laD (R CamLookSide)) (dot vh crt)))))
  (bind laT (selv (and cOn (> Speed 60.0)) (selv folOn laV (vscale vh laD)) "(X=0,Y=0,Z=0)"))
  (set CamLookAhead (selv tele "(X=0,Y=0,Z=0)" (+ CamLookAhead (vscale (- laT CamLookAhead) (- 1.0 (exp (/ (- 0.0 h) (max (R CamLookAheadTau) 0.05))))))))
  (set CamOffset (+ CamOffset (vscale (+ CamLookAhead (vec 0.0 0.0 CamStepZ)) fx)))
  ; speed FOV: small at jog, the rest above jog speed; rises slower than speed changes, falls slower still (Shift taps)
  (bind fT (select cOn (* (R CamFOVSpeedMax) (+ (* 0.3 (clamp (/ (- Speed 150.0) 150.0) 0.0 1.0)) (* 0.7 (clamp (/ (- Speed 320.0) 170.0) 0.0 1.0)))) 0.0))
  (bind fTau (select (> fT CamFOVSpd) (R CamFOVRiseTau) (R CamFOVFallTau)))
  (set CamFOVSpd (select tele 0.0 (+ CamFOVSpd (* (- fT CamFOVSpd) (- 1.0 (exp (/ (- 0.0 h) (max fTau 0.05))))))))
  (set CamFOVDelta (+ CamFOVDelta (* CamFOVSpd fx)))
  ; ---- V2.25 inspection: what the player looks at (one sphere trace along the view), dwell -> latch, calm framing, limited look-at
  (bind insOn (and (R CamInspectEnabled) (not tele)))
  (bind camL (Kamera|GetCameraLocation :self pcm3))
  (bind cfw3 (Matematik|Vektör|GetForwardVector :InRot (Matematik|Döndürücü|MakeRotator :Roll 0.0 :Pitch cp3 :Yaw cy3)))
  (bind gazeEnd (+ camL (vscale cfw3 (+ (R InspectMaxDist) 200.0))))
  (bind (ihx ihh ihok) (Çarpışma|SphereTraceByChannel :Start camL :End gazeEnd :Radius (R InspectRadius) :TraceChannel "TraceTypeQuery1" :bTraceComplex false :bIgnoreSelf true))
  (bind (ibh iio itm idd iloc iip inrm iinrm ipm iact icomp) (Çarpışma|BreakHitResult :Hit ihh))
  (bind iname (İşlevsellikler|GetDisplayName :Object iact))
  ; V2.26 I4 contract: actor tag or component tag GR_Inspect; focus point = actor bounds origin
  ; V2.30 null-safe inspection: no member call on the (possibly missing) hit actor / component
  (bind (iorg iext irad) (Çarpışma|GetComponentBounds :Component icomp))
  (bind imatch (or (İşlevsellikler|Dize|Contains :SearchIn iname :Substring (R InspectKey1)) (or (İşlevsellikler|Dize|Contains :SearchIn iname :Substring (R InspectKey2)) (or (İşlevsellikler|Dize|Contains :SearchIn iname :Substring (R InspectKey3)) (İşlevsellikler|Dize|Contains :SearchIn iname :Substring (R InspectKey4))))))
  (bind itag (or (İşlevsellikler|Dize|Contains :SearchIn iname :Substring (R InspectKey1)) (İşlevsellikler|Dize|Contains :SearchIn iname :Substring (R InspectKey2))))   ; INS_ test props / Mask (the GR_Inspect-tagged set)
  (bind idist (vlenxy (- iip Position)))
  (bind iyd0 (- cy3 InspectPrevYaw))
  (bind iydw (Matematik|Trig|Atan2(Degrees) :Y (Matematik|Trig|Sin(Degrees) :A iyd0) :X (Matematik|Trig|Cos(Degrees) :A iyd0)))
  (bind iyawRate (abs (/ iydw (max h 0.001))))
  (bind islow (< Speed (R InspectMaxSpeed)))
  (bind icalm (< iyawRate (R InspectYawRateMax)))
  ; V2.31 inspection: explicit tag contract resolved behind IsValid (SHM231_InspectResolve), identity = the same object path, focus = mask mesh
  (bind m231 (> (R InspectFocusMode) 1.5))
  (bind ipath (İşlevsellikler|GetObjectPathString :Object iact))   ; full object path (= KismetSystemLibrary GetPathName; static, None -> "None")
  (bind itag231 (and SHM231_InsTag (and (İşlevsellikler|Dize|Contains :SearchIn ipath :Substring SHM231_InsId) (İşlevsellikler|Dize|Contains :SearchIn SHM231_InsId :Substring ipath))))
  (bind itagU (selb m231 itag231 itag))
  (bind cand (and insOn (and ihok (and itagU (and (> idist (R InspectMinDist)) (< idist (R InspectMaxDist)))))))   ; V2.26 I4: tag, not name (V2.31: resolved tag)
  ; V2.28 I5 target identity: the SAME target = the same actor object under the gaze as last frame (object name equality, both-way
  ; Contains), not a distance between two centres (InspectJump made two masks 29 cm apart one target). InspectIdOn 0 = V2.26 rule.
  (bind inameo (İşlevsellikler|GetObjectName :Object iact))
  (bind idsame (and (İşlevsellikler|Dize|Contains :SearchIn inameo :Substring InspectPrevHitName) (İşlevsellikler|Dize|Contains :SearchIn InspectPrevHitName :Substring inameo)))
  (bind isameD (< (dist iorg InspectPoint) (R InspectJump)))
  (bind isame (selb m231 (and (İşlevsellikler|Dize|Contains :SearchIn ipath :Substring SHM231_InsPrevId) (İşlevsellikler|Dize|Contains :SearchIn SHM231_InsPrevId :Substring ipath)) (selb (> (R InspectIdOn) 0.5) idsame isameD)))
  ; V2.28 I5 focus = the actor location (the mask pivot = the mask centre; the probe sphere shifts the bounds origin 15 cm into the room)
  (bind ifocus (selv m231 SHM231_InsFocus iorg))
  (bind dwell1 (min (+ (R InspectDwellOn) 0.15) (select cand (select isame (+ InspectDwell dt) 0.0) (max 0.0 (- InspectDwell (* dt 2.0))))))   ; V2.25 I2 dwell cap
  (bind acquire (and (> dwell1 (R InspectDwellOn)) (and islow icalm)))
  ; V2.28 I5: a new candidate under the gaze keeps the latch (switch after InspectSwitchOn s of dwell on it); the latch is lost on speed /
  ; turning or when nothing inspectable is under the gaze and the dwell decayed
  (bind lose (or (not islow) (or (not icalm) (and (not cand) (< dwell1 0.001)))))
  (set InspectLatch (select acquire 1.0 (select lose 0.0 InspectLatch)))
  (bind iswitch (and cand (or (not (> (R InspectIdOn) 0.5)) (or (< InspectLatch 0.5) (> dwell1 (R InspectSwitchOn))))))
  ; V2.28 I5: no current target (latch off) -> the point snaps to the focus (a lerp from the stale point travelled from the origin); latched -> smooth switch
  (set InspectPoint (selv (and cand (or (< InspectLatch 0.5) (and (not isame) (not (> (R InspectIdOn) 0.5))))) ifocus (selv iswitch (+ InspectPoint (vscale (- ifocus InspectPoint) (min 1.0 (* dt 6.0)))) InspectPoint)))   ; V2.26 I4 origin / V2.28 I5 smooth switch
  (set InspectSwitch (select (and cand (not isame)) 1.0 0.0))
  (set InspectDwell dwell1)
  (set InspectCand (select cand 1.0 0.0))
  ; V2.26 I3 gaze telemetry: the first blocker of the gaze trace (name / distance / impact height / key match)
  (set InspectHitName iname)
  (set InspectHitDist (select ihok idd 0.0))
  (set InspectHitZ (select ihok (.z iip) 0.0))
  (set InspectMatch (select (and ihok itagU) 1.0 0.0))
  (set InspectHitActorName inameo)
  (set InspectPrevHitName inameo)
  (set SHM231_InsPrevId ipath)
  (set SHM231_InsHit icomp)
  (bind aIns (- 1.0 (exp (/ (- 0.0 h) (max (select (> InspectLatch 0.5) (R InspectTauOn) (R InspectTauOff)) 0.02)))))
  (set InspectOn (select tele 0.0 (+ InspectOn (* (- InspectLatch InspectOn) aIns))))
  (bind toP (- InspectPoint Position))
  (bind toPh (vec (.x toP) (.y toP) 0.0))
  (bind toPl (vlenxy toPh))
  (bind ishare (vscale toPh (/ (min toPl (R InspectOffsetMax)) (max toPl 0.001))))
  ; V2.26 I4 framing split: the along-view part of the pivot share is closeness (InspectZoomOn); the view-lateral part is composition
  (bind cfwH (normal (vec (.x cfw3) (.y cfw3) 0.0)))
  (bind ishareAlong (vscale cfwH (dot ishare cfwH)))
  (bind ishareLat (- ishare ishareAlong))
  (set CamOffset (+ CamOffset (vscale (+ ishareLat (selv (R InspectZoomOn) ishareAlong (vec 0.0 0.0 0.0))) (* InspectOn (R InspectShare)))))
  (bind lookDir (normal toPh))
  (bind lookYaw (acosd (clamp (dot lookDir (normal (vec (.x Facing) (.y Facing) 0.0))) -1.0 1.0)))
  (bind lookGate (clamp (/ (- (R InspectLookMaxYaw) lookYaw) 25.0) 0.0 1.0))
  (set InspectLookAlpha (* InspectOn lookGate))
  (set InspectLookPoint InspectPoint)
  (set InspectPrevYaw cy3)
  ; ---- V2.23 perceptual follow: per-axis soft zone in the camera frame (e = follow point - capsule, cm; + right / + view forward)
  ; the capsule's displacement this frame (Position - CamV221Pos, before its update) moves e; the zone law then pulls the point:
  ; spring on the part of e outside the zone, velocity reference = the capsule's own axis velocity while it pushes the edge
  (bind dP (- Position CamV221Pos))
  (bind vL (dot PlanarVelocity crt))
  (bind vF (dot PlanarVelocity cfw))
  ; V2.23b world-frame follow: the stored offset / velocity are world x / y, projected on the camera axes for the zone law
  (bind eW (vec (- CamFolLat (.x dP)) (- CamFolFwd (.y dP)) 0.0))
  (bind uW (vec CamFolVLat CamFolVFwd 0.0))
  (bind eL0 (dot eW crt))
  (bind eF0 (dot eW cfw))
  (bind uL0 (dot uW crt))
  (bind uF0 (dot uW cfw))
  (bind wz (clamp (/ (- Speed (R CamWalkSpeedLo)) (max (- (R CamWalkSpeedHi) (R CamWalkSpeedLo)) 1.0)) 0.0 1.0))   ; V2.29 walk -> run zone blend
  (bind zL (lerp (R CamFolDZLatWalk) (R CamFolDZLat) wz))
  (bind zF (lerp (R CamFolDZFwdWalk) (R CamFolDZFwd) wz))
  (bind xL (- eL0 (clamp eL0 (- 0.0 zL) zL)))
  (bind xF (- eF0 (clamp eF0 (- 0.0 zF) zF)))
  ; edge weight: 0 inside 60 % of the zone, 1 at the edge; push = the capsule moves away from the point on that axis
  (bind kL (* (clamp (/ (- (abs eL0) (* 0.6 zL)) (max (* 0.4 zL) 1.0)) 0.0 1.0) (clamp (/ (- 0.0 (* eL0 vL)) (+ (* (abs eL0) 30.0) 1.0)) 0.0 1.0)))
  (bind kF (* (clamp (/ (- (abs eF0) (* 0.6 zF)) (max (* 0.4 zF) 1.0)) 0.0 1.0) (clamp (/ (- 0.0 (* eF0 vF)) (+ (* (abs eF0) 30.0) 1.0)) 0.0 1.0)))
  ; resting (slow, no input): re-centre gently, then rest
  (bind rest (select (< Speed 20.0) 1.0 0.0))
  (bind wR (R CamFolRecentreW))
  (bind wL (R CamFolWLat))
  (bind wF (R CamFolWFwd))
  ; damping: critical for the zone spring; while resting inside the zone critical for the slow re-centre spring
  (bind dL (* 2.0 (select (and (> rest 0.5) (< (abs xL) 0.5)) wR wL)))
  (bind dF (* 2.0 (select (and (> rest 0.5) (< (abs xF) 0.5)) wR wF)))
  ; V2.24 D: while the view turns the follow re-centres (critically damped, CamFolYawW) instead of being re-pushed by the zone
  (bind yd3 (- cy3 CamFolPrevYaw))
  (bind ydw (Matematik|Trig|Atan2(Degrees) :Y (Matematik|Trig|Sin(Degrees) :A yd3) :X (Matematik|Trig|Cos(Degrees) :A yd3)))
  (bind yK0 (select (and (> (R CamFolYawFade) 0.5) (not tele)) (clamp (/ (abs (/ ydw (max h 0.001))) (R CamFolYawFade)) 0.0 1.0) 0.0))
  (bind yK (max yK0 InspectOn))   ; V2.25: inspecting = the follow re-centres (calm frame)
  (bind wY (R CamFolYawW))
  (bind aL (+ (* (- 1.0 yK) (- (- (* (* wL wL) (- 0.0 xL)) (* (* (* wR wR) rest) eL0)) (* dL (- uL0 (* kL vL))))) (* yK (- (* (* wY wY) (- 0.0 eL0)) (* (* 2.0 wY) uL0)))))
  (bind aF (+ (* (- 1.0 yK) (- (- (* (* wF wF) (- 0.0 xF)) (* (* (* wR wR) rest) eF0)) (* dF (- uF0 (* kF vF))))) (* yK (- (* (* wY wY) (- 0.0 eF0)) (* (* 2.0 wY) uF0)))))
  (set CamFolYawK yK)
  (set CamFolPrevYaw cy3)
  (bind uL (+ uL0 (* aL h)))
  (bind uF (+ uF0 (* aF h)))
  (bind fm (R CamFolMax))
  (bind live (and folOn (not tele)))
  (bind eL1 (clamp (+ eL0 (* uL h)) (- 0.0 fm) fm))
  (bind eF1 (clamp (+ eF0 (* uF h)) (- 0.0 fm) fm))
  (bind eW1 (+ (vscale crt eL1) (vscale cfw eF1)))
  (bind uW1 (+ (vscale crt uL) (vscale cfw uF)))
  (set CamFolVLat (select live (.x uW1) 0.0))
  (set CamFolVFwd (select live (.y uW1) 0.0))
  (set CamFolLat (select live (.x eW1) 0.0))
  (set CamFolFwd (select live (.y eW1) 0.0))
  (set CamOffset (+ CamOffset (vec CamFolLat CamFolFwd 0.0)))
  ; ---- V2.22 closeness by speed: boom x k(v) (stand / walk 140 / jog 300 / sprint 490 cm/s keys), outdoors only (x CamOpenness)
  (bind kw (lerp (R CamCloseStand) (R CamCloseWalk) (clamp (/ Speed 140.0) 0.0 1.0)))
  (bind kj (lerp (R CamCloseWalk) (R CamCloseJog) (clamp (/ (- Speed 140.0) 160.0) 0.0 1.0)))
  (bind ks (lerp (R CamCloseJog) (R CamCloseSprint) (clamp (/ (- Speed 300.0) 190.0) 0.0 1.0)))
  (bind kv (select (< Speed 140.0) kw (select (< Speed 300.0) kj ks)))
  (bind kt (* (select (R CamCloseEnabled) (lerp 1.0 kv CamOpenness) 1.0) (lerp 1.0 (select (R InspectZoomOn) (R InspectBoom) 1.0) InspectOn)))   ; V2.25 inspect boom, V2.26 gated by InspectZoomOn
  (set CamCloseK (select tele kt (+ CamCloseK (* (- kt CamCloseK) (- 1.0 (exp (/ (- 0.0 h) (max (R CamCloseTau) 0.05))))))))
  (set CamBoomScale (* CamBoomScale CamCloseK))
  ; ---- V2.32 cinematic orbit (CamOrbitEnabled): a bounded VISUAL azimuth added to the boom yaw only (BP_GR_Player GR_UpdateRig <-
  ; GR_SHM_CamOrbit), never the control rotation and never the movement input frame (input stays on the control yaw: no feedback loop).
  ; Target = the body's own yaw (+ CamOrbitTravelW x the travel direction) relative to the player's view, sin-shaped (full at 90 deg, none along or against the view), x the
  ; reached speed (walk almost nothing, jog some, sprint most), x the side room the camera swings into (+ orbit = camera moves to the view's
  ; left) and the indoor scale. The camera reaches it with a lag (it keeps the old direction while the body brakes and turns, then settles in
  ; the new follow place) through a critically damped smoother. Player look (control yaw rate) wins: target 0 during a look and for
  ; CamOrbitLookHold s after it, with the faster CamOrbitLookTau settle. Teleport / PIE start resets it.
  (bind (ocr ocp ocy) (Matematik|Döndürücü|BreakRotator :InRot (Piyon|GetControlRotation :self OwnerChar)))
  (bind od0 (- (- ocy CamOrbitPrevCtl) CamRecDelta))   ; V2.33: minus the auto recentre's own last-frame turn (else it reads as a player look)
  (bind odc (Matematik|Trig|Atan2(Degrees) :Y (Matematik|Trig|Sin(Degrees) :A od0) :X (Matematik|Trig|Cos(Degrees) :A od0)))
  (bind olook (and CamOrbitInit (> (abs (/ odc (max h 0.001))) (R CamOrbitLookRate))))
  (bind olt (select (or olook tele) 0.0 (+ CamOrbitLookT dt)))
  (bind orl0 (- Yaw ocy))
  (bind orl (Matematik|Trig|Atan2(Degrees) :Y (Matematik|Trig|Sin(Degrees) :A orl0) :X (Matematik|Trig|Cos(Degrees) :A orl0)))
  (bind om1 (lerp (R CamOrbitMaxWalk) (R CamOrbitMaxJog) (clamp (/ (- Speed 150.0) 150.0) 0.0 1.0)))
  (bind omS (lerp om1 (R CamOrbitMaxSprint) (clamp (/ (- Speed 320.0) 150.0) 0.0 1.0)))
  ; + the real travel direction relative to the view (walk / jog are directional: the body keeps facing the view while it travels sideways)
  (bind ovy (Matematik|Trig|Atan2(Degrees) :Y (.y PlanarVelocity) :X (.x PlanarVelocity)))
  (bind ovr0 (- ovy ocy))
  (bind otw (max (R CamOrbitTravelW) 0.0))
  (bind osn (/ (+ (Matematik|Trig|Sin(Degrees) :A orl) (* otw (Matematik|Trig|Sin(Degrees) :A ovr0))) (+ 1.0 otw)))
  (bind oroom (clamp (/ (- (select (> osn 0.0) EnvLeft EnvRight) (R CamOrbitRoomMin)) (max (R CamOrbitRoomSpan) 1.0)) 0.0 1.0))
  (bind oin (lerp (R CamOrbitIndoorScale) 1.0 CamOpenness))
  (bind oOn (and (R CamOrbitEnabled) (and Grounded (and (> Speed 40.0) (and (< InspectOn 0.05) (> olt (R CamOrbitLookHold)))))))
  ; V2.34 phase envelope (CamEnvEnabled): brake / reversal / turn / redirect episode -> rise, hold, then decay CamEnvHold s after it ended
  (bind etr (or RedirectActive (> (max (max BrakingDemand ReversalDemand) TurnSeverity) (R CamEnvTrig))))
  (bind etT (select etr 0.0 (+ CamEnvT dt)))
  (bind etg (select (< etT (R CamEnvHold)) 1.0 0.0))
  (bind etau (select (> etg CamEnv) (R CamEnvRise) (R CamEnvRelease)))
  (bind envN (select tele 0.0 (+ CamEnv (* (- etg CamEnv) (- 1.0 (exp (/ (- 0.0 h) (max etau 0.03))))))))
  (bind envK (select (R CamEnvEnabled) envN 1.0))
  (bind otg (select oOn (* (* (* omS osn) envK) (* (* oroom oin) (clamp (R CamComfortScale) 0.0 1.0))) 0.0))
  (bind otau (select (< olt (R CamOrbitLookHold)) (R CamOrbitLookTau) (R CamOrbitLagTau)))
  (set CamOrbitTarget (select tele 0.0 (+ CamOrbitTarget (* (- otg CamOrbitTarget) (- 1.0 (exp (/ (- 0.0 h) (max otau 0.05))))))))
  (bind ow (R CamOrbitFreq))
  (set CamOrbitVel (select tele 0.0 (+ CamOrbitVel (* (- (* ow ow (- CamOrbitTarget CamOrbitYaw)) (* ow CamOrbitVel 2.0)) h))))
  (set CamOrbitYaw (select tele 0.0 (+ CamOrbitYaw (* CamOrbitVel h))))
  ; pure binds re-evaluate at every consumer: CamOrbitLookT (reads the look edge from CamOrbitPrevCtl) is written BEFORE CamOrbitPrevCtl
  (set LocoLookD (abs odc))   ; V2.34: the player's own look this frame (stored before CamOrbitPrevCtl / CamRecDelta change: pure-bind rule)
  (set CamEnv envN)
  (set CamEnvT etT)
  (set CamOrbitLookT olt)
  (set CamOrbitPrevCtl ocy)
  (set CamOrbitInit true)
  ; ---- V2.33 camera direction (sphirus-camera-direction): FOLLOW -> REACTION (the orbit above) -> SETTLE -> AUTO RECENTRE behind the
  ; stable travel direction without the right stick (CamRecEnabled). Output CamRecDelta = deg added to the CONTROL yaw this frame by
  ; BP_GR_Player (the only writer while LookDrivenLocomotion). Critically damped angular velocity CamRecVel (eases in and out, no overshoot,
  ; no constant-rate sweep). Conditions are body states, not a timer: grounded, moving > CamRecMinSpeed, travel direction stable (turn rate
  ; < CamRecTravelRate for CamRecStable s), no brake / reversal / redirect episode, no player look for CamRecLookHold s (a look this frame
  ; stops it at once: the seen angle is kept, no jump to an old centre), no inspection, error between CamRecDead and CamRecMaxErr deg
  ; (backward travel - error near 180 - never turns the view around). CamRecState: 0 follow, 1 reaction (orbit), 2 settle, 3 recentre.
  (bind rty (Matematik|Trig|Atan2(Degrees) :Y (.y PlanarVelocity) :X (.x PlanarVelocity)))
  (bind rtd0 (- rty CamRecPrevTravel))
  (bind rtd (Matematik|Trig|Atan2(Degrees) :Y (Matematik|Trig|Sin(Degrees) :A rtd0) :X (Matematik|Trig|Cos(Degrees) :A rtd0)))
  (bind rmov (and Grounded (> Speed (R CamRecMinSpeed))))
  (bind rstab (and rmov (< (abs (/ rtd (max h 0.001))) (R CamRecTravelRate))))
  (bind rst (select (or tele (not rstab)) 0.0 (+ CamRecStableT dt)))
  (bind re0 (- rty ocy))
  (bind re (Matematik|Trig|Atan2(Degrees) :Y (Matematik|Trig|Sin(Degrees) :A re0) :X (Matematik|Trig|Cos(Degrees) :A re0)))
  (bind rcalm (and (< BrakingDemand 0.12) (and (< ReversalDemand 0.12) (not RedirectActive))))
  ; pure-bind rule (V2.14 / V2.32 trap): a bind re-evaluates at every consumer - the look timer is read from the STORED CamOrbitLookT (set
  ; above before CamOrbitPrevCtl; re-evaluating olt here would read this frame's own turn as a player look), and every state var is
  ; written only after all outputs that depend on its OLD value (delta -> state -> latch -> velocity -> stable time -> previous travel)
  ; V2.34 (b) body faces the travel, (c) real turn side
  (bind rfa (abs (Matematik|Trig|Atan2(Degrees) :Y (Matematik|Trig|Sin(Degrees) :A (- Yaw rty)) :X (Matematik|Trig|Cos(Degrees) :A (- Yaw rty)))))
  (bind rface (or (< (R CamRecFaceMax) 0.5) (< rfa (R CamRecFaceMax))))
  (bind rbig (and (R CamRecTurnSide) (and rface (not (< (abs re) (R CamRecMaxErr))))))
  (bind reE (select rbig (* (select (< CamRecTurnSign 0.0) -1.0 1.0) (abs re)) re))
  (bind rok (and (R CamRecEnabled) (and (> rst (R CamRecStable)) (and rcalm (and (> CamOrbitLookT (R CamRecLookHold)) (and (< InspectOn 0.05) (and rface (and (> (abs re) (R CamRecDead)) (or rbig (< (abs re) (R CamRecMaxErr)))))))))))
  (bind rw (R CamRecFreq))
  (bind racc (select rok (- (* (* rw rw) reE) (* (* 2.0 rw) CamRecVel)) (- 0.0 (* (* 2.0 rw) CamRecVel))))
  (bind rmr (select (> (R CamRecWalkRate) 0.5) (lerp (R CamRecWalkRate) (R CamRecMaxRate) (clamp (/ (- Speed 140.0) 160.0) 0.0 1.0)) (R CamRecMaxRate)))   ; V2.34 B2: calmer walk follow
  (bind rv1 (clamp (+ CamRecVel (* racc h)) (- 0.0 rmr) rmr))
  (bind rv (select (or tele (or (< CamOrbitLookT 0.05) (not (R CamRecEnabled)))) 0.0 rv1))
  (set CamRecDelta (* (* rv h) (clamp CamRecScale 0.0 1.0)))   ; device profile scale written by BP_GR_Player (gamepad 1.0, mouse 0.35)
  (set CamRecState (select rok 3.0 (select (> (abs rv) 0.5) 2.0 (select (> (abs CamOrbitYaw) 1.0) 1.0 0.0))))
  ; ---- V2.33 movement input frame latch (no circles / zig-zag while the view turns): when the auto recentre starts turning the view while
  ; a move input is held, the WORLD direction of that input is kept (MoveLatchYaw = the control yaw at that moment; the AAMS move handler
  ; builds its frame from it). A deliberate new input (world input direction changes > 30 deg), a release or a player look hands the frame
  ; back to the live control yaw in ~0.1 s (MoveLatchState 2) - a new deliberate input is camera-relative to the view the player sees.
  (bind miv DesiredDir)   ; the held move input's world direction (CMC current acceleration, SHM_UpdateState)
  (bind mheld HasIntent)
  (bind miy (Matematik|Trig|Atan2(Degrees) :Y (.y miv) :X (.x miv)))
  (bind mdy0 (- miy MoveLatchInYaw))
  (bind mdy (Matematik|Trig|Atan2(Degrees) :Y (Matematik|Trig|Sin(Degrees) :A mdy0) :X (Matematik|Trig|Cos(Degrees) :A mdy0)))
  (bind mst0 MoveLatchState)
  (bind mengage (and (R CamRecEnabled) (and mheld (and (> (abs rv) 2.0) (< mst0 0.5)))))
  (bind mkeep (and mheld (and (< (abs mdy) 30.0) (> CamOrbitLookT 0.05))))
  (bind mld0 (- ocy MoveLatchYaw))
  (bind mld (Matematik|Trig|Atan2(Degrees) :Y (Matematik|Trig|Sin(Degrees) :A mld0) :X (Matematik|Trig|Cos(Degrees) :A mld0)))
  ; ---- V2.34 locomotion frame (LocoFrameEnabled; sphirus-camera-direction + sphirus-natural-motion): the automatic camera never changes
  ; the body's direction, speed class, gait or facing. InFrameOff = the part of the auto recentre the player has not taken over: every auto
  ; turn (CamRecDelta) is subtracted while a move input is held, so the held input keeps its WORLD direction. The hand-over is continuous
  ; (no angle threshold, no jump): the offset shrinks in proportion to the stick's own angular change plus the player's look (LocoHandK
  ; deg = full hand-over) and is 0 on release. LocoIFY = next frame's input frame (control yaw after this frame's auto turn + offset).
  ; LocoYaw = the body / locomotion frame that BP_GR_Player's locomotion functions read instead of the control yaw (speed class, gait,
  ; backward intent, facing target, idle turn): the input frame, or - exploration (LocoExploreEnabled): a held lateral / forward-diagonal
  ; input (LocoExploreMin..Max deg off the input frame, moving > LocoExploreMinSpeed) while the player is not looking - the input's own
  ; world direction: the body decides to walk that way and the camera follows the body. A deliberate look ends it (look-driven again);
  ; after a release the body frame is held until a look or a new input. LocoState 0 frame, 1 exploration, 2 hold.
  (bind lon (R LocoFrameEnabled))
  (bind lsl0 (- miy MoveLatchYaw))
  (bind lsl (Matematik|Trig|Atan2(Degrees) :Y (Matematik|Trig|Sin(Degrees) :A lsl0) :X (Matematik|Trig|Cos(Degrees) :A lsl0)))
  ; B3: InFrameOff = the RAW un-handed auto turn (only a player look hands it over, LocoLookD / LocoHandK); the stick hands it over by its NET
  ; deviation from the stick angle held when the auto turn began (LocoPrevStick = that reference while an offset is outstanding): small
  ; corrections steer relative to the kept frame (never ignored, never re-interpreted), a deliberate re-aim of 10..70 deg hands the frame
  ; over continuously (world direction changes smoothly, no jump), a release hands it over at once.
  (bind lnet0 (- lsl LocoPrevStick))
  (bind lnet (abs (Matematik|Trig|Atan2(Degrees) :Y (Matematik|Trig|Sin(Degrees) :A lnet0) :X (Matematik|Trig|Cos(Degrees) :A lnet0))))
  (bind lhs (clamp (/ (- (select (and mheld LocoPrevHeld) lnet 0.0) 10.0) 60.0) 0.0 1.0))
  (bind lioff (select mheld (- (* InFrameOff (- 1.0 (clamp (/ LocoLookD (max (R LocoHandK) 1.0)) 0.0 1.0))) CamRecDelta) 0.0))
  (set LocoIFY (+ (+ ocy CamRecDelta) (* lioff (- 1.0 lhs))))
  (bind lrel0 (- miy LocoIFY))
  (bind lrel (abs (Matematik|Trig|Atan2(Degrees) :Y (Matematik|Trig|Sin(Degrees) :A lrel0) :X (Matematik|Trig|Cos(Degrees) :A lrel0))))
  (bind lkp0 (- miy LocoInYaw))   ; B3: keep = the held input itself did not jump (LocoYaw is rate-limited and may lag)
  (bind lkp (abs (Matematik|Trig|Atan2(Degrees) :Y (Matematik|Trig|Sin(Degrees) :A lkp0) :X (Matematik|Trig|Cos(Degrees) :A lkp0))))
  (bind lbase (and (R LocoExploreEnabled) (and mheld (and Grounded (and (> CamOrbitLookT (R CamRecLookHold)) (< InspectOn 0.05))))))
  ; B3: exploration only below LocoExploreMaxSpeed (0 = any; sprint already faces the movement - a sprint cut is not exploration) and for an
  ; input direction held LocoExploreStable s (a quick A / D cut is not a decision to walk that way)
  (bind lin0 (- miy LocoInYaw))
  (bind linT (select (and mheld (< (abs (Matematik|Trig|Atan2(Degrees) :Y (Matematik|Trig|Sin(Degrees) :A lin0) :X (Matematik|Trig|Cos(Degrees) :A lin0))) 15.0)) (+ LocoInT dt) 0.0))
  (bind lstart (and (and (> Speed (R LocoExploreMinSpeed)) (or (< (R LocoExploreMaxSpeed) 1.0) (< Speed (R LocoExploreMaxSpeed)))) (and (not (< linT (R LocoExploreStable))) (and (> lrel (R LocoExploreMin)) (< lrel (R LocoExploreMax))))))
  ; B6/B12: an exploration only STARTS outside a reversal and outside a redirect that began at SPRINT speed (RedirectGait 1), in the normal
  ; family >= 0.5 s after the last route switch (never inside / right after a start clip) or in the minor-turn family at once - a walk /
  ; jog turn starts WITH the input change (braking demand is not a gate)
  (bind lexp (and lbase (or (and LocoExplore (< lkp (R LocoExploreKeep))) (and (not LocoExplore) (and lstart (and (and (< ReversalDemand 0.12) (not (and RedirectActive (> RedirectGait 0.5)))) (and (< Family 1.5) (or (> Family 0.5) (> FamilyTime 0.5)))))))))
  (bind lhold (and lon (and (not mheld) (and (or LocoPrevHeld (or LocoExplore LocoHold)) (> CamOrbitLookT 0.05)))))   ; V2.34 B2: any release holds the body frame (the camera never turns a standing body)
  (set LocoState (select lexp 1.0 (select lhold 2.0 0.0)))
  (bind ltg (select (< (abs (- LocoState 1.0)) 0.5) miy (select (> LocoState 1.5) LocoYaw LocoIFY)))
  (bind ld0 (- ltg LocoYaw))
  (bind ld (Matematik|Trig|Atan2(Degrees) :Y (Matematik|Trig|Sin(Degrees) :A ld0) :X (Matematik|Trig|Cos(Degrees) :A ld0)))
  (bind lmax (select (> (R LocoTurnRate) 0.5) (* (R LocoTurnRate) h) 360.0))   ; B3: the body frame turns at most LocoTurnRate deg/s (0 = at once)
  (set LocoYaw (select lon (+ LocoYaw (clamp ld (- 0.0 lmax) lmax)) ocy))
  (set LocoInT linT)
  (set LocoInYaw (select mheld miy LocoInYaw))
  (set LocoExplore (< (abs (- LocoState 1.0)) 0.5))
  (set LocoHold (> LocoState 1.5))
  (set InFrameOff lioff)
  (set LocoPrevStick (select (or (not LocoPrevHeld) (< (abs InFrameOff) 0.5)) lsl LocoPrevStick))   ; B3: the stick reference while an auto offset is outstanding
  (set LocoPrevHeld mheld)
  (set LocoOn lon)
  (set MoveLatchStateN (select (< mst0 0.5) (select mengage 1.0 0.0) (select (< mst0 1.5) (select mkeep 1.0 (select mheld 2.0 0.0)) (select (< (abs mld) 1.0) 0.0 2.0))))
  (set MoveLatchYaw (select lon LocoIFY (select mengage ocy (select (> MoveLatchStateN 1.5) (+ MoveLatchYaw (* mld (- 1.0 (exp (/ (- 0.0 h) 0.06))))) (select (< MoveLatchStateN 0.5) ocy MoveLatchYaw)))))   ; V2.34: the locomotion-frame input frame when LocoFrameEnabled
  (set MoveLatchInYaw (select mengage miy (select (and (> MoveLatchStateN 0.5) (< MoveLatchStateN 1.5)) MoveLatchInYaw miy)))
  (set MoveLatchState MoveLatchStateN)
  (set MoveLatchOn (or lon (> MoveLatchStateN 0.5)))   ; V2.34: always on with the locomotion frame (the frame IS LocoIFY)
  (set CamRecVel rv)
  (set CamRecStableT rst)
  (set CamRecTurnSign (select (> (abs YawRate) 60.0) (select (> YawRate 0.0) 1.0 -1.0) CamRecTurnSign))   ; V2.34 (c) the side the body last turned
  (set CamRecPrevTravel rty)
  ; comfort scale (CamComfortScale 1 = authored, ~0.3 = low-motion profile): the WHOLE SHME camera offset and FOV change
  (bind cs (clamp (R CamComfortScale) 0.0 1.0))
  (set CamOffset (vscale CamOffset cs))
  (set CamFOVDelta (* CamFOVDelta cs))
  (set CamV221Pos Position)
  (set CamV221Init true)
  (set CamV24Init true)
  (set CamV21Init true))
""")
