# CHANGES V2.53 (2026-11-03)

Every write went through the gated runner with a write manifest (`Saved/Codex/SHME_V233_20261027/checkpoint/manifests/v253_*.json`).

**Rollback:**
- `promote253.py` with `V253_PROM={'mode':'rollback'}`: WalkHold 0, V2.52 APA databases, PSD_SHM237_JogStop.
- Content: `Tools/SHME_V249_20261102/restore249.py <manifest> --apply`, e.g. `v253_kink` restores the two crops.

**Untouched:** source clips, source databases and vendor assets.

## Production (promoted, manifest v253_prom)
| Change | Where | Script |
|---|---|---|
| SHM253_WalkHold = 1: on the first frame of a walk start from rest (GroundSpeed < 5 cm/s), MM searches the current database with DoNotInterrupt (no stray vendor sample in the blend stack) | ABP base + child (install: manifest v253_walkhold) | install253_walkhold.py, promote253.py |
| SHM236_DB_JogStop := PSD_SHM253_JogStop (post-brake settle) | ABP CDO | promote253.py |
| 180/135 crop kink re-key at 0.900 s (pelvis + upper body C1 Hermite, legs re-solved, foot error 0) | SHM248_Jog_Start_TurnR180_crop, _TurnR135_crop, in place (manifest v253_kink, backups) | fix253_cropkink.py |

## New assets
| Assets | What | Manifest |
|---|---|---|
| /Game/GraceRanger/SHME/Animations/V253/SHM253_JogStop_B{l,r}_P00..23 (24) + PSD_SHM253_JogStop | post-brake settle (v2: source length, settle reaches 0 at the source SHM_StopSettle drop); BranchIn SHME_V253_Settle, BlockTransition SHME_V253_Block | v253_settle (new), v253_dbclean (inherited V237 BranchIn stripped), v253_settle2 (v2 rewrite) |
| /Game/GraceRanger/SHME/Animations/V253/SHM253_StartTransfer_*_APA3 (14) + PSD_SHM253_StartTransferAPA_L/_R | APA v3 (min-jerk, visible accel cap 3 m/s2); tested, NOT promoted | v253_apa3 (new) |

## Installed but off
- **SHM253_WalkEntry (0):** request-frame start-DB search; broke the tap gate. Installed by install253_walkentry.py, manifest v253_walkentry.

## Tools (`Tools/SHME_V253_20261104/`)
**Analysis:**
- stance253.py: stance foot ball / heel / yaw / step per start, pelvis lateral and acceleration.
- settle253.py, brake253.py, brakepair253.py: jog-stop body response.
- ana253.sh: run summary.

**Probes and generators:**
- probe253_clips.py: clip component-space samples and keys; local data only, not published.
- gen253_settle.py, gen253_apa.py.
- fix253_cropkink.py.
- fix253_swingdip.py: dry only, lift 0.3-0.5 cm, not written.
- dbclean253.py.

**Install / promote:** install253_walkentry.py, install253_walkhold.py, promote253.py.

**Harness:** v253_ab.sh, ab_safe253.sh.

## Verify
- verify241 after promotion flagged only the intended change: `stop SHM236_DB_JogStop = PSD_SHM253_JogStop` (base + child).
- Its fixed expectation list still names PSD_SHM237_JogStop.

## Disk
- 4047 reproducible test outputs (13.39 GB: raw telemetry of rounds 245-249 and warm-ups, capture frames of rounds 246-249, published bundles of rounds 246-249 and older pivots) were moved to the Recycle Bin.
- Log: `Saved/Codex/Retention/recycle253_log.txt`, list `recycle253_list.txt`.
- Not touched: kept rounds 250-253, the protect list, checkpoint, data, reports, .uasset files.
- Space is freed when the Recycle Bin is emptied.
