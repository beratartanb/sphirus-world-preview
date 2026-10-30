# SPHIRUS project invariants

Short, durable rules every skill inherits. Domain detail lives in the owning skill. AGENTS.md and the current user request outrank this file.

1. **Actual project is the source of truth.** Current editor/world state > saved packages > dated evidence > documentation > memory. Old reports, delivery JSONs, bindings CSVs and scripts are history, never proof of current wiring.
2. **Trace authority before adding.** Find the object that already owns a behaviour; extend it through project-owned layers. No parallel controller, camera, save system, event bus or manager because it is easier than tracing.
3. **Preserve user work.** The current house scene (`/Game/GraceRanger/Maps/L_GR_SphirusHouse` with `L_GR_CurrentHouseContent`), its architecture, interior, materials and atmosphere are user-authored. Never replay historical scene-building scripts or restore old maps over current edits.
4. **Vendor originals stay untouched.** Tune through project-owned copies/instances (e.g. `/Game/GraceRanger/Environment/Exterior20260921/`, `/Game/SphirusHouse/LivedIn_R05/`, `/Game/GraceRanger/Profiles/`).
5. **Checkpoint → mutate → verify → report.** Reversible checkpoint before any asset/map mutation; see `sphirus-source-control-asset-safety`. No git repository exists in the project root (checked 2026-09-24).
6. **Scope discipline.** Research/audit/skill tasks authorize no save, compile, PIE, export or publish. A request for one zone/system is not permission for global edits.
7. **Evidence labels.** PASS only for directly observed current evidence; FAIL for observed defects; PARTIAL/REVIEW_REQUIRED for incomplete or ambiguous; NOT_TESTED for unrun checks. Compile/save/export success is not gameplay or visual acceptance.
8. **Technical pass ≠ acceptance.** Motion, camera and environment work also needs game-feel/visual acceptance from the owning domain.
9. **Measure, don't guess, performance.** Baseline → measurement → bottleneck → targeted change → re-measurement. Never raise streaming/memory budgets or suppress warnings to claim a fix.
10. **Character identity.** Physically readable human motion: weight transfer, momentum, braking, recovery, support steps, pelvis/torso counter-reaction, grounded jumps. No arbitrary wobble, slow motion or camera shake to fake weight. Owner: `sphirus-character-camera`.
11. **Environment identity.** Enclosed Woodland Refuge; old lived-in house on a knoll above an enlarged woodland pond (never enlarge again); forest as enclosing volume; natural paths; no open vista. Owners: AGENTS.md + art-direction skills.
12. **No invented facts.** Never invent asset paths, plugin state, Blueprint ownership or implementation state; verify on disk or in the editor and label the freshness.
