# m_bedcam_mcp.py (MCP, in-memory edits of BP_GR_DayHub + BP_GR_DayStation; saved by a gated write job) - 2026-11-21 round 4.
# Bed camera: with the body really lying on the mattress the shoulder camera ended inside the bedding (black frame). The bed
# station (kind 9) now switches to the hub's bedside camera (GR_Cam at GR_CamLoc -> GR_CamAim, the wake view) when the lie-down
# montage starts (new hub event GR_BedCam); the existing GR_Sleep -> GR_Wake chain returns the view to the player.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
H = '/Game/GraceRanger/SF/Day/BP_GR_DayHub'; S = '/Game/GraceRanger/SF/Day/BP_GR_DayStation'; out = {}; NL = chr(10)
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': H, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '`GR_BedCam`' not in dsl:
    a = [l.strip() for l in dsl.split(NL) if 'K2_SetActorLocationAndRotation` (`self.GR_Cam`)' in l]; assert len(a) == 1, len(a)
    b = [l.strip() for l in dsl.split(NL) if 'SetViewTargetWithBlend' in l and '(`self.GR_Cam`)' in l]; assert len(b) == 1, len(b)
    l1 = a[0]; l2 = b[0]
    while l1.count(')') > l1.count('('): l1 = l1[:-1]
    while l2.count(')') > l2.count('('): l2 = l2[:-1]
    ev = NL + NL + '(event `GR_BedCam`' + NL + '  ' + l1 + NL + '  ' + l2 + ')'
    tail = dsl.rstrip(NL)[-200:]
    r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': H, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': tail, 'newString': tail + ev}]})
    out['hub'] = str(r2)[:1500] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
    out['hub_compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': H + '.BP_GR_DayHub'}, 'bWarningsAsErrors': False}))[:200]
else: out['hub'] = 'present'
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': S, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
open('Saved/UE59Work/dsl/station_before_bedcam.dsl', 'w', encoding='utf8').write(dsl)
if 'GR_BedCam' not in dsl:
    a = [l for l in dsl.split(NL) if l.strip() == '(if (> (`self.GR_AwaitAt`) 0.0)']; assert len(a) == 1, len(a)
    ind = a[0][:len(a[0]) - len(a[0].lstrip())]
    add = ind + '(if (== (`self.GR_Kind`) 9)' + NL + ind + '  (`/Game/GraceRanger/SF/Day/BP_GR_DayHub.GR_BedCam` (`self.GR_Hub`)))' + NL
    r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': S, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': a[0], 'newString': add + a[0]}]})
    out['station'] = str(r2)[:1500] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
    out['st_compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': S + '.BP_GR_DayStation'}, 'bWarningsAsErrors': False}))[:200]
else: out['station'] = 'present'
print('BEDCAM', json.dumps(out)[:3000])
