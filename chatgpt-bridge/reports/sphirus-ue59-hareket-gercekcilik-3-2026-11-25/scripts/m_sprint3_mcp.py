# m_sprint3_mcp.py (MCP, in-memory; BP_HybridA_Player GR_Posture; re-appliable) - movement realism pass 3.
# SPRINT ATTITUDE. Measured trunk inclination (pelvis -> neck from vertical, travel direction): run 12-18 deg, sprint 12-13 deg: the
# sprint loop (M_Relaxed_Sprint_Loop_F) is MORE upright than the run. The posture layer's spine targets (spine_02/03/04 terms) get a
# sprint term PS_S2/PS_S3/PS_S4 x clamp((speed - 430) / 130): the trunk inclines only at real sprint speed, distributed over three
# joints (no single fold); the existing head-level layer keeps the gaze.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); K = '`KismetMathLibrary.%s`'; V = lambda n: '(`self.%s`)' % n
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}})); ch = False
for n in ('PS_S2', 'PS_S3', 'PS_S4'):
    if '"%s"' % n not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True}); ch = True
if ch: T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '`self.PS_S2`' in dsl: print('SPRINT3 already'); sys.exit(0)
L = dsl.split(NL); i0 = [i for i, x in enumerate(L) if x.startswith('(event `GR_Posture`')][0]; i1 = [i for i, x in enumerate(L) if i > i0 and x.startswith('(event ')][0]; ev = L[i0:i1]; edits = []
for n in ('2', '3', '4'):
    a = '(* %s %s)))' % (V('PS_E' + n), V('PS_Eff')); m = [x for x in ev if x.startswith('  (bind ') and x.endswith(a) and V('PS_R' + n) in x]; assert len(m) == 1, (n, len(m))
    edits.append({'oldString': m[0], 'newString': m[0][:-len(a)] + '(+ (* %s %s) (* %s (%s (/ (- _returnvalue_17 430.0) 130.0))))))' % (V('PS_E' + n), V('PS_Eff'), V('PS_S' + n), K % 'FClamp')})
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('SPRINT3', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:2500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:160])
