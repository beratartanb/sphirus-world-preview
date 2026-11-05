# Epic MCP direct calls log (2026-11-05)

Brief: `Tools/ClaudeUnreal_20261105/direct_test_brief.md`

## Result: STOPPED before step A

Brief rule: "If those tools are missing, stop and report."
This session has no `mcp__unreal-mcp__*` tools, so no direct call was made. Nothing below counts as a direct Claude MCP call.

Cause: the session started outside the project folder and moved in afterwards, so `.mcp.json` was not loaded.
- `ToolSearch` for `mcp__unreal-mcp__list_toolsets`, `describe_toolset`, `call_tool`: no match.
- `session_connectors_status`: `unreal-mcp` not listed (only claude-artifacts, Claude Docs, Gmail, scheduled-tasks).

## Editor state at stop (19:52)
| Check | Result | Route |
|---|---|---|
| `UnrealEditor.exe` | PID 51872, started 19:18:18, log `epic_1.log` | tasklist / Get-Process |
| Port 8000 | owned by PID 51872 | Get-NetTCPConnection |
| MCP `ping` | HTTP 200 | plain HTTP POST, not a Claude MCP tool |
| Lock | `LOCKED owner=epiconly 2026-11-05 19:18`, not released | `lock233.sh status` |
| `tools/list` | 3 meta-tools: `list_toolsets`, `describe_toolset`, `call_tool` | `umcp.py`, helper client, diagnostic only |
| `list_toolsets` | answered, 52 toolsets by a regex count of the text (notes say 53; difference not investigated) | `umcp.py`, helper client, diagnostic only |
| `get_current_level` | `/Game/GraceRanger/Maps/L_GR_SphirusHouse` | `umcp.py`, helper client, diagnostic only |

All helper client calls were read-only and were made for the session start probe, not for the brief.

## Steps
| Step | Status | Evidence |
|---|---|---|
| A. Read | NOT_TESTED | direct tools missing |
| B. Widget edit and image | NOT_TESTED | direct tools missing |
| C. PCG on the open test map | NOT_TESTED | direct tools missing |
| D. Save and reopen | NOT_TESTED | direct tools missing |

Start text: not read in this session. Start `treeDensity`: not read in this session.
No asset, map or widget was changed. No PIE, no save, no editor restart. Editor left open, lock held.

## To resume
Start a new session in the project folder with the editor open, confirm the `mcp__unreal-mcp__*` tools appear, then run the brief from step A.

---

# Run 2: direct `mcp__unreal-mcp__*` session (started 19:59, project folder, editor open)

The section above is the earlier stopped attempt, kept as written. This session has the three direct tools. Guide used: `.agents/skills/sphirus-editor-automation-mcp/references/claude-unreal-tooling.md` (path from `CLAUDE.md` > Unreal tooling), plus `.mcp.json`. Lock at start: `LOCKED owner=epiconly 2026-11-05 19:18`. Editor PID 51872.

| Time | Tool | Arguments | Short response |
|---|---|---|---|
| 20:00:13 | mcp__unreal-mcp__list_toolsets | none | answered; Turkish descriptions; includes SceneTools, BlueprintTools, UMGToolSet, PCGToolset, EditorAppToolset |
| 20:00:13 | mcp__unreal-mcp__describe_toolset | SceneTools | schema incl. get_current_level, load_level |
| 20:00:13 | mcp__unreal-mcp__call_tool | SceneTools.get_current_level {} | /Game/GraceRanger/Maps/L_GR_SphirusHouse |
| 20:00:49 | mcp__unreal-mcp__describe_toolset | BlueprintTools | 73,864 chars, saved by the client to a tool-results file; names read from it |
| 20:00:49 | mcp__unreal-mcp__call_tool | BlueprintTools.list_variables {blueprint: BP_GR_MaskBench} | 14 vars: GR_Stage, GR_TaskHeader, GR_TaskData, GR_JournalData, GR_HasItemData, GR_FinishedMask, GR_FinishedRag, GR_BoundRag, GR_PlaceData, GR_TwTo, GR_TwRun, GR_StartTaskData, GR_StartHeader, GR_InspectData |
| 20:00:49 | mcp__unreal-mcp__call_tool | BlueprintTools.get_graph {EventGraph} | ref ...BP_GR_MaskBench:EventGraph |
| 20:00:49 | mcp__unreal-mcp__call_tool | BlueprintTools.find_nodes {entry_points_only:true} | 10 entry nodes |
| 20:00:49 | mcp__unreal-mcp__call_tool | BlueprintTools.get_node_infos {K2Node_CustomEvent_0} | GR_ApplyStage, exec pin then -> K2Node_IfThenElse_0 input 0 |
| 20:01:14 | mcp__unreal-mcp__describe_toolset | AssetTools | schema incl. is_dirty, load_asset |
| 20:01:14 | mcp__unreal-mcp__call_tool | AssetTools.is_dirty {L_GR_SphirusHouse} | false |
| 20:01:14 | mcp__unreal-mcp__call_tool | AssetTools.is_dirty {BP_GR_MaskBench} | false |
| 20:01:14 | mcp__unreal-mcp__call_tool | SceneTools.load_level {/Game/GraceRanger/ToolTest/L_ToolTest_PCG} | null, no error |
| 20:01:14 | mcp__unreal-mcp__call_tool | SceneTools.get_current_level {} | /Game/GraceRanger/ToolTest/L_ToolTest_PCG |
| 20:01:29 | mcp__unreal-mcp__describe_toolset | ObjectTools | set_properties, get_properties, list_properties |
| 20:01:29 | mcp__unreal-mcp__describe_toolset | UMGToolSet.UMGToolSet | 60,131 chars saved to a tool-results file; CompileWidgetBlueprint(widgetBlueprint) read from it |
| 20:01:29 | mcp__unreal-mcp__call_tool | ObjectTools.get_properties {W_ToolTest_HUD:WidgetTree.TextBlock_0, [Text, Visibility]} | Text=E_KALICILIK_20261105, Visibility=Collapsed (START TEXT) |
| 20:02:19 | bash pie_shot.sh | epiconly hud_before | IMAGE images/hud_before.png, SAVEGAMES_UNCHANGED. PIE pawn BP_PBI_Player_C, runtime text E_KALICILIK_20261105 |
| 20:02:19 | Read image | images/hud_before.png | Editor window with PIE view, pause/stop bar active. White text bottom right of PIE view reads E_KALICILIK_20261105. Character back view, arms raised, black ground below horizon |
| 20:02:19 | mcp__unreal-mcp__call_tool | ObjectTools.set_properties {TextBlock_0, Text=EPIC MCP TEST 1105} | true. Sent after pie_shot.sh printed stop and exited; PIE state not queried before this one call (IsPIERunning found afterwards, false) |
| 20:02:19 | mcp__unreal-mcp__call_tool | ObjectTools.get_properties {TextBlock_0} | Text=EPIC MCP TEST 1105, Visibility=Collapsed |
| 20:02:19 | mcp__unreal-mcp__call_tool | UMGToolSet.CompileWidgetBlueprint {W_ToolTest_HUD} | true |
| 20:02:19 | mcp__unreal-mcp__describe_toolset | EditorToolset.EditorAppToolset | CaptureViewport, IsPIERunning, Get/SetCameraTransform |
| 20:02:19 | mcp__unreal-mcp__call_tool | EditorAppToolset.IsPIERunning {} | false |
| 20:03:03 | bash pie_shot.sh | epiconly hud_changed | IMAGE images/hud_changed.png, SAVEGAMES_UNCHANGED. Runtime text EPIC MCP TEST 1105 |
| 20:03:03 | Read image | images/hud_changed.png | Same PIE view, bottom right text reads EPIC MCP TEST 1105. Status bar shows 1 Kaydedilmedi (1 unsaved) |
| 20:03:03 | mcp__unreal-mcp__call_tool | EditorAppToolset.IsPIERunning {} | false |
| 20:03:03 | mcp__unreal-mcp__call_tool | ObjectTools.set_properties {TextBlock_0, Text=E_KALICILIK_20261105} | true |
| 20:03:03 | mcp__unreal-mcp__call_tool | ObjectTools.get_properties {TextBlock_0} | Text=E_KALICILIK_20261105, Visibility=Collapsed |
| 20:03:03 | mcp__unreal-mcp__call_tool | UMGToolSet.CompileWidgetBlueprint {W_ToolTest_HUD} | true |
| 20:03:37 | bash pie_shot.sh | epiconly hud_restored | IMAGE images/hud_restored.png, SAVEGAMES_UNCHANGED. Runtime text E_KALICILIK_20261105 |
| 20:03:37 | Read image | images/hud_restored.png | Same PIE view, bottom right text reads E_KALICILIK_20261105 again. Status bar 1 Kaydedilmedi |
| 20:03:37 | mcp__unreal-mcp__describe_toolset | PCGToolset.PCGToolset | ListGraphInstances, Get/SetGraphInstanceParams, ExecuteGraphInstance, GetGraphSchema, GetGraphStructure |
| 20:03:53 | mcp__unreal-mcp__call_tool | EditorAppToolset.IsPIERunning {} | false |
| 20:03:53 | mcp__unreal-mcp__call_tool | PCGToolset.ListGraphInstances {} | 1: TT_PCGForest_blurdnf2kwwb3_2146316066, graph PCG_ToolTest_Forest |
| 20:03:53 | mcp__unreal-mcp__call_tool | PCGToolset.GetGraphInstanceParams {volume} | treeDensity=0.03 (START treeDensity; returned as 0.029999999999999999) |
| 20:03:53 | mcp__unreal-mcp__call_tool | EditorAppToolset.GetCameraTransform {} | loc -191.7, 27.9, -66237.6, rot 0,0,0 |
| 20:03:53 | mcp__unreal-mcp__call_tool | ActorTools.get_transform {volume} | ERROR Unknown tool get_transform. My mistake: name guessed without describe_toolset. No effect on the editor |
| 20:04:32 | mcp__unreal-mcp__describe_toolset | ActorTools | get_actor_transform, get_actor_bounds |
| 20:04:32 | mcp__unreal-mcp__call_tool | ActorTools.get_actor_bounds {volume} | min -2260,-2266,-700 max 2609,2506,3185 |
| 20:04:32 | mcp__unreal-mcp__call_tool | EditorAppToolset.CaptureViewport {loc -3500,-3500,2500; rot pitch -27 yaw 45; annotations all 0, classFilter Actor; bShowUI false} | Direct call returned 3,058,715 chars, the client wrote them to a tool-results file; base64 decoded to images/pcg_before.png (2,293,832 bytes, cam matches pose, fov 90). capd.py not needed |
| 20:04:32 | Read image | images/pcg_before.png | Editor camera. Grey ground plane, tight cluster of pine trees inside the orange volume box, 2 rocks visible, small ground cover near the front edge |
| 20:04:32 | run_v2.sh pcg_check.py (brief-specified runner job, measure) | epic_chk 120 | OK. Trees 6+13+6=25, stones 2+3=5, ground cover 171+156=327, no_ground 0, max gap 0 cm. Copied to pcg_counts_before.json |
| 20:05:39 | mcp__unreal-mcp__call_tool | PCGToolset.SetGraphInstanceParams {treeDensity 0.06} | true |
| 20:05:39 | mcp__unreal-mcp__call_tool | PCGToolset.GetGraphInstanceParams {volume} | treeDensity=0.06 |
| 20:05:39 | mcp__unreal-mcp__call_tool | PCGToolset.ExecuteGraphInstance {volume} | [] (no messages) |
| 20:05:39 | mcp__unreal-mcp__call_tool | EditorAppToolset.CaptureViewport {same pose} | saved by client; decoded to images/pcg_after.png (cam matches) |
| 20:05:39 | run_v2.sh pcg_check.py | epic_chk 120 | Counts IDENTICAL to before: trees 25, stones 5, cover 327. Copied to pcg_counts_after.json. Component order changed, so the graph did regenerate |
| 20:05:39 | Read image | images/pcg_after.png | Same tree positions and same 2 rocks as pcg_before; only foliage tint differs a little. 0.06 shows no visible density change |
| 20:05:39 | mcp__unreal-mcp__call_tool | PCGToolset.GetGraphStructure {PCG_ToolTest_Forest} | edge GetTreeDensity.Out -> SurfaceSampler_3.PointsPerSquaredMeter present |
| 20:05:39 | note | earlier report | 2026-11-05 report measured 0.01 -> 15 trees, 0.03 -> 25. 0.06 = 25 suggests saturation, not proven. Extra run at 0.01 added beyond the brief so that a changed count is on record; 0.06 evidence kept |
| 20:06:33 | mcp__unreal-mcp__call_tool | PCGToolset.SetGraphInstanceParams {0.01}, GetGraphInstanceParams, ExecuteGraphInstance | true; treeDensity=0.01; [] |
| 20:06:33 | mcp__unreal-mcp__call_tool | EditorAppToolset.CaptureViewport {same pose} | saved by client; decoded to images/pcg_after_0p01.png |
| 20:06:33 | run_v2.sh pcg_check.py | epic_chk 120 | trees 3+8+4=15, stones 5, cover 172+157=329. Copied to pcg_counts_after_0p01.json. Matches the earlier report's 15 |
| 20:06:33 | Read image | images/pcg_after_0p01.png | Clearly fewer trees, gaps in the middle, extra rock groups now visible where trees stood |
| 20:06:33 | mcp__unreal-mcp__call_tool | PCGToolset.SetGraphInstanceParams {0.03}, GetGraphInstanceParams, ExecuteGraphInstance | true; treeDensity=0.03; [] |
| 20:06:33 | mcp__unreal-mcp__call_tool | EditorAppToolset.CaptureViewport {same pose} | saved by client; decoded to images/pcg_restored.png |
| 20:06:33 | run_v2.sh pcg_check.py | epic_chk 120 | see pcg_counts_restored.json |
| 20:06:57 | Read image | images/pcg_restored.png | Same layout as pcg_before: dense cluster, 2 front rocks. Counts 25/5/327 equal to the start |
| 20:06:57 | mcp__unreal-mcp__call_tool | EditorAppToolset.IsPIERunning {} | false |
| 20:06:57 | mcp__unreal-mcp__call_tool | ObjectTools.set_properties {TextBlock_0, Text=EPIC_ONLY_KALICILIK_20261105} | true |
| 20:06:57 | mcp__unreal-mcp__call_tool | ObjectTools.get_properties {TextBlock_0} | Text=EPIC_ONLY_KALICILIK_20261105, Visibility=Collapsed |
| 20:06:57 | mcp__unreal-mcp__call_tool | UMGToolSet.CompileWidgetBlueprint {W_ToolTest_HUD} | true |
| 20:07:26 | bash gsave.sh | epiconly epic_hud W_ToolTest_HUD | manifest epic_hud_200657 (existing 1, new 0), save True, DIRTY [], gate 20:06:59 WRITE_END ok written W_ToolTest_HUD |
| 20:07:26 | bash gsave_map.sh | epiconly epic_map L_ToolTest_PCG | manifest epic_map_200700, save True, DIRTY [] [], gate 20:07:02 WRITE_END ok written L_ToolTest_PCG |
| 20:07:26 | mcp__unreal-mcp__call_tool | AssetTools.is_dirty {W_ToolTest_HUD} | false |
| 20:07:26 | run_v2.sh dirty.py | epic_dirty 60 | DIRTY [] []. PCG_ToolTest_Forest sha1 7e0a8a84... equals the checkpoint |
| 20:07:26 | run_v2.sh quit.py (control) | epic_quit 30 | OK, quit. Log before restart: epic_1.log, PID 51872 |
| 20:08:10 | tasklist | UnrealEditor.exe | gone |
| 20:08:15 | bash v2_editor_launch.sh (background) | epic_2 | RUNNER_READY epic_2.log at 20:10:37, PID 46756. Also printed THROTTLE err module 'unreal' has no attribute 'EditorPerformanceSettings' |
| 20:11 | mcp__unreal-mcp__call_tool | SceneTools.get_current_level {} | /Game/GraceRanger/Maps/L_GR_SphirusHouse. Direct tools work after the restart with no client change by me |
| 20:11 | mcp__unreal-mcp__call_tool | AssetTools.load_asset {W_ToolTest_HUD} | ref W_ToolTest_HUD.W_ToolTest_HUD |
| 20:11 | mcp__unreal-mcp__call_tool | ObjectTools.get_properties {TextBlock_0} | Text=EPIC_ONLY_KALICILIK_20261105, Visibility=Collapsed |
| 20:11 | mcp__unreal-mcp__call_tool | PCGToolset.GetGraphSchema {PCG_ToolTest_Forest} | treeDensity number, "Trees per square metre" |
| 20:11 | mcp__unreal-mcp__call_tool | PCGToolset.GetGraphStructure {PCG_ToolTest_Forest} | edge GetTreeDensity.Out -> SurfaceSampler_3.PointsPerSquaredMeter still present |
| 20:11 | mcp__unreal-mcp__call_tool | AssetTools.is_dirty {L_GR_SphirusHouse} | false |
| 20:11 | mcp__unreal-mcp__call_tool | SceneTools.load_level {L_ToolTest_PCG}, get_current_level | /Game/GraceRanger/ToolTest/L_ToolTest_PCG |
| 20:11 | mcp__unreal-mcp__call_tool | PCGToolset.ListGraphInstances, GetGraphInstanceParams | same volume, treeDensity=0.03 |
| 20:12 | mcp__unreal-mcp__call_tool | AssetTools.is_dirty {L_ToolTest_PCG} | false |

## Run 2 result

Start text: `E_KALICILIK_20261105`. Start `treeDensity`: `0.03`. Saved text now: `EPIC_ONLY_KALICILIK_20261105` (start text deliberately not restored, step D sets the new one).

| Step | Status | Evidence |
|---|---|---|
| A. Read | PASS | table above; level, 14 variables, GR_ApplyStage -> K2Node_IfThenElse_0, test map opened and confirmed |
| B. Widget edit and image | PASS | `images/hud_before.png`, `hud_changed.png`, `hud_restored.png`; SAVEGAMES_UNCHANGED on all three |
| C. PCG | PASS with a note | `images/pcg_before.png`, `pcg_after.png`, `pcg_after_0p01.png`, `pcg_restored.png`; `pcg_counts_before.json`, `_after.json`, `_after_0p01.json`, `_restored.json` |
| D. Save and reopen | PASS | gate lines 20:06:59 and 20:07:02; DIRTY [] []; `restart_times.txt`, `restart_lines.txt`; post-restart reads above |

| treeDensity | Trees | Stones | Ground cover |
|---|---|---|---|
| 0.03 start | 25 | 5 | 327 |
| 0.06 (brief's changed value) | 25 | 5 | 327 |
| 0.01 (extra run) | 15 | 5 | 329 |
| 0.03 restored | 25 | 5 | 327 |

C note: 0.06 changed nothing, so on its own it would not prove the parameter works. The 0.01 run does. Why the count stops at 25 above 0.03 was not investigated.

Deviations and mistakes:
- Extra 0.01 run, beyond the brief, in memory on the test map only; returned to 0.03 before saving.
- First `set_properties` in B went out without an `IsPIERunning` check first. pie_shot.sh had printed stop and exited, and the check right after returned false. Later writes were preceded by it, or by a pie_shot.sh exit plus check.
- `ActorTools.get_transform` was a guessed name: Unknown tool, no effect.
- `dirty.py` through the runner in D4 is not named in the brief. It is read-only; MCP `is_dirty` only answers per asset, and the brief asks for no dirty package at all.
- `CaptureViewport` images came from the direct call: the client wrote the large result to a tool-results file and I decoded the base64. `capd.py` and `umcp.py` were not used.

Other findings:
- Engine is 5.8.4, CL 58902052, in both epic_1.log and epic_2.log. Notes say 5.8.1, CL 56057345. Stale notes, not caused by this test. Not edited.
- Launch printed a THROTTLE error: editor throttling was not switched off by the launch script in this editor.
- epic_2.log: 21 `Error:` lines (epic_1.log: 19), none mention ToolTest. Non-AutomationTest ones are 4 LogModelContextProtocol lines at 17:10:46-47 UTC: 1 unknown session id (the old client session after restart, client should reinitialize), 3 unknown method server/discover. The direct tools worked afterwards.

End state: editor open (PID 46756), open map `L_ToolTest_PCG`, lock held by `epiconly`. Main map, character, camera, Story Framework not changed. PCG graph file sha1 equals the checkpoint.
