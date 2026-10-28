---
name: sphirus-safe-unreal-iteration
description: Mandatory gates for every SPHIRUS editor iteration that writes assets, rebuilds databases, starts PIE or promotes - write manifest with verified backup, single job owner lock, runner-level PIE/stale/owner refusal, post-job disk/dirty audit, early error-flood stop, limited staged testing and evidence-version control. Use before queueing any editor job, generator, DB rebuild, A/B batch or promotion.
---

# SPHIRUS safe Unreal iteration

Procedure owner for *how* an editor iteration runs. Checkpoint philosophy: `sphirus-source-control-asset-safety`; runner / Python
mechanics: `sphirus-editor-automation-mcp`. This skill is the enforced gate list - the gates run in code, not as advice.

## When
Any job that saves, creates, deletes or renames a package; any PoseSearch DB rebuild; any PIE batch; any promotion. Read-only
inspection still declares `SHME_KIND=measure` (the runner then refuses every save).

## Inputs
- Exact list of packages the job may write (from the generator's dry run, never "the folder").
- Lock owner id for the session (`lock233.sh acquire <owner> "<reason>"`).

## Procedure
1. **Lock** - `bash Tools/SHME_V233_20261027/lock233.sh acquire <owner> "<reason>"`; refused if another owner holds it, an A/B process
   runs or runner jobs are pending. Chains `export SHME_OWNER=<owner>` (lib233.sh does).
2. **Manifest + backup** - dry-run the generator to a JSON list, then
   `MSYS_NO_PATHCONV=1 python Tools/SHME_V233_20261027/manifest233.py <name> --assets <pkgs...> [--new <created pkgs>]` (or `--from list.json`).
   Every existing package is copied and read back (sha1 equal). A listed package that does not exist stops it (`--new` for creations).
3. **Queue with a header** - `run_v2.sh` / `SHME_V1/run.sh` add `# SHME_KIND / OWNER / MANIFEST` (Tools/SHME_V233_20261027/jobhdr.sh;
   kind inferred from the script name, override `SHME_KIND=`). Write jobs need `SHME_MANIFEST=<json>`.
4. **Runner gates** (scratchpad `b2runner/runner.py`, log `Saved/Codex/SHME_V233_20261027/gate233.log`):
   G1 jobs queued before the runner started -> `stale/`, never run; G2 write / pie job while a PIE world exists -> REFUSED_PIE;
   G3 owner != lock owner -> REFUSED_OWNER; G4 write job without manifest / stale backup -> REFUSED; during every job `unreal` is a proxy
   whose save / delete / rename / duplicate calls refuse packages outside the manifest (measure / pie / control jobs: all refused);
   G5 after a write job: files written on disk or packages newly dirtied outside the manifest -> GUARD_WRITTEN / GUARD_DIRTY (job fails).
5. **Early failure** - qa_pie ends a run with ERROR_FLOOD after 200 Blueprint runtime errors (first line kept in `<label>_pie.json`
   `bp_error_first`); `build_funcs.py` re-applies the LastHitBy repair and verify232 fails on any LINKED GetLastHitBy - run a 1-run PIE
   smoke right after every build, before any batch.
6. **Staged tests** - one broken case + one sound counter-case first; then the family / entry phases / cancels; the combined regression,
   FPS 20/30/60/120 + real time + media only for a stable candidate. Two attempts without progress -> narrow the owner or change the method.
7. **Before the final verification** - no A/B process alive, empty queue (`lock233.sh acquire` proves both), then promote -> clean reopen ->
   verify -> final evidence, strictly in that order, each chain waiting for every earlier chain's DONE marker.
8. **Release** - `lock233.sh release <owner>`.

## Failed examples (real)
- V2.32: stopfix232 scanned /Game/GraceRanger/Animations and wrote 6 clips outside its checkpoint (A_CT_Ref_Walk_Stop_F_L/R active).
  Now: the generator's write list is the manifest; any other save is refused (G4) or fails the job (G5).
- V2.32: a second P1 instance queued a DB rebuild into a running PIE -> game thread frozen, runner hung 20 min (G2 refuses it).
- V2.32: a final chain relaunched the editor under the still-running ISO A/B; the old jobs ran in the new editor (G1 + lock).
- V2.32: the orbit read the control yaw through Pawn.LastHitBy for 9 hours of tests (3 errors / frame) - now ERROR_FLOOD + post-build check.
- V2.33: a DSL function build FAILED (unknown node) but the job returned OK; the emptied SHM_UpdateCameraV21 was saved by the next
  save job and a 0-error smoke run passed (an empty camera function makes no errors). Now build_funcs.py raises on any FAIL, chains
  also grep `FAIL DSL`, and a node census of the rebuilt function (probe233_camfn.py) must pass before any save.

- V2.34: a chain checked the installer result on a log line cut to 600 chars - '"ok": true' was cut off and a successful save was called
  FAILED. Chains now keep each job's full output (`last_<step>.out`) and check that, not the summarised log.
- V2.34 build gate beyond node counts: the census checks that every new state setter exists (`probe234_camfn.py` / `probe234_route.py`)
  and a behaviour check (`check234.py`) proves the new state really changes in a run before any batch (an empty / partial function that
  runs without errors is not a success). Census rules must match the source: 'exactly one setter' failed a correct build where the source
  writes FamilyTime twice by design - require >= 1 for every NEW state and a node floor, not exact counts of old code.- V2.35: an in-place content generator that is re-run on its own output compounds the edit (a capped swing cannot be uncapped). Every
  iteration restores the manifest backup with the editor CLOSED (a loaded .uasset cannot be replaced), checks the sha1, then writes the
  next revision under a new manifest (stop1 -> stop2..stop6).
- V2.35: the first run after a new / edited pose-search database read 'DB None' and picked a vendor pivot (63 cm): discard the first run
  after any DB build or property change (warm run), never judge content on it.

## Acceptance test (run once per new runner version)
`Saved/Codex/SHME_V233_20261027/run233_gates2.sh`: T1 owner, T2 measure save, T3 no manifest, T4 outside manifest, T5 write during PIE,
T6 write after PIE, T7 bypass save of an unlisted created asset (GUARD_WRITTEN), T8 listed cleanup. 2026-10-27: all 8 as expected.

## Rollback
Restore the manifest's backup copies (`Saved/Codex/SHME_V233_20261027/checkpoint/manifests/<name>/Content/...`) with the editor closed;
the manifest JSON lists file, sha1 before and backup path per package. Runner rollback: `b2runner/runner_v2_pre233.py`.

## Evidence version
Tables compare only runs of one build: record the build in the chain (`RELAUNCH` / `TEL_BUILT` markers) and never mix labels across
a rebuild; a same-session interleaved repeat decides, cross-session numbers only inform.
