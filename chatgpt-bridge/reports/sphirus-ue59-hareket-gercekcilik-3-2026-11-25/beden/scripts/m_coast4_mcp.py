# m_coast4_mcp.py (MCP, in-memory; BP_HybridA_Player tick; replaces the m_coast3 trace block; re-appliable) - pass 3, B4 follow-up.
# Braking steps v2: the coast (keys released at run / sprint speed) gets a DISTANCE BUDGET measured once, when it starts:
#  - the character's capsule (radius / half height - 2 cm) is swept along the velocity over speed x CS_Look + 60 cm (walls, corners,
#    narrow passages, furniture, low obstacles that would block the body - not a single thin line);
#  - four floor probes at 1/4..4/4 of that distance check ground continuity and walkability (hit, ImpactNormal.z > CS_Walk, ground
#    within +-CS_Step of the feet): a gap, a cliff edge, the water surface (no blocking hit) or a steep slope end the usable distance;
#  - budget = min(sweep, floor) - (stop clip distance from CS_VEnd + CS_Margin). The coast runs only while the travelled distance is
#    below the budget; with no budget the character stops with the normal stop clip at once (as before pass 3).
# One episode per release (CS_Latch, reset by any move key or near rest). Any key (new move, reverse), crouch, air, a montage
# (interaction, traversal, reaction) or a reaction lock ends or prevents it. Telemetry: CS_Avail, CS_Floor, CS_Budget, CS_Dist.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); K = '`KismetMathLibrary.%s`'; V = lambda n: '(`self.%s`)' % n
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}})); ch = False
for nme in ('CS_Avail', 'CS_Floor', 'CS_Budget', 'CS_Dist', 'CS_Latch', 'CS_Margin', 'CS_Walk', 'CS_Step', 'CS_ClipDec'):
    if '"%s"' % nme not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': nme, 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': nme, 'bInstanceEditable': True}); ch = True
if ch: T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '`self.CS_Budget`' in dsl: print('COAST4 already'); sys.exit(0)
L = dsl.split(NL)
i0 = [i for i, x in enumerate(L) if x.startswith('  (if (and (and (and (> (`self.CS_On`) 0.5)')]; assert len(i0) == 1; i0 = i0[0]
i1 = [i for i in range(i0, i0 + 12) if L[i].startswith('  (set `self.CS_T` ')]; assert len(i1) == 1; i1 = i1[0]
old = NL.join(L[i0:i1]); pre = L[i0].strip()[len('(if '):]
assert pre.endswith('0.7))))'), pre[-40:]
pre = '(and %s (not (`AnimInstance.IsAnyMontagePlaying` (`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`)))))' % pre
LOC = '(`self.K2_GetActorLocation`)'; VD = '(%s (`self.GetVelocity`))' % (K % 'Vector_Normal2D'); SPD = '(%s (`self.GetVelocity`))' % (K % 'VSizeXY')
MV = lambda a, b, c: '(%s %s %s %s)' % (K % 'MakeVector', a, b, c)
LEN = '(+ (* %s %s) 60.0)' % (SPD, V('CS_Look'))
R = '(`CapsuleComponent.GetScaledCapsuleRadius` (`self.CapsuleComponent`))'; HH = '(`CapsuleComponent.GetScaledCapsuleHalfHeight` (`self.CapsuleComponent`))'
FEETZ = '(- (.z %s) %s)' % (LOC, HH)
lines = ['  (set `self.CS_Latch` (%s 0.0 %s (or (> (%s %s) 0.1) (< %s 60.0))))' % (K % 'SelectFloat', V('CS_Latch'), K % 'VSize', V('GR_RawIn'), SPD),
         '  (if (and %s (or (> %s 0.0) (< %s 0.5)))' % (pre, V('CS_T'), V('CS_Latch')),
         '    (if (<= %s 0.0)' % V('CS_T'),
         '      (bind (_cs4hit _cs4blk) (`KismetSystemLibrary.CapsuleTraceSingle` :`Start` %s :`End` (+ %s (* %s %s)) :`Radius` (- %s 2.0) :`HalfHeight` (- %s 2.0)))' % (LOC, LOC, VD, MV(LEN, LEN, LEN), R, HH),
         '      (bind (_cs4b _cs4i _cs4t _cs4dist) (`GameplayStatics.BreakHitResult` _cs4hit))',
         '      (set `self.CS_Avail` (%s _cs4dist %s _cs4blk))' % (K % 'SelectFloat', LEN)]
oks = []
for k in (1, 2, 3, 4):
    a = '(* %s %s)' % (V('CS_Avail'), '%.2f' % (k / 4.0)); st = '(+ (+ %s (* %s %s)) %s)' % (LOC, VD, MV(a, a, a), MV('0.0', '0.0', '-40.0'))
    lines.append('      (bind (_cs4f%d _cs4ok%d) (`KismetSystemLibrary.LineTraceSingle` %s (+ %s %s)))' % (k, k, st, st, MV('0.0', '0.0', '-110.0')))
    lines.append('      (bind (_cs4fb%d _cs4fi%d _cs4ft%d _cs4fd%d _cs4fl%d _cs4fp%d _cs4fn%d _cs4fin%d) (`GameplayStatics.BreakHitResult` _cs4f%d))' % ((k,) * 9))
    oks.append('(and (and _cs4ok%d (> (.z _cs4fin%d) %s)) (< (%s (- (.z _cs4fp%d) %s)) %s))' % (k, k, V('CS_Walk'), K % 'Abs', k, FEETZ, V('CS_Step')))
fl = '(%s (%s (%s (%s %s (* %s 0.75) %s) (* %s 0.5) %s) (* %s 0.25) %s) 0.0 %s)' % (K % 'SelectFloat', K % 'SelectFloat', K % 'SelectFloat', K % 'SelectFloat', V('CS_Avail'), V('CS_Avail'), oks[3], V('CS_Avail'), oks[2], V('CS_Avail'), oks[1], oks[0])
stopd = '(+ (/ (* %s %s) (* 2.0 %s)) %s)' % (V('CS_VEnd'), V('CS_VEnd'), V('CS_ClipDec'), V('CS_Margin'))
lines += ['      (set `self.CS_Floor` %s)' % fl,
          '      (set `self.CS_Budget` (%s (- (%s %s %s) %s) 0.0))' % (K % 'FMax', K % 'FMin', V('CS_Avail'), V('CS_Floor'), stopd),
          '      (set `self.CS_Dist` 0.0)',
          '      (set `self.CS_Latch` 1.0)',
          '      (set `self.CS_Clear` (> %s 1.0))' % V('CS_Budget'),
          '      (else',
          '        (set `self.CS_Dist` (+ %s (* %s DeltaSeconds)))' % (V('CS_Dist'), SPD),
          '        (set `self.CS_Clear` (< %s %s))))' % (V('CS_Dist'), V('CS_Budget')),
          '    (else',
          '      (set `self.CS_Clear` false)))']
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': old, 'newString': NL.join(lines)}]})
print('COAST4', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:3000], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:300])
