# m_camykeep_mcp.py (MCP, in-memory edit of AC_Sph_Camera; save via gsave.sh) - 2026-11-19 late.
# Tight spaces: the boom-sweep fraction SafeFrac shortened the camera distance AND the shoulder (lateral) offset Y, so in a narrow
# passage the camera ended straight behind the head; with TightRaise lifting it, the head/hair then filled the lower-middle of the
# frame (an_camocc: lowmid >25 % in 3.9 % of the kitchen-passage frames, max 50 %). Y is already limited by the side probe
# (Yf <= side distance - 28 cm), so the lateral offset keeps at least YKeep of its value: Y = Y x max(SafeFrac, YKeep). YKeep 0 = old.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
BP = '/Game/Sphirus/Player/Camera/AC_Sph_Camera.AC_Sph_Camera'; AP = '/Game/Sphirus/Player/Camera/AC_Sph_Camera'; out = {}
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
out['add'] = 'exists' if '"YKeep"' in have else T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': 'YKeep', 'typeName': 'float'})
out['ie'] = T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': 'YKeep', 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']
old = "(set `self.Y` (* (`self.Y`) (`self.SafeFrac`)))"; assert rv['dsl'].count(old) == 1
new = "(set `self.Y` (* (`self.Y`) (`KismetMathLibrary.FMax` (`self.SafeFrac`) (`self.YKeep`))))"
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': old, 'newString': new}]})
out['edit'] = r2 if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
json.dump(out, open('Saved/UE59Work/dsl/camykeep_apply.json', 'w'), indent=1, default=str); print('YKEEP', json.dumps(out, default=str)[:800])
