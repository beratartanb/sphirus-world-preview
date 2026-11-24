# m_flip9b_mcp.py (MCP, in-memory; re-appliable) - round 9: the flip-frame opening acceleration gets its own variable AC_Sph_Motion.RcOpen
# (m_flip9 used RcMin). RcOpen sets how long the first predicted stop is, i.e. how early in the turn clip Motion Matching enters.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
MA = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; MB = MA + '.AC_Sph_Motion'; AP = '/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'; BP = AP + '.BP_Sph_GASPCharacter'; NL = chr(10); out = {}
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': MB}}))
if '"RcOpen"' not in have:
    out['add'] = str(T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': MB}, 'name': 'RcOpen', 'typeName': 'float'}))[:120]
    T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': MB}, 'variableName': 'RcOpen', 'bInstanceEditable': True})
    out['compM'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': MB}, 'bWarningsAsErrors': False}))[:120]
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': 'CalculateMaxAcceleration'}); rv = r['content']['returnValue']; dsl = rv['dsl']
l = [x for x in dsl.split(NL) if x.strip().startswith('(return ')][0]
a = '(return (`KismetMathLibrary.SelectFloat` (`/Game/Sphirus/Player/Motion/AC_Sph_Motion.RcMin` (`self.SphMotion`))'
if a in l:
    r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': 'CalculateMaxAcceleration', 'edits': [{'oldString': l, 'newString': l.replace(a, a.replace('.RcMin`', '.RcOpen`'))}]})
    out['acc'] = 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:900]
else: out['acc'] = 'already' if 'RcOpen' in l else 'PATTERN? ' + l[:200]
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:120]
print('FLIP9B', json.dumps(out))
