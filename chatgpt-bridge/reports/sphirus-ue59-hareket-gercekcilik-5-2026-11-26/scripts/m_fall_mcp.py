# m_fall_mcp.py (MCP, in-memory; BP_HybridA_Player; re-appliable) - physical fall + face-down get-up.
# Request: FL_Imp (vel-change cm/s, world) and FL_Fire = 1. State 1 (fall): the driver mesh (self.Mesh, PA_UEFN_Mannequin) goes full ragdoll
# with weak PhysicalAnimation tone (FL_OS / FL_AVS), capsule collision off, movement disabled. When the pelvis speed stays under FL_StillV
# for 0.35 s (or after FL_TMax): prone check n = (head - pelvis) x (thigh_r - thigh_l), n.z > 0 = prone (same sign as the get-up clip's
# first frame). Supine -> roll impulse on the upper body toward the front (max FL_TryMax tries, then get up anyway). Prone -> the actor is
# teleported under the pelvis, yawed so the clip's lying direction (head at 143.1 deg in component space, mesh yaw -90) matches the
# ragdoll, the face-down get-up (FL_GetUp, root motion) plays in DefaultSlot and the physics weight fades 1 -> 0 over FL_Fade (state 2).
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); BQ = chr(96)
def K(f): return BQ + 'KismetMathLibrary.' + f + BQ
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
V = [(n, 'float') for n in ('FL_Fire', 'FL_State', 'FL_T', 'FL_Still', 'FL_W', 'FL_Tries', 'FL_TryMax', 'FL_Len', 'FL_Fade', 'FL_StillV', 'FL_TMax', 'FL_OS', 'FL_AVS', 'FL_Roll', 'FL_Prone')] + [('FL_Imp', 'vector')]
for nme, ty in V:
    if '"%s"' % nme not in have:
        r = T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': nme, 'typeName': ty})
        if r.get('isError'): print('var ERR', nme, ty, str(r)[:300])
        T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': nme, 'bInstanceEditable': True})
T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '(set `self.FL_State` 1.0)' in dsl: print('FALL already'); sys.exit(0)
L = dsl.split(NL); t = [i for i, x in enumerate(L) if x.startswith('  (if (> (`self.IMP_Fire`) 0.5)')]; assert len(t) == 1, t
M = '(`self.Mesh`)'; P = '"pelvis"'; PAC = '(`self.SphPhysAnim`)'
def SL(b): return '(`SceneComponent.GetSocketLocation` %s "%s")' % (M, b)
fire = [
 '  (if (and (> (`self.FL_Fire`) 0.5) (< (`self.FL_State`) 0.5))',
 '    (`PhysicalAnimationComponent.SetSkeletalMeshComponent` %s %s)' % (PAC, M),
 '    (`PhysicalAnimationComponent.ApplyPhysicalAnimationSettingsBelow` %s %s (make `PhysicalAnimationData` false (`self.FL_OS`) (`self.FL_AVS`)) true)' % (PAC, P),
 '    (`SkeletalMeshComponent.SetAllBodiesBelowSimulatePhysics` %s %s true true)' % (M, P),
 '    (`SkeletalMeshComponent.SetAllBodiesBelowPhysicsBlendWeight` %s %s 1.0 false true)' % (M, P),
 '    (`SkeletalMeshComponent.AddImpulseToAllBodiesBelow` %s (`self.FL_Imp`) %s true true)' % (M, P),
 '    (`CharacterMovementComponent.DisableMovement` (`self.CharacterMovement`))',
 '    (`PrimitiveComponent.SetCollisionEnabled` (`self.CapsuleComponent`) "NoCollision")',
 '    (set `self.FL_T` 0.0)',
 '    (set `self.FL_Still` 0.0)',
 '    (set `self.FL_Tries` 0.0)',
 '    (set `self.FL_State` 1.0)',
 '    (set `self.FL_Fire` 0.0))']
nvec = '(%s (- %s %s) (- %s %s))' % (K('Cross_VectorVector'), SL('head'), SL('pelvis'), SL('thigh_r'), SL('thigh_l'))
dw = '(- %s %s)' % (SL('head'), SL('pelvis'))
st1 = [
 '  (if (and (> (`self.FL_State`) 0.5) (< (`self.FL_State`) 1.5))',
 '    (set `self.FL_T` (+ (`self.FL_T`) DeltaSeconds))',
 '    (set `self.FL_Still` (%s (+ (`self.FL_Still`) DeltaSeconds) 0.0 (< (%s (`PrimitiveComponent.GetPhysicsLinearVelocity` %s %s)) (`self.FL_StillV`))))' % (K('SelectFloat'), K('VSize'), M, P),
 '    (if (or (> (`self.FL_Still`) 0.35) (> (`self.FL_T`) (`self.FL_TMax`)))',
 '      (set `self.FL_Prone` (%s 1.0 0.0 (> (.z %s) 0.0)))' % (K('SelectFloat'), nvec),
 '      (if (and (< (`self.FL_Prone`) 0.5) (< (`self.FL_Tries`) (`self.FL_TryMax`)))',
 '        (`SkeletalMeshComponent.AddImpulseToAllBodiesBelow` %s (+ (* (%s (- %s %s)) (`self.FL_Roll`)) (%s 0.0 0.0 (* 0.6 (`self.FL_Roll`)))) "spine_02" true true)' % (M, K('Normal'), SL('thigh_r'), SL('thigh_l'), K('MakeVector')),
 '        (set `self.FL_Tries` (+ (`self.FL_Tries`) 1.0))',
 '        (set `self.FL_Still` 0.0)',
 '        (set `self.FL_T` 0.0)',
 '        (else',
 '          (`Actor.K2_SetActorLocation` self (%s (.x %s) (.y %s) (+ (.z %s) 74.0)) false true)' % (K('MakeVector'), SL('pelvis'), SL('pelvis'), SL('pelvis')),
 '          (`Actor.K2_SetActorRotation` self (%s 0.0 0.0 (- (%s (.y %s) (.x %s)) 53.13)) true)' % (K('MakeRotator'), K('DegAtan2'), dw, dw),
 '          (`PrimitiveComponent.SetCollisionEnabled` (`self.CapsuleComponent`) "QueryAndPhysics")',
 '          (`CharacterMovementComponent.SetMovementMode` (`self.CharacterMovement`) "MOVE_Walking" 0)',
 '          (`AnimInstance.PlaySlotAnimationAsDynamicMontage` (`SkeletalMeshComponent.GetAnimInstance` %s) "/Game/Sphirus/Player/Anim/Fall/SphF_am_InjuredBelly_DropToFloor_GetUp.SphF_am_InjuredBelly_DropToFloor_GetUp" "DefaultSlot" 0.0 0.5 1.0 1 -1.0 0.0)' % M,
 '          (set `self.FL_T` 0.0)',
 '          (set `self.FL_State` 2.0)))))']
st2 = [
 '  (if (> (`self.FL_State`) 1.5)',
 '    (set `self.FL_T` (+ (`self.FL_T`) DeltaSeconds))',
 '    (set `self.FL_W` (- 1.0 (* (* (%s (/ (`self.FL_T`) (`self.FL_Fade`))) (%s (/ (`self.FL_T`) (`self.FL_Fade`)))) (- 3.0 (* 2.0 (%s (/ (`self.FL_T`) (`self.FL_Fade`))))))))' % (K('FClamp'), K('FClamp'), K('FClamp')),
 '    (`SkeletalMeshComponent.SetAllBodiesBelowPhysicsBlendWeight` %s %s (`self.FL_W`) false true)' % (M, P),
 '    (if (>= (`self.FL_T`) (`self.FL_Fade`))',
 '      (`SkeletalMeshComponent.SetAllBodiesBelowSimulatePhysics` %s %s false true))' % (M, P),
 '    (if (>= (`self.FL_T`) (`self.FL_Len`))',
 '      (set `self.FL_State` 0.0)))']
edits = [{'oldString': L[t[0]], 'newString': NL.join(fire + st1 + st2) + NL + L[t[0]]}]
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('FALL edit', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:2500])
print('FALL compile', str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:600])
