# m_impact_mcp.py (MCP, in-memory; BP_HybridA_Player; re-appliable) - region impact reaction (physical hit reaction).
# A hit is requested by setting IMP_Bone (region root bone), IMP_Imp (velocity-change impulse, cm/s, world) and IMP_Fire = 1.
# Tick: the driver mesh (self.Mesh, PA_UEFN_Mannequin) simulates the bodies below IMP_Bone, held toward the animated pose by the
# PhysicalAnimationComponent motors (IMP_OS orientation / IMP_AVS angular-velocity strength), the impulse is applied to IMP_Bone,
# and the physics blend weight fades IMP_W0 -> 0 over IMP_Dur (smoothstep) before simulation is switched off. The visible body
# copies the driver pose, so the reaction stays local to the hit region (head / chest / one shoulder / pelvis).
# IMP_Push scales an optional capsule push (LaunchCharacter, horizontal part of the impulse) for strong hits.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10); K = '`KismetMathLibrary.%s`'
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
V = [('IMP_Fire', 'float'), ('IMP_T', 'float'), ('IMP_Act', 'float'), ('IMP_W0', 'float'), ('IMP_Dur', 'float'), ('IMP_OS', 'float'), ('IMP_AVS', 'float'), ('IMP_Push', 'float'), ('IMP_W', 'float'), ('IMP_Bone', 'name'), ('IMP_Imp', 'vector')]
for nme, ty in V:
    if '"%s"' % nme not in have:
        r = T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': nme, 'typeName': ty}); print('var', nme, ty, str(r)[:160])
        T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': nme, 'bInstanceEditable': True})
print('compile', str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200])
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '(set `self.IMP_Act`' in dsl: print('IMPACT already'); sys.exit(0)
L = dsl.split(NL); t = [i for i, x in enumerate(L) if x.startswith('  (set `self.TR_SpPk` ')]; assert len(t) == 1, t
M = '(`self.Mesh`)'; B = '(`self.IMP_Bone`)'
pad = '(make `PhysicalAnimationData` false (`self.IMP_OS`) (`self.IMP_AVS`) 0.0 0.0 0.0 0.0)'
fire = NL.join([
 '  (if (> (`self.IMP_Fire`) 0.5)',
 '      (`PhysicalAnimationComponent.SetSkeletalMeshComponent` (`self.SphPhysAnim`) %s)' % M,
 '      (`PhysicalAnimationComponent.ApplyPhysicalAnimationSettingsBelow` (`self.SphPhysAnim`) %s %s true)' % (B, pad),
 '      (`SkeletalMeshComponent.SetAllBodiesBelowSimulatePhysics` %s %s true true)' % (M, B),
 '      (`SkeletalMeshComponent.SetAllBodiesBelowPhysicsBlendWeight` %s %s (`self.IMP_W0`) false true)' % (M, B),
 '      (`PrimitiveComponent.AddImpulse` %s (`self.IMP_Imp`) %s true)' % (M, B),
 '      (`Character.LaunchCharacter` self (* (`KismetMathLibrary.MakeVector` (.x (`self.IMP_Imp`)) (.y (`self.IMP_Imp`)) 0.0) (`self.IMP_Push`)) false false)',
 '      (set `self.IMP_T` 0.0)',
 '      (set `self.IMP_Act` 1.0)',
 '      (set `self.IMP_Fire` 0.0))'])
act = NL.join([
 '  (if (> (`self.IMP_Act`) 0.5)',
 '      (set `self.IMP_T` (+ (`self.IMP_T`) DeltaSeconds))',
 '      (set `self.IMP_W` (* (`self.IMP_W0`) (- 1.0 (* (* (%s (/ (`self.IMP_T`) (`self.IMP_Dur`))) (%s (/ (`self.IMP_T`) (`self.IMP_Dur`)))) (- 3.0 (* 2.0 (%s (/ (`self.IMP_T`) (`self.IMP_Dur`)))))))))' % (K % 'FClamp', K % 'FClamp', K % 'FClamp'),
 '      (`SkeletalMeshComponent.SetAllBodiesBelowPhysicsBlendWeight` %s %s (`self.IMP_W`) false true)' % (M, B),
 '      (if (>= (`self.IMP_T`) (`self.IMP_Dur`))',
 '          (`SkeletalMeshComponent.SetAllBodiesBelowSimulatePhysics` %s %s false true)' % (M, B),
 '          (set `self.IMP_Act` 0.0)))'])
edits = [{'oldString': L[t[0]], 'newString': fire + NL + act + NL + L[t[0]]}]
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('IMPACT edit', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:3000])
print('IMPACT compile', str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:600])
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); d2 = r['content']['returnValue']['dsl']
i = d2.find('IMP_Fire'); print('READBACK', d2[i - 40:i + 2600] if i > 0 else 'missing')
