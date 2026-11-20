# m_mask_mcp.py (MCP, in-memory edit of BP_GR_MaskBench; saved by a gated write job) - 2026-11-21 round 4.
# Mask inspection was not readable: the station camera kept aiming at the bench (CtxTarget = bench location, weight 0.4) from
# behind the head, so the mask held in front of the chest was hidden by head, shoulder and forearm. While the mask is inspected
# (GR_P 3) the camera context now aims at the mask itself (CtxTarget = mask mesh location every tick) with the inspection framing
# GR_InB / GR_InS / GR_InH / GR_InW (boom / side / height / aim weight overrides of AC_Sph_Camera); the overrides are cleared when
# the inspection ends (put-back starts) so the other stations keep their own framing.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/GraceRanger/SF/MaskJob/BP_GR_MaskBench'; BP = AP + '.BP_GR_MaskBench'; out = {}; NL = chr(10)
CAM = '/Game/Sphirus/Player/Camera/AC_Sph_Camera'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n in ('GR_InB', 'GR_InS', 'GR_InH', 'GR_InW'):
    if '"%s"' % n in have: continue
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': 'float'})
    T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
open('Saved/UE59Work/dsl/maskbench_before_cam.dsl', 'w', encoding='utf8').write(dsl)
assert 'GR_InB' not in dsl, 'already built'
GET = '(`self.GetComponentByClass` (`GameplayStatics.GetPlayerCharacter` 0) "%s.AC_Sph_Camera_C")' % CAM
def setter(vals, ind, nm):
    L = [ind + '(bind %s (cast `%s` %s)' % (nm, CAM, GET), ind + '  (:`then`']
    for k, v in vals: L.append(ind + '    (set `%s.%s` %s %s)' % (CAM, k, v, nm))
    L[-1] += ')'
    L += [ind + '  (:`CastFailed`', ind + '    _))']
    return NL.join(L)
a = [l for l in dsl.split(NL) if l.startswith('  (set `self.GR_YawT`')]; assert len(a) == 1
on = setter([('CtxTarget', '(`SceneComponent.K2_GetComponentLocation` (`self.StaticMesh`))'), ('OvB', '(`self.GR_InB`)'), ('OvS', '(`self.GR_InS`)'),
             ('OvH', '(`self.GR_InH`)'), ('OvW', '(`self.GR_InW`)')], '  ', '_camin')
b = [l for l in dsl.split(NL) if l.strip() == '(set `self.GR_P` 4)))']; assert len(b) == 1, len(b)
ind = b[0][:len(b[0]) - len(b[0].lstrip())]
off = setter([('OvB', '0.0'), ('OvS', '0.0'), ('OvH', '0.0'), ('OvW', '0.0')], ind, '_camout')
edits = [{'oldString': a[0], 'newString': on + NL + a[0]},
         {'oldString': b[0], 'newString': off + NL + b[0]}]
if '--dry' in sys.argv: print(on); print(off); sys.exit(0)
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': edits})
out['edit'] = str(r2)[:2200] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:300]
print('MASK', json.dumps(out)[:3000])
