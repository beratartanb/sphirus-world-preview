# m_coast5_mcp.py (MCP, in-memory; BP_HybridA_Player tick; replaces the m_coast4 block; re-appliable) - movement pass 4.
# Brake assist v3. While the coast (keys released at run / sprint speed) is a candidate or running, EVERY FRAME:
#  - the capsule is swept along the velocity over speed x CS_Look + 60 cm, raised by CS_Step (bottom lifted) so climbable steps and the
#    floor are not obstacles; a hit counts as an obstacle only when its surface is NOT walkable (ImpactNormal.z < CS_Walk) - a walkable
#    ramp is floor. Moving obstacles and paths that close are seen because the sweep runs again each frame.
#  - floor continuity: a probe at the capsule's leading edge plus 10 probes spread over the swept length (<= 32 cm apart). A probe is
#    floor if it hits, the surface is walkable and the hit lies within +-(CS_Step + distance x CS_SlopeTan) of the feet; the usable
#    distance ends at the first failing probe (gap, cliff edge, water surface without a walkable hit, too steep).
#  - budget = min(sweep, floor) - CS_Margin; the coast continues only while the clip stop distance v^2/(2 CS_ClipDec) fits the
#    budget measured from the CURRENT position. No budget -> the normal stop clip at once.
#  - slope / stairs (a probe surface not level or not at feet height): the coast is kept but decelerates with CS_DecSlope (controlled
#    slowing) instead of CS_Dec.
# A new key, crouch, air, a montage or a reaction lock still ends it (pre-condition from m_coast4). Telemetry: CS_Avail, CS_Floor,
# CS_Budget, CS_Dist, CS_Slope.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); K = '`KismetMathLibrary.%s`'; V = lambda n: '(`self.%s`)' % n
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}})); ch = False
for nme in ('CS_Slope', 'CS_DecSlope', 'CS_SlopeTan', 'CS_V5'):
    if '"%s"' % nme not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': nme, 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': nme, 'bInstanceEditable': True}); ch = True
if ch: T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '`self.CS_Slope`' in dsl and '_c5hit' in dsl: print('COAST5 already'); sys.exit(0)
L = dsl.split(NL)
i0 = [i for i, x in enumerate(L) if x.startswith('  (set `self.CS_Latch` ')]; assert len(i0) == 1, i0; i0 = i0[0]
i1 = [i for i in range(i0, i0 + 40) if L[i].startswith('  (set `self.CS_T` ')]; assert len(i1) == 1; i1 = i1[0]
old = NL.join(L[i0:i1]); ifl = L[i0 + 1].strip(); assert ifl.startswith('(if (and '), ifl[:80]
# keep the m_coast4 pre-condition (gates) exactly: '(if (and PRE (or (> CS_T 0) (< CS_Latch 0.5)))'
tail = ' (or (> (`self.CS_T`) 0.0) (< (`self.CS_Latch`) 0.5)))'; assert ifl.endswith(tail), ifl[-120:]
pre = ifl[len('(if (and '):-len(tail)]
LOC = '(`self.K2_GetActorLocation`)'; VD = '(%s (`self.GetVelocity`))' % (K % 'Vector_Normal2D'); SPD = '(%s (`self.GetVelocity`))' % (K % 'VSizeXY')
MV = lambda a, b, c: '(%s %s %s %s)' % (K % 'MakeVector', a, b, c)
LEN = '(+ (* %s %s) 60.0)' % (SPD, V('CS_Look'))
R = '(`CapsuleComponent.GetScaledCapsuleRadius` (`self.CapsuleComponent`))'; HH = '(`CapsuleComponent.GetScaledCapsuleHalfHeight` (`self.CapsuleComponent`))'
FEETZ = '(- (.z %s) %s)' % (LOC, HH)
UP = MV('0.0', '0.0', '(* %s 0.5)' % V('CS_Step'))
lines = ['  (set `self.CS_Latch` (%s 0.0 %s (or (> (%s %s) 0.1) (< %s 60.0))))' % (K % 'SelectFloat', V('CS_Latch'), K % 'VSize', V('GR_RawIn'), SPD),
         '  (if (and %s (or (> %s 0.0) (< %s 0.5)))' % (pre, V('CS_T'), V('CS_Latch')),
         '    (bind (_c5hit _c5blk) (`KismetSystemLibrary.CapsuleTraceSingle` :`Start` (+ %s %s) :`End` (+ (+ %s %s) (* %s %s)) :`Radius` (- %s 2.0) :`HalfHeight` (- (- %s (* %s 0.5)) 2.0)))' % (LOC, UP, LOC, UP, VD, MV(LEN, LEN, LEN), R, HH, V('CS_Step')),
         '    (bind (_c5b _c5i _c5t _c5dist _c5l _c5ip _c5n _c5in) (`GameplayStatics.BreakHitResult` _c5hit))',
         '    (set `self.CS_Avail` (%s _c5dist %s (and _c5blk (< (.z _c5in) %s))))' % (K % 'SelectFloat', LEN, V('CS_Walk'))]
oks = []; slope = []
fr = ['R'] + ['%.1f' % (k / 10.0) for k in range(1, 11)]
for k, f in enumerate(fr):
    a = R if f == 'R' else '(* %s %s)' % (V('CS_Avail'), f)
    st = '(+ (+ %s (* %s %s)) %s)' % (LOC, VD, MV(a, a, a), MV('0.0', '0.0', '(- 60.0 %s)' % HH))
    lines.append('    (bind (_c5f%d _c5ok%d) (`KismetSystemLibrary.LineTraceSingle` %s (+ %s %s)))' % (k, k, st, st, MV('0.0', '0.0', '-150.0')))
    lines.append('    (bind (_c5fb%d _c5fi%d _c5ft%d _c5fd%d _c5fl%d _c5fp%d _c5fn%d _c5fin%d) (`GameplayStatics.BreakHitResult` _c5f%d))' % ((k,) * 9))
    dz = '(%s (- (.z _c5fp%d) %s))' % (K % 'Abs', k, FEETZ)
    oks.append('(and (and _c5ok%d (> (.z _c5fin%d) %s)) (< %s (+ %s (* %s %s))))' % (k, k, V('CS_Walk'), dz, V('CS_Step'), a, V('CS_SlopeTan')))
    slope.append('(and _c5ok%d (or (< (.z _c5fin%d) 0.985) (> %s 4.0)))' % (k, k, dz))
# floor = distance of the first failing probe (leading-edge probe fails -> 0)
fl = V('CS_Avail')
for k in range(10, 0, -1):
    fl = '(%s %s (* %s %.1f) %s)' % (K % 'SelectFloat', fl, V('CS_Avail'), (k - 1) / 10.0, oks[k])
fl = '(%s %s 0.0 %s)' % (K % 'SelectFloat', fl, oks[0])
slp = slope[0]
for s_ in slope[1:]: slp = '(or %s %s)' % (slp, s_)
stopd = '(/ (* %s %s) (* 2.0 %s))' % (SPD, SPD, V('CS_ClipDec'))
lines += ['    (set `self.CS_Floor` %s)' % fl,
          '    (set `self.CS_Slope` (%s 1.0 0.0 %s))' % (K % 'SelectFloat', slp),
          '    (set `self.CS_Budget` (%s (- (%s %s %s) %s) 0.0))' % (K % 'FMax', K % 'FMin', V('CS_Avail'), V('CS_Floor'), V('CS_Margin')),
          '    (set `self.CS_Dist` (%s 0.0 (+ %s (* %s DeltaSeconds)) (<= %s 0.0)))' % (K % 'SelectFloat', V('CS_Dist'), SPD, V('CS_T')),
          '    (set `self.CS_Latch` 1.0)',
          '    (set `self.CS_Clear` (< %s %s))' % (stopd, V('CS_Budget')),
          '    (else',
          '      (set `self.CS_Clear` false)))']
edits = [{'oldString': old, 'newString': NL.join(lines)}]
oc = '(set `/Game/Sphirus/Player/Motion/AC_Sph_Motion.DmCoastDec` (`KismetMathLibrary.SelectFloat` (`self.CS_Dec`) 0.0 (`self.CS_Clear`)) (`self.SphMotion`))'
assert dsl.count(oc) == 1, dsl.count(oc)
edits.append({'oldString': oc, 'newString': '(set `/Game/Sphirus/Player/Motion/AC_Sph_Motion.DmCoastDec` (`KismetMathLibrary.SelectFloat` (`KismetMathLibrary.SelectFloat` (`self.CS_DecSlope`) (`self.CS_Dec`) (> (`self.CS_Slope`) 0.5)) 0.0 (`self.CS_Clear`)) (`self.SphMotion`))'})
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('COAST5', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:3000], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:300])
