(event `self.ReceiveBeginPlay`
  (bind _returnvalue (`GameplayStatics.DoesSaveGameExist` "SphComfort"))
  (if _returnvalue
    (bind _returnvalue_2 (`GameplayStatics.LoadGameFromSlot` "SphComfort"))
    (bind _assg_sph_comfort (cast `/Game/Sphirus/Player/Camera/SG_Sph_Comfort` _returnvalue_2)
      (:`then`
        (set `/Game/Sphirus/Player/Camera/AC_Sph_Camera.ReduceMotion` (`/Game/Sphirus/Player/Camera/SG_Sph_Comfort.ReduceMotion` _assg_sph_comfort) (`self.SphCamera`))
        (set `/Game/Sphirus/Player/Camera/AC_Sph_Camera.Side` (`/Game/Sphirus/Player/Camera/SG_Sph_Comfort.Side` _assg_sph_comfort) (`self.SphCamera`))
        (set `/Game/Sphirus/Player/Camera/AC_Sph_Camera.UserFov` (`/Game/Sphirus/Player/Camera/SG_Sph_Comfort.UserFov` _assg_sph_comfort) (`self.SphCamera`))
        (set `/Game/Sphirus/Player/Camera/AC_Sph_Camera.KickScale` (`/Game/Sphirus/Player/Camera/SG_Sph_Comfort.KickScale` _assg_sph_comfort) (`self.SphCamera`))
        (set `/Game/Sphirus/Player/Camera/AC_Sph_Camera.DynFovScale` (`/Game/Sphirus/Player/Camera/SG_Sph_Comfort.DynFovScale` _assg_sph_comfort) (`self.SphCamera`))
        (set `/Game/Sphirus/Player/Camera/AC_Sph_Camera.DofScale` (`/Game/Sphirus/Player/Camera/SG_Sph_Comfort.DofScale` _assg_sph_comfort) (`self.SphCamera`))
        (set `/Game/Sphirus/Player/Camera/AC_Sph_Camera.ResScale` (`/Game/Sphirus/Player/Camera/SG_Sph_Comfort.ResScale` _assg_sph_comfort) (`self.SphCamera`)))
      (:`CastFailed`
        _)))
  (`self.Sph_GASPBeginPlay`)
  (`parent.ReceiveBeginPlay`)
  (`SkinnedMeshComponent.SetLeaderPoseComponent` (`self.Henley`) (`self.Manny`) false false)
  (`SkinnedMeshComponent.SetLeaderPoseComponent` (`self.Shorts`) (`self.Manny`) false false)
  (`SkinnedMeshComponent.SetLeaderPoseComponent` (`self.GR_Under`) (`self.Manny`) false false)
  (`SkinnedMeshComponent.SetLeaderPoseComponent` (`self.GR_BeltSk`) (`self.Manny`) false false))

(event `self.ReceiveActorBeginOverlap`
  (params (OtherActor :type "Actor Object Reference"))
  (`parent.ReceiveActorBeginOverlap` OtherActor) ; Bu düğüm devre dışı bırakıldı ve çağrılmayacak.\nİşlevsellik oluşturmak için pinleri sürükle.
)

(event `self.ReceiveTick`
  (params (DeltaSeconds :type "Float (single-precision)"))
  (bind _returnvalue (`KismetMathLibrary.MakeRotator` 0.0 0.0 (.yaw (`self.GetControlRotation`))))
  (bind _returnvalue_2 (`KismetMathLibrary.GetForwardVector` _returnvalue))
  (bind _returnvalue_3 (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)))
  (bind _returnvalue_4 (`AnimInstance.Montage_IsActive` _returnvalue_3 "/Game/Sphirus/Player/Anim/Bed/AM_Sph_Bed.AM_Sph_Bed"))
  (bind _returnvalue_5 (`KismetMathLibrary.GetRightVector` _returnvalue))
  (bind _returnvalue_6 (`KismetMathLibrary.MapRangeClamped` (`KismetMathLibrary.VSizeXY` (`self.GetVelocity`)) 200.0 450.0 0.0 1.0))
  (bind _returnvalue_7 (`Controller.IsLookInputIgnored` (`self.GetController`)))
  (bind _returnvalue_8 (`SceneComponent.K2_GetComponentLocation` (`self.Cine`)))
  (bind _returnvalue_9 (`self.GetVelocity`))
  (bind _returnvalue_10 (`KismetMathLibrary.VSize` _returnvalue_9))
  (bind _returnvalue_11 (`MovementComponent.GetMaxSpeed` (`self.GetMovementComponent`)))
  (bind _returnvalue_12 (`KismetMathLibrary.SelectFloat` (+ (`self.GR_SteadyT`) DeltaSeconds) 0.0 (and (and (and (< (`KismetMathLibrary.Abs` (- _returnvalue_10 _returnvalue_11)) (* _returnvalue_11 0.15)) (> (`KismetMathLibrary.Dot_VectorVector` (`self.GetActorForwardVector`) (`KismetMathLibrary.Normal` _returnvalue_9)) 0.978)) (> _returnvalue_10 60.0)) (`self.GR_SteadyEnable`))))
  (bind _returnvalue_13 (`self.K2_GetActorLocation`))
  (bind _returnvalue_14 (`KismetMathLibrary.GetForwardVector` (`KismetMathLibrary.MakeRotator` 0.0 0.0 (.yaw (`self.GetControlRotation`)))))
  (bind _returnvalue_15 (- (`self.GR_LagPivot`) _returnvalue_13))
  (bind _returnvalue_16 (`KismetMathLibrary.FClamp` (`KismetMathLibrary.Dot_VectorVector` _returnvalue_15 _returnvalue_14) -45.0 45.0))
  (bind _returnvalue_17 (`self.GetLastMovementInputVector`))
  (bind _returnvalue_18 (`KismetMathLibrary.SelectFloat` (`KismetMathLibrary.DegAcos` (`KismetMathLibrary.FClamp` (`KismetMathLibrary.Dot_VectorVector` (`self.GetActorForwardVector`) (`KismetMathLibrary.Normal` _returnvalue_17)) -1.0)) 0.0 (> (`KismetMathLibrary.VSize` _returnvalue_17) 0.1)))
  (bind _returnvalue_19 (`KismetMathLibrary.VSizeXY` (`self.GetVelocity`)))
  (bind _returnvalue_20 (`KismetMathLibrary.GetRightVector` (`KismetMathLibrary.MakeRotator` 0.0 0.0 (.yaw (`self.GetControlRotation`)))))
  (bind _returnvalue_21 (`self.GetLastMovementInputVector`))
  (bind _returnvalue_22 (`NavMovementComponent.IsFalling` (`self.CharacterMovement`)))
  (bind _returnvalue_23 (== (`self.GR_Gait`) 1))
  (bind _returnvalue_24 (+ (`self.K2_GetActorLocation`) (`KismetMathLibrary.MakeVector` 0.0 0.0 66.0)))
  (bind _returnvalue_25 (> (`self.GR_HomeContext`) 0.5))
  (bind _returnvalue_26 (> (`self.GR_HomeContext`) 0.5))
  (bind _gr_camopen (`self.GR_CamOpen`))
  (bind _charactermovement (`self.CharacterMovement`))
  (bind _gr_latoff (`self.GR_LatOff`))
  (`parent.ReceiveTick` DeltaSeconds)
  (if (> (`self.GR_JumpPend`) 1.0)
    (if (`NavMovementComponent.IsFalling` (`self.CharacterMovement`))
      (`self.LaunchCharacter` (* (`KismetMathLibrary.Vector_Normal2D` (`self.GetVelocity`)) (`self.GR_JumpPend`)) true)
      (set `self.GR_JumpPend` 0.0)
      (else
        (set `self.GR_JumpT` (+ (`self.GR_JumpT`) DeltaSeconds))
        (if (> (`self.GR_JumpT`) 0.25)
          (set `self.GR_JumpPend` 0.0)))))
  (set `self.GR_Load2H` (or (`AnimInstance.Montage_IsActive` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) "/Game/Sphirus/Player/Anim/Day/AM_GR_Day_CarryArms.AM_GR_Day_CarryArms") (`self.GR_CarryActive`)))
  (set `/Game/Sphirus/Player/Camera/AC_Sph_Camera.Arm` (`self.GR_SpringArm`) (`self.SphCamera`))
  (set `/Game/Sphirus/Player/Camera/AC_Sph_Camera.Cine` (`self.Cine`) (`self.SphCamera`))
  (set `/Game/Sphirus/Player/Camera/AC_Sph_Camera.Body` (`self.Manny`) (`self.SphCamera`))
  (set `/Game/Sphirus/Player/Camera/AC_Sph_Camera.Home` (`self.GR_HomeContext`) (`self.SphCamera`))
  (set `/Game/Sphirus/Player/Camera/AC_Sph_Camera.Carry` (or (`self.GR_CarryActive`) (`self.GR_Load2H`)) (`self.SphCamera`))
  (set `self.GR_Back` (or (and _returnvalue_22 (`self.GR_Back`)) (and (not _returnvalue_22) (and (> (`KismetMathLibrary.VSize` _returnvalue_21) 0.1) (< (`KismetMathLibrary.Dot_VectorVector` (`KismetMathLibrary.Normal` _returnvalue_21) (`KismetMathLibrary.GetForwardVector` (`KismetMathLibrary.MakeRotator` 0.0 0.0 (.yaw (`Controller.GetControlRotation` (`self.GetController`)))))) (`KismetMathLibrary.SelectFloat` (`self.GR_BackOff`) (`self.GR_BackCos`) (`self.GR_Back`)))))))
  (set `self.GR_HoldT` (`KismetMathLibrary.SelectFloat` (+ (`self.GR_HoldT`) DeltaSeconds) 0.0 (and (and (and (`self.GR_Back`) (not (or (> (`self.GR_HomeContext`) 0.5) (`self.GR_Load2H`)))) (>= (`self.GR_GaitSel`) 1)) (or (> (`self.GR_HoldT`) 0.0) (and (> (`KismetMathLibrary.VSizeXY` (`self.GetVelocity`)) 200.0) (< (`KismetMathLibrary.Dot_VectorVector` (`KismetMathLibrary.Vector_Normal2D` (`self.GetLastMovementInputVector`)) (`KismetMathLibrary.Vector_Normal2D` (`self.GetVelocity`))) -0.2))))))
  (set `self.GR_BrakeHold` (and (and (> (`self.GR_HoldT`) 0.0) (< (`self.GR_HoldT`) (`self.GR_HoldMax`))) (not (and (> (`KismetMathLibrary.Dot_VectorVector` (`KismetMathLibrary.Vector_Normal2D` (`self.GetLastMovementInputVector`)) (`KismetMathLibrary.Vector_Normal2D` (`self.GetVelocity`))) 0.5) (> (`KismetMathLibrary.VSizeXY` (`self.GetVelocity`)) 120.0)))))
  (set `self.GR_GaitSel` (`KismetMathLibrary.SelectInt` 1 (`KismetMathLibrary.SelectInt` (`KismetMathLibrary.SelectInt` 1 0 (or (and (or (== (`self.GR_Gait`) 1) (== (`self.GR_Pace`) 1)) (not (or (> (`self.GR_HomeContext`) 0.5) (`self.GR_Load2H`)))) (and (`self.GR_TempoOn`) (not (or (> (`self.GR_HomeContext`) 0.5) (`self.GR_Load2H`)))))) (`KismetMathLibrary.SelectInt` 2 (`KismetMathLibrary.SelectInt` 1 0 (or (and (or (== (`self.GR_Gait`) 1) (== (`self.GR_Pace`) 1)) (not (or (> (`self.GR_HomeContext`) 0.5) (`self.GR_Load2H`)))) (and (`self.GR_TempoOn`) (not (or (> (`self.GR_HomeContext`) 0.5) (`self.GR_Load2H`)))))) (and (and (== (`self.GR_Pace`) 1) (not (or (> (`self.GR_HomeContext`) 0.5) (`self.GR_Load2H`)))) (and (not (`self.GR_CarryActive`)) (or (> (`KismetMathLibrary.VSizeXY` (`self.GetVelocity`)) 250.0) (== (`self.GR_GaitSel`) 2))))) (`self.GR_Back`)) (`self.GR_BrakeHold`)))
  (set `self.GR_TempoAct` (and (and (not (`self.GR_BrakeHold`)) (== (`self.GR_GaitSel`) 1)) (or (`self.GR_Back`) (not (and (or (== (`self.GR_Gait`) 1) (== (`self.GR_Pace`) 1)) (not (or (> (`self.GR_HomeContext`) 0.5) (`self.GR_Load2H`))))))))
  (if (and (`self.GR_TempoAct`) (not (`self.GR_TempoPrev`)))
    (bind _asabp_sph_gasp (cast `/Game/Sphirus/Player/GASP/ABP_Sph_GASP` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)))
      (:`then`
        (set `/Game/Sphirus/Player/GASP/ABP_Sph_GASP.CM_Vals` (`self.GR_TempoVals`) _asabp_sph_gasp))
      (:`CastFailed`
        _))
    (set `self.GR_TempoPrev` true))
  (if (and (not (`self.GR_TempoAct`)) (`self.GR_TempoPrev`))
    (bind _asabp_sph_gasp_2 (cast `/Game/Sphirus/Player/GASP/ABP_Sph_GASP` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)))
      (:`then`
        (set `/Game/Sphirus/Player/GASP/ABP_Sph_GASP.CM_Vals` (`self.GR_NormVals`) _asabp_sph_gasp_2))
      (:`CastFailed`
        _))
    (set `self.GR_TempoPrev` false))
  (set `self.GR_Tempo` (and (== (`self.GR_Gait`) 1) (or (> (`self.GR_HomeContext`) 0.5) (`self.GR_Load2H`))))
  (set `self.GR_RunBlock` (`KismetMathLibrary.SelectInt` 1 (`KismetMathLibrary.SelectInt` (`KismetMathLibrary.SelectInt` 3 2 (`self.GR_CarryActive`)) 0 (`self.GR_Load2H`)) (> (`self.GR_HomeContext`) 0.5)))
  (set `self.GR_Pace` (`self.GR_Pace`))
  (set `self.CharacterInputState` (make `/Game/Blueprints/Data/S_PlayerInputState` (and (and (and (== (`self.GR_GaitSel`) 2) (not _returnvalue_26)) (not (`self.GR_Load2H`))) (not (`self.GR_Back`))) (or (== (`self.GR_GaitSel`) 0) _returnvalue_26) (`self.GR_Back`)))
  (if (`self.GR_Back`)
    (set `CharacterMovementComponent.RotationRate` (`KismetMathLibrary.MakeRotator` 0.0 0.0 (`self.GR_BackTurn`)) (`self.CharacterMovement`)))
  (set `self.SphContextSpeedScale` (* (`KismetMathLibrary.SelectFloat` (`KismetMathLibrary.SelectFloat` (`self.GR_KHomeTempo`) 0.9091 (`self.GR_Tempo`)) (`KismetMathLibrary.SelectFloat` (`KismetMathLibrary.SelectFloat` (`self.GR_KLoadTempo`) (`self.GR_KLoad`) (`self.GR_Tempo`)) (`KismetMathLibrary.SelectFloat` (* (`KismetMathLibrary.SelectFloat` (`self.GR_KCarryJog`) 1.0 (`self.GR_CarryActive`)) (`KismetMathLibrary.SelectFloat` (`KismetMathLibrary.SelectFloat` (`self.GR_KTempoBack`) (`self.GR_KTempoRun`) (`self.GR_Back`)) 1.0 (`self.GR_TempoAct`))) (`KismetMathLibrary.SelectFloat` (`self.GR_KTempo`) 1.0 (`self.GR_Tempo`)) (>= (`self.GR_GaitSel`) 1)) (`self.GR_Load2H`)) (> (`self.GR_HomeContext`) 0.5)) (`KismetMathLibrary.SelectFloat` (`self.GR_BackK`) 1.0 (and (`self.GR_Back`) (== (`self.GR_GaitSel`) 0)))))
  (set `self.GR_SteadyT` _returnvalue_12)
  (set `self.GR_Steady` (> _returnvalue_12 0.35))
  (set `self.GR_HeadErr` _returnvalue_18)
  (set `self.GR_Reverse` (or (and (`self.GR_Reverse`) (> (`self.GR_HeadErr`) 9999.0)) (and (not (`self.GR_Reverse`)) (> (`self.GR_HeadErr`) 9999.0))))
  (set `self.GR_TurnScale` (`KismetMathLibrary.FInterpTo` (`self.GR_TurnScale`) (`KismetMathLibrary.MapRangeClamped` _returnvalue_18 25.0 135.0 1.0 0.5) DeltaSeconds 12.0))
  (if (not (`/Game/Sphirus/Player/Camera/AC_Sph_Camera.Enabled` (`self.SphCamera`)))
    (set `self.GR_LagPivot` (`KismetMathLibrary.VInterpTo` (`self.GR_LagPivot`) _returnvalue_13 DeltaSeconds 7.0))
    (set `self.GR_LatOff` (`KismetMathLibrary.FInterpTo` (`self.GR_LatOff`) (`KismetMathLibrary.FClamp` (`KismetMathLibrary.Dot_VectorVector` (- (`SceneComponent.GetSocketLocation` (`self.Manny`) "head") (`self.K2_GetActorLocation`)) _returnvalue_20) -30.0 30.0) DeltaSeconds 4.0))
    (set `SpringArmComponent.TargetOffset` (+ (+ (* _returnvalue_14 (`KismetMathLibrary.MakeVector` _returnvalue_16 _returnvalue_16 _returnvalue_16)) (`KismetMathLibrary.MakeVector` 0.0 0.0 (`KismetMathLibrary.FClamp` (.z _returnvalue_15) -15.0 15.0))) (* _returnvalue_20 (`KismetMathLibrary.MakeVector` _gr_latoff _gr_latoff _gr_latoff))) (`self.GR_SpringArm`)))
  (if (and _returnvalue_4 (not (`self.GR_BedMode`)))
    (set `self.GR_BedMode` true)
    (`self.SetActorEnableCollision` false)
    (`CharacterMovementComponent.SetMovementMode` _charactermovement "MOVE_Flying" 0)
    (`AnimInstance.SetRootMotionMode` _returnvalue_3 "RootMotionFromMontagesOnly")
    (elif (and (`self.GR_BedMode`) (not _returnvalue_4))
      (set `self.GR_BedMode` false)
      (`self.SetActorEnableCollision` true)
      (`CharacterMovementComponent.SetMovementMode` _charactermovement "MOVE_Walking" 0)
      (`AnimInstance.SetRootMotionMode` _returnvalue_3 "IgnoreRootMotion")))
  (set `self.GR_ShiftT` (`KismetMathLibrary.SelectFloat` (+ (`self.GR_ShiftT`) DeltaSeconds) 0.0 _returnvalue_23))
  (set `self.GR_SpeedBase` (`KismetMathLibrary.FInterpTo` (`self.GR_SpeedBase`) (`KismetMathLibrary.SelectFloat` 150.0 (`KismetMathLibrary.SelectFloat` (`KismetMathLibrary.SelectFloat` 500.0 300.0 (and (> (`self.GR_ShiftT`) 0.9) (or (> (`KismetMathLibrary.VSizeXY` (`self.GetVelocity`)) 250.0) (== (`self.GR_GaitSel`) 2)))) 180.0 _returnvalue_23) (> (`self.GR_HomeContext`) 0.5)) DeltaSeconds 3.0))
  (if (not (`/Game/Sphirus/Player/Camera/AC_Sph_Camera.Enabled` (`self.SphCamera`)))
    (bind (_outhit _returnvalue_27) (`KismetSystemLibrary.LineTraceSingle` _returnvalue_24 (+ _returnvalue_24 (* _returnvalue_5 (`KismetMathLibrary.MakeVector` 260.0 260.0 260.0))) "TraceTypeQuery2"))
    (bind (_outhit_2 _returnvalue_28) (`KismetSystemLibrary.LineTraceSingle` _returnvalue_24 (+ _returnvalue_24 (* (* _returnvalue_5 (`KismetMathLibrary.MakeVector` -1.0 -1.0 -1.0)) (`KismetMathLibrary.MakeVector` 260.0 260.0 260.0))) "TraceTypeQuery2"))
    (bind (_outhit_3 _returnvalue_29) (`KismetSystemLibrary.LineTraceSingle` _returnvalue_24 (+ _returnvalue_24 (* (* _returnvalue_2 (`KismetMathLibrary.MakeVector` -1.0 -1.0 -1.0)) (`KismetMathLibrary.MakeVector` 260.0 260.0 260.0))) "TraceTypeQuery2"))
    (bind (_outhit_4 _returnvalue_30) (`KismetSystemLibrary.LineTraceSingle` _returnvalue_24 (+ _returnvalue_24 (* (`KismetMathLibrary.Normal` (+ (* _returnvalue_2 (`KismetMathLibrary.MakeVector` -1.0 -1.0 -1.0)) _returnvalue_5)) (`KismetMathLibrary.MakeVector` 260.0 260.0 260.0))) "TraceTypeQuery2"))
    (bind (_outhit_5 _returnvalue_31) (`KismetSystemLibrary.LineTraceSingle` _returnvalue_24 (+ _returnvalue_24 (* (`KismetMathLibrary.MakeVector` 0.0 0.0 0.4) (`KismetMathLibrary.MakeVector` 260.0 260.0 260.0))) "TraceTypeQuery2"))
    (bind _returnvalue_32 (`KismetMathLibrary.SelectFloat` (`.Distance` (`GameplayStatics.BreakHitResult` _outhit)) 260.0 _returnvalue_27))
    (bind _returnvalue_33 (`KismetMathLibrary.SelectFloat` (`.Distance` (`GameplayStatics.BreakHitResult` _outhit_3)) 260.0 _returnvalue_29))
    (set `self.GR_CamOpen` (`KismetMathLibrary.FInterpTo` (`self.GR_CamOpen`) (`KismetMathLibrary.FMin` (`KismetMathLibrary.MapRangeClamped` (`KismetMathLibrary.FMin` (`KismetMathLibrary.FMin` _returnvalue_32 (`KismetMathLibrary.SelectFloat` (`.Distance` (`GameplayStatics.BreakHitResult` _outhit_2)) 260.0 _returnvalue_28)) (`KismetMathLibrary.FMin` _returnvalue_33 (`KismetMathLibrary.SelectFloat` (`.Distance` (`GameplayStatics.BreakHitResult` _outhit_4)) 260.0 _returnvalue_30))) 60.0 260.0 0.0 1.0) (`KismetMathLibrary.FMax` (`KismetMathLibrary.MapRangeClamped` (`KismetMathLibrary.SelectFloat` (`.Distance` (`GameplayStatics.BreakHitResult` _outhit_5)) 260.0 _returnvalue_31) 60.0 120.0 0.0 1.0) 0.35)) DeltaSeconds 1.6))
    (set `self.GR_ArmBase` (`KismetMathLibrary.FInterpTo` (`self.GR_ArmBase`) (`KismetMathLibrary.SelectFloat` 70.0 (`KismetMathLibrary.FMin` (+ (+ (`KismetMathLibrary.SelectFloat` (`KismetMathLibrary.Lerp` 85.0 115.0 _gr_camopen) (`KismetMathLibrary.Lerp` 105.0 140.0 _gr_camopen) _returnvalue_25) (* _returnvalue_6 12.0)) (* (`self.GR_CamFocus`) -35.0)) (`KismetMathLibrary.FMax` (+ _returnvalue_33 -25.0) 65.0)) (`Controller.IsLookInputIgnored` (`self.GetController`))) DeltaSeconds 2.2))
    (set `self.GR_Accel` (`KismetMathLibrary.FInterpTo` (`self.GR_Accel`) (/ (- _returnvalue_19 (`self.GR_PrevSpeed`)) (`KismetMathLibrary.FMax` DeltaSeconds 0.004)) DeltaSeconds 8.0))
    (set `self.GR_PrevSpeed` _returnvalue_19)
    (set `self.GR_CamKick` (+ (`self.GR_CamKick`) (* (- (* (`self.GR_Accel`) 0.05) (* (`self.GR_CamKick`) 3.0)) DeltaSeconds)))
    (set `SpringArmComponent.TargetArmLength` (+ (`self.GR_ArmBase`) (`KismetMathLibrary.FClamp` (`self.GR_CamKick`) -8.0 8.0)) (`self.GR_SpringArm`))
    (set `self.GR_CamShoulder` (`KismetMathLibrary.FInterpTo` (`self.GR_CamShoulder`) (`KismetMathLibrary.SelectFloat` 17.0 (`KismetMathLibrary.FClamp` (`KismetMathLibrary.FMin` (`KismetMathLibrary.SelectFloat` (`KismetMathLibrary.Lerp` 21.0 27.0 _gr_camopen) (`KismetMathLibrary.Lerp` 26.0 33.0 _gr_camopen) _returnvalue_25) (+ _returnvalue_32 -30.0)) 12.0 60.0) (`Controller.IsLookInputIgnored` (`self.GetController`))) DeltaSeconds 2.0))
    (set `self.GR_CamZ` (`KismetMathLibrary.FInterpTo` (`self.GR_CamZ`) (`KismetMathLibrary.SelectFloat` 8.0 (+ (`KismetMathLibrary.Lerp` 0.0 6.0 _gr_camopen) (* (`KismetMathLibrary.MapRangeClamped` _returnvalue_33 60.0 130.0 1.0) 28.0)) (`Controller.IsLookInputIgnored` (`self.GetController`))) DeltaSeconds 2.0))
    (set `SpringArmComponent.SocketOffset` (`KismetMathLibrary.MakeVector` 0.0 (`self.GR_CamShoulder`) (`self.GR_CamZ`)) (`self.GR_SpringArm`))
    (set `self.GR_CamFov` (`KismetMathLibrary.FInterpTo` (`self.GR_CamFov`) (+ (`KismetMathLibrary.SelectFloat` 62.0 66.0 _returnvalue_25) (* _returnvalue_6 3.0)) DeltaSeconds 1.2))
    (`CameraComponent.SetFieldOfView` (`self.Camera`) (`self.GR_CamFov`))
    (`CameraComponent.SetFieldOfView` (`self.Cine`) (`self.GR_CamFov`))
    (bind (_outhit_6 _returnvalue_34) (`KismetSystemLibrary.LineTraceSingle` _returnvalue_8 (+ _returnvalue_8 (* (`SceneComponent.GetForwardVector` (`self.Cine`)) (`KismetMathLibrary.MakeVector` 3000.0 3000.0 3000.0)))))
    (`CineCameraComponent.SetFocusSettings` (`self.Cine`) (make `CameraFocusSettings` "Manual" (`KismetMathLibrary.FClamp` (`KismetMathLibrary.SelectFloat` (`KismetMathLibrary.Vector_Distance` _returnvalue_8 (`SceneComponent.GetSocketLocation` (`self.Manny`) "hand_r")) (`KismetMathLibrary.SelectFloat` (`.Distance` (`GameplayStatics.BreakHitResult` _outhit_6)) 1500.0 _returnvalue_34) _returnvalue_7) 120.0 3000.0) (struct) true 5.0))
    (`CineCameraComponent.SetCurrentAperture` (`self.Cine`) (`KismetMathLibrary.SelectFloat` 4.0 9.0 _returnvalue_7))
    (if (`Controller.IsLookInputIgnored` (`self.GetController`))
      (`Controller.SetControlRotation` (`self.GetController`) (`KismetMathLibrary.RInterpTo` (`self.GetControlRotation`) (`KismetMathLibrary.MakeRotator` 0.0 -18.0 (.yaw (`self.K2_GetActorRotation`))) (`GameplayStatics.GetWorldDeltaSeconds`) 2.5)))))

(event `EnhancedInput|/Game/Sphirus/Player/Input/IA_Sph_Use`
  (params (ActionValue :type Boolean) (ElapsedSeconds :type "Float (double-precision)") (TriggeredSeconds :type "Float (double-precision)") (InputAction :type "InputAction Object Reference" :default "/Game/Sphirus/Player/Input/IA_Sph_Use.IA_Sph_Use"))
  (:`Started`
    (bind _outactors (`GameplayStatics.GetAllActorsOfClass` "/Game/GraceRanger/SF/Day/BP_GR_DayStation.BP_GR_DayStation_C"))
    (for _array_element _outactors
      (bind _asbp_gr_day_station (cast `/Game/GraceRanger/SF/Day/BP_GR_DayStation` _array_element))
      (`/Game/GraceRanger/SF/Day/BP_GR_DayStation.GR_Swing` _asbp_gr_day_station))))

(event `self.OnLanded`
  (params (Hit :type "HitResult Structure (by ref)"))
  (`self.Sph_GASPLanded`)
  (if (and (< (`KismetMathLibrary.VSizeXY` (`self.GetVelocity`)) 60.0) (< (.z (`self.GetVelocity`)) -700.0))
    (`self.PlayAnimMontage` "/Game/Sphirus/Player/Anim/Air/AM_Sph_Jump_LandRecovery.AM_Sph_Jump_LandRecovery" 1.4)))

(event `GR_ComfortToggle`
  (if (`KismetSystemLibrary.IsValid` (`self.GR_ComfortW`)) :!label _label
    (`Widget.RemoveFromParent` (`self.GR_ComfortW`))
    (set `self.GR_ComfortW` null)
    (`WidgetBlueprintLibrary.SetInputMode_GameOnly` (`GameplayStatics.GetPlayerController` 0))
    (set `PlayerController.bShowMouseCursor` false (`GameplayStatics.GetPlayerController` 0))
    (`GameplayStatics.SetGamePaused` false)
    (bind _returnvalue (`GameplayStatics.CreateSaveGameObject` "/Game/Sphirus/Player/Camera/SG_Sph_Comfort.SG_Sph_Comfort_C"))
    (bind _assg_sph_comfort (cast `/Game/Sphirus/Player/Camera/SG_Sph_Comfort` _returnvalue))
    (set `/Game/Sphirus/Player/Camera/SG_Sph_Comfort.ReduceMotion` (`/Game/Sphirus/Player/Camera/AC_Sph_Camera.ReduceMotion` (`self.SphCamera`)) _assg_sph_comfort)
    (set `/Game/Sphirus/Player/Camera/SG_Sph_Comfort.Side` (`/Game/Sphirus/Player/Camera/AC_Sph_Camera.Side` (`self.SphCamera`)) _assg_sph_comfort)
    (set `/Game/Sphirus/Player/Camera/SG_Sph_Comfort.UserFov` (`/Game/Sphirus/Player/Camera/AC_Sph_Camera.UserFov` (`self.SphCamera`)) _assg_sph_comfort)
    (set `/Game/Sphirus/Player/Camera/SG_Sph_Comfort.KickScale` (`/Game/Sphirus/Player/Camera/AC_Sph_Camera.KickScale` (`self.SphCamera`)) _assg_sph_comfort)
    (set `/Game/Sphirus/Player/Camera/SG_Sph_Comfort.DynFovScale` (`/Game/Sphirus/Player/Camera/AC_Sph_Camera.DynFovScale` (`self.SphCamera`)) _assg_sph_comfort)
    (set `/Game/Sphirus/Player/Camera/SG_Sph_Comfort.DofScale` (`/Game/Sphirus/Player/Camera/AC_Sph_Camera.DofScale` (`self.SphCamera`)) _assg_sph_comfort)
    (set `/Game/Sphirus/Player/Camera/SG_Sph_Comfort.ResScale` (`/Game/Sphirus/Player/Camera/AC_Sph_Camera.ResScale` (`self.SphCamera`)) _assg_sph_comfort)
    (`GameplayStatics.SaveGameToSlot` _assg_sph_comfort "SphComfort")
    (else
      (bind _returnvalue_2 (`|CreateWidget` "/Game/Sphirus/Player/Camera/WBP_Sph_Comfort.WBP_Sph_Comfort_C" (`GameplayStatics.GetPlayerController` 0)))
      (set `self.GR_ComfortW` _returnvalue_2)
      (`UserWidget.AddToViewport` (`self.GR_ComfortW`) 20)
      (`WidgetBlueprintLibrary.SetInputMode_GameAndUIEx` (`GameplayStatics.GetPlayerController` 0) (`self.GR_ComfortW`))
      (set `PlayerController.bShowMouseCursor` true (`GameplayStatics.GetPlayerController` 0))
      (`GameplayStatics.SetGamePaused` true))))

(event `EnhancedInput|/Game/Sphirus/Player/Input/IA_Sph_Move`
  (params (ActionValue :type "Vector2D Structure") (ElapsedSeconds :type "Float (double-precision)") (TriggeredSeconds :type "Float (double-precision)") (InputAction :type "InputAction Object Reference" :default "/Game/Sphirus/Player/Input/IA_Sph_Move.IA_Sph_Move"))
  (bind (_x _y) (`KismetMathLibrary.BreakVector2D` ActionValue))
  (bind _returnvalue (`KismetMathLibrary.MakeRotator` 0.0 0.0 (.yaw (`self.GetControlRotation`))))
  (:`Triggered`
    (`self.AddMovementInput` (`KismetMathLibrary.GetForwardVector` _returnvalue) _y)
    (`self.AddMovementInput` (`KismetMathLibrary.GetRightVector` _returnvalue) _x)))

(event `EnhancedInput|/Game/Sphirus/Player/Input/IA_Sph_Look`
  (params (ActionValue :type "Vector2D Structure") (ElapsedSeconds :type "Float (double-precision)") (TriggeredSeconds :type "Float (double-precision)") (InputAction :type "InputAction Object Reference" :default "/Game/Sphirus/Player/Input/IA_Sph_Look.IA_Sph_Look"))
  (bind (_x _y) (`KismetMathLibrary.BreakVector2D` ActionValue))
  (:`Triggered`
    (`self.AddControllerYawInput` _x)
    (`self.AddControllerPitchInput` _y)))

(event `EnhancedInput|/Game/Sphirus/Player/Input/IA_Sph_Gait`
  (params (ActionValue :type Boolean) (ElapsedSeconds :type "Float (double-precision)") (TriggeredSeconds :type "Float (double-precision)") (InputAction :type "InputAction Object Reference" :default "/Game/Sphirus/Player/Input/IA_Sph_Gait.IA_Sph_Gait"))
  (:`Started`
    (set `self.GR_Gait` 1))
  (:`Completed`
    (set `self.GR_Gait` 0)))

(event `EnhancedInput|/Game/Sphirus/Player/Input/IA_Sph_Jump`
  (params (ActionValue :type Boolean) (ElapsedSeconds :type "Float (double-precision)") (TriggeredSeconds :type "Float (double-precision)") (InputAction :type "InputAction Object Reference" :default "/Game/Sphirus/Player/Input/IA_Sph_Jump.IA_Sph_Jump"))
  (bind _returnvalue (`KismetMathLibrary.VSizeXY` (`self.GetVelocity`)))
  (bind _returnvalue_2 (`KismetMathLibrary.VSizeXY` (`self.GetVelocity`)))
  (bind _returnvalue_3 (`KismetMathLibrary.VSizeXY` (`self.GetVelocity`)))
  (:`Started`
    (if (not (`self.GR_Load2H`))
      (set `CharacterMovementComponent.JumpZVelocity` (`KismetMathLibrary.SelectFloat` (`self.GR_JzStand`) (`KismetMathLibrary.SelectFloat` (`self.GR_JzWalk`) (`KismetMathLibrary.SelectFloat` (`self.GR_JzJog`) (`self.GR_JzRun`) (< _returnvalue 470.0)) (< _returnvalue 280.0)) (< _returnvalue 60.0)) (`self.CharacterMovement`))
      (`self.Jump`)
      (set `self.GR_JumpPend` (`KismetMathLibrary.SelectFloat` (`KismetMathLibrary.SelectFloat` 0.0 (`KismetMathLibrary.SelectFloat` (`KismetMathLibrary.FMax` _returnvalue_2 (`self.GR_JbWalk`)) (`KismetMathLibrary.SelectFloat` (+ _returnvalue_2 (`self.GR_JbJog`)) (+ _returnvalue_2 (`self.GR_JbRun`)) (< _returnvalue_3 470.0)) (< _returnvalue_3 280.0)) (< _returnvalue_3 60.0)) 0.0 (> (`KismetMathLibrary.VSizeXY` (`self.GetLastMovementInputVector`)) 0.1)))
      (set `self.GR_JumpT` 0.0)
      (`self.PlayAnimMontage` "/Game/Sphirus/Player/Anim/Air/AM_Sph_Jump.AM_Sph_Jump")))
  (:`Completed`
    (`self.StopJumping`)))

(event `EnhancedInput|/Game/Sphirus/Player/Input/IA_Sph_Crouch`
  (params (ActionValue :type Boolean) (ElapsedSeconds :type "Float (double-precision)") (TriggeredSeconds :type "Float (double-precision)") (InputAction :type "InputAction Object Reference" :default "/Game/Sphirus/Player/Input/IA_Sph_Crouch.IA_Sph_Crouch"))
  (:`Started`
    (if (`self.bIsCrouched`)
      (`self.UnCrouch`)
      (else
        (`self.Crouch`)))))

(event `EnhancedInput|/Game/Sphirus/Player/Input/IA_Sph_Comfort`
  (params (ActionValue :type Boolean) (ElapsedSeconds :type "Float (double-precision)") (TriggeredSeconds :type "Float (double-precision)") (InputAction :type "InputAction Object Reference" :default "/Game/Sphirus/Player/Input/IA_Sph_Comfort.IA_Sph_Comfort"))
  (:`Started`
    (goto _label)))

(event `EnhancedInput|/Game/Sphirus/Player/Input/IA_Sph_Sprint`
  (params (ActionValue :type Boolean) (ElapsedSeconds :type "Float (double-precision)") (TriggeredSeconds :type "Float (double-precision)") (InputAction :type "InputAction Object Reference" :default "/Game/Sphirus/Player/Input/IA_Sph_Sprint.IA_Sph_Sprint"))
  (:`Started`
    (set `self.GR_Pace` 1))
  (:`Canceled`
    (set `self.GR_Pace` 0))
  (:`Completed`
    (set `self.GR_Pace` 0)))

(event `EnhancedInput|/Game/Sphirus/Player/Input/IA_Sph_Pace`
  (params (ActionValue :type Boolean) (ElapsedSeconds :type "Float (double-precision)") (TriggeredSeconds :type "Float (double-precision)") (InputAction :type "InputAction Object Reference" :default "/Game/Sphirus/Player/Input/IA_Sph_Pace.IA_Sph_Pace"))
  (:`Started`
    (set `self.GR_TempoOn` (not (`self.GR_TempoOn`)))))

(fn `GR_ApplyOutfit`
  (bind _gr_beltsk (`self.GR_BeltSk`))
  (`SkeletalMeshComponent.SetSkeletalMeshAsset` (`self.Henley`) (`KismetArrayLibrary.Array_Get` (`self.GR_OutfitTop`) (`self.GR_Outfit`)))
  (`SkeletalMeshComponent.SetSkeletalMeshAsset` (`self.Shorts`) (`KismetArrayLibrary.Array_Get` (`self.GR_OutfitLow`) (`self.GR_Outfit`)))
  (`PrimitiveComponent.SetMaterial` (`self.Manny`) 0 (`KismetArrayLibrary.Array_Get` (`self.GR_OutfitBody`) (`self.GR_Outfit`)))
  (`SkinnedMeshComponent.SetLeaderPoseComponent` (`self.Henley`) (`self.Manny`) false false)
  (`SkinnedMeshComponent.SetLeaderPoseComponent` (`self.Shorts`) (`self.Manny`) false false)
  (`SkinnedMeshComponent.SetLeaderPoseComponent` (`self.GR_Under`) (`self.Manny`) false false)
  (`SceneComponent.SetVisibility` _gr_beltsk (`KismetArrayLibrary.Array_Get` (`self.GR_OutfitBelt`) (`self.GR_Outfit`)) false)
  (`SkinnedMeshComponent.SetLeaderPoseComponent` _gr_beltsk (`self.Manny`) false false)
  (`SceneComponent.SetVisibility` (`self.GR_Under`) (`KismetArrayLibrary.Array_Get` (`self.GR_OutfitUnder`) (`self.GR_Outfit`)) false))

(fn `GR_DropProp`
  (`SceneComponent.SetVisibility` (`self.GR_Prop`) false false))

(fn `GR_DropPropL`
  (`SceneComponent.SetVisibility` (`self.GR_PropL`) false false))

(fn `GR_HoldProp`
  (params (Mesh :type "StaticMesh Object Reference") (Rel :type "Transform Structure"))
  (`SceneComponent.K2_AttachToComponent` (`self.GR_Prop`) (`self.Manny`) "hand_r" "KeepRelative" "KeepRelative" "KeepRelative" true)
  (`StaticMeshComponent.SetStaticMesh` (`self.GR_Prop`) Mesh)
  (`SceneComponent.K2_SetRelativeTransform` (`self.GR_Prop`) Rel false false)
  (`SceneComponent.SetVisibility` (`self.GR_Prop`) true false))

(fn `GR_HoldPropL`
  (params (Mesh :type "StaticMesh Object Reference") (Rel :type "Transform Structure"))
  (`SceneComponent.K2_AttachToComponent` (`self.GR_PropL`) (`self.Manny`) "hand_l" "KeepRelative" "KeepRelative" "KeepRelative" true)
  (`StaticMeshComponent.SetStaticMesh` (`self.GR_PropL`) Mesh)
  (`SceneComponent.K2_SetRelativeTransform` (`self.GR_PropL`) Rel false false)
  (`SceneComponent.SetVisibility` (`self.GR_PropL`) true false))

(fn `GR_SetBelt`
  (params (Index :type Integer))
  (`SkeletalMeshComponent.SetSkeletalMeshAsset` (`self.GR_BeltSk`) (`KismetArrayLibrary.Array_Get` (`self.GR_BeltList`) Index)))

(fn `GR_SetOutfit`
  (params (Index :type Integer))
  (set `self.GR_Outfit` Index)
  (`self.GR_ApplyOutfit`))

(fn `UserConstructionScript`
  (`parent.UserConstructionScript`)
  (`self.GR_ApplyOutfit`))
