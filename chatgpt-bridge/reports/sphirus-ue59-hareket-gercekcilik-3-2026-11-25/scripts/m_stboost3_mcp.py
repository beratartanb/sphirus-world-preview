# m_stboost3_mcp.py (MCP, in-memory; AC_Sph_Motion; re-appliable) - movement realism pass 3.
# The clip-bound start acceleration (StBoost) had one ceiling (StBoostMax 1400) for standing starts and for reversal exits. A standing
# start with a turn reached walk speed in 0.15-0.18 s and Motion Matching entered the reface start clip after its first step (47 cm foot
# relocation). With a ceiling of 800 the start takes 0.37-0.47 s and the clip is entered from its beginning (worst 3.3-5.3 cm at
# 60 / 30 / variable Hz). A reversal exit needs the old ceiling (with 800 a quick A/D re-command slid 24.8 cm), so the ceiling is now
# StBoostMaxSt for standing starts and StBoostMax while RcExit > 0.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); K = '`KismetMathLibrary.%s`'; V = lambda n: '(`self.%s`)' % n
MA = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; BP = MA + '.AC_Sph_Motion'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
if '"StBoostMaxSt"' not in have:
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': 'StBoostMaxSt', 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': 'StBoostMaxSt', 'bInstanceEditable': True}); T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': MA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '`self.StBoostMaxSt`' in dsl: print('STBOOST3 already'); sys.exit(0)
m = [x for x in dsl.split(NL) if x.startswith('  (set `self.StBoost` ')]; assert len(m) == 1; l = m[0]; a = '0.0 %s)' % V('StBoostMax'); assert l.count(a) == 1
# 0 = never set -> fall back to StBoostMax
new = '0.0 (%s %s (%s %s %s (> %s 1.0)) (> %s 0.0)))' % (K % 'SelectFloat', V('StBoostMax'), K % 'SelectFloat', V('StBoostMaxSt'), V('StBoostMax'), V('StBoostMaxSt'), V('RcExit'))
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': MA, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': l, 'newString': l.replace(a, new)}]})
print('STBOOST3', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:2500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:160])
