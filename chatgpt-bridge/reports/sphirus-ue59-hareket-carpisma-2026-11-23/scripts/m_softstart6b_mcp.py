# m_softstart6b_mcp.py (MCP, in-memory; BP_HybridA_Player) - soft start only for STRAIGHT starts.
# Final chain f7: two 30 Hz starts that begin with a 90 / 180 deg re-facing (f7_C_30 t 34.1: 43 cm, f7_Cv_30 t 11.4: 39 cm) slid because the
# walk-to-run / walk-to-sprint transition clip stays at walking speed for ~0.25 s while the capsule already accelerates (202-278 against
# the clip's 165 cm/s). Straight starts were clean in every plan. The soft start is now skipped when AC_Sph_Motion.StartTurn is set.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; MOT = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; NL = chr(10)
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
l = [x for x in dsl.split(NL) if 'GR_SoftStartOn' in x]; assert len(l) == 1, len(l); l = l[0]
if 'StartTurn' in l: print('SOFT6B already'); sys.exit(0)
a = '(`self.GR_SoftStartOn`)'; assert l.count(a) == 1
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': l, 'newString': l.replace(a, '(and (`self.GR_SoftStartOn`) (not (`%s.StartTurn` (`self.SphMotion`))))' % MOT)}]})
print('SOFT6B', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1200], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': AP + '.BP_HybridA_Player'}, 'bWarningsAsErrors': False}))[:120])
