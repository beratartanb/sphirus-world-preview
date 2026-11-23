# m_fat8_mcp.py (MCP, in-memory; BP_HybridA_Player ReceiveTick; re-appliable) - round 8. FATIGUE PACE: real fatigue only trimmed the
# acceleration (AccScale). Run / sprint target speed is now scaled by (1 - GR_KFat x Fat): the pace, and with it the Motion Matching step
# rhythm, drops gradually as fatigue builds and returns as it recovers. Walk is not slowed.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = AP + '.BP_HybridA_Player'; NL = chr(10)
if '"GR_KFat"' not in json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}})):
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': 'GR_KFat', 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': 'GR_KFat', 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if 'GR_KFat' in dsl: print('FAT8 already'); sys.exit(0)
l = [x for x in dsl.split(NL) if x.strip().startswith('(set `self.SphContextSpeedScale`')]; assert len(l) == 1, len(l); l = l[0]; ind = l[:len(l) - len(l.lstrip())]
new = l + NL + ind + '(set `self.SphContextSpeedScale` (* (`self.SphContextSpeedScale`) (- 1.0 (* (`self.GR_KFat`) (`KismetMathLibrary.SelectFloat` (`/Game/Sphirus/Player/Motion/AC_Sph_Motion.Fat` (`self.SphMotion`)) 0.0 (>= (`self.GR_GaitSel`) 1))))))'
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': l, 'newString': new}]})
print('FAT8', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:120])
