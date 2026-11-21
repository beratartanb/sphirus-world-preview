# m_maskgrip_mcp.py (MCP, in-memory edit of BP_GR_MaskBench) - 2026-11-22 round 5.
# The mask keeps the world offset it had to the right hand at the moment of the take (hand in front of the mask's face), so during the
# inspection the fingers of both hands covered the face of the mask (r5_maskE t9). During the inspection phase the mask is now eased to
# the point between the two wrists, GR_GripF cm forward (between the palms) and GR_GripZ cm up, so the hands hold it by its side edges.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/GraceRanger/SF/MaskJob/BP_GR_MaskBench'; BP = AP + '.BP_GR_MaskBench'; out = {}; NL = chr(10)
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n in ('GR_GripF', 'GR_GripZ'):
    if '"%s"' % n in have: continue
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': 'float'})
    T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
assert 'GR_GripF' not in dsl, 'already built'
open('Saved/UE59Work/dsl/maskbench_before_grip.dsl', 'w', encoding='utf8').write(dsl)
i0 = dsl.index('(event `GR_Tick3`'); first = dsl[i0:].split(NL)[1]; assert first.strip().startswith('(bind (_deltax _deltay)'), first[:60]
M = '`KismetMathLibrary.%s`'
def sock(b): return '(`SceneComponent.GetSocketLocation` (`self.GR_Body`) "%s")' % b
mid = '(* (+ %s %s) (%s 0.5 0.5 0.5))' % (sock('hand_r'), sock('hand_l'), M % 'MakeVector')
fwd = '(* (`self.GetActorForwardVector` (`self.GR_Char`)) (%s (`self.GR_GripF`) (`self.GR_GripF`) (`self.GR_GripF`)))' % (M % 'MakeVector')
tgt = '(+ (+ %s %s) (%s 0.0 0.0 (`self.GR_GripZ`)))' % (mid, fwd, M % 'MakeVector')
st = '  (`SceneComponent.K2_SetWorldLocation` (`self.StaticMesh`) (%s (`SceneComponent.K2_GetComponentLocation` (`self.StaticMesh`)) %s (`GameplayStatics.GetWorldDeltaSeconds`) 8.0) false true)' % (M % 'VInterpTo', tgt)
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': '(event `GR_Tick3`' + NL + first, 'newString': '(event `GR_Tick3`' + NL + first + NL + st}]})
out['edit'] = str(r2)[:1800] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200]
print('MASKGRIP', json.dumps(out)[:2600])
