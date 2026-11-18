# m_turnsev_mcp.py (MCP client, in memory): TurnSev target = max(input/velocity disagreement term (unchanged), heading-rate term
# MapRangeClamped(TurnW, 30, 240 deg/s) * MapRangeClamped(speed, 60, 400)) while there is move input; then compile.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp
umcp.init()
def T(full, args):
    ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; BP = AP + '.AC_Sph_Motion'
old = '(`KismetMathLibrary.SelectFloat` (* (`KismetMathLibrary.MapRangeClamped` _returnvalue_7 0.8 -0.9 0.0 1.0) (`KismetMathLibrary.MapRangeClamped` _returnvalue_4 0.0 400.0 0.0 1.0)) 0.0 _returnvalue_8)'
new = '(`KismetMathLibrary.SelectFloat` (`KismetMathLibrary.FMax` (* (`KismetMathLibrary.MapRangeClamped` _returnvalue_7 0.8 -0.9 0.0 1.0) (`KismetMathLibrary.MapRangeClamped` _returnvalue_4 0.0 400.0 0.0 1.0)) (* (`KismetMathLibrary.MapRangeClamped` (`self.TurnW`) 30.0 240.0 0.0 1.0) (`KismetMathLibrary.MapRangeClamped` _returnvalue_4 60.0 400.0 0.0 1.0))) 0.0 _returnvalue_8)'
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']
n = rv['dsl'].count(old); print('OLD_COUNT', n); assert n == 1
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': old, 'newString': new}]})
print('EDIT', 'ok' if not r2.get('isError') else json.dumps(r2)[:800])
print('COMPILE', json.dumps(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:300])
r3 = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); d = r3['content']['returnValue']['dsl']
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Saved', 'UE59Work', 'dsl', 'ac_motion_after.dsl'), 'w', encoding='utf8').write(d)
print('AFTER has slope', d.count('SlopeLean'), 'turnw-term', d.count('(`self.TurnW`) 30.0 240.0'))
