# m_gov6b_mcp.py (MCP, in-memory): StBoost also during the re-push after a clip-bound reversal (RcExit > 0). Measured (g6b_B_30 t 15.7-16.1):
# the brake now tracks the clip (K 1.02) but the re-push accelerated with 300 cm/s2 against the clip's 730 -> the planted pivot foot was
# dragged 23 cm; StartT is not reset inside a held-input reversal, so the boost window never opened there.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
MOT = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; NL = chr(10)
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': MOT, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
l = [x for x in dsl.split(NL) if x.strip().startswith('(set `self.StBoost`')]; assert len(l) == 1; l = l[0]
a = '(and (> (`self.StartT`) 0.0) (< (`self.StartT`) (`self.StBoostDur`)))'; assert l.count(a) == 1, l.count(a)
if '(> (`self.RcExit`) 0.0)' in l: print('GOV6B already'); sys.exit(0)
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': MOT, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': l, 'newString': l.replace(a, '(or %s (> (`self.RcExit`) 0.0))' % a)}]})
print('GOV6B', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': MOT + '.AC_Sph_Motion'}, 'bWarningsAsErrors': False}))[:120])
