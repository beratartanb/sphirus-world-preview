# m_day_mcp.py (MCP, in-memory edits of BP_GR_DayHub + BP_GR_DayStation; saved by w_day_save.py) - 2026-11-20 round 3.
# 1 Station prompts after use: the hearth (kind 4) and the tea (kind 5) stations kept their interaction prompt ("Odun koy / Yak")
#   after the fire was lit / the tea was drunk although their gate refused every further E. GR_Apply now turns their collision
#   (= interaction trace + prompt) off when GR_Fire == 2 / GR_Tea == 2 and on again otherwise (GR_FireSt / GR_TeaSt refs).
# 2 Day change: the bed station (kind 9) only played lie-down / get-up. GR_Sleep (new hub event) runs after the bed station has
#   finished: input locked, camera fades to black, the day state resets (fire out: GR_Fire 0 and GR_FireLit false, tea 0, wardrobe
#   door closed, GR_Woke 0), state applied and saved, then the existing GR_Wake sequence (wake-up montage at the bed, outfit 0,
#   task "get ready for the day") runs while the camera fades back in. Wood / herbs / pieces already gathered are kept.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
out = {}
H = '/Game/GraceRanger/SF/Day/BP_GR_DayHub'; S = '/Game/GraceRanger/SF/Day/BP_GR_DayStation'
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': H, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
open('Saved/UE59Work/dsl/hub_before_day.dsl', 'w', encoding='utf8').write(dsl)
assert '`GR_Sleep`' not in dsl, 'already built'
a0 = "  (if (and (== (`self.GR_Fire`) 2) (not (`self.GR_FireLit`)))"
assert dsl.count(a0) == 1
add = ("  (if (`KismetSystemLibrary.IsValid` (`self.GR_FireSt`))\n"
       "    (`self.SetActorEnableCollision` (`self.GR_FireSt`) (< (`self.GR_Fire`) 2)))\n"
       "  (if (`KismetSystemLibrary.IsValid` (`self.GR_TeaSt`))\n"
       "    (`self.SetActorEnableCollision` (`self.GR_TeaSt`) (< (`self.GR_Tea`) 2)))\n")
ev = ("\n\n(event `GR_Sleep`\n"
      "  (set `self.GR_Busy` true)\n"
      "  (`Controller.SetIgnoreMoveInput` (`GameplayStatics.GetPlayerController` 0) true)\n"
      "  (`Controller.SetIgnoreLookInput` (`GameplayStatics.GetPlayerController` 0) true)\n"
      "  (`PlayerCameraManager.StartCameraFade` (`GameplayStatics.GetPlayerCameraManager` 0) 0.0 1.0 1.2 (`KismetMathLibrary.MakeColor` 0.0 0.0 0.0 1.0) false true)\n"
      "  (`KismetSystemLibrary.Delay` 1.8)\n"
      "  (set `self.GR_Fire` 0)\n"
      "  (set `self.GR_FireLit` false)\n"
      "  (set `self.GR_Tea` 0)\n"
      "  (set `self.GR_DoorOpen` false)\n"
      "  (set `self.GR_Woke` 0)\n"
      "  (set `self.GR_Days` (+ (`self.GR_Days`) 1))\n"
      "  (`self.GR_Apply`)\n"
      "  (`PlayerCameraManager.StartCameraFade` (`GameplayStatics.GetPlayerCameraManager` 0) 1.0 0.0 2.0 (`KismetMathLibrary.MakeColor` 0.0 0.0 0.0 1.0) false false)\n"
      "  (`self.GR_Wake`))")
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': H + '.BP_GR_DayHub'}}))
if '"GR_Days"' not in have:
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': H + '.BP_GR_DayHub'}, 'name': 'GR_Days', 'typeName': 'int'})
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': H, 'revision': rv['revision'], 'scope': '', 'edits': [
    {'oldString': a0, 'newString': add + a0}, {'oldString': dsl.rstrip('\n')[-200:], 'newString': dsl.rstrip('\n')[-200:] + ev}]})
out['hub'] = str(r2)[:1500] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['hub_compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': H + '.BP_GR_DayHub'}, 'bWarningsAsErrors': False}))[:200]
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': S, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
open('Saved/UE59Work/dsl/station_before_day.dsl', 'w', encoding='utf8').write(dsl)
b0 = "(`/Game/GraceRanger/SF/Day/BP_GR_DayHub.GR_Store` (`self.GR_Hub`))))))))))))))))))))))"
assert dsl.count(b0) == 1, dsl.count(b0)
b1 = ("(`/Game/GraceRanger/SF/Day/BP_GR_DayHub.GR_Store` (`self.GR_Hub`))\n"
      "                                      (if (== (`self.GR_Kind`) 9)\n"
      "                                        (`/Game/GraceRanger/SF/Day/BP_GR_DayHub.GR_Sleep` (`self.GR_Hub`)))))))))))))))))))))))")
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': S, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': b0, 'newString': b1}]})
out['station'] = str(r2)[:1500] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['st_compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': S + '.BP_GR_DayStation'}, 'bWarningsAsErrors': False}))[:200]
print('DAY', json.dumps(out)[:3000])
