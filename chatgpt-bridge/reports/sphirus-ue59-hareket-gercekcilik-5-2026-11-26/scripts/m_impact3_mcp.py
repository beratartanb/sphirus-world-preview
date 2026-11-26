# m_impact3_mcp.py (MCP, in-memory): separate simulation root (IMP_SimB) from the hit bone (IMP_Bone). IMP_All > 0.5: impulse to every body
# below IMP_Bone (chest shove); else impulse to the IMP_Bone body only (head / shoulder: the torso twists through the joints, arms lag).
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
for nme, ty in (('IMP_SimB', 'name'), ('IMP_All', 'float')):
    if '"%s"' % nme not in have:
        T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': nme, 'typeName': ty}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': nme, 'bInstanceEditable': True})
T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if 'IMP_SimB' in dsl: print('IMP3 already'); sys.exit()
M = '(`self.Mesh`)'; B = '(`self.IMP_Bone`)'; S = '(`self.IMP_SimB`)'
edits = []
for old in ['(`PhysicalAnimationComponent.ApplyPhysicalAnimationSettingsBelow` (`self.SphPhysAnim`) %s' % B,
            '(`SkeletalMeshComponent.SetAllBodiesBelowSimulatePhysics` %s %s true true)' % (M, B),
            '(`SkeletalMeshComponent.SetAllBodiesBelowPhysicsBlendWeight` %s %s (`self.IMP_W0`) false true)' % (M, B),
            '(`SkeletalMeshComponent.SetAllBodiesBelowPhysicsBlendWeight` %s %s (`self.IMP_W`) false true)' % (M, B),
            '(`SkeletalMeshComponent.SetAllBodiesBelowSimulatePhysics` %s %s false true)' % (M, B)]:
    assert dsl.count(old) == 1, old; edits.append({'oldString': old, 'newString': old.replace(B, S)})
old = '    (`SkeletalMeshComponent.AddImpulseToAllBodiesBelow` %s (`self.IMP_Imp`) %s true true)' % (M, B); assert dsl.count(old) == 1
edits.append({'oldString': old, 'newString': '    (if (> (`self.IMP_All`) 0.5)\n      (`SkeletalMeshComponent.AddImpulseToAllBodiesBelow` %s (`self.IMP_Imp`) %s true true)\n      (else\n        (`PrimitiveComponent.AddImpulse` %s (`self.IMP_Imp`) %s true)))' % (M, B, M, B)})
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': edits})
print('IMP3', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200])
