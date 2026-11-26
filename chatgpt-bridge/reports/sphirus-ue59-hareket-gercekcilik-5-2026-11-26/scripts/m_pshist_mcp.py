# m_pshist_mcp.py (MCP, in-memory; ABP_Sph_GASP AnimGraph; argv[1] = 'early' | 'late') - pass 5.
# POSE HISTORY SOURCE. Measured chain (pass 5): MotionMatching -> Slot -> OffsetRootBone -> RemapCurves -> LocalToComponent ->
# ModifyBone_0/1/2 (project SphBob / SphHipRot / SphSpineRot) -> FootPlacement -> LegIK -> ComponentToLocal -> PoseSearchHistoryCollector
# -> Output. The history that Motion Matching matches against therefore contains every project correction ('late', GASP default).
# 'early' moves the collector to right after RemapCurves (local pose of the selected animation + root offset, before the project's
# procedural corrections and foot placement); 'late' restores the original wiring.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
G = '/Game/Sphirus/Player/GASP/ABP_Sph_GASP.ABP_Sph_GASP:AnimGraph.'
pin = lambda n, d: {'node': {'refPath': G + n}, 'indexId': 0, 'direction': d}
O = lambda n: pin(n, 'EGPD_Output'); I = lambda n: pin(n, 'EGPD_Input')
H, ROOT, C2L, RC, L2C = 'AnimGraphNode_PoseSearchHistoryCollector_0', 'AnimGraphNode_Root_0', 'AnimGraphNode_ComponentToLocalSpace_2', 'AnimGraphNode_RemapCurves_0', 'AnimGraphNode_LocalToComponentSpace_0'
mode = sys.argv[1]
if mode == 'early':
    cut = [(C2L, H), (H, ROOT), (RC, L2C)]; link = [(C2L, ROOT), (RC, H), (H, L2C)]
else:
    cut = [(C2L, ROOT), (RC, H), (H, L2C)]; link = [(C2L, H), (H, ROOT), (RC, L2C)]
for a, b in cut: print('cut', a, b, str(T('BlueprintToolsets.BlueprintToolset.DisconnectPins', {'outputPin': O(a), 'inputPin': I(b)}))[:160])
for a, b in link: print('link', a, b, str(T('BlueprintToolsets.BlueprintToolset.ConnectPins', {'outputPin': O(a), 'inputPin': I(b)}))[:160])
print('PSHIST', mode, str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': '/Game/Sphirus/Player/GASP/ABP_Sph_GASP.ABP_Sph_GASP'}, 'bWarningsAsErrors': False}))[:300])
