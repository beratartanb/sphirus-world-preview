# m_hip3_mcp.py (MCP, in-memory; BP_HybridA_Player GR_Bob; after m_hip2 + c_hip3; re-appliable) - movement realism pass 2.
# Head keeps the clip's orientation: ABP SphNeckRot = yaw -(SH_Yaw x HD_K) (HD_K 1 = full counter-rotation of the shoulder correction).
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = AP + '.BP_HybridA_Player'; NL = chr(10); K = '`KismetMathLibrary.%s`'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
if '"HD_K"' not in have:
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': 'HD_K', 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': 'HD_K', 'bInstanceEditable': True})
    T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if 'ABP_Sph_GASP.SphNeckRot' in dsl: print('HIP3M already'); sys.exit(0)
l = [x for x in dsl.split(NL) if x.strip().startswith('(set `/Game/Sphirus/Player/GASP/ABP_Sph_GASP.SphSpineRot` ')]; assert len(l) == 1, len(l); l = l[0]; ind = l[:len(l) - len(l.lstrip())]
print('HIP3M spine line', l.strip()[:400])
neck = ind + '(set `/Game/Sphirus/Player/GASP/ABP_Sph_GASP.SphNeckRot` (%s 0.0 0.0 (* (- (`self.SH_Yaw`)) (`self.HD_K`))) _asabp_sph_gasp)' % (K % 'MakeRotator')
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': l, 'newString': neck + NL + l}]})
print('HIP3M', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1800], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:100])
