# m_wakecam_mcp.py (MCP, in-memory edit of BP_GR_DayHub): the wake-up sequence blended the view to GR_Cam (GR_Day_Cam) without
# placing it: the camera actor sits at (0,0,3000) and the wake-up (new game start and after sleeping) was shown from above the
# forest. GR_Wake now places GR_Cam at GR_CamLoc looking at GR_CamAim (bedroom, values already on the hub) before the blend.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
H = '/Game/GraceRanger/SF/Day/BP_GR_DayHub'
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': H, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
L = [l for l in dsl.split('\n') if '(`PlayerController.SetViewTargetWithBlend` (`GameplayStatics.GetPlayerController` 0) (`self.GR_Cam`)' in l]; assert len(L) == 1; old = L[0]
ind = old[:len(old) - len(old.lstrip())]
new = ind + "(`self.K2_SetActorLocationAndRotation` (`self.GR_Cam`) (`self.GR_CamLoc`) (`KismetMathLibrary.FindLookAtRotation` (`self.GR_CamLoc`) (`self.GR_CamAim`)) false true)\n" + old
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': H, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': old, 'newString': new}]})
print('WAKECAM', str(r2)[:900] if r2.get('isError') else 'ok', str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': H + '.BP_GR_DayHub'}, 'bWarningsAsErrors': False}))[:150])
