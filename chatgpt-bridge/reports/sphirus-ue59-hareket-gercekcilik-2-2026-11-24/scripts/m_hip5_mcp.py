# m_hip5_mcp.py (MCP, in-memory; BP_HybridA_Player GR_Bob; after m_hip4; re-appliable) - movement realism pass 2.
# The turn gate of m_hip4 removes the correction in one frame (pelvis tilt pop up to 6 deg at a turn entry). The three corrections
# (HIP_Yaw, HIP_Obl, SH_Yaw) are now rate limited: FInterpTo_Constant(previous, target, dt, HIP_Rate deg/s). 150 deg/s is above the
# fastest cyclic change they make in steady gait (~75 deg/s, sprint shoulders), so steady gait is not filtered.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = AP + '.BP_HybridA_Player'; NL = chr(10); K = '`KismetMathLibrary.%s`'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
if '"HIP_Rate"' not in have:
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': 'HIP_Rate', 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': 'HIP_Rate', 'bInstanceEditable': True})
    T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '`self.HIP_Rate`' in dsl: print('HIP5 already'); sys.exit(0)
edits = []
for C in ('HIP_Yaw', 'HIP_Obl', 'SH_Yaw'):
    pre = '(set `self.%s` ' % C; l = [x for x in dsl.split(NL) if x.strip().startswith(pre)]; assert len(l) == 1; l = l[0]; s_ = l.strip(); ind = l[:len(l) - len(l.lstrip())]; assert s_.endswith(')')
    val = s_[len(pre):-1]; assert val.startswith('(`KismetMathLibrary.FClamp`'), val[:60]
    edits.append({'oldString': l, 'newString': ind + pre + '(%s (`self.%s`) %s _returnvalue (`self.HIP_Rate`)))' % (K % 'FInterpTo_Constant', C, val)})
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('HIP5', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:2500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:160])
