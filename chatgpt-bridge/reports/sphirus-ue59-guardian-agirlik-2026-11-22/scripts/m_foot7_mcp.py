# m_foot7_mcp.py (MCP, in-memory edit of BP_HybridA_Player; re-appliable) - round 7. Event GR_Foot (called after GR_Bob every tick):
# swing-foot clearance over low obstacles for the visible body (ABP_Sph_Body_GASP FootTR/TL + FootAR/AL, c_footik7.py).
# Per foot: base = driver mesh foot bone (world, last evaluated pose; the driver is not affected by the visible-body IK, so no feedback),
#  extrapolated one frame with its own velocity. Ground under the capsule = trace straight down at the capsule. Surface under the foot =
#  trace down from 70 cm above the ground to 5 cm below it, at the extrapolated foot. If that surface is an obstacle (> FT_Min above the
#  ground under the capsule) and the foot's sole (bone - FT_Sole) is below it + FT_Clear, the foot is lifted onto it. Lift <= FT_Max.
#  Alpha eases in fast (FT_In 1/s) and out slower (FT_Out). Feet planted on top of the obstacle are already above it -> lift ~0.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = AP + '.BP_HybridA_Player'; NL = chr(10); out = {}
BA = '/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP'
M = '`KismetMathLibrary.%s`'
def v(n): return '(`self.%s`)' % n
def F(name, *a): return '(%s %s)' % (M % name, ' '.join(a))
def S(n, x): return '(set `self.%s` %s)' % (n, x)
def mv(x, y, z): return F('MakeVector', x, y, z)
L = []
L.append('(bind _dt %s)' % F('FClamp', v('GR_PDt'), '0.004', '0.05'))
L.append('(bind _loc (`self.K2_GetActorLocation`))')
L.append('(bind (_hg _bg) (`KismetSystemLibrary.LineTraceSingle` _loc (- _loc %s) "TraceTypeQuery1"))' % mv('0.0', '0.0', '160.0'))
L.append('(bind _gz %s)' % F('SelectFloat', '(.z (`.ImpactPoint` (`GameplayStatics.BreakHitResult` _hg)))', '(- (.z _loc) 92.0)', '_bg'))
L.append('(bind _on (and %s (`NavMovementComponent.IsMovingOnGround` (`self.CharacterMovement`))))' % v('FT_On'))
# round 7b: the toe reaches an obstacle before the ankle -> three samples per foot: ankle (sole 8 cm below the bone), ball (3.5 cm) and
# toe tip (ball + 0.6 x ankle->ball), all extrapolated FT_Ext frames ahead with the ankle's own motion; the lift is the largest need.
for sd, P in (('r', 'FT_PR'), ('l', 'FT_PL')):
    f = '_f' + sd; b = '_b' + sd + 'b'
    L.append('(bind %s (`SceneComponent.GetSocketLocation` (`self.Mesh`) "foot_%s"))' % (f, sd))
    L.append('(bind %s (`SceneComponent.GetSocketLocation` (`self.Mesh`) "ball_%s"))' % (b, sd))
    L.append('(bind _d%s (* (- %s %s) %s))' % (sd, f, v(P), mv(v('FT_Ext'), v('FT_Ext'), '0.0')))
    L.append(S(P, f))
    pts = (('a', '(+ %s _d%s)' % (f, sd), '(.z %s)' % f, '8.0'), ('b', '(+ %s _d%s)' % (b, sd), '(.z %s)' % b, '3.5'),
           ('t', '(+ (+ %s (* (- %s %s) %s)) _d%s)' % (b, b, f, mv('0.6', '0.6', '0.0'), sd), '(.z %s)' % b, '3.5'))
    need = []
    for k, pos, z0, sole in pts:
        L.append('(bind _p%s%s %s)' % (sd, k, pos))
        L.append('(bind (_h%s%s _k%s%s) (`KismetSystemLibrary.LineTraceSingle` %s %s "TraceTypeQuery1"))' % (sd, k, sd, k, mv('(.x _p%s%s)' % (sd, k), '(.y _p%s%s)' % (sd, k), '(+ %s 60.0)' % z0), mv('(.x _p%s%s)' % (sd, k), '(.y _p%s%s)' % (sd, k), '(- %s 30.0)' % z0)))
        L.append('(bind _z%s%s %s)' % (sd, k, F('SelectFloat', '(.z (`.ImpactPoint` (`GameplayStatics.BreakHitResult` _h%s%s)))' % (sd, k), '-100000.0', '_k%s%s' % (sd, k))))
        # round 7d: only surfaces up to FT_HMax above the ground under the capsule are stepped over / onto; a taller (knee-high) block is the
        # contact system's (stand-off, trip): lifting the swing foot onto it put the foot into its front face.
        L.append('(bind _n%s%s %s)' % (sd, k, F('SelectFloat', '(- (+ _z%s%s %s) (- %s %s))' % (sd, k, v('FT_Clear'), z0, sole), '0.0', '(and _k%s%s (< (- _z%s%s _gz) %s))' % (sd, k, sd, k, v('FT_HMax')))))
        need.append('_n%s%s' % (sd, k))
    L.append('(bind _lift%s %s)' % (sd, F('FClamp', F('FMax', need[0], F('FMax', need[1], need[2])), '0.0', v('FT_Max'))))
    # round 7c: only a swinging foot (driver contact curve > 50 = free) is lifted, and only when the surface under it is more than FT_Min
    # above its sole: the capsule stepping onto the obstacle no longer hides it (the reference was the ground under the capsule).
    L.append('(bind _need%s (and (and _on (> _lift%s %s)) (> (`AnimInstance.GetCurveValue` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)) "contact_%s") 50.0)))' % (sd, sd, v('FT_Min'), sd))
    L.append(S('FT_A' + sd.upper(), F('FInterpTo', v('FT_A' + sd.upper()), F('SelectFloat', '1.0', '0.0', '_need' + sd), '_dt', F('SelectFloat', v('FT_In'), v('FT_Out'), '_need' + sd))))
    L.append(S('FT_L' + sd.upper(), F('SelectFloat', F('FMax', '_lift' + sd, F('FInterpTo', v('FT_L' + sd.upper()), '0.0', '_dt', v('FT_Out'))), F('FInterpTo', v('FT_L' + sd.upper()), '0.0', '_dt', v('FT_Out')), '_need' + sd)))
L.append('(bind _ab (cast `%s` (`SkeletalMeshComponent.GetAnimInstance` (`self.Manny`)))' % BA)
L.append('  (:`then`')
for sd, tv, av in (('r', 'FootTR', 'FootAR'), ('l', 'FootTL', 'FootAL')):
    L.append('    (set `%s.%s` (+ _f%s %s) _ab)' % (BA, tv, sd, mv('0.0', '0.0', v('FT_L' + sd.upper()))))   # driver foot (not the IK'd visible one: no feedback)
    L.append('    (set `%s.%s` %s _ab)' % (BA, av, v('FT_A' + sd.upper())))
L[-1] = L[-1] + '))'
ev = NL + NL + '(event `GR_Foot`' + NL + NL.join('  ' + x for x in L) + ')'
if '--dry' in sys.argv: print(ev); sys.exit(0)
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for n, ty in [(x, 'float') for x in ('FT_AR', 'FT_AL', 'FT_LR', 'FT_LL', 'FT_HMax', 'FT_Min', 'FT_Sole', 'FT_Clear', 'FT_Max', 'FT_In', 'FT_Out', 'FT_Ext')] + [('FT_On', 'bool'), ('FT_PR', 'vector'), ('FT_PL', 'vector')]:
    if '"%s"' % n in have: continue
    r = T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': ty})
    if isinstance(r, dict) and r.get('isError'): out['var_' + n] = str(r)[:200]
    T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '(event `GR_Foot`' in dsl:
    i0 = dsl.index('(event `GR_Foot`'); c = [x for x in (dsl.find(NL + NL + '(event', i0), dsl.find(NL + NL + '(fn', i0)) if x > 0]
    old = dsl[i0:min(c)] if c else dsl[i0:]; edits = [{'oldString': old.rstrip(NL), 'newString': ev.strip()}]
else:
    call = [l for l in dsl.split(NL) if l.strip() == '(`self.GR_Bob`)']; assert len(call) == 1, len(call); ind = call[0][:len(call[0]) - len(call[0].lstrip())]
    i0 = dsl.index('(event `GR_Bob`'); c = [x for x in (dsl.find(NL + NL + '(event', i0), dsl.find(NL + NL + '(fn', i0)) if x > 0]
    ce = (dsl[i0:min(c)] if c else dsl[i0:]).rstrip(NL)
    edits = [{'oldString': call[0], 'newString': call[0] + NL + ind + '(`self.GR_Foot`)'}, {'oldString': ce[-300:], 'newString': ce[-300:] + ev}]
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': edits})
out['edit'] = str(r2)[:2500] if (not isinstance(r2, dict) or r2.get('isError')) else 'ok'
out['compile'] = str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200]
print('FOOT7', json.dumps(out)[:3000])
