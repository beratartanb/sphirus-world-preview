# m_impact2_mcp.py (MCP, in-memory): impact impulse to every body below IMP_Bone (AddImpulseToAllBodiesBelow) instead of the root body only.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
old = '(`PrimitiveComponent.AddImpulse` (`self.Mesh`) (`self.IMP_Imp`) (`self.IMP_Bone`) true)'
new = '(`SkeletalMeshComponent.AddImpulseToAllBodiesBelow` (`self.Mesh`) (`self.IMP_Imp`) (`self.IMP_Bone`) true true)'
if new in dsl: print('IMP2 already'); sys.exit()
assert dsl.count(old) == 1
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': old, 'newString': new}]})
print('IMP2', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:200])
