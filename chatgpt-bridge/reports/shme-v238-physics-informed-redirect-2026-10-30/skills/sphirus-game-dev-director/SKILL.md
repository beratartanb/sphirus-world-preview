---
name: sphirus-game-dev-director
description: Entry router for any SPHIRUS Unreal game-development task (gameplay, character, camera, interaction, environment, rendering, VFX, audio, UI, save, narrative, AI, cinematics, assets, automation, performance, build, QA). Use first to classify the task, load the right specialist SPHIRUS/ue skills, establish ownership before editing, pick validation, and prevent isolated fixes that break adjacent systems.
---

# SPHIRUS game-dev director

Lightweight router. It does not solve domain problems; it composes the skills that do.

## When to use / not
Use at the start of any implementation, diagnosis or review in this project, or when a task crosses systems. Skip for a narrow follow-up inside a domain whose skill is already loaded.

## Read first
- [Project invariants](references/project-invariants.md) — always.
- [Ownership map](references/ownership-map.md) — before choosing an editing owner.
- [Systems inventory](references/systems-inventory.md) — verified facts with dates; recheck before relying on them.
- [Validation matrix](references/validation-matrix.md) — when defining acceptance.
- Root `AGENTS.md` (environment/art contract) and the current user request, which outrank all skills.

## Workflow
INSPECT → TRACE → IDENTIFY AUTHORITY → DIAGNOSE → DEFINE ACCEPTANCE → PLAN → IMPLEMENT → COMPILE → RUNTIME TEST → VISUAL/GAME-FEEL TEST (when relevant) → REGRESSION → PERFORMANCE (when relevant) → REPORT

1. Classify the task and its scope (research/audit vs authorized production). Audit scope forbids save/compile/PIE/export/publish.
2. Load the owner skill plus only the consulted skills the ownership map names. Do not load everything.
3. Trace the real project chain (editor state first, disk second) before proposing changes; record freshness.
4. Name one mutating owner per asset/file. Define rollback (`sphirus-source-control-asset-safety`).
5. Choose checks from the validation matrix; state what will remain NOT_TESTED.
6. After implementation, run the owner's validation and the regression rows for shared owners.

## Composition examples
| Task | Skills |
|---|---|
| Character turn / start-stop feel | `sphirus-character-camera` + `ue-character-and-movement` + `ue-animation-system` (+ `ue-control-rig-and-ik` for feet/hands) |
| Motion defect (slide, pop, dip, wrong family, "big" start/stop) — find the owner first | `sphirus-human-motion-engine` `references/motion-diagnosis.md` + `sphirus-character-camera` (`support-momentum-intents.md`, acceptance) + `sphirus-qa-regression` (`locomotion-visual-qa.md`) |
| Hard direction change (45/90/135/180), brake, catch / recovery step, "mechanical / locked / waits in a pose" | `sphirus-balance-recovery` (decision) + `sphirus-motion-synthesis` (content) + `sphirus-natural-motion` (procedure) + `sphirus-human-motion-engine` (contracts / routes) |
| New / corrected locomotion clip, MM coverage, transition quality | `sphirus-human-motion-engine` (`contact-authoring.md`, `mm-coverage.md`) + `ue-animation-system` + `sphirus-project-assets` (asset gap decision before any purchase) |
| Terrain / step / slope / bump / slip reactions | `sphirus-human-motion-engine` `references/environment-reactions.md` + `sphirus-character-camera` + `ue-physics-and-chaos` (traces) |
| Space sizing from motion (run-out, turn room, doorways, steps), traversal camera / FPS acceptance | `sphirus-level-design-player-flow` `references/motion-metrics-space.md` + `sphirus-level-art-direction` (wayfinding, rhythm) + `sphirus-performance-profiling` |
| Lived-in exterior / Sphirus identity check | `sphirus-environment-art` `references/lived-in-exterior.md` + `sphirus-level-art-direction` + `sphirus-visual-art-direction` |
| Camera clipping or look behaviour | `sphirus-character-camera` (+ `ue-physics-and-chaos` for traces) |
| Forest composition | `sphirus-environment-art` + `sphirus-level-art-direction` + `sphirus-visual-art-direction` + `sphirus-project-assets` |
| Forest final quality | above + `sphirus-aaa-environment-polish` + `sphirus-performance-profiling` + `sphirus-qa-regression` |
| Any environment visual task (exterior area, house exterior, shoreline, paths) | `sphirus-environment-art` + `sphirus-level-art-direction` + `sphirus-visual-art-direction` + `sphirus-project-assets` + the relevant area card (`sphirus-environment-art/references/areas/`) + `sphirus-aaa-environment-polish` (final reviewer) + `sphirus-performance-profiling` + `sphirus-qa-regression` |
| Interior visual task (room dressing, clutter, wear, interior light mood) | `sphirus-interior-lived-in` + `sphirus-visual-art-direction` + `sphirus-project-assets` + `sphirus-materials-lighting-rendering` + `sphirus-aaa-environment-polish` + `sphirus-qa-regression` (interaction logic stays with `sphirus-interaction-traversal`) |
| Asset shortage / "need new assets" / purchase or generation question | `sphirus-project-assets` with `references/asset_gap_decision.md` (+ `sphirus-asset-pipeline` only after the decision) |
| Route readability / pacing | `sphirus-level-design-player-flow` + `sphirus-level-art-direction` |
| Dust, pollen, light shafts | `sphirus-visual-art-direction` + `sphirus-vfx-atmosphere-niagara` + `sphirus-materials-lighting-rendering` + `sphirus-performance-profiling` |
| Door / ladder / pickup | `sphirus-interaction-traversal` + `ue-gameplay-framework-architecture` (+ animation/IK, `sphirus-audio-ambience`, `sphirus-qa-regression`) |
| Female body anatomy / sculpt review, body realism, body readiness for fitted clothes, body skin realism | `character-female-body-art-direction` (+ its `references/sphirus-body-profile.md`) + `sphirus-asset-pipeline` / `sphirus-editor-automation-mcp` / `sphirus-source-control-asset-safety` only when production edits are authorized; deformation mechanics with `ue-animation-system` / `ue-control-rig-and-ik` |
| Character look vs an approved concept: hair/groom look or colour, skin complexion, garment silhouette/construction/drape/textile, "looks procedural / MetaHuman demo" | `character-lookdev-costume-groom-art-direction` (+ its `references/sphirus-guardian-profile.md`) + `character-female-body-art-direction` for the body under clothes + `sphirus-materials-lighting-rendering` for shader work + `ue-physics-and-chaos` for cloth/groom simulation + `sphirus-asset-pipeline` / `sphirus-editor-automation-mcp` / `sphirus-source-control-asset-safety` when production edits are authorized |
| Blueprint error or crash | `ue-blueprint-cpp-debugging` + domain owner |
| Import a generated/Blender asset | `sphirus-asset-pipeline` + `sphirus-project-assets` |
| Any editor mutation by script / MCP / Bridge export | `sphirus-editor-automation-mcp` + `sphirus-source-control-asset-safety` |

For Claude multi-agent delegation, load `sphirus-claude-orchestration` (Claude-only). Other agents follow their own orchestration conventions.

## Anti-patterns
- Fixing a symptom in the most convenient object instead of its owner.
- Adding a new system when an accepted one (AAMS, GraceRanger PCM, owned profiles, existing materials/foliage owners) already covers it.
- Declaring done on compile/save/export success.
- Loading every skill "to be safe" (context waste, conflicting instructions).

## Report contract
Owner(s) used; what was inspected (with freshness); what changed (paths); checks run with PASS/FAIL/PARTIAL/NOT_TESTED; technical vs acceptance verdict; cost delta when relevant; rollback location; remaining risks.
