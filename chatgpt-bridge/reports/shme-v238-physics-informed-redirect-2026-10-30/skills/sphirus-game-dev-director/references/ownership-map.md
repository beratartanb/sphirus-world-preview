# SPHIRUS skill ownership map

One owner per layer. When two skills touch a problem, the **owner** decides and implements; the others supply constraints or acceptance. Precedence below resolves conflicts. Paths are relative to `.agents/skills/`.

## Character, input, camera

| Layer | Owner | Consulted |
|---|---|---|
| Project locomotion/camera target feel, runtime-authority tracing, protected accepted behaviour, final character/camera acceptance (AAMS, Core Motion, PBI layer, GraceRanger camera rig/PCM, MetaHuman retarget) | `sphirus-character-camera` | all below |
| Capsule, CharacterMovement values, movement modes, speed/braking | `ue-character-and-movement` (under `sphirus-character-camera` authority) | animation |
| SHME biomechanical layer: `BP_SHM_*` component/profiles, COM/support/capture point, turn/brake/landing demand, camera-space environment perception, SHME→PBI/camera signals, SHME budgets/validation | `sphirus-human-motion-engine` (under `sphirus-character-camera` authority) | character-camera, animation, physics |
| Final pose, AnimBP, Motion Matching / PoseSearch / Chooser, montages | `ue-animation-system` | `ue-control-rig-and-ik` |
| Foot/hand IK, Control Rig, IK Retargeter | `ue-control-rig-and-ik` | animation |
| Input actions, mapping contexts, triggers/modifiers | `ue-enhanced-input` | character-camera |
| Collision channels, traces, physics bodies | `ue-physics-and-chaos` | interaction, environment |
| Character body art direction: proportions, anatomy, soft tissue, sculpt direction/review, body-under-clothing read, body skin intent, ARTIST-GRADE verdict (face identity, hair, garment construction excluded) | `character-female-body-art-direction` | asset pipeline, materials-lighting-rendering, animation, control rig |
| Character lookdev and costume/groom art direction: concept matching, groom look (shape, parting, face framing, bun, hair colour/material), skin complexion and face/body skin coherence, garment silhouette/construction/drape/textile look, character material hierarchy, character review studio, visual art gates and ARTIST-GRADE for these areas (face geometry and body anatomy excluded) | `character-lookdev-costume-groom-art-direction` | body art direction, materials-lighting-rendering, physics and Chaos, asset pipeline, animation |
| Final gameplay camera | `sphirus-character-camera` | cinematics (temporary view target only) |

Generic `ue-*` skills describe engine mechanics; `sphirus-character-camera` decides *which* project object owns a behaviour and gives the final verdict. A generic example never justifies replacing AAMS, the PBI layer, the GraceRanger camera rig/PCM or the owned profile data assets.

## Gameplay systems

| Layer | Owner | Consulted |
|---|---|---|
| GameMode/PC/Pawn/Components/Subsystems/Data Assets responsibility boundaries | `ue-gameplay-framework-architecture` | domain skill |
| Blueprint/C++ failure diagnosis, logs, crashes | `ue-blueprint-cpp-debugging` | domain skill |
| Doors, ladders, pickups, inspectables, interaction traces/prompts/alignment | `sphirus-interaction-traversal` | character-camera, animation, IK, UI |
| Persistent state, SaveGame, flags, checkpoints | `sphirus-save-state-progression` | narrative, UI |
| Scripted/world-state events, triggers, narrative flags | `sphirus-narrative-events` | save-state, cinematics |
| AI/NPC/creature behaviour | `sphirus-ai-npc-behavior` | animation, framework |
| UMG, prompts, menus, settings, accessibility | `sphirus-ui-ux-accessibility` | save-state (settings), input |
| Sequencer, cinematic ↔ gameplay handoff | `sphirus-cinematics-sequencer` | character-camera, narrative |
| Ambience, foley, attenuation, mix | `sphirus-audio-ambience` | interaction, environment |

## World and image

| Layer | Owner | Consulted |
|---|---|---|
| How a space reads to the player (spatial grammar, reveal, enclosure, lookback) | `sphirus-level-art-direction` | player-flow, visual |
| Gameplay topology: metrics, pacing, loops, interaction placement, dead space | `sphirus-level-design-player-flow` | level-art direction |
| Image intent: value, colour, material age, focal hierarchy | `sphirus-visual-art-direction` | environment art |
| Physical/technical realisation of environment (terrain, habitat, foliage placement, water, weathering, environment lighting passes) | `sphirus-environment-art` | all world skills |
| Landscape/foliage/PCG *systems*, streaming, HLOD, instancing, culling, navmesh | `sphirus-worldbuilding-pcg-streaming` | environment art |
| Rendering pipeline (Lumen, VSM, ray tracing, exposure, PP, scalability), master materials, non-environment materials | `sphirus-materials-lighting-rendering` | environment art, visual |
| Niagara atmosphere and interaction VFX | `sphirus-vfx-atmosphere-niagara` | visual, rendering, performance |
| Interior art direction: room purpose, clutter hierarchy, wear/dust, interior light language | `sphirus-interior-lived-in` | visual, rendering, interaction (logic) |
| Final visual acceptance of any environment or interior pass | `sphirus-aaa-environment-polish` | — (gate, never implements) |
| Which existing asset fits a role; asset-gap / purchase / generation decision | `sphirus-project-assets` | asset pipeline |
| Import/ingest of new assets (Blender, Meshy, FBX, MetaHuman) | `sphirus-asset-pipeline` | project assets |

Precedence for environment work: AGENTS.md → user scope → level-art/visual-art intent → environment-art implementation → AAA gate verdict. Worldbuilding and rendering skills supply technical constraints; they never overrule agreed composition. Shared contract: [reference authority](../../sphirus-level-art-direction/references/reference-authority.md).

## Cross-cutting

| Layer | Owner |
|---|---|
| Editor mutation mechanics, runner, MCP, Python, captures, Bridge export/publish | `sphirus-editor-automation-mcp` |
| Measurement methodology and bottleneck diagnosis | `sphirus-performance-profiling` (environment specifics: `sphirus-environment-art/references/performance.md`) |
| Compile/cook/package | `sphirus-build-packaging` |
| Test selection, technical PASS vs acceptance, regression matrix | `sphirus-qa-regression` (character protocol: `sphirus-character-camera/references/verification.md`; environment image gate: `sphirus-aaa-environment-polish`) |
| Checkpoints, rollback, file/asset safety | `sphirus-source-control-asset-safety` |
| Task routing | `sphirus-game-dev-director` |
| Multi-agent delegation (Claude) | `.claude/skills/sphirus-claude-orchestration` |
