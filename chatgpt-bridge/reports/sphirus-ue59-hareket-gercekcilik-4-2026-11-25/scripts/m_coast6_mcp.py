# m_coast6_mcp.py (MCP, in-memory; BP_HybridA_Player tick; replaces the m_coast5 block; re-appliable) - movement pass 4.
# Brake assist v3.1 (fixes found on the v3 scene tests: 35 cm box treated as a step, 60 cm platform edge passed as slope, stairs
# blocked by a horizontal sweep). Every frame while the coast is a candidate or running:
#  1. FLOOR PROFILE first, along the whole look-ahead LEN = speed x CS_Look + 60: a probe at the capsule's leading edge and 10
#     probes spread over LEN. Probe k is supported when it hits a walkable surface (ImpactNormal.z > CS_Walk) whose height differs
#     from the PREVIOUS supported probe by less than CS_Step + spacing x CS_SlopeTan (a ramp or stair tread passes, a drop / gap /
#     cliff / water surface without a walkable hit fails). The usable floor ends at the last supported probe before the first failure.
#  2. The capsule SWEEP follows the measured incline (end raised by incline x LEN) and is lifted by CS_StepUp (climbable riser
#     height); a blocking hit counts only when its surface is not walkable. A knee-high box (> CS_StepUp) is therefore an obstacle,
#     stairs and ramps are not; a moving obstacle or a closing path is seen because this runs again every frame.
#  3. budget = min(sweep, floor) - CS_Margin from the CURRENT position; the coast continues while v^2/(2 CS_ClipDec) < budget.
#  4. CS_Slope = 1 when a supported probe is inclined or off the feet height -> deceleration CS_DecSlope (controlled slowing).
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); K = '`KismetMathLibrary.%s`'; V = lambda n: '(`self.%s`)' % n
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}})); ch = False
for nme, ty in (('CS_StepUp', 'float'), ('CS_Zp', 'float'), ('CS_Last', 'float'), ('CS_FlDone', 'bool'), ('CS_Incl', 'float')):
    if '"%s"' % nme not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': nme, 'typeName': ty}); ch = True
        if ty == 'float': T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': nme, 'bInstanceEditable': True})
if ch: T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '(set `self.CS_FlDone` true)' in dsl: print('COAST6 already'); sys.exit(0)
assert '`self.CS_Slope`' in dsl, 'coast5 block expected'
L = dsl.split(NL)
i0 = [i for i, x in enumerate(L) if x.startswith('  (set `self.CS_Latch` ')]; assert len(i0) == 1; i0 = i0[0]
i1 = [i for i in range(i0, i0 + 60) if L[i].startswith('  (set `self.CS_T` ')]; assert len(i1) == 1; i1 = i1[0]
old = NL.join(L[i0:i1]); ifl = L[i0 + 1].strip(); tail = ' (or (> (`self.CS_T`) 0.0) (< (`self.CS_Latch`) 0.5)))'; assert ifl.endswith(tail)
pre = ifl[len('(if (and '):-len(tail)]
LOC = '(`self.K2_GetActorLocation`)'; VD = '(%s (`self.GetVelocity`))' % (K % 'Vector_Normal2D'); SPD = '(%s (`self.GetVelocity`))' % (K % 'VSizeXY')
MV = lambda a, b, c: '(%s %s %s %s)' % (K % 'MakeVector', a, b, c)
LEN = '(+ (* %s %s) 60.0)' % (SPD, V('CS_Look'))
R = '(`CapsuleComponent.GetScaledCapsuleRadius` (`self.CapsuleComponent`))'; HH = '(`CapsuleComponent.GetScaledCapsuleHalfHeight` (`self.CapsuleComponent`))'
FEETZ = '(- (.z %s) %s)' % (LOC, HH)
lines = ['  (set `self.CS_Latch` (%s 0.0 %s (or (> (%s %s) 0.1) (< %s 60.0))))' % (K % 'SelectFloat', V('CS_Latch'), K % 'VSize', V('GR_RawIn'), SPD),
         '  (if (and %s (or (> %s 0.0) (< %s 0.5)))' % (pre, V('CS_T'), V('CS_Latch')),
         '    (set `self.CS_Zp` %s)' % FEETZ, '    (set `self.CS_Last` 0.0)', '    (set `self.CS_FlDone` false)', '    (set `self.CS_Slope` 0.0)']
fr = ['R'] + ['%.1f' % (k / 10.0) for k in range(1, 11)]
for k, f in enumerate(fr):
    a = R if f == 'R' else '(* %s %s)' % (LEN, f)
    sp_ = R if f == 'R' else '(* %s 0.1)' % LEN
    st = '(+ (+ %s (* %s %s)) %s)' % (LOC, VD, MV(a, a, a), MV('0.0', '0.0', '(- 80.0 %s)' % HH))
    lines.append('    (bind (_c6f%d _c6ok%d) (`KismetSystemLibrary.LineTraceSingle` %s (+ %s %s)))' % (k, k, st, st, MV('0.0', '0.0', '-200.0')))
    lines.append('    (bind (_c6fb%d _c6fi%d _c6ft%d _c6fd%d _c6fl%d _c6fp%d _c6fn%d _c6fin%d) (`GameplayStatics.BreakHitResult` _c6f%d))' % ((k,) * 9))
    ok = '(and (and (and _c6ok%d (> (.z _c6fin%d) %s)) (< (%s (- (.z _c6fp%d) %s)) (+ %s (* %s %s)))) (not %s))' % (k, k, V('CS_Walk'), K % 'Abs', k, V('CS_Zp'), V('CS_Step'), sp_, V('CS_SlopeTan'), V('CS_FlDone'))
    lines += ['    (if %s' % ok,
              '      (if (or (< (.z _c6fin%d) 0.985) (> (%s (- (.z _c6fp%d) %s)) 4.0))' % (k, K % 'Abs', k, FEETZ),
              '        (set `self.CS_Slope` 1.0))',
              '      (set `self.CS_Zp` (.z _c6fp%d))' % k,
              '      (set `self.CS_Last` %s)' % a,
              '      (else',
              '        (set `self.CS_FlDone` true)))']
lines += ['    (set `self.CS_Floor` (%s %s %s %s))' % (K % 'SelectFloat', V('CS_Last'), LEN, V('CS_FlDone')),
          '    (set `self.CS_Incl` (%s (/ (- %s %s) (%s %s 1.0)) -0.6 0.8))' % (K % 'FClamp', V('CS_Zp'), FEETZ, K % 'FMax', V('CS_Last')),
          '    (bind (_c6hit _c6blk) (`KismetSystemLibrary.CapsuleTraceSingle` :`Start` (+ %s %s) :`End` (+ (+ (+ %s %s) (* %s %s)) %s) :`Radius` (- %s 2.0) :`HalfHeight` (- (- %s (* %s 0.5)) 2.0)))' % (
              LOC, MV('0.0', '0.0', '(* %s 0.5)' % V('CS_StepUp')), LOC, MV('0.0', '0.0', '(* %s 0.5)' % V('CS_StepUp')), VD, MV(LEN, LEN, LEN), MV('0.0', '0.0', '(* %s %s)' % (V('CS_Incl'), LEN)), R, HH, V('CS_StepUp')),
          '    (bind (_c6b _c6i _c6t _c6dist _c6l _c6ip _c6n _c6in) (`GameplayStatics.BreakHitResult` _c6hit))',
          '    (set `self.CS_Avail` (%s _c6dist %s (and _c6blk (< (.z _c6in) %s))))' % (K % 'SelectFloat', LEN, V('CS_Walk')),
          '    (set `self.CS_Budget` (%s (- (%s %s %s) %s) 0.0))' % (K % 'FMax', K % 'FMin', V('CS_Avail'), V('CS_Floor'), V('CS_Margin')),
          '    (set `self.CS_Dist` (%s 0.0 (+ %s (* %s DeltaSeconds)) (<= %s 0.0)))' % (K % 'SelectFloat', V('CS_Dist'), SPD, V('CS_T')),
          '    (set `self.CS_Latch` 1.0)',
          '    (set `self.CS_Clear` (< (/ (* %s %s) (* 2.0 %s)) %s))' % (SPD, SPD, V('CS_ClipDec'), V('CS_Budget')),
          '    (else',
          '      (set `self.CS_Clear` false)))']
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': old, 'newString': NL.join(lines)}]})
print('COAST6', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:3000], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:300])
