# Sources (accessed 2026-10-31)

## Web
- **Unreal Sensei:** https://www.unrealsensei.com/ (course "AI for Unreal Engine Development": in production, no syllabus) and https://www.unrealsensei.com/news (2026-07-03, "Unreal's Plans for AI and UE6 Revealed").
- **Epic Unreal MCP docs (UE 5.8):** https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor
- **UE 5.8 release coverage:** https://gamefromscratch.com/unreal-engine-5-8-released/ (2026-06-17).
- **Epic Claude Code plugin:** https://github.com/EpicGames/unreal-engine-skills-for-claude-code-plugin (v3.1.2, 2026-10-23); marketplace listing https://claude.com/marketplace/plugins/unreal-engine-skills-for-claude-code
- **Third-party `ue-*` skills:** https://github.com/quodsoler/unreal-engine-skills
- **Community MCP servers:**
  - https://github.com/chongdashu/unreal-mcp
  - https://playbooks.com/mcp/runreal-unreal-engine
  - https://gittrend.io/repo/flopperam/unreal-engine-mcp
- **Screenshot Comparison:** https://dev.epicgames.com/documentation/en-us/unreal-engine/screenshot-comparison-tool-in-unreal-engine
- **Gauntlet:** https://dev.epicgames.com/documentation/unreal-engine/gauntlet-automation-framework-overview-in-unreal-engine
- **Taking screenshots (HighResShot):** https://dev.epicgames.com/documentation/en-us/unreal-engine/taking-screenshots-in-unreal-engine
- **MoviePipelineQueueSubsystem:** https://dev.epicgames.com/documentation/unreal-engine/python-api/class/MoviePipelineQueueSubsystem (5.7 API page)
- **Image metrics:**
  - NVIDIA FLIP: https://github.com/NVlabs/flip
  - LPIPS: https://github.com/richzhang/PerceptualSimilarity

## Local (read-only)
- **Project and engine:** `sphirus.uproject`; `C:/Program Files/Epic Games/UE_5.8/Engine/Build/Build.version`.
- **Engine plugins:**
  - `Engine/Plugins/Experimental/ModelContextProtocol/ModelContextProtocol.uplugin`
  - `Engine/Plugins/Experimental/Toolsets/*`, including `EditorToolset/Source/EditorToolset/Private/EditorAppToolset.h` and `SlateInspectorToolset/.../SlateInspectorToolset.h`
- **Editor state:**
  - running editor process command line and listening ports;
  - `Saved/Logs/shmv240_jend.log` (LogModelContextProtocol lines);
  - `Saved/Config/WindowsEditor/EditorPerProjectUserSettings.ini`.
- **Earlier MCP evidence:** `Saved/Codex/LookStrafe_20260915/{toolsets.json, editor_schema.json, mcp_call.py}` (2026-09-15).
- **Agent configuration and skills:**
  - `.codex/config.toml`
  - `.agents/skills/sphirus-editor-automation-mcp/SKILL.md`
  - `.agents/skills/sphirus-character-camera/references/epic-mcp.md` (plus the `epic/` upstream copy)
  - `.agents/skills/sphirus-level-art-direction/references/reference-authority.md`
