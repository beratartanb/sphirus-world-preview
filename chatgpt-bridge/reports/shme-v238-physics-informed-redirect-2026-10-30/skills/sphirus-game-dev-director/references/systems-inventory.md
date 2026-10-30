# Verified systems inventory — 2026-09-24 (file audit)

Read-only disk audit during the skill-system task. **Presence on disk is not proof of runtime use.** Recheck before relying on any row; update this file (with date) when it changes.

## Engine and project

| Fact | Evidence |
|---|---|
| Engine association `5.8`; installed build 5.8.1 CL56057345 | `sphirus.uproject`; `sphirus-character-camera/references/project-map.md` |
| Blueprint-only project (no root `Source/`) | directory listing; only `Plugins/Marketplace/Black_Eye` has `Source` |
| Project plugins: PythonScriptPlugin (Editor), ModelingToolsEditorMode, MotionWarping, AnimationWarping, PoseSearch, Chooser, MetaHuman, MetaHumanCharacter, MetaHumanGenerator, ModelContextProtocol, AllToolsets, NiagaraToolsets, PhysicsToolsets, LandscapePatch | `sphirus.uproject` |
| Marketplace plugins in project: `Black_Eye`, `GravityScatterTool` | `Plugins/Marketplace/` |
| Default and editor-startup map `/Game/GraceRanger/Maps/L_GR_SphirusHouse`; GameMode `/Game/GraceRanger/BP_GM_GR_GraceRanger` | `Config/DefaultEngine.ini` |
| RHI DX12; Lumen GI (`r.DynamicGlobalIlluminationMethod=1`) and Lumen reflections (`r.ReflectionMethod=1`); Virtual Shadow Maps on; `r.RayTracing=True` | `Config/DefaultEngine.ini` |
| Enhanced Input default classes | `Config/DefaultInput.ini` |
| No git repository at project root; no Git LFS | `git status` |
| Unreal MCP endpoint `http://127.0.0.1:8000/mcp` (Codex config); server started with `-ModelContextProtocolStartServer` or editor console | `.codex/config.toml`; `sphirus-character-camera/references/epic-mcp.md` |

## Gameplay ownership (saved-package evidence; live possession needs re-verification)

Current chain (09-21 handoff; GameMode→`BP_PBI_Player` reference re-checked on disk 2026-09-25): `BP_GM_GR_GraceRanger` → `BP_PBI_Player` → `BP_GR_Player` (AAMS/Core Motion lineage) + `BP_PC_GR_GraceRanger` → `BP_GR_InputBase`; source AnimBP = Body Inertia **Sandbox** `ABP_GR_MotionMatching`/`Base`; camera `BP_GR_Player.GR_UpdateRig` → `BP_PCM_GR_Camera`; profiles `DA_PBI_Prototype` + `DA_GR_LocomotionBehavior`. Details and tracing method: `sphirus-character-camera/references/runtime-authority.md` (`project-map.md` there is 09-15 history).

Placed interaction/house actors observed in the map (2026-09-24 editor audit): `BP_SphirusHinged_C` doors, `BP_GR_LeverDoor_C`, `BP_GR_AtticLadder_C`, `BP_SphirusVentPull_C`, `BP_GR_HomeContext_C` (`GR_HomeIdentityVolume`), `BP_GR_AtticContext_C`, `BP_Outside_Lamp_C`, `BP_SmartSharpen_C`.
Interaction source folders: `/Game/GraceRanger/Interactions/{Door,Ladder}`, `/Game/SphirusHouse/{DoorInteraction_R01,Playable_R04,LivedIn_R05}/Blueprints` — several variants (`_Final`, `_Ready`, `_Release`, `_Production`, `_Stable`). **Which variant a placed actor uses must be read from the map, not inferred from the name.** Door work was suspended by the user in earlier character tasks; confirm scope before touching doors.

## Systems present / absent on disk

| Domain | Found | Not found |
|---|---|---|
| AI | `/Game/AI_Test/BP_AI_MCP_Test` (test only) | Behavior Trees, Blackboards, StateTree assets, EQS |
| Save | AAMS tutorial `BP_SaveGame` only | project SaveGame class/schema |
| Narrative/context | `BP_GR_HomeContext`, `BP_GR_AtticContext` | narrative flag system |
| Cinematics | — | Level Sequence assets |
| UI | vendor/demo WBPs (AAMS demo, InfinityAssets, SmartSharpen) | project HUD/menu WBPs; CommonUI not enabled in uproject |
| Audio | `/Game/Audio/Foley` (AAMS foley bank, MetaSounds), `/Game/Audio/Mix` (SM_Ambient/Final/Foley/Reverb submixes), Calysto `MS_CalystoWater` | Soundscape, project ambience system |
| VFX | Sphirus atmosphere systems (`/Game/Sphirus/World/Chapter01/*/Atmosphere/NS_*`), `NS_TW_RefugeLocalAir` placed as `AD_Air_*`, `NS_R05_WindowDust`, DustBox, ForestFloor bugs, MsvFx_Ambiance_Pack | — |
| World | Landscape `EX_HouseValley_Landscape`, native foliage `InstancedFoliageActor`, Calysto PCG graphs (not proven placed), mesh water `EX_Pond_CalmSurface` | World Partition use not verified; no Water plugin body |
| Tooling | `Tools/ChatGPTBridge` (editor export), `Publish-ChatGPTBridge-v5.ps1`, `Mirror-ChatGPTBridge-ForConnector.ps1`, pass tools under `Tools/<Pass>_<date>/` | Scenario skills/configuration; Claude CLI on PATH |
