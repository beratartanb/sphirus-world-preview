# m_gov6e_mcp.py (MCP, in-memory; BP_Sph_GASPCharacter.CalculateGroundFriction): the same-frame reversal friction relief (m_gov6d) only
# above 480 cm/s (sprint). At run speed (415) it made one A<->D reversal of planC1 slide 28-66 cm (h6b_C_60 / f7_C_60); before m_gov6d that
# plan's worst contact was 3.5 cm, and the sprint case (584 cm/s) is the one the relief was written for.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
GC = '/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'; MOT = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': GC, 'scope': 'CalculateGroundFriction'}); rv = r['content']['returnValue']; d = rv['dsl']
a = '(`%s.RcSpMin` (`self.SphMotion`))' % MOT; assert d.count(a) == 1, d.count(a)
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': GC, 'revision': rv['revision'], 'scope': 'CalculateGroundFriction', 'edits': [{'oldString': a, 'newString': '480.0'}]})
print('GOV6E', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1200], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': GC + '.BP_Sph_GASPCharacter'}, 'bWarningsAsErrors': False}))[:120])
