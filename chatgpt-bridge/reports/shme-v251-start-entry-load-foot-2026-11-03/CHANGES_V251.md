# CHANGES V2.51 (2026-11-03)

Every write went through the gated runner with a write manifest + verified backup (`Saved/Codex/SHME_V233_20261027/checkpoint/manifests/v251_*.json`). Rollback: `Tools/SHME_V249_20261102/restore249.py <manifest> --apply`. Vendor assets, Candidate originals and `/Game/CoreMotion_Retargeted/` untouched.

## In production (ABP CDO knobs, promote251.py, manifest v251_prom)
| knob | value | installer (manifest) | what |
|---|---|---|---|
| SHM251_StartEntry | 1 | install251_entry_yaw.py (v251_entryyaw) | request-frame SHM start database for every jog start from rest (Update_MotionMatching, false path of the V2.49 entry branch) |
| SHM251_YawSlew | 1 (rate 150 deg/s, window 0.35 s) | install251_entry_yaw.py | continuous ClipYaw hand-over after the turn servo releases (SHM_Snapshot after SetSHM249_PrevServo) |
| SHM251_StartLoad | 1 (margin 0.1) | install251_startload.py (v251_startload), install251_startload2.py (v251_startload2) | start latch rawSide: COM SupportLoad split, then relaxed-leg curve SHM251_IdleSupport |
| SHM251_ExitOn | 0 (inert) | install251_exitdone.py (v251_exitdone) | TurnDone OR SHM251_Exit curve - had no effect, left off |

## Assets
| assets | change | manifest | script |
|---|---|---|---|
| 6 crops SHM248_Jog_Start_Turn*_crop | BlockTransition notify [0.25 s, end] (track SHME_V251_Block) | v251_cropblock | add251_cropblock.py |
| same | continuing-pose cost addend -6 on [0, len-0.12] (track SHME_V251_Hold) - no measurable effect | v251_cropbias | add251_cropbias.py |
| same | curve SHM251_Exit (step at len-0.32) - read only with ExitOn | v251_exitcurve | add251_exitcurve.py |
| SHM244_Idle_Weighted | curve SHM251_IdleSupport (+1 = right heel up, left leg loaded; 1.0 over the whole clip) | v251_idlesup | add251_idlesupport.py |

Adding curves lowercased existing curve names on the crops (shm249_rx/ry; FName comparison is case-insensitive, verify241 ALL_OK).

## Not promoted
- Weighted idle (SHM242_IdleOn): wstart 30.0 / gait 14.7 regressions (REPORT §5).

## Tools (`Tools/SHME_V251_20261103/`)
install251_entry_yaw.py, install251_startload.py, install251_startload2.py, install251_exitdone.py, add251_cropbias.py, add251_exitcurve.py, add251_cropblock.py, add251_idlesupport.py, promote251.py, probe251_dbmirror.py, probe251_mmnode.py; contact250.py / score250.sh copies; harness v251_ab.sh / ab_safe251.sh.

## Disk (closing)
Retention dry run 2026-11-03 03:31: kept rounds 249-251, nothing else prunable yet (round outputs are younger than the 2-day minimum age; only 0.3 MB pycache). Free space 77.2 GB (V2.50 close 84.2 GB): this round's telemetry, capture frames and manifest backups, kept as the latest round. Older rounds drop out automatically once they are 2 days old and outside the latest three.
