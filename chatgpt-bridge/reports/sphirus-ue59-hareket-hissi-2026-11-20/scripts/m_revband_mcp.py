# m_revband_mcp.py (MCP, in-memory; saved by w_rev_save.py): reversal softening limited to the run speed band.
# Rev (0..1) lowers the ground friction (RevFricMul) while the input opposes the velocity, so the first ~0.1 s of a reversal is
# no longer an instant velocity redirect (CMC friction term, ~4000 cm/s2 at 415). A/B 2026-11-20 (U_A/U_B n1 vs rev): run A<->D
# t_rev 0.22 -> 0.38 s with the same foot drift; at walk and sprint the same switch raised drift (mean 5 -> 16 cm), so the
# speed gate is now a band RevSpLo..RevSpHi on the latched reversal speed instead of "> 60..140".
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; BP = AP + '.AC_Sph_Motion'; out = {}
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n in ('RevSpLo', 'RevSpHi'):
    if '"%s"' % n in have: continue
    out['add_' + n] = str(T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': 'float'}))[:60]
    T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
ln = [l for l in dsl.split('\n') if l.strip().startswith('(set `self.Rev` ')]; assert len(ln) == 1
old = "(`KismetMathLibrary.MapRangeClamped` (`self.RevLatch`) 60.0 140.0 0.0 1.0)"; assert ln[0].count(old) == 1
new = "(* (`KismetMathLibrary.MapRangeClamped` (`self.RevLatch`) (`self.RevSpLo`) (+ (`self.RevSpLo`) 80.0) 0.0 1.0) (`KismetMathLibrary.MapRangeClamped` (`self.RevLatch`) (`self.RevSpHi`) (+ (`self.RevSpHi`) 50.0) 1.0 0.0))"
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': ln[0], 'newString': ln[0].replace(old, new)}]})
out['edit'] = str(r2)[:900] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:120]
print('REVBAND', json.dumps(out)[:900])
