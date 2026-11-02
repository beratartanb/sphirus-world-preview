# CHANGES V2.50 (2026-11-03)

Every write went through the gated runner with a write manifest and a verified backup (`Saved/Codex/SHME_V233_20261027/checkpoint/manifests/v250_*.json`). Rollback: `Tools/SHME_V249_20261102/restore249.py <manifest> --apply [--only a,b]` (sha1 verified). Vendor assets, `CoreMotionAAMS/Candidate` originals and `/Game/CoreMotion_Retargeted/` (read-only reference) were not modified.

## In production
| assets | change | manifest | script |
|---|---|---|---|
| 6 crops `SHM248_Jog_Start_Turn{L,R}{090,135,180}_crop` | foot_l / foot_r orientation from the correct retarget (`/Game/CoreMotion_Retargeted/AAMS/Walk/af_Loco_Jog_Start_Turn*`), re-expressed under the crop calf | v250_footorient | fix250_footorient.py (v3) |
| 16 copies in `/Game/GraceRanger/SHME/Animations/Starts/Jog/` (SHM_JogQ_af_* and SHM232_IS_af_* Fwd/Bwd/Left/Right starts, SHM_JogQ Turn L/R 045/090/135/180) | same foot orientation repair | v250_footorient2 | fix250_footorient.py |
| crops TurnL090 (both feet), TurnL135 (both feet), TurnR180 (right foot) | first-step ball pivot: ball pinned in the first contact phase, leg re-solved with the V2.10 hinge solver, 6-frame fade (thigh/calf/foot of that leg) | v250_ballpin | fix250_ballpin.py |

No ABP / Blueprint / DB change in V2.50. The V2.49 production state is unchanged otherwise (servo, rest gate, TurnDone, HoldT 0, T2 bias −2.0, FPOff installed with knob 0).

## Not promoted
- Weighted idle (SHM242_IdleOn + PSD_SHM242_IdleC): regressions w42_id / gait / wstart@60 (REPORT §5).
- Ball pivot on the other turn feet: the knee hinge-axis frame-to-frame jump rose > 3 deg over the source.

## Tools (`Tools/SHME_V250_20261103/`)
contact250.py (per-foot PEN / PITCH / PLANT / BALL / YAW on the visible skeleton), score250.sh, probe250_animgraph.py, probe250_addnodes.py, probe250_lean.py, probe250_blendfk.py (offline crossfade + FK), probe250_footaxes.py, probe250_footpath.py, fix250_footorient.py, fix250_ballpin.py; harness copies v250_ab.sh / ab_safe250.sh. Retention: `Tools/Retention/retention.py` media-temp age guard.

## Disk (closing)
Retention dry run 2026-11-03 00:07: nothing prunable outside the kept rounds 248-250 (0.3 MB pycache); free space 84.2 GB (V2.49 close 88.3 GB; this round's telemetry, capture frames and manifest backups ~4 GB, kept as the latest rounds).
