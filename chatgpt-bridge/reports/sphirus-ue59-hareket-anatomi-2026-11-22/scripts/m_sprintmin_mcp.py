# m_sprintmin_mcp.py (MCP, in-memory edit of BP_HybridA_Player) - 2026-11-22 round 5.
# The sprint gait engaged only above 250 cm/s (literal), so a sprint from rest began as a run start and switched to the sprint set in
# the middle of the first left stance (Run_Start_F -> Transition_Walk_to_Sprint at +0.65 s: planted foot 15-19 cm). The literal becomes
# the variable GR_SprintMinSp (default set by c_player5_defaults.py) so the sprint start clips can own the start.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = AP + '.BP_HybridA_Player'; out = {}; NL = chr(10)
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
if '"GR_SprintMinSp"' not in have:
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': 'GR_SprintMinSp', 'typeName': 'float'})
    T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': 'GR_SprintMinSp', 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
L = [l for l in dsl.split(NL) if l.strip().startswith('(set `self.GR_GaitSel`')]; assert len(L) == 1, len(L)
old = '(> (`KismetMathLibrary.VSizeXY` (`self.GetVelocity`)) 250.0) (== (`self.GR_GaitSel`) 2)'; assert L[0].count(old) == 1, L[0].count(old)
new = '(> (`KismetMathLibrary.VSizeXY` (`self.GetVelocity`)) (`self.GR_SprintMinSp`)) (== (`self.GR_GaitSel`) 2)'
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': L[0], 'newString': L[0].replace(old, new)}]})
out['edit'] = str(r2)[:1500] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200]
print('SPRINTMIN', json.dumps(out)[:2000])
