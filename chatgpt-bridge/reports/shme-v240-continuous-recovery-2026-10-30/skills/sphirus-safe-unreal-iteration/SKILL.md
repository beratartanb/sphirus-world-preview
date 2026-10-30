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
- V2.36 candidate databases without restarts: a literal database pin (SetDatabaseToSearch) was given an ABP variable whose default is the
  production database (install236_stopvar.py) -> candidates are an abp_flag in the SAME editor (no in-place edit, no relaunch per try).
  Check EVERY node that passes the literal: the first hook missed K2Node_Select_3 and two batches ran the production stop while the
  state record said 'candidate'. Copies of production databases: duplicate_asset keeps the entry list (no BranchIn edits on production clips).
- V2.36 lock233 acquire counts processes by command line: a shell command whose own text contains 'ab_safe' / 'v23x_ab' blocks itself
  (LOCK233_REFUSED 3 A/B processes) - run acquire as its own command.
- V2.36 first use after a database build / edit: the search returns NO database for 2 frames (av_CurrentSelectedDatabase None) - harmless
  in a stop, but a reversal / loaded route then falls to the vendor pivot or loop (j35_rev 32.6 cm, e29_load 21.1, j34_chain1 50 cm).
  Report cold first use separately from warm runs and test it again after the clean reopen (the cooked / DDC index is the real case).

- V2.37 editing a clip (a BranchIn track added for another database) invalidates EVERY database that contains it: the next run that
  enters such a database reads 'None' for 2-4 frames (j36_sside 9.70-9.80 s). Runs with no-DB frames are invalid (ab237 / tables237
  mark them) - repeat them, never compare them; the clean-reopen cold runs are the real first-use evidence.
- V2.37 a list generator that writes per spec must catch per spec: one failing spec killed the job after earlier clips were saved.
- V2.37 a chain's wait loop that searches process command lines for 'v237_ab.sh' (PowerShell) matched its OWN command line and waited
  forever; killing a chain shell leaves its A/B loop running as an orphan - stop the A/B loop too and wait for an empty job queue.
- V2.37 a phase-binned family that passed at 30 FPS slid 15-20 cm at 60/120 FPS: in the first ~0.08 s after entry the search re-picked a
  NEW bin at clip time 0 on consecutive frames (P04 -> P16 -> P05 ...). Only the FPS table caught it - always run 60/120 before promoting a
  binned family. Lever tested without restarts: database copies with another continuing_pose_cost_bias (dbcopy237_bias.py) swapped in via
  the ABP database variable (-10 only shortened the hopping, -25 held the first bin); then the production property, clean reopen, verify.
- V2.37 sheet235.ps1 `-Step` is in FRAMES (int): `-Step 0.1` rounds to 0 and loops forever - use 3 for 0.1 s at 30 fps.
- V2.38 harness `abp_flags` write the ABP class defaults in the editor -> the ABPs are DIRTY after any candidate run; a graph installer
  must reload them from disk first (its dirty check allows exactly ABP base + child + the profile DAs), otherwise it refuses - and an
  installer that failed half-way leaves its earlier steps in memory: resume with a keep flag, never reload a class BP holding them.
- V2.38 node lookup by type id alone is ambiguous in big graphs (5 SetVelocity, 2 SetSHM_Family): anchor on the exec chain of a known
  node, or patch every match on purpose; `Less_DoubleDouble` / `Add_VectorVector` resolve to promotable operators (qa_graph refuses) -
  use InRange / MakeVector forms.
- V2.38 wait loops: grep for a line-anchored marker (`^C1_DONE`) - `C1_DONE` also matched an earlier `JC1_DONE`.
- V2.38 a guard patch installed AFTER the broad regression set was only re-checked on its own family (walk); the final clean-reopen set
  then showed it had silenced reversals (j35_rev 6 -> 34 cm, e29 6 -> 44). Every patch after the last broad regression needs the broad
  set again before it counts as final; and before calling a table row a regression, diff clip / clip time / capsule per frame against
  the counter-run - cross-session runs with identical knobs can enter the loop half a cycle apart (different later bins) and planted
  balls differ by up to 4 cm with identical clips (j36_sside).

- V2.39 the editor is localized: node type ids read 'Dal' (Branch) / 'Matematik|Boolean|ANDBoolean' - match by pin names / sources
  (a Condition pin fed by GetX), never by English type-id words. A builder that `exec`s inside a loop clobbers the caller's globals
  (`V`) - prefix request variables. A clip writer that rebuilds keys also strips notify tracks: every database that held the clip needs
  its BranchIn rebuilt afterwards. A manifest that lists a guard-rejected (never created) asset is refused - list saved assets only.
- V2.39 a 20 s `timeout` around an A/B call killed the shell but the PIE run it had queued still ran: check the job folder and wait for
  `qa_pie.done` before the next job. A summary line cut at N characters hid the `ok` flag - print the verdict FIRST.
- V2.39 MM behaviour questions are answered with ONE-variable telemetry (a call counter in `Update_MotionMatching`, the selected DB per
  frame) before patching: three plausible patches (search gate, alternating force, short blend) changed nothing; the counter showed the
  function ran every frame and isolated the throttle.

- V2.40 CRITICAL: `disconnect((node, 'execute'))` removes ALL incoming exec links of that node. Splicing a step in front of a node that
  is the join of a branch's then / else (or a cast's CastFailed) cut the other paths - the rest of SHM_Snapshot stopped on every normal
  frame and the V2.38 cut route failed in EVERY run, production included (knob-gated patches do not protect the exec chain itself).
  Splice by reading `src((node, 'execute'))` first and re-adding every other predecessor; after ANY snapshot splice run a production
  behaviour gate (a production cut must still route: `SHM238_Cut` frames > 0) before tests - a structural verify passes a dead chain.

- V2.40 `Update_MotionMatching` (and the AnimGraph pin bindings) are THREAD-SAFE: `TryGetPawnOwner` / `GetVelocity` there is a compile
  ERROR (the job did not save; the dirty package is reloaded by the next job's guard). Compute game-state reads in `SHM_Snapshot` (game
  thread) into a member variable and only READ the variable in the thread-safe graph.
- V2.40 a forced database switch (SetDatabaseToSearch ForceInterrupt) is silently ignored while the redirect hold throttles the search -
  it fired at 120 FPS and not at 30 (same scene). Any new forced switch must also release `SearchThrottleTime` for its frame(s).
- V2.40 querying a pin that does not exist (`src((node, 'PickA'))`) raises AssertionError inside qa_graph - never probe pin names by
  trial in a list comprehension; read `info(node).input_pins` first.

## Acceptance test (run once per new runner version)
`Saved/Codex/SHME_V233_20261027/run233_gates2.sh`: T1 owner, T2 measure save, T3 no manifest, T4 outside manifest, T5 write during PIE,
T6 write after PIE, T7 bypass save of an unlisted created asset (GUARD_WRITTEN), T8 listed cleanup. 2026-10-27: all 8 as expected.

## Rollback
Restore the manifest's backup copies (`Saved/Codex/SHME_V233_20261027/checkpoint/manifests/<name>/Content/...`) with the editor closed;
the manifest JSON lists file, sha1 before and backup path per package. Runner rollback: `b2runner/runner_v2_pre233.py`.

## Evidence version
Tables compare only runs of one build: record the build in the chain (`RELAUNCH` / `TEL_BUILT` markers) and never mix labels across
a rebuild; a same-session interleaved repeat decides, cross-session numbers only inform.
