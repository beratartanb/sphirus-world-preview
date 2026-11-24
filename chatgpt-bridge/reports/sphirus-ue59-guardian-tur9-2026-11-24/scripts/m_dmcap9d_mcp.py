# m_dmcap9d_mcp.py (MCP, in-memory; re-appliable; after m_dmcap9c) - round 9: the gait step-down ramp only applies while moving FORWARD
# (velocity within 60 deg of the actor's facing). Backward run -> backward walk has no transition clip: with the ramp the capsule stayed
# at 257 cm/s under M_Neutral_Walk_Loop_B and the foot slid 44-56 cm (r9_gait_back_60_v11 / _s1, s9). Backward keeps the old quick drop.
import json, sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
MA = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; MB = MA + '.AC_Sph_Motion'; NL = chr(10)
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': MA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
l = [x for x in dsl.split(NL) if x.strip().startswith('(set `self.DmCap` ')]; assert len(l) == 1; l = l[0]
if 'GetActorForwardVector' in l: print('DMCAP9D already'); sys.exit(0)
a = '(< (`self.GaitV`) (`self.DmWalkV`))'; assert l.count(a) == 1, l
ch = re.findall(r'\(`Actor\.GetVelocity` (_[a-z0-9_]+)\)', dsl); assert ch, 'no velocity expr'; c = ch[0]
b = '(and %s (> (`KismetMathLibrary.Dot_VectorVector` (`KismetMathLibrary.Vector_Normal2D` (`Actor.GetVelocity` %s)) (`Actor.GetActorForwardVector` %s)) 0.5))' % (a, c, c)
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': MA, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': l, 'newString': l.replace(a, b)}]})
print('DMCAP9D', c, 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': MB}, 'bWarningsAsErrors': False}))[:100])
