# m_fall2_mcp.py (MCP, in-memory): get-up start fix. While every body (pelvis included) simulates, the pelvis root body drags the driver mesh
# component (measured fall3_idle: relative (150,-8,-9), yaw -174 instead of (0,0,-86) / -90) and it stays there after simulation ends ->
# mesh 77 cm above the floor, foot placement pulls the pelvis to 35 cm. At the get-up start: all bodies off, spine_01 / thighs (everything
# but the pelvis) back on (they keep fading from the ragdoll pose with FL_W), and the mesh relative transform is restored.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
NL = chr(10)
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if 'K2_SetRelativeLocationAndRotation` (`self.Mesh`)' in dsl: print('FALL2 already'); sys.exit()
L = dsl.split(NL); a = [i for i, x in enumerate(L) if 'K2_SetActorRotation' in x and 'DegAtan2' in x]; assert len(a) == 1, a
ind = L[a[0]][:len(L[a[0]]) - len(L[a[0]].lstrip())]; M = '(`self.Mesh`)'
add = [ind + '(`SkeletalMeshComponent.SetAllBodiesBelowSimulatePhysics` %s "pelvis" false true)' % M,
       ind + '(`SceneComponent.K2_SetRelativeLocationAndRotation` %s (`KismetMathLibrary.MakeVector` 0.0 0.0 -86.0) (`KismetMathLibrary.MakeRotator` 0.0 0.0 -90.0) false true)' % M]
for b in ('spine_01', 'thigh_l', 'thigh_r'):
    add.append(ind + '(`SkeletalMeshComponent.SetAllBodiesBelowSimulatePhysics` %s "%s" true true)' % (M, b))
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': L[a[0]], 'newString': L[a[0]] + NL + NL.join(add)}]})
print('FALL2', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200])
