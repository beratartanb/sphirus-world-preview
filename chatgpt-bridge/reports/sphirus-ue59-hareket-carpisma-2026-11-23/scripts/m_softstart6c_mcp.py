# m_softstart6c_mcp.py (MCP, in-memory; BP_HybridA_Player) - soft start only when the body already faces the travel direction.
# AC_Sph_Motion.StartTurn (m_softstart6b) did not separate the cases, and capping the capsule to the transition clip (GR_SoftCapT, now 0)
# made a re-facing sprint start slide 81 cm and cost the benefit. A re-facing start is recognised directly: at the first input frame the
# driver mesh root still points where the body faced (root right vector = mesh forward) while the capsule already faces the input.
# GR_SoftOK is latched in the first 0.04 s of a start: dot(mesh forward, actor forward) > GR_SoftCos.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = AP + '.BP_HybridA_Player'; MOT = '/Game/Sphirus/Player/Motion/AC_Sph_Motion'; NL = chr(10)
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n, ty in (('GR_SoftOK', 'bool'), ('GR_SoftCos', 'float')):
    if '"%s"' % n in have: continue
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': ty}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
l = [x for x in dsl.split(NL) if 'GR_SoftStartOn' in x and x.strip().startswith('(set `self.GR_GaitSel`')]; assert len(l) == 1, len(l); l = l[0]; ind = l[:len(l) - len(l.lstrip())]
if 'GR_SoftOK' in dsl: print('SOFT6C already'); sys.exit(0)
st = '(`%s.StartT` (`self.SphMotion`))' % MOT
fwd = '(`KismetMathLibrary.GetRightVector` (`SceneComponent.GetSocketRotation` (`self.Mesh`) "root"))'
latch = ind + '(set `self.GR_SoftOK` (or (and (`self.GR_SoftOK`) (> %s 0.04)) (and (<= %s 0.04) (> (`KismetMathLibrary.Dot_VectorVector` %s (`self.GetActorForwardVector`)) (`self.GR_SoftCos`)))))' % (st, st, fwd)
a = '(`self.GR_SoftStartOn`)'; assert l.count(a) == 1
new = latch + NL + l.replace(a, '(and (`self.GR_SoftStartOn`) (`self.GR_SoftOK`))')
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': l, 'newString': new}]})
print('SOFT6C', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:120])
