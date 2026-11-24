# m_hip6_mcp.py (MCP, in-memory; BP_HybridA_Player GR_Bob; after c_hip6; re-appliable) - movement realism pass 2: ABP SphSpineTr.
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ClaudeUnreal_20261105')); import umcp; umcp.init()
umcp.tool('list_toolsets', {})
def T(full, args): ts, nm = full.rsplit('.', 1); return umcp.tool('call_tool', {'toolset_name': ts, 'tool_name': nm, 'arguments': args})
AP = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; BP = AP + '.BP_HybridA_Player'; NL = chr(10); K = '`KismetMathLibrary.%s`'
have = json.dumps(T('BlueprintToolsets.BlueprintToolset.ListVariables', {'blueprint': {'refPath': BP}}))
if '"HD_T"' not in have:
    T('BlueprintToolsets.BlueprintToolset.AddVariable', {'blueprint': {'refPath': BP}, 'name': 'HD_T', 'typeName': 'float'}); T('BlueprintToolsets.BlueprintToolset.SetVariableInstanceEditable', {'blueprint': {'refPath': BP}, 'variableName': 'HD_T', 'bInstanceEditable': True})
    T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False})
r = T('BlueprintToolsets.BlueprintDslToolset.Read', {'assetPath': AP, 'scope': ''}); rv = r['content']['returnValue']; dsl = rv['dsl']
if 'ABP_Sph_GASP.SphSpineTr' in dsl: print('HIP6M already'); sys.exit(0)
l = [x for x in dsl.split(NL) if x.strip().startswith('(set `/Game/Sphirus/Player/GASP/ABP_Sph_GASP.SphSpineRot` ')]; assert len(l) == 1; l = l[0]; ind = l[:len(l) - len(l.lstrip())]
S = lambda b: '(.y (.location (`SceneComponent.GetSocketTransform` (`self.Mesh`) "%s" "RTS_Component")))' % b
new = ind + '(set `/Game/Sphirus/Player/GASP/ABP_Sph_GASP.SphSpineTr` (%s (* (* (`self.HD_T`) (%s (`self.SH_Yaw`))) (%s (- %s %s) -30.0 30.0)) 0.0 0.0) _asabp_sph_gasp)' % (K % 'MakeVector', K % 'DegSin', K % 'FClamp', S('head'), S('spine_01'))
r2 = T('BlueprintToolsets.BlueprintDslToolset.Edit', {'assetPath': AP, 'revision': rv['revision'], 'scope': '', 'edits': [{'oldString': l, 'newString': new + NL + l}]})
print('HIP6M', 'ok' if not (isinstance(r2, dict) and r2.get('isError')) else str(r2)[:1800], str(T('BlueprintToolsets.BlueprintToolset.CompileBlueprint', {'blueprint': {'refPath': BP}, 'bWarningsAsErrors': False}))[:100])
