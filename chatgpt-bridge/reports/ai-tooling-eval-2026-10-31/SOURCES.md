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

## Added in v2 (2026-10-31)
- **Unreal Sensei video:** "How to Make Games in Unreal Engine 5 with AI", https://www.youtube.com/watch?v=R_HFCPd5eAw
  - The metadata and the description (including chapters) were read. No transcript was available: the caption endpoints returned 404 or were refused, and in the built-in browser the player showed "subtitles unavailable".
  - Companion asset page: https://www.unrealsensei.com/asset/ai-game-starter-assets
  - PLAYBOARD: https://playboard.co/en/channel/UCue7TFlrt9FxXarpsl872Dg
- **Engine source read (UE 5.8.1):**
  - `Engine/Plugins/Experimental/ModelContextProtocol/Source/ModelContextProtocol/Private/ModelContextProtocolModule.cpp` (RefreshTools / StartServer / StopServer)
  - `.../ModelContextProtocolEditor/Private/ModelContextProtocolEditor.cpp` (OnRefreshTools → adapter re-registration)
  - `.../ModelContextProtocolToolsetRegistryAdapter.cpp`
  - `Engine/Plugins/Experimental/ToolsetRegistry/Source/ToolsetRegistry/Public/ToolsetRegistry/UToolsetRegistry.h` (ExecuteTool)
  - `Engine/Source/Developer/ScreenShotComparisonTools/Private/ImageComparer.cpp` (tolerances, AA rule, block errors, SSIM routine)
  - `Engine/Source/Developer/ScreenShotComparisonTools/Private/ScreenShotManager.cpp` (SSIM call commented out)
  - `Engine/Source/Developer/FunctionalTesting/Public/AutomationScreenshotOptions.h` (tolerance presets, noisy-feature and tonemapping defaults)
  - `Engine/Source/Developer/FunctionalTesting/Private/AutomationBlueprintFunctionLibrary.cpp` (CompareImageAgainstReference requires GIsAutomationTesting)
  - `Engine/Plugins/MovieScene/MovieRenderPipeline/MovieRenderPipeline.uplugin` (EnabledByDefault false; not in sphirus.uproject)
- **Project skills used for the design:**
  - `sphirus-aaa-environment-polish/references/{player-camera-validation,visual-acceptance,reference-comparison}.md`
  - `sphirus-level-art-direction/references/validation-and-pilot.md` (P00–P11)
