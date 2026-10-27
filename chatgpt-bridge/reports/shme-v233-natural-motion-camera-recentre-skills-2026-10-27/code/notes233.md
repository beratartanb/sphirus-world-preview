# V2.33 working notes (2026-10-27)

## 0 Cleanup (user request, before the brief): Saved/Codex/_Cleanup_20261027 - 40 947 files / 33.96 GB, C: 79 -> 110 GB free.

## 1 Safety gates (enforced in the runner, b2runner/runner.py; log gate233.log)
- G1 stale queue -> stale/ (proved: zz_stale_test never ran), G2 write / pie job during PIE refused (proved T5 = the V2.32 bfx_write2 case),
  G3 owner != lock (lock233.sh) refused, G4 write needs a verified-backup manifest (manifest233.py); during every job `unreal` is a proxy
  whose save / delete / rename / duplicate refuse packages outside the manifest (unreal types are immutable -> class patching impossible),
  G5 disk + dirty audit after write jobs (proved T7: a bypass save of an unlisted created asset -> GUARD_WRITTEN).
- Real catches during the work: REFUSED_MANIFEST when a chain's second job met the first job's legitimate write (fixed: manifest state
  file of gated writes); revert_quit refused a dirty component -> relaunch would have opened a SECOND editor -> lib233 relaunch now stops.
- jobhdr.sh writes '# SHME_KIND / OWNER / MANIFEST' for run_v2.sh and SHME_V1/run.sh.
- A_CT_Ref_Walk_Stop_F_L/R: no older copy in any Saved checkpoint (only derived SRC_Sample variants); current files backed up
  (manifest actref_current); the only route to the pre-V2.32 version is OneDrive version history (user side).

## 2 Telemetry: SHM| line -> component TelemetryLine -> qa_pie side file Saved/Codex/SHME_V1_20260925/SHM/<label>.shm
  (shm_evidence reads it first). Smoke: log SHM| lines 0, side rows 352, evidence identical (352 vs 354 rows, same fields / values).
  Editor log of a whole session: 2.25 MB. qa_pie ERROR_FLOOD (> 200 BP runtime errors) ends a run with the first error kept.

## 3 Camera owner trace (game asset /Game/GraceRanger/BP_GR_Player - NOT the Sandbox copy at .../Experimental/BodyInertia/Sandbox/)
- pawn chain BP_PBI_Player -> /Game/GraceRanger/BP_GR_Player -> Integrated/BP_Player_MM -> Integrated/BP_ExampleCharacter_MotionMatching.
- movement input = AddMovementInput(DetermineMovement(Right/Forward of GetControlRotation.Yaw)) in the Integrated ExampleCharacter.
- an auto-follow owner already exists: TurnWorld (GR_UpdateRig TW_CameraWorldYaw + EventGraph SetControlRotation) active only when
  GR_Profile.LookDrivenLocomotion is false (production true): RInterpTo_Constant (constant-rate sweep), no input latch, engages 12..180 deg.

## 4 Chain 1 - true stand -> backward start
- cause: the AAMS-derived jog back start begins 16 cm per foot off the idle stance, 5 cm lower, feet rotated 58-68 deg, root still 0.25 s
  while the capsule accelerates at once; + a one-frame vendor dense start (family 0 one frame late).
- content v2 (gen233_standback2): frame 0 = idle pose, bridge fade, root = the MEASURED capsule profile, stance re-plant (world-fixed
  at the clip's root-relative landing points), swing lift-before-slide, idle foot rotation while planted. Own DB PSD_SHM233_StandBackStart2
  (+ the back jog loop). v1 (pin + capsule root early) = 10 cm.
- route: ABP SHM_Snapshot SHM233_StandBack (knob SHM233_StandBackOn, jog gait, straight backward intent incl. the ABP current-frame CMC
  acceleration, truly stopped = speed < 15 + both contacts + the pose in an idle DB, latch <= 1.2 s); knob 1 = family-4 branch, knob 2 =
  Update_MotionMatching entry override (also covers the first intent frame).
- C1B (2 rep): true-stand back starts 38-41 -> 0 cm (sb22) inside the start; jstart / j30_rel_3200 wrongly took it (diagonal 135 deg
  passed dot < -0.7; re-press before the stop finished) -> gate narrowed (dot < -0.95, idle-DB pose) -> C1C.
