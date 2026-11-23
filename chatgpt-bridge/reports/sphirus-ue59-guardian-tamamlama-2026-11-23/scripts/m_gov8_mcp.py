# m_gov8_mcp.py (MCP, in-memory; AC_Sph_Motion; re-appliable) - round 8.
# Round 7 raised the early reversal brake floor RcMin 150 -> 750 for the RUN reversal (pivot clip; without it Motion Matching fell back to
# the forward run loop for 0.5 s). A/B (ab8.sh, planU_B 30 Hz): the same floor made the SPRINT -> back case, which plays a stop clip and
# then a back start, brake harder than its stop clip -> right foot 2.1 -> 16.5 cm slide. The floor now depends on the entry speed:
# RcMinSpr above RcMinV cm/s (sprint entries keep the clip-bound brake), RcMin below it.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
MOT = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; MBP = MOT + '.AC_Sph_Motion'; NL = chr(10)
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': MBP}}))
for n in ('RcMinSpr', 'RcMinV'):
    if '"%s"' % n not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': MBP}, 'name': n, 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': MBP}, 'variableName': n, 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': MOT, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
l = [x for x in dsl.split(NL) if x.strip().startswith('(set `self.RcA`')]; assert len(l) == 1, len(l); l = l[0]
if 'RcMinSpr' in l: print('GOV8 already'); sys.exit(0)
a = '(`self.RcMin`) (> (`self.RcT`) (`self.RcTz`)))'; assert l.count(a) == 1, l.count(a)
b = '(`KismetMathLibrary.SelectFloat` (`self.RcMinSpr`) (`self.RcMin`) (> (`self.RcVin`) (`self.RcMinV`))) (> (`self.RcT`) (`self.RcTz`)))'
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': MOT, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': l, 'newString': l.replace(a, b)}]})
print('GOV8', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': MBP}, 'bWarningsAsErrors': False}))[:120])
