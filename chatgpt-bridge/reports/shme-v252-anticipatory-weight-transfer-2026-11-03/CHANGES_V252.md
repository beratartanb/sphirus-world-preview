# CHANGES V2.52 (2026-11-03)

Every write went through the gated runner with a write manifest (`Saved/Codex/SHME_V233_20261027/checkpoint/manifests/v252_*.json`). Rollback: `promote252.py` with V252_PROM='rollback' (restores the V2.51 databases and YawTau 0) or `Tools/SHME_V249_20261102/restore249.py <manifest> --apply`. Source clips (`SHM_StartTransfer_*`), source databases and vendor assets untouched.

## New assets (manifest v252_apa --new, rewritten under v252_apa2)
| assets | what | script |
|---|---|---|
| `/Game/GraceRanger/SHME/Animations/V252/SHM252_StartTransfer_<dir>_<foot>_APA` (14) | walk start-transfer clips with the anticipatory weight transfer baked (pelvis + both legs re-solved; v2 blend-compensated, cap 8 cm, fade 0.3 s, roll 2 deg); source BranchIn removed, BranchIn SHME_V252_APA_<side> into the new DBs | gen252_apa.py |
| `/Game/GraceRanger/SHME/Animations/V252/PSD_SHM252_StartTransferAPA_L` / `_R` | same membership and settings as PSD_SHM_StartTransfer_L / _R | gen252_apa.py |

## ABP (ABP_GR_MotionMatchingBase + child)
| change | manifest | script |
|---|---|---|
| SHM252_YawTau: exponential factor in the V2.51 yaw hand-over step (FClamp value = err * dt / (tau + dt)) | v252_yawtau | install252_yawtau.py |
| SHM252_KeepRM: keep RootMotionFromMontagesOnly while owned (inert, no effect on the pop) | v252_rmmode | install252_rmmode.py |
| PROMOTION: SHM_StartTransferDB_L/_R := PSD_SHM252_StartTransferAPA_L/_R, SHM252_YawTau := 0.08, SHM252_KeepRM 0 | v252_prom | promote252.py |

## Tools (`Tools/SHME_V252_20261103/`)
probe252_starttransfer.py, gen252_apa.py, apa252.py (in-game weight transfer at swing toe-off), install252_yawtau.py, install252_rmmode.py, promote252.py; harness v252_ab.sh / ab_safe252.sh; contact250.py / score250.sh copies.

## Disk (closing)
Retention dry run: free space 70.4 GB; nothing prunable outside the kept rounds (250-252) and the 2-day minimum age. Older V2.49 outputs leave the kept set and are pruned by the next --apply after they age.
Retention fix: --min-age-days accepted only integers (int default); now float. Dry run with --min-age-days 0.3 lists ~13 GB of reproducible test output outside the kept rounds 250-252 (raw telemetry of rounds 245-249 and warm-up runs, old capture frames, already-published pub copies); reports, data/ and manifests/backups are never listed. Not applied in this round (permanent deletion is left to the user): python Tools/Retention/retention.py --apply --min-age-days 0.3
