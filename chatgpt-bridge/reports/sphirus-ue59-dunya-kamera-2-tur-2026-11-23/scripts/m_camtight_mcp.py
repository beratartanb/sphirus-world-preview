# m_camtight_mcp.py (MCP, in-memory edit of AC_Sph_Camera; save via gated write) - 2026-11-23 world pass.
# Tight interiors: the lateral (shoulder) offset is derived from HeadX so the head sits at 0.30 of the frame width everywhere. Between walls
# and in doorways (Open -> 0) the arm is short, so head and hair cover the middle-left of the frame. New float HeadXTight: the screen head
# position blends HeadXTight (Open 0) -> HeadX (Open 1); the offset stays limited by the side probe (side distance - 28 cm). HeadXTight = HeadX = old.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
BP = '/Game/Sphirus/Player/Camera/AC_Sph_Camera.AC_Sph_Camera'; AP = '/Game/Sphirus/Player/Camera/AC_Sph_Camera'; out = {}
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
out['add'] = 'exists' if '"HeadXTight"' in have else T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': 'HeadXTight', 'typeName': 'float'})
out['ie'] = T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': 'HeadXTight', 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']
open('Saved/UE59Work/dsl/camtight_before.dsl', 'w', encoding='utf8').write(rv['dsl'])
old = "(- (`self.HeadX`) (* (`self.CarryA`) 0.04))"
new = "(- (`KismetMathLibrary.Lerp` (`self.HeadXTight`) (`self.HeadX`) (`self.Open`)) (* (`self.CarryA`) 0.04))"
if rv['dsl'].count(new) == 1: out['edit'] = 'already'
else:
    assert rv['dsl'].count(old) == 1, rv['dsl'].count(old)
    r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': old, 'newString': new}]})
    out['edit'] = r2 if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r3 = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); open('Saved/UE59Work/dsl/camtight_after.dsl', 'w', encoding='utf8').write(r3['content']['returnValue']['dsl'])
json.dump(out, open('Saved/UE59Work/dsl/camtight_apply.json', 'w'), indent=1, default=str); print('CAMTIGHT', json.dumps(out, default=str)[:900])
