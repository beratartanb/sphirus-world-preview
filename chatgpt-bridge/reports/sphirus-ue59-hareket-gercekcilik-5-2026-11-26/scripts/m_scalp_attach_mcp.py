# m_scalp_attach_mcp.py (MCP, in-memory; BP_HybridA_Player; re-appliable): BeginPlay attaches the HairScalp cover (static mesh built in
# head-bone space) to the Face component at socket 'head' (KeepRelative), the same pattern as GR_HoldProp / hand_r.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
PA = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = PA + '.BP_HybridA_Player'
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': PA, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if '(`self.HairScalp`) (`self.Face`) "head"' in dsl: print('SCALPATT already'); sys.exit(0)
old = '  (`SkinnedMeshComponent.SetLeaderPoseComponent` (`self.GR_BeltSk`) (`self.Manny`) false false))'
assert dsl.count(old) == 1, dsl.count(old)
new = old[:-1] + '\n  (`SceneComponent.K2_AttachToComponent` (`self.HairScalp`) (`self.Face`) "head" "KeepRelative" "KeepRelative" "KeepRelative" true))'
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': PA, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': old, 'newString': new}]})
print('SCALPATT', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1500], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:300])
