# m_ledge6_mcp.py (MCP, in-memory; BP_HybridA_Player; re-appliable) - ledge catch / hang / climb up / drop (pass 6).
# Clips: AAMS braced-ledge set retargeted to the driver skeleton with root motion restored (w_ledge_rtg.py, w_ledge_root.py).
# Detection (only while FALLING, i.e. after a jump or a drop; never from merely seeing a wall): wall in front (line trace from the capsule
# centre + 50 cm along the facing, LG_Reach), wall normal near horizontal; the top surface found by a downward trace just behind the wall
# face; the hang position = hands on the edge (hands 52 cm above the capsule centre, 36 cm out from the wall in the braced pose). It is taken
# only if it is within LG_Snap cm of the current capsule (no teleports to unreachable edges) and the space for the hanging body is free.
# LG_Room: a standing capsule fits on top (else climbing up is refused and she stays hanging / drops).
# States: 1 catch (FallToBracedIdle), 2 hang (Idle loop), 3 climb (Mantle, root motion, world-static collision ignored meanwhile), drop =
# release to falling with a small push off the wall and a 0.8 s re-grab cooldown. Inputs while hanging: forward or jump = climb (if LG_Room),
# backward = drop.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); BQ = chr(96)
def K(f): return BQ + 'KismetMathLibrary.' + f + BQ
def S(v): return '(' + BQ + 'self.' + v + BQ + ')'
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
V = [(n, 'float') for n in ('LG_On', 'LG_State', 'LG_T', 'LG_Cool', 'LG_Jump', 'LG_Room', 'LG_Reach', 'LG_Up', 'LG_Snap', 'LG_HandUp', 'LG_HandBack', 'LG_Dist', 'LG_N2')] + [(n, 'Vector') for n in ('LG_N', 'LG_P', 'LG_C')]
for n, ty in V:
    if '"%s"' % n not in have:
        r = T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': n, 'typeName': ty})
        if r.get('isError'): print('var ERR', n, str(r)[:200])
        T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': n, 'bInstanceEditable': True})
T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '(set `self.LG_State` 1.0)' in dsl: print('LG6 already'); sys.exit()
L = dsl.split(NL); edits = []
LD = '/Game/Sphirus/Player/Anim/Ledge/SphL_AS_Ledge_Braced_'
def clip(n): return '"%s%s.SphL_AS_Ledge_Braced_%s"' % (LD, n, n)
AI = '(`SkeletalMeshComponent.GetAnimInstance` (`self.Mesh`))'
def play(n, bi, loops, ind): return ind + '(`AnimInstance.PlaySlotAnimationAsDynamicMontage` %s %s "DefaultSlot" %s 0.2 1.0 %s -1.0 0.0)' % (AI, clip(n), bi, loops)
A = '(`Actor.K2_GetActorLocation` self)'; F = '(`Actor.GetActorForwardVector` self)'; UP = '(%s 0.0 0.0 1.0)' % K('MakeVector')
start = '(+ %s (%s 0.0 0.0 50.0))' % (A, K('MakeVector'))
blk = [
 '  (set `self.LG_Cool` (- (`self.LG_Cool`) DeltaSeconds))',
 '  (if (and (and (> (`self.LG_On`) 0.5) (< (`self.LG_State`) 0.5)) (and (and (`NavMovementComponent.IsFalling` (`self.CharacterMovement`)) (<= (`self.LG_Cool`) 0.0)) (< (`self.FL_State`) 0.5)))',
 '    (bind (_lgw _lgwok) (`KismetSystemLibrary.LineTraceSingle` %s (+ %s (* %s (`self.LG_Reach`)))))' % (start, start, F),
 '    (if (and _lgwok (< (%s (.z (`.ImpactNormal` (`GameplayStatics.BreakHitResult` _lgw)))) 0.3))' % K('Abs'),
 '      (set `self.LG_N` (`.ImpactNormal` (`GameplayStatics.BreakHitResult` _lgw)))',
 '      (bind (_lgt _lgtok) (`KismetSystemLibrary.LineTraceSingle` (+ (- (`.ImpactPoint` (`GameplayStatics.BreakHitResult` _lgw)) (* (`self.LG_N`) 12.0)) (* %s (`self.LG_Up`))) (- (- (`.ImpactPoint` (`GameplayStatics.BreakHitResult` _lgw)) (* (`self.LG_N`) 12.0)) (* %s 70.0))))' % (UP, UP),
 '      (if (and _lgtok (> (.z (`.ImpactNormal` (`GameplayStatics.BreakHitResult` _lgt))) 0.7))',
 '        (set `self.LG_P` (`.ImpactPoint` (`GameplayStatics.BreakHitResult` _lgt)))',
 '        (set `self.LG_C` (%s (+ (.x (`.ImpactPoint` (`GameplayStatics.BreakHitResult` _lgw))) (* (.x (`self.LG_N`)) (`self.LG_HandBack`))) (+ (.y (`.ImpactPoint` (`GameplayStatics.BreakHitResult` _lgw))) (* (.y (`self.LG_N`)) (`self.LG_HandBack`))) (- (.z (`self.LG_P`)) (`self.LG_HandUp`))))' % K('MakeVector'),
 '        (set `self.LG_Dist` (%s (- (`self.LG_C`) %s)))' % (K('VSize'), A),
 '        (bind (_lgc _lgcok) (`KismetSystemLibrary.CapsuleTraceSingle` (+ (`self.LG_C`) (* (`self.LG_N`) 5.0)) (+ (`self.LG_C`) (* (`self.LG_N`) 6.0)) 25.0 60.0))',
 '        (if (and (< (`self.LG_Dist`) (`self.LG_Snap`)) (not _lgcok))',
 '          (bind (_lgr _lgrok) (`KismetSystemLibrary.CapsuleTraceSingle` (+ (- (`self.LG_P`) (* (`self.LG_N`) 45.0)) (%s 0.0 0.0 95.0)) (+ (- (`self.LG_P`) (* (`self.LG_N`) 46.0)) (%s 0.0 0.0 95.0)) 30.0 86.0))' % (K('MakeVector'), K('MakeVector')),
 '          (set `self.LG_Room` (%s 0.0 1.0 _lgrok))' % K('SelectFloat'),
 '          (`CharacterMovementComponent.SetMovementMode` (`self.CharacterMovement`) "MOVE_Flying" 0)',
 '          (`CharacterMovementComponent.StopMovementImmediately` (`self.CharacterMovement`))',
 '          (`Actor.K2_SetActorLocation` self (`self.LG_C`) false true)',
 '          (`Actor.K2_SetActorRotation` self (%s 0.0 0.0 (%s (* (.y (`self.LG_N`)) -1.0) (* (.x (`self.LG_N`)) -1.0))) false)' % (K('MakeRotator'), K('DegAtan2')),
 play('FallToBracedIdle', '0.12', '1', '          '),
 '          (set `self.LG_T` 0.0)',
 '          (set `self.LG_Jump` 0.0)',
 '          (set `self.LG_State` 1.0)))))',
 '  (if (> (`self.LG_State`) 0.5)',
 '    (set `self.LG_T` (+ (`self.LG_T`) DeltaSeconds))',
 '    (set `self.LG_N2` (%s (`self.GR_RawIn`) %s))' % (K('Dot_VectorVector'), F),
 '    (if (and (< (`self.LG_State`) 1.5) (> (`self.LG_T`) 1.05))',
 play('Idle', '0.2', '999', '      '),
 '      (set `self.LG_State` 2.0))',
 '    (if (and (> (`self.LG_State`) 1.5) (< (`self.LG_State`) 2.5))',
 '      (if (and (or (> (`self.LG_N2`) 0.5) (> (`self.LG_Jump`) 0.5)) (> (`self.LG_Room`) 0.5))',
 '        (`PrimitiveComponent.SetCollisionResponseToChannel` (`self.CapsuleComponent`) "ECC_WorldStatic" "ECR_Ignore")',
 play('Mantle', '0.1', '1', '        '),
 '        (set `self.LG_T` 0.0)',
 '        (set `self.LG_State` 3.0)',
 '        (elif (< (`self.LG_N2`) -0.5)',
 '          (`AnimInstance.StopSlotAnimation` %s 0.25 "DefaultSlot")' % AI,
 '          (`CharacterMovementComponent.SetMovementMode` (`self.CharacterMovement`) "MOVE_Falling" 0)',
 '          (`Character.LaunchCharacter` self (* (`self.LG_N`) 120.0) true true)',
 '          (set `self.LG_Cool` 0.8)',
 '          (set `self.LG_State` 0.0))))',
 '    (if (and (> (`self.LG_State`) 2.5) (> (`self.LG_T`) 2.05))',
 '      (`PrimitiveComponent.SetCollisionResponseToChannel` (`self.CapsuleComponent`) "ECC_WorldStatic" "ECR_Block")',
 '      (`CharacterMovementComponent.SetMovementMode` (`self.CharacterMovement`) "MOVE_Walking" 0)',
 '      (set `self.LG_Cool` 0.5)',
 '      (set `self.LG_State` 0.0)))']
t = [i for i, x in enumerate(L) if x.startswith('  (if (and (> (`self.FL_Fire`) 0.5) (< (`self.FL_State`) 0.5))')]; assert len(t) == 1, t
edits.append({'oldString': L[t[0]], 'newString': NL.join(blk) + NL + L[t[0]]})
j = [i for i, x in enumerate(L) if x.startswith('(event `EnhancedInput|/Game/Sphirus/Player/Input/IA_Sph_Jump`')][0]
k = j + 1
while not L[k].strip().startswith('(:`Started`'): k += 1
edits.append({'oldString': L[k] + NL + L[k + 1], 'newString': L[k] + NL + '    (set `self.LG_Jump` (`KismetMathLibrary.SelectFloat` 1.0 (`self.LG_Jump`) (> (`self.LG_State`) 1.5)))' + NL + L[k + 1]})
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('LG6', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:3000])
print('LG6 compile', str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:300])
