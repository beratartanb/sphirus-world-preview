# m_ctbrake_mcp.py (MCP, in-memory edit of AC_Sph_Motion) - 2026-11-22 round 5.
# The anticipation cap (CtCap) lowered the max speed before a surface, but with the input held the capsule brakes with only 500 cm/s2
# (+ friction), so a run still reached the wall at 216 cm/s (ct_wall_run). While CtCap is active the braking deceleration is at least
# CtBrake (default set by c_motion5_defaults.py), so the capsule can follow the comfortable brake curve.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; BP = AP + '.AC_Sph_Motion'; out = {}; NL = chr(10)
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
if '"CtBrake"' not in have:
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': 'CtBrake', 'typeName': 'float'})
    T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': 'CtBrake', 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
assert '`self.CtBrake`' not in dsl, 'already built'
L = [l for l in dsl.split(NL) if l.strip().startswith('(set `self.RevDecel`')]; assert len(L) == 1
old = '(`self.DmDecel`)))'; assert L[0].rstrip().endswith(old), L[0][-80:]
new = '(`KismetMathLibrary.FMax` (`self.DmDecel`) (`KismetMathLibrary.SelectFloat` (`self.CtBrake`) 0.0 (< (`self.CtCap`) 9000.0)))))'
l2 = L[0].rstrip()[:-len(old)] + new
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': L[0], 'newString': l2}]})
out['edit'] = str(r2)[:1500] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200]
print('CTBRAKE', json.dumps(out)[:2000])
