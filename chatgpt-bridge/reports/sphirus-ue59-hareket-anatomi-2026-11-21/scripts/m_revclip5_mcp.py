# m_revclip5_mcp.py (MCP, in-memory): the clip-bound reversal starts only above RcSpMin (250 cm/s: tempo / run / sprint). At walk
# speed the slow clip-following brake kept the predicted velocity forward, the strafe direction flipped B -> F and Motion Matching
# played a Walk_Turn_180 clip for 0.4 s (planted foot 20-29 cm); the movement component's own quick walk reversal (0.18 s) is kept.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; BP = AP + '.AC_Sph_Motion'; NL = chr(10)
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
if '"RcSpMin"' not in have:
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': 'RcSpMin', 'typeName': 'float'})
    T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': 'RcSpMin', 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
SPD = '(`KismetMathLibrary.VSizeXY` (`Actor.GetVelocity` _ascharacter))'
L = [l for l in dsl.split(NL) if l.strip().startswith('(set `self.RcW`')]; assert len(L) == 1
old = '(> %s 80.0)' % SPD; assert L[0].count(old) == 1 and 'RcSpMin' not in L[0], 'RcW form'
new = '(and (> %s 80.0) (or (> (`self.RcT`) 0.0) (> %s (`self.RcSpMin`))))' % (SPD, SPD)
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': L[0], 'newString': L[0].replace(old, new)}]})
out = {'edit': str(r2)[:1500] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'}
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200]
print('REVCLIP5', json.dumps(out)[:2000])
