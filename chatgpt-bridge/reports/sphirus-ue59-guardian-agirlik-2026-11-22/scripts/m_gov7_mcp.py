# m_gov7_mcp.py (MCP, in-memory; AC_Sph_Motion; re-appliable) - round 7.
# StBoost (round 6: the capsule may follow the clip's push-off during a start) followed ANY clip: a walk start from rest jumped to 180 cm/s
# in 0.23 s at 1405 cm/s2 following the tail of a run-to-walk transition clip (md 133-160) out of the walk LOOP database. GASP's
# IsStarting (future speed >= speed + 100) was then true for 1-2 frames only, so a start database was never chosen (no push-off step).
# Now the boost only acts while the clip itself accelerates (movedata_speed rising faster than StBoostRise cm/s2) = a real start /
# re-push clip.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
MOT = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; MBP = MOT + '.AC_Sph_Motion'; NL = chr(10)
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': MBP}}))
if '"StBoostRise"' not in have:
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': MBP}, 'name': 'StBoostRise', 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': MBP}, 'variableName': 'StBoostRise', 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': MOT, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
l = [x for x in dsl.split(NL) if x.strip().startswith('(set `self.StBoost`')]; assert len(l) == 1; l = l[0]
if 'StBoostRise' in l: print('GOV7 already'); sys.exit(0)
a = '(and (> (`AnimInstance.GetCurveValue` (`SkeletalMeshComponent.GetAnimInstance` (`Character.Mesh` _ascharacter)) "movedata_speed") 5.0)'
assert l.count(a) == 1
md = '(`AnimInstance.GetCurveValue` (`SkeletalMeshComponent.GetAnimInstance` (`Character.Mesh` _ascharacter)) "movedata_speed")'
b = '(and (and (> %s (+ (`self.RcPrevC`) (* (`self.StBoostRise`) DeltaSeconds))) (> %s 5.0))' % (md, md)
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': MOT, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': l, 'newString': l.replace(a, b)}]})
print('GOV7', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': MBP}, 'bWarningsAsErrors': False}))[:120])
