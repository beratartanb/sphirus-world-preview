# m_bob7_mcp.py (MCP, in-memory edit of BP_HybridA_Player; re-appliable) - round 7. Event GR_Bob (called after GR_Contact every tick):
# writes ABP_Sph_GASP.SphBob, the additive pelvis offset applied before FootPlacement (c_bob7.py).
#  estimate of the clip pelvis (component space of the driver mesh, last evaluated frame) = socket - last written offset
#  baseline = first-order low-pass (BOB_LP 1/s) of that estimate -> follows posture / crouch / slope changes, not the step rhythm
#  offset z = -Kz x (estimate - baseline), Kz from BOB_KzWalk (<= 180 cm/s) to BOB_KzSpr (>= 585 cm/s); offset lateral (component X) =
#  -BOB_Kx x (estimate - baseline); both clamped; faded in / out (BOB_A) with ground contact, no montage, speed > 40 cm/s.
# The running flight phase is kept (lower gain at speed); nothing is pinned: half or more of the clip's own rhythm stays.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = AP + '.BP_HybridA_Player'; NL = chr(10); out = {}
GA = '/Game/Sphirus/Player/GASP/ABP_Sph_GASP'
M = '`KismetMathLibrary.%s`'
def v(n): return '(`self.%s`)' % n
def F(name, *a): return '(%s %s)' % (M % name, ' '.join(a))
def S(n, x): return '(set `self.%s` %s)' % (n, x)
L = []
L.append('(bind _dt %s)' % F('FClamp', v('GR_PDt'), '0.004', '0.05'))
L.append('(bind _ai (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)))')
L.append('(bind _sp %s)' % F('VSizeXY', '(`self.GetVelocity`)'))
L.append('(bind _pl (`SceneComponent.GetSocketTransform` (`self.Mesh`) "pelvis" "RTS_Component"))')
L.append('(bind _pz (- (.z (`KismetMathLibrary.BreakTransform` _pl)) (.z %s)))' % v('BOB_Prev'))
L.append('(bind _px (- (.x (`KismetMathLibrary.BreakTransform` _pl)) (.x %s)))' % v('BOB_Prev'))
# round 7b: only in steady gait (speed change below BOB_AccMax cm/s2, low-passed): starts, stops and gait transitions keep the clip as is
# (the damping lagged the sprint-start pelvis drop and added foot velocity jumps).
L.append(S('BOB_Acc', F('FInterpTo', v('BOB_Acc'), F('Abs', '(/ (- _sp %s) _dt)' % v('BOB_PrevSp')), '_dt', '8.0')))
L.append(S('BOB_PrevSp', '_sp'))
L.append('(bind _act (and (and (`NavMovementComponent.IsMovingOnGround` (`self.CharacterMovement`)) (not (`AnimInstance.IsAnyMontagePlaying` _ai))) (and (and (> _sp 40.0) %s) (< %s %s))))' % (v('BOB_On'), v('BOB_Acc'), v('BOB_AccMax')))
L.append(S('BOB_A', F('FInterpTo', v('BOB_A'), F('SelectFloat', '1.0', '0.0', '_act'), '_dt', '4.0')))
L.append(S('BOB_Bz', F('SelectFloat', F('FInterpTo', v('BOB_Bz'), '_pz', '_dt', v('BOB_LP')), '_pz', '(> %s 0.01)' % v('BOB_A'))))
L.append(S('BOB_Bx', F('SelectFloat', F('FInterpTo', v('BOB_Bx'), '_px', '_dt', v('BOB_LP')), '_px', '(> %s 0.01)' % v('BOB_A'))))
L.append('(bind _kz %s)' % F('MapRangeClamped', '_sp', '180.0', '585.0', v('BOB_KzWalk'), v('BOB_KzSpr')))
L.append('(bind _oz %s)' % F('FClamp', '(* (* (- 0.0 _kz) (- _pz %s)) %s)' % (v('BOB_Bz'), v('BOB_A')), '-6.0', '6.0'))
L.append('(bind _ox %s)' % F('FClamp', '(* (* (- 0.0 %s) (- _px %s)) %s)' % (v('BOB_Kx'), v('BOB_Bx'), v('BOB_A')), '-4.0', '4.0'))
L.append(S('BOB_Prev', F('MakeVector', '_ox', '0.0', '_oz')))
L.append('(bind _ag (cast `%s` _ai)' % GA)
L.append('  (:`then`')
L.append('    (set `%s.SphBob` %s _ag)))' % (GA, v('BOB_Prev')))
ev = NL + NL + '(event `GR_Bob`' + NL + NL.join('  ' + x for x in L) + ')'
if '--dry' in sys.argv: print(ev); sys.exit(0)
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n, ty in [(x, 'float') for x in ('BOB_A', 'BOB_Bz', 'BOB_Bx', 'BOB_LP', 'BOB_KzWalk', 'BOB_KzSpr', 'BOB_Kx', 'BOB_Acc', 'BOB_PrevSp', 'BOB_AccMax')] + [('BOB_On', 'bool'), ('BOB_Prev', 'vector')]:
    if '"%s"' % n in have: continue
    r = T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': ty})
    if isinstance(r, dict) and r.get('isError'): out['var_' + n] = str(r)[:200]
    T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '(event `GR_Bob`' in dsl:
    i0 = dsl.index('(event `GR_Bob`'); c = [x for x in (dsl.find(NL + NL + '(event', i0), dsl.find(NL + NL + '(fn', i0)) if x > 0]
    old = dsl[i0:min(c)] if c else dsl[i0:]; edits = [{'oldString': old.rstrip(NL), 'newString': ev.strip()}]
else:
    call = [l for l in dsl.split(NL) if l.strip() == '(`self.GR_Contact`)']; assert len(call) == 1, len(call); ind = call[0][:len(call[0]) - len(call[0].lstrip())]
    i0 = dsl.index('(event `GR_Contact`'); c = [x for x in (dsl.find(NL + NL + '(event', i0), dsl.find(NL + NL + '(fn', i0)) if x > 0]
    ce = (dsl[i0:min(c)] if c else dsl[i0:]).rstrip(NL)
    edits = [{'oldString': call[0], 'newString': call[0] + NL + ind + '(`self.GR_Bob`)'}, {'oldString': ce[-400:], 'newString': ce[-400:] + ev}]
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': edits})
out['edit'] = str(r2)[:2500] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200]
print('BOB7', json.dumps(out)[:3000])
