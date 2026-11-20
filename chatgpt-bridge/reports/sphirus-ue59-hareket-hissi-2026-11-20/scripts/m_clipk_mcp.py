# m_clipk_mcp.py (MCP, in-memory; save via gsave): stop profile scale for high release speeds. The sprint stop now uses the Relaxed
# run stop clip (root 375 -> 0 in ~0.55 s); the capsule follows that profile scaled by release speed / ClipHiRef when the release
# speed is above ClipHiMin, instead of dropping to the clip speed at once and stopping in 0.32-0.37 s (Dense run stop).
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; BP = AP + '.AC_Sph_Motion'; out = {}
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n in ('ClipHiRef', 'ClipHiMin'):
    if '"%s"' % n in have: continue
    out['add_' + n] = str(T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': 'float'}))[:80]
    T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
ln = [l for l in dsl.split('\n') if l.strip().startswith('(set `self.BrakeDecel`')]; assert len(ln) == 1
old = "(`self.ClipPrevC`))) (`self.ClipK`))"; assert ln[0].count(old) == 1
new = "(`self.ClipPrevC`))) (`KismetMathLibrary.FMax` (`self.ClipK`) (`KismetMathLibrary.SelectFloat` (/ (`self.BrakeLatchSpeed`) (`KismetMathLibrary.FMax` (`self.ClipHiRef`) 1.0)) 0.0 (> (`self.BrakeLatchSpeed`) (`self.ClipHiMin`)))))"
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': ln[0], 'newString': ln[0].replace(old, new)}]})
out['edit'] = str(r2)[:900] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200]
print('CLIPK', json.dumps(out)[:1200])
