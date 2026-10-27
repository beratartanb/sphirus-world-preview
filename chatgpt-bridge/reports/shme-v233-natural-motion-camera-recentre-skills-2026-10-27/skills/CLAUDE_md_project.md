# SPHIRUS — Claude Code instructions

SPHIRUS is a Blueprint-only Unreal Engine 5.8 third-person game (project `sphirus.uproject`, default map `/Game/GraceRanger/Maps/L_GR_SphirusHouse`): a grounded human character (AAMS + Core Motion + MetaHuman, GraceRanger camera) in an enclosed woodland refuge around an old lived-in house above a woodland pond.

## Non-negotiables
- `AGENTS.md` (environment/art contract) and the current user request outrank every skill. Read `AGENTS.md` for any world/environment task.
- The actual project is the source of truth: current editor state > saved packages > dated evidence > documentation. Never invent asset paths, plugin state, Blueprint ownership or implementation status; verify and label freshness.
- Trace the existing owner before adding anything; no parallel controllers, cameras or systems.
- Preserve user work: the current house scene, its architecture/interior/materials, and vendor originals are not to be overwritten. Never replay historical scene-building scripts.
- No git in this project: checkpoint before any asset/map mutation (`sphirus-source-control-asset-safety`). Binary `.uasset`/`.umap` change only through the editor.
- Editor writes run only through the gated runner: write manifest + verified backup (`manifest233.py`), one lock owner (`lock233.sh`), no write / DB rebuild / PIE start while PIE runs, no stale queued jobs (`sphirus-safe-unreal-iteration`).
- Research/audit/skill tasks authorize no save, compile, PIE, export or publish.
- Verification is required after implementation; compile/save/export success is not acceptance. Report PASS/FAIL/PARTIAL/NOT_TESTED honestly and separate technical pass from visual/game-feel acceptance.

## Skills
Project skills are exposed in `.claude/skills/`. Shared skills are thin entry points to canonical files in `.agents/skills/` (also used by other agents); `sphirus-claude-orchestration` is Claude-only. Start any game-development task with `sphirus-game-dev-director`, which routes to the owning specialist skills. Locomotion actions follow `sphirus-natural-motion` (intent -> speed/support -> plan -> source -> integration -> visible body); camera behaviour follows `sphirus-camera-direction` (look -> follow -> reaction -> recentre -> collision/input audit); every editor iteration follows `sphirus-safe-unreal-iteration`. After editing a canonical skill, run `Tools/SkillSystem/sync_claude_skills.py` (use the engine Python: `C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe`).
